#!/bin/bash
set -x

pip install --user -r requirements.txt

wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip
sudo mv ngrok /usr/local/bin/
rm ngrok-stable-linux-amd64.zip