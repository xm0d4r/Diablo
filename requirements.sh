#!/bin/bash

# Define the installation directory
INSTALL_DIR="/usr/local/bin"

# Ensure the directory exists
sudo mkdir -p "$INSTALL_DIR"

# Ensure git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Installing Git..."
    sudo apt update
    sudo apt install -y git
else
    echo "Git is already installed ✅"
fi

# Install Go if not installed
if ! command -v go &> /dev/null; then
    echo "Go is not installed. Installing Go..."
    sudo apt update
    sudo apt install -y golang
else
    echo "Go is already installed ✅"
fi

# Ensure Go bin path is in PATH
export PATH=$PATH:$HOME/go/bin
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.zshrc
source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null

# Install tools with APT if available
apt_tools=("enum4linux" "ffuf" "nmap" "wpscan")
for tool in "${apt_tools[@]}"; do
    if ! command -v $tool &> /dev/null; then
        echo "Installing $tool..."
        sudo apt install -y $tool > /dev/null 2>&1
    else
        echo "$tool is already installed ✅"
    fi
done

# Install Go tools
go_tools=("shortscan" "webanalyze")
for tool in "${go_tools[@]}"; do
    if ! command -v $tool &> /dev/null; then
        echo "Installing $tool using Go..."
        go install github.com/projectdiscovery/$tool@latest
    else
        echo "$tool is already installed ✅"
    fi
done

# Install additional tools manually
cd "$INSTALL_DIR"

# Install lazy-hunter
if command -v lazyhunter &> /dev/null; then
    echo "lazy-hunter is already installed ✅"
else
    echo "Installing lazy-hunter..."
    sudo git clone https://github.com/iamunixtz/Lazy-Hunter.git "$INSTALL_DIR/Lazy-Hunter"
    cd "$INSTALL_DIR/Lazy-Hunter" || exit
    pip install --user -r requirements.txt --break-system-packages
    sudo chmod +x lazyhunter.py
    sudo ln -s "$INSTALL_DIR/Lazy-Hunter/lazyhunter.py" /usr/local/bin/lazyhunter
fi

# Install NetExec
if command -v netexec &> /dev/null; then
    echo "netexec is already installed ✅"
else
    echo "Installing netexec..."
    sudo git clone https://github.com/Pennyw0rth/NetExec.git "$INSTALL_DIR/NetExec"
    cd "$INSTALL_DIR/NetExec" || exit
    pip install -r requirements.txt
    cd "$INSTALL_DIR"
fi

# Install shcheck
if command -v shcheck.py &> /dev/null; then
    echo "shcheck is already installed ✅"
else
    echo "Installing shcheck..."
    sudo git clone https://github.com/santoru/shcheck.git "$INSTALL_DIR/shcheck"
    sudo chmod +x "$INSTALL_DIR/shcheck/shcheck.py"
    sudo ln -s "$INSTALL_DIR/shcheck/shcheck.py" /usr/local/bin/shcheck
fi

# Install testssl
if command -v testssl &> /dev/null; then
    echo "testssl is already installed ✅"
else
    echo "Installing testssl..."
    sudo git clone --depth 1 https://github.com/drwetter/testssl.sh.git "$INSTALL_DIR/testssl.sh"
    sudo chmod +x "$INSTALL_DIR/testssl.sh/testssl.sh"
    sudo ln -s "$INSTALL_DIR/testssl.sh/testssl.sh" /usr/local/bin/testssl
fi

echo "Installation completed. Restart the terminal to apply changes."
