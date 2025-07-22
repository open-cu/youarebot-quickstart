#!/bin/bash
# IF YOU DO NOT KNOW HOW ALL THIS WORKS, DO NOT CHANGE ANYTHING


# Setup
set -e
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
WHITE='\033[1;37m'
NC='\033[0m'


# Vars
remote_host="158.160.135.246"
private_key="portforward_key"
port_file="/tmp/random_port.txt"


# Loading or generating port
echo "Loading or generating random port..."
if [[ -f "$port_file" ]]; then
  random_port=$(cat "$port_file")
  echo "Loaded port: $random_port"
else
  random_port=$(awk -v min=1024 -v max=65535 'BEGIN{srand(); print int(min+rand()*(max-min+1))}')
  echo "$random_port" > "$port_file"
  echo "Generated port: $random_port"
fi


# Installing Poetry
echo "Checking if Poetry is installed..."
if command -v poetry &> /dev/null; then
  echo "Poetry is already installed."
  echo "Checking poetry version..."
  poetry_version=$(poetry --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
  if [[ "$poetry_version" == "2.1.1" ]]; then
    echo "Poetry version is correct: $poetry_version"
  else
    echo -e "${YELLOW}Poetry version is not correct. Updating...${NC}"
    poetry self update 2.1.1
    echo -e "${WHITE}Poetry updated successfully.${NC}"
  fi
else
  echo "Poetry is not installed. Installing..."
  curl -sSL https://install.python-poetry.org | POETRY_VERSION=2.1.1 python3 -
  echo -e "${WHITE}Poetry installed successfully.${NC}"
fi


# Installing Project's dependencies
echo "Installing Project's dependencies..."
poetry install
echo "Dependencies installed successfully."


# Starting SSH tunnel
echo "Starting SSH tunnel..."
chmod 600 portforward_key
ssh -f -i "$private_key" -N -R "0.0.0.0:$random_port:localhost:6872" "forwarduser@$remote_host"
if [[ $? -eq 0 ]]; then
  echo -e "${WHITE}SSH tunnel started successfully.${NC}"
else
  echo -e "${RED}Failed to start SSH tunnel.${NC}"
fi


# Starting the app
echo -e "${WHITE}Launching the app...${NC}"
poetry run fastapi dev app/api/main.py --host 0.0.0.0 --port 6872 &

# Starting the web-client (streamlit)
PYTHONPATH=$(pwd) poetry run streamlit run app/web/streamlit_app.py --server.port=8502 --server.address=0.0.0.0


# 10. Log address for registration
echo "Your address for registration is:"
echo "http://$remote_host:$random_port"
