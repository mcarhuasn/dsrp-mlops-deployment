#!/bin/bash

# --- Install Pyenv
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
cd ~/.pyenv && src/configure && make -C src

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init --path)"' >>~/.profile
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

source ~/.profile
source ~/.bashrc

# --- Install Python Build dependencies before installing any python version
sudo apt-get update; yes Y | sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# --- Install a Python version
pyenv install 3.11.5

# --- Install Pyenv VirtualEnv
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc
source ~/.profile

# --- Create DS Environment
pyenv virtualenv 3.11.5 dsrpmlops
pyenv global dsrpmlops

# --- Reset the shell
exec "$SHELL"

# --- Install python libraries
pip install --upgrade pip
pip install ipython jupyter jupyterlab
