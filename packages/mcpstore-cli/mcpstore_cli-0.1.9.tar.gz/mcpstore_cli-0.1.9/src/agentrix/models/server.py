"""Models for MCP server definitions and configurations."""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl, validator


class ServerType(str, Enum):
    """Supported server types."""
    
    NPM = "npm"
    PYPI = "pypi" 
    GITHUB = "github"
    DOCKER = "docker"
    LOCAL = "local"
    REMOTE = "remote"


class ServerStatus(str, Enum):
    """Server status enumeration."""
    
    UNKNOWN = "unknown"
    INSTALLING = "installing"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


class ToolInfo(BaseModel):
    """Information about an MCP tool."""
    
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    input_schema: Dict[str, Any] = Field(default_factory=dict, description="Input schema")
    
    class Config:
        frozen = True


class AuthConfig(BaseModel):
    """Authentication configuration for a server."""
    
    required: bool = Field(default=False, description="Whether authentication is required")
    api_key_env: Optional[str] = Field(None, description="Environment variable for API key")
    token_url: Optional[HttpUrl] = Field(None, description="Token endpoint URL")
    scopes: List[str] = Field(default_factory=list, description="Required scopes")


class ServerConfig(BaseModel):
    """Configuration for running an MCP server."""
    
    name: str = Field(..., description="Server instance name")
    server_id: str = Field(..., description="Server identifier from registry")
    type: ServerType = Field(..., description="Server type")
    version: str = Field(default="latest", description="Server version")
    
    # Execution configuration
    command: Optional[str] = Field(None, description="Custom command to run")
    args: List[str] = Field(default_factory=list, description="Command arguments")
    env: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    working_dir: Optional[str] = Field(None, description="Working directory")
    
    # Authentication
    auth: AuthConfig = Field(default_factory=AuthConfig, description="Authentication config")
    api_key: Optional[str] = Field(None, description="API key for this server")
    
    # Advanced options
    timeout: int = Field(default=30, description="Startup timeout in seconds")
    restart_policy: str = Field(default="on-failure", description="Restart policy")
    max_retries: int = Field(default=3, description="Maximum restart retries")
    
    @validator('name')
    def validate_name(cls, v: str) -> str:
        """Validate server name."""
        if not v:
            raise ValueError("Server name cannot be empty")
        # Allow alphanumeric, hyphens, underscores, @, and forward slashes for package names
        import re
        if not re.match(r'^[@\w\-/]+$', v):
            raise ValueError("Server name must be alphanumeric with hyphens/underscores/@/slash")
        return v.lower()


class ServerInfo(BaseModel):
    """Information about an MCP server from registry."""
    
    id: str = Field(..., description="Unique server identifier")
    name: str = Field(..., description="Display name")
    description: str = Field(..., description="Server description")
    version: str = Field(..., description="Current version")
    author: str = Field(..., description="Author name")
    
    # Installation information
    type: ServerType = Field(..., description="Server type")
    package_name: Optional[str] = Field(None, description="Package name (npm/pypi)")
    repository_url: Optional[HttpUrl] = Field(None, description="Source repository")
    docker_image: Optional[str] = Field(None, description="Docker image name")
    
    # Metadata
    tags: List[str] = Field(default_factory=list, description="Server tags")
    categories: List[str] = Field(default_factory=list, description="Categories")
    tools: List[ToolInfo] = Field(default_factory=list, description="Available tools")
    
    # Requirements
    python_version: Optional[str] = Field(None, description="Required Python version")
    node_version: Optional[str] = Field(None, description="Required Node.js version")
    dependencies: List[str] = Field(default_factory=list, description="System dependencies")
    
    # Authentication
    auth: AuthConfig = Field(default_factory=AuthConfig, description="Auth requirements")
    
    # Statistics
    downloads: int = Field(default=0, description="Download count")
    stars: int = Field(default=0, description="Star count")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update")
    
    class Config:
        use_enum_values = True


class ServerInstance(BaseModel):
    """Running server instance information."""
    
    config: ServerConfig = Field(..., description="Server configuration")
    info: Optional[ServerInfo] = Field(None, description="Server metadata")
    status: ServerStatus = Field(default=ServerStatus.UNKNOWN, description="Current status")
    
    # Process information
    pid: Optional[int] = Field(None, description="Process ID")
    started_at: Optional[datetime] = Field(None, description="Start time")
    
    # Health information
    last_heartbeat: Optional[datetime] = Field(None, description="Last heartbeat")
    error_message: Optional[str] = Field(None, description="Last error message")
    restart_count: int = Field(default=0, description="Restart count")
    
    # Performance metrics
    cpu_usage: Optional[float] = Field(None, description="CPU usage percentage")
    memory_usage: Optional[int] = Field(None, description="Memory usage in MB")
    
    class Config:
        use_enum_values = True


class InstallationResult(BaseModel):
    """Result of server installation."""
    
    success: bool = Field(..., description="Whether installation succeeded")
    server_id: str = Field(..., description="Server identifier")
    version: str = Field(..., description="Installed version")
    message: str = Field(..., description="Status message")
    config: Optional[ServerConfig] = Field(None, description="Generated configuration")
    duration: float = Field(..., description="Installation duration in seconds")
    
    class Config:
        frozen = True 