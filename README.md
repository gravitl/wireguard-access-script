# WireGuard Configuration Generator

This script helps you generate WireGuard configuration files for multiple peers and a gateway. It uses Python to automate the process of creating these files, which makes setting up a WireGuard VPN easier and faster.

# How It Works
#### 1. Generate Keys: 
For each peer, the script creates a unique set of keys (a private key and a public key).
#### 2. Create Peer Configurations: 
Each peer gets its own configuration file with its unique keys and settings.
#### 3. Create Gateway Configuration: 
A special configuration file is created for the gateway. It includes all the peer public keys and necessary settings for the gateway.

# Features
Automatic Key Generation: Uses python_wireguard to generate WireGuard keys.
Config Files Creation: Generates configuration files for each peer and the gateway.
File Storage: Saves configuration files to a specified folder in Google Drive.

# Requirements
Python 3.x
python_wireguard library (install with pip install python_wireguard)

# How to Use

#### 1. Prepare Your Environment: 
Make sure you have Python and the required library installed.

#### 2. Run the Script:

  Open the script in a Python environment (like a Jupyter notebook).
  Execute the script.
  When prompted, enter the number of peers you want to configure.
  
#### 3. Check the Output:

Configuration files will be saved in the wg_config files folder in your Google Drive.

# Script Details
## Functions

#### 1. generate_key_pair():
Creates a private and public key pair for WireGuard.

#### 2. create_config(peer_num, private_key, address):

Generates a configuration file for a peer with its private key and IP address. Saves the file in the wg_config files folder. The peer's public key is also stored in a list to be used later in the gateway configuration.

#### 3. create_gateway_config(peers_public_keys):

Creates a configuration file for the gateway.
Includes all peer public keys in the configuration.
Saves the file in the wg_config files folder.
#### 4. main():

Main function that runs the script.
Asks for the number of peers.
Generates configuration files for each peer and the gateway.

# Notes
The PostUp and PostDown commands in the gateway configuration manage NAT rules using nftables. You can customize these commands based on your system's requirements.
Make sure the folder path (/content/drive/MyDrive/wg_config files) is correct and accessible in your environment.
