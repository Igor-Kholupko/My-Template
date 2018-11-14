#!/bin/bash
# Reloading project:


# Stop  services:
    sudo systemctl disable templater
    sudo systemctl stop templater

# Start services:
    sudo systemctl start templater
    sudo systemctl enable templater

