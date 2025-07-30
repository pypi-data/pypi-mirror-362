export TWINE_USERNAME=__token__
export TWINE_PASSWORD=$(grep "password" .pypirc | head -1 | cut -d="=" -f2 | xargs)
export TWINE_TEST_PASSWORD=$(grep "password" .pypirc | tail -1 | cut -d="=" -f2 | xargs)
