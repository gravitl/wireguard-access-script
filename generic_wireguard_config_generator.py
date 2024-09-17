from python_wireguard import Key
import os
import time

def generate_key_pair():
    private_key, public_key = Key.key_pair()
    return private_key, public_key

##################################################################################################################################################################
def create_peer_config(peer_num, private_key, address, gateway_public_key, gateway_endpoint, allowed_ips, dns_server, config_dir):
    config = f"""
[Interface]
PrivateKey = {private_key}
Address = {address}
DNS = {dns_server}

[Peer]
PublicKey = {gateway_public_key}
Endpoint = {gateway_endpoint}
AllowedIPs = {allowed_ips}
PersistentKeepalive = 25
"""
    peer_num = peer_num - 1
    filename = os.path.join(config_dir, f'wg_peer_{peer_num}.conf')
    with open(filename, 'w') as file:
        file.write(config)
    print(f"Configuration file for peer {peer_num} created: {filename}")

################################################################################################################################################################
def create_gateway_config(peers_public_keys, gateway_private_key, gateway_allowed_ips, config_dir):
    config = f"""
[Interface]
PrivateKey = {gateway_private_key}
Address = 10.191.143.1/32
ListenPort = 51820

PostUp = sysctl -w net.ipv4.ip_forward=1
PostUp = nft add rule ip nat postrouting oifname "eth1" masquerade
PostDown = nft delete rule ip nat postrouting oifname "eth1" masquerade
"""
    for i, public_key in enumerate(peers_public_keys, start=2):
        config += f"""
[Peer]
PublicKey = {public_key}
AllowedIPs = 10.191.143.{i}/32
PersistentKeepalive = 25
"""
    filename = os.path.join(config_dir, 'wg_gateway.conf')
    with open(filename, 'w') as file:
        file.write(config)
    print(f"Gateway configuration file created: {filename}")

####################################################################################################################################################################

def main():
    num_peers = int(input("Enter the number of peers: "))
    gateway_private_key = input("Enter the private key for the gateway: ")
    gateway_public_key = input("Enter the public key for the gateway: ")
    gateway_endpoint = input("Enter the endpoint for the gateway (IP:Port): ")
    gateway_allowed_ips = input("Enter the AllowedIPs for the gateway: ")
    dns_server = input("Enter the DNS server address: ")

    base_peer_address = input("Enter the base address for the peers (e.g., 10.191.143.2/32): ")
    base_ip = base_peer_address.split('.')[0:3]  # ['10', '191', '143']
    start_ip = int(base_peer_address.split('.')[3].split('/')[0])  # Starting number (e.g., 2)

    peer_allowed_ips = input("Enter the AllowedIPs for all peers: ")
    config_dir = input("Enter the directory path to save configuration files: ")

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    peers_public_keys = []
    for i in range(num_peers):
        private_key, public_key = generate_key_pair()
        peer_address = f"{'.'.join(base_ip)}.{start_ip + i}/32"  # Increment IP address for each peer
        peers_public_keys.append(public_key)
        create_peer_config(i + 2, private_key, peer_address, gateway_public_key, gateway_endpoint, peer_allowed_ips, dns_server, config_dir)
        time.sleep(10)

    create_gateway_config(peers_public_keys, gateway_private_key, gateway_allowed_ips, config_dir)

    print("Done")

if __name__ == "__main__":
    main()
