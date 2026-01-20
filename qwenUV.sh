#!/bin/bash

# Combined script to install Node.js and @qwen-code/qwen-code, then set up Python environment with ML/AI packages

set -e  # Exit immediately if a command exits with a non-zero status

echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y && sudo apt install btop -y

echo "Setting up Node.js and @qwen-code/qwen-code..."

# Check if Node.js is already installed
if command -v node &> /dev/null; then
    echo "Node.js is already installed. Current version:"
    node --version
    echo "Current npm version:"
    npm --version

    read -p "Do you want to update Node.js to the latest version anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping Node.js update."
    else
        # Install the latest version of Node.js using the official NodeSource repository
        NODE_SETUP_URL="https://deb.nodesource.com/setup_lts.x"
        curl -fsSL "$NODE_SETUP_URL" | sudo -E bash -
        sudo apt-get install -y nodejs
    fi
else
    # Install the latest version of Node.js using the official NodeSource repository
    NODE_SETUP_URL="https://deb.nodesource.com/setup_lts.x"
    curl -fsSL "$NODE_SETUP_URL" | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Verify the Node.js installation
echo ""
echo "Verifying Node.js installation..."
echo "Node.js version:"
node -v
echo "npm version:"
npm -v

# Install the latest version of @qwen-code/qwen-code globally using a local directory to avoid permission issues
echo "Configuring npm for local global installations..."
mkdir -p "$HOME/.npm-global"
npm config set prefix "$HOME/.npm-global"
export PATH="$HOME/.npm-global/bin:$PATH"

echo "Installing @qwen-code/qwen-code..."
npm install -g @qwen-code/qwen-code@latest

echo "Setting up Python environment with ML/AI packages..."

# Check if uv is installed, if not install it
if ! command -v uv &> /dev/null; then
    echo "uv not found, installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Update PATH to include the location where uv was installed
    export PATH="$HOME/.local/bin:$PATH"
    echo "uv installed successfully."
else
    echo "uv is already installed."
fi

# Initialize a new Python project if pyproject.toml doesn't exist
if [ ! -f "pyproject.toml" ]; then
    echo "Initializing new Python project..."
    uv init
    echo "Python project initialized."
else
    echo "pyproject.toml already exists, skipping initialization."
fi

# Create a virtual environment
echo "Creating virtual environment..."
uv venv
echo "Virtual environment created."

# Activate the virtual environment
source .venv/bin/activate

echo "Adding ML/AI packages..."

# Add the requested ML/AI packages
uv add datasets torch transformers tqdm

# Add additional commonly used ML/AI packages
uv add numpy pandas scikit-learn matplotlib seaborn jupyter notebook ipykernel

# Add deep learning related packages
uv add tensorflow accelerate

# Add utilities for machine learning experiments
uv add wandb tensorboard

echo "Python packages added successfully!"

echo ""
echo "Setup complete!"
echo "- Node.js and npm are installed"
echo "- @qwen-code/qwen-code is installed globally"
echo "- Python environment with ML/AI packages is ready"
echo ""
echo "To activate the Python virtual environment in the future, run: source .venv/bin/activate"
echo "To start Jupyter notebook, run: jupyter notebook"