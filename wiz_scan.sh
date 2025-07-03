#!/bin/bash
set -e

# Download and run Wiz CLI scan (replace with your actual Wiz CLI commands)
curl -Lo wizcli https://wizcli.app/download/latest/linux/wizcli
chmod +x wizcli
./wizcli scan --path . --token $WIZ_TOKEN