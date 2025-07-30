"""Command-line interface for Agentrix."""

import asyncio
import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .core.config import ConfigManager
from .core.registry import ServerRegistry
from .core.server_manager import ServerManager
from .core.auth import AuthManager
from .core.dev_server import DevServer
from .core.builder import ServerBuilder
from .core.playground import PlaygroundManager
from .models.config import AgentrixConfig, ClientInstallConfig
from .models.server import ServerType
from .utils.logger import get_logger, setup_logging

# Initialize console and logger
console = Console()
logger = get_logger(__name__)

# Create Typer app
app = typer.Typer(
    name="agentrix",
    help="🤖 Agentrix - Python MCP server registry and proxy for AI agents",
    add_completion=False,
)

# Global config
_config: Optional[AgentrixConfig] = None


def get_config() -> AgentrixConfig:
    """Get or initialize global configuration."""
    global _config
    if _config is None:
        _config = AgentrixConfig()
        _config.ensure_directories()
        setup_logging(_config.logging)
    return _config


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
    config_file: Optional[Path] = typer.Option(None, "--config", help="Config file path"),
):
    """Agentrix - Python MCP server registry and proxy for AI agents."""
    config = get_config()
    
    if verbose:
        config.logging.level = "DEBUG"
        setup_logging(config.logging)
    
    if debug:
        config.debug = True
        config.dev_mode = True


@app.command()
def search(
    query: Optional[str] = typer.Argument(None, help="Search query"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    server_type: Optional[str] = typer.Option(None, "--type", "-t", help="Filter by server type"),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of results"),
):
    """🔍 Search for MCP servers in the registry."""
    asyncio.run(_search(query, category, server_type, limit))


async def _search(
    query: Optional[str],
    category: Optional[str], 
    server_type: Optional[str],
    limit: int
):
    """Async search implementation."""
    config = get_config()
    registry = ServerRegistry(config)
    
    try:
        # Parse server type
        parsed_type = None
        if server_type:
            try:
                parsed_type = ServerType(server_type.lower())
            except ValueError:
                console.print(f"❌ Invalid server type: {server_type}", style="red")
                console.print(f"Valid types: {', '.join([t.value for t in ServerType])}")
                return
        
        # Perform search
        servers = await registry.search_servers(
            query=query,
            category=category,
            server_type=parsed_type,
            limit=limit
        )
        
        # Display results
        if not servers:
            console.print("❌ No servers found matching your criteria", style="yellow")
            return
        
        registry.display_search_results(servers)
        
        # Show usage hint
        console.print(f"\n💡 Use [cyan]agentrix inspect <server-name>[/cyan] for details")
        console.print(f"💡 Use [cyan]agentrix install <server-name> --client <client>[/cyan] to install")
    
    except Exception as e:
        logger.error(f"Search failed: {e}")
        console.print(f"❌ Search failed: {e}", style="red")


@app.command()
def inspect(
    server_id: str = typer.Argument(..., help="Server identifier"),
):
    """🔍 Inspect a server interactively."""
    asyncio.run(_inspect(server_id))


async def _inspect(server_id: str):
    """Async inspect implementation."""
    config = get_config()
    registry = ServerRegistry(config)
    
    try:
        server = await registry.get_server_info(server_id)
        if not server:
            console.print(f"❌ Server '{server_id}' not found", style="red")
            return
        
        registry.display_server_info(server)
        
        # Interactive inspection
        from .core.inspector import ServerInspector
        inspector = ServerInspector(config)
        await inspector.inspect_server(server)
        
    except Exception as e:
        logger.error(f"Inspect command failed: {e}")
        console.print(f"❌ Failed to inspect server: {e}", style="red")


# For backward compatibility, keep the 'info' command
@app.command()
def info(
    server_id: str = typer.Argument(..., help="Server identifier"),
):
    """📋 Show detailed information about a server."""
    asyncio.run(_inspect(server_id))


@app.command()
def install(
    package: str = typer.Argument(..., help="Package identifier to install"),
    client: str = typer.Option(..., "--client", "-c", help="Target MCP client (cursor, claude, vscode)"),
    config_json: Optional[str] = typer.Option(None, "--config", help="Configuration data as JSON"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Custom server name"),
    api_key: Optional[str] = typer.Option(None, "--key", "-k", help="API key for server"),
    force: bool = typer.Option(False, "--force", "-f", help="Force reinstall if exists"),
):
    """📦 Install a package."""
    asyncio.run(_install(package, client, config_json, name, api_key, force))


async def _install(
    package: str,
    client: str, 
    config_json: Optional[str],
    name: Optional[str],
    api_key: Optional[str],
    force: bool
):
    """Async install implementation."""
    config = get_config()
    config_manager = ConfigManager(config)
    registry = ServerRegistry(config)
    
    try:
        # Validate client
        if not config_manager.validate_client(client):
            available_clients = config_manager.list_clients()
            console.print(f"❌ Invalid client: {client}", style="red")
            console.print(f"Available clients: {', '.join(available_clients)}")
            return
        
        # Get server info
        server = await registry.get_server_info(package)
        if not server:
            console.print(f"❌ Server '{package}' not found", style="red")
            console.print("💡 Use [cyan]agentrix search[/cyan] to find servers")
            return
        
        # Use server name if custom name not provided
        server_name = name or server.name.lower().replace(' ', '-')
        
        # Check if already installed
        installed_servers = config_manager.list_installed_servers(client)
        if server_name in installed_servers and not force:
            console.print(f"❌ Server '{server_name}' already installed in {client}", style="yellow")
            console.print("💡 Use --force to reinstall")
            return
        
        # Parse config JSON if provided
        extra_config = {}
        if config_json:
            try:
                import json
                extra_config = json.loads(config_json)
            except json.JSONDecodeError as e:
                console.print(f"❌ Invalid config JSON: {e}", style="red")
                return
        
        # Create install config
        install_config = ClientInstallConfig(
            client=client,
            server_name=server_name,
            server_id=package,
            api_key=api_key,
            env_vars=extra_config.get("env", {}),
            custom_args=extra_config.get("args", [])
        )
        
        # Install server configuration
        success = config_manager.install_server_config(install_config)
        
        if success:
            console.print(f"\n🎉 Successfully installed '{server_name}' to {client}!")
            console.print(f"💡 Restart {client} to use the new server")
            
            # Show server info
            registry.display_server_info(server)
        else:
            console.print("❌ Installation failed", style="red")
    
    except Exception as e:
        logger.error(f"Install command failed: {e}")
        console.print(f"❌ Installation failed: {e}", style="red")


@app.command()
def uninstall(
    package: str = typer.Argument(..., help="Package name to uninstall"),
    client: str = typer.Option(..., "--client", "-c", help="Target MCP client"),
):
    """🗑️ Uninstall a package."""
    config = get_config()
    config_manager = ConfigManager(config)
    
    try:
        # Validate client
        if not config_manager.validate_client(client):
            available_clients = config_manager.list_clients()
            console.print(f"❌ Invalid client: {client}", style="red")
            console.print(f"Available clients: {', '.join(available_clients)}")
            return
        
        # Uninstall server
        success = config_manager.uninstall_server_config(client, package)
        
        if success:
            console.print(f"\n🎉 Successfully uninstalled '{package}' from {client}!")
            console.print(f"💡 Restart {client} to apply changes")
        else:
            console.print("❌ Uninstallation failed", style="red")
    
    except Exception as e:
        logger.error(f"Uninstall command failed: {e}")
        console.print(f"❌ Uninstallation failed: {e}", style="red")


@app.command()
def list(
    target: str = typer.Argument("clients", help="What to list: 'clients' or 'servers'"),
    client: Optional[str] = typer.Option(None, "--client", "-c", help="Specific client for servers list"),
):
    """📋 List clients or servers."""
    config = get_config()
    config_manager = ConfigManager(config)
    
    if target == "clients":
        # List available clients
        clients = config_manager.list_clients()
        console.print("\n📱 Available MCP clients:")
        for client_name in clients:
            client_config = config_manager.get_client_config(client_name)
            if client_config:
                status = "✅" if config_manager.validate_client(client_name) else "❌"
                console.print(f"  {status} {client_name} ({client_config.config_path})")
    
    elif target == "servers":
        if not client:
            console.print("❌ Please specify --client for servers list", style="red")
            return
        
        # List servers for specific client
        if not config_manager.validate_client(client):
            console.print(f"❌ Invalid client: {client}", style="red")
            return
        
        servers = config_manager.list_installed_servers(client)
        if servers:
            console.print(f"\n📦 Installed servers in {client}:")
            for server in servers:
                console.print(f"  • {server}")
        else:
            console.print(f"❌ No servers installed in {client}")
    
    else:
        console.print(f"❌ Invalid target: {target}. Use 'clients' or 'servers'", style="red")


@app.command()
def login(
    api_key: Optional[str] = typer.Option(None, "--key", "-k", help="API key for authentication"),
):
    """🔐 Login with an API key (interactive)."""
    asyncio.run(_login(api_key))


async def _login(api_key: Optional[str]):
    """Async login implementation."""
    config = get_config()
    auth_manager = AuthManager(config)
    
    try:
        if api_key:
            # Non-interactive login
            success = await auth_manager.login(api_key)
        else:
            # Interactive login
            success = await auth_manager.interactive_login()
        
        if success:
            console.print("✅ Successfully logged in!", style="green")
        else:
            console.print("❌ Login failed", style="red")
    
    except Exception as e:
        logger.error(f"Login failed: {e}")
        console.print(f"❌ Login failed: {e}", style="red")


@app.command()
def run(
    server_id: str = typer.Argument(..., help="Server identifier to run"),
    config_json: Optional[str] = typer.Option(None, "--config", help="Configuration JSON for the server"),
    key: Optional[str] = typer.Option(None, "--key", "-k", help="API key"),
):
    """🚀 Run a server."""
    asyncio.run(_run(server_id, config_json, key))


async def _run(server_id: str, config_json: Optional[str], key: Optional[str]):
    """Async run implementation."""
    config = get_config()
    server_manager = ServerManager(config)
    
    try:
        # This is the core proxy functionality
        await server_manager.run_server_proxy(server_id, api_key=key, config_str=config_json)
    
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server run failed: {e}")
        console.print(f"❌ Server run failed: {e}", style="red")
        sys.exit(1)


@app.command()
def dev(
    entry_file: Optional[str] = typer.Argument(None, help="Entry file for development server"),
    port: int = typer.Option(8181, "--port", "-p", help="Port to run the server on"),
    api_key: Optional[str] = typer.Option(None, "--key", "-k", help="API key"),
    no_open: bool = typer.Option(False, "--no-open", help="Don't automatically open the playground"),
    prompt: Optional[str] = typer.Option(None, "--prompt", help="Initial message to start the playground with"),
    config_path: Optional[str] = typer.Option(None, "--config", "-c", help="Path to config file"),
):
    """🛠️ Start development server with hot-reload and tunnel."""
    asyncio.run(_dev(entry_file, port, api_key, no_open, prompt, config_path))


async def _dev(
    entry_file: Optional[str],
    port: int,
    api_key: Optional[str],
    no_open: bool,
    prompt: Optional[str],
    config_path: Optional[str]
):
    """Async dev implementation."""
    config = get_config()
    dev_server = DevServer(config)
    
    try:
        await dev_server.start(
            entry_file=entry_file,
            port=port,
            api_key=api_key,
            auto_open=not no_open,
            initial_prompt=prompt,
            config_path=config_path
        )
    except KeyboardInterrupt:
        logger.info("Development server stopped by user")
    except Exception as e:
        logger.error(f"Development server failed: {e}")
        console.print(f"❌ Development server failed: {e}", style="red")


@app.command()
def build(
    entry_file: Optional[str] = typer.Argument(None, help="Entry file to build"),
    output: Optional[str] = typer.Option(None, "--out", "-o", help="Output file path"),
    transport: str = typer.Option("shttp", "--transport", help="Transport type: shttp or stdio"),
    config_path: Optional[str] = typer.Option(None, "--config", "-c", help="Path to config file"),
):
    """🏗️ Build MCP server for production."""
    asyncio.run(_build(entry_file, output, transport, config_path))


async def _build(
    entry_file: Optional[str],
    output: Optional[str],
    transport: str,
    config_path: Optional[str]
):
    """Async build implementation."""
    config = get_config()
    builder = ServerBuilder(config)
    
    try:
        result = await builder.build(
            entry_file=entry_file,
            output=output,
            transport=transport,
            config_path=config_path
        )
        
        if result.success:
            console.print(f"✅ Build successful: {result.output_file}", style="green")
        else:
            console.print(f"❌ Build failed: {result.error}", style="red")
    
    except Exception as e:
        logger.error(f"Build failed: {e}")
        console.print(f"❌ Build failed: {e}", style="red")


@app.command()
def playground(
    port: int = typer.Option(3000, "--port", "-p", help="Port to expose"),
    api_key: Optional[str] = typer.Option(None, "--key", "-k", help="API key"),
    command: Optional[List[str]] = typer.Argument(None, help="Command to run after --"),
):
    """🎮 Open MCP playground in browser."""
    asyncio.run(_playground(port, api_key, command))


async def _playground(port: int, api_key: Optional[str], command: Optional[List[str]]):
    """Async playground implementation."""
    config = get_config()
    playground = PlaygroundManager(config)
    
    try:
        await playground.start(
            port=port,
            api_key=api_key,
            command=command
        )
    except KeyboardInterrupt:
        logger.info("Playground stopped by user")
    except Exception as e:
        logger.error(f"Playground failed: {e}")
        console.print(f"❌ Playground failed: {e}", style="red")


@app.command()
def featured():
    """⭐ Show featured MCP servers."""
    asyncio.run(_featured())


async def _featured():
    """Async featured implementation."""
    config = get_config()
    registry = ServerRegistry(config)
    
    try:
        servers = await registry.list_featured_servers()
        
        if not servers:
            console.print("❌ No featured servers available", style="yellow")
            return
        
        console.print(f"\n⭐ Featured MCP Servers")
        registry.display_search_results(servers)
    
    except Exception as e:
        logger.error(f"Featured command failed: {e}")
        console.print(f"❌ Failed to get featured servers: {e}", style="red")


@app.command()
def categories():
    """📂 List available server categories."""
    asyncio.run(_categories())


async def _categories():
    """Async categories implementation."""
    config = get_config()
    registry = ServerRegistry(config)
    
    try:
        categories = await registry.get_categories()
        
        if not categories:
            console.print("❌ No categories available", style="yellow")
            return
        
        console.print("\n📂 Available categories:")
        for category in categories:
            console.print(f"  • {category}")
        
        console.print(f"\n💡 Use [cyan]agentrix search --category <name>[/cyan] to filter by category")
    
    except Exception as e:
        logger.error(f"Categories command failed: {e}")
        console.print(f"❌ Failed to get categories: {e}", style="red")


@app.command()
def stats():
    """📊 Show registry statistics."""
    asyncio.run(_stats())


async def _stats():
    """Async stats implementation."""
    config = get_config()
    registry = ServerRegistry(config)
    
    try:
        stats = await registry.get_server_stats()
        
        console.print("\n📊 Registry Statistics:")
        console.print(f"  📦 Total servers: {stats['total_servers']:,}")
        console.print(f"  📥 Total downloads: {stats['total_downloads']:,}")
        
        console.print("\n📋 By type:")
        for server_type, count in stats['by_type'].items():
            console.print(f"  • {server_type}: {count:,}")
    
    except Exception as e:
        logger.error(f"Stats command failed: {e}")
        console.print(f"❌ Failed to get stats: {e}", style="red")


@app.command() 
def clear_cache():
    """🗑️ Clear the local registry cache."""
    config = get_config()
    registry = ServerRegistry(config)
    registry.clear_cache()


@app.command()
def version():
    """📋 Show version information."""
    from . import __version__, __author__
    
    console.print(Panel(
        f"[bold cyan]Agentrix[/bold cyan] v{__version__}\n"
        f"Python MCP server registry and proxy\n"
        f"Author: {__author__}",
        title="🤖 Version Info",
        border_style="cyan"
    ))


def main_cli():
    """Main CLI entry point."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"CLI error: {e}")
        console.print(f"❌ Error: {e}", style="red")
        sys.exit(1)


if __name__ == "__main__":
    main_cli() 