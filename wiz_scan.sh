#!/bin/bash
set -e

# Download and run Wiz CLI scan (replace with your actual Wiz CLI commands)
curl -Lo wizcli https://downloads.wiz.io/wizcli/latest/wizcli-linux-amd64
chmod +x wizcli
./wizcli scan --path . --token $WIZ_TOKEN