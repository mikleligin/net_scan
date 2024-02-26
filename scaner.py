from platform import system
from socket import socket, AF_INET, SOCK_DGRAM
from subprocess import check_output
import subprocess
import os

import scapy.all as scapy

def get_ip():
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ip_l = s.getsockname()[0]
        return ip_l
    except:
        ip_l = '127.0.0.1'
    finally:
        s.close()
    
def get_ip_mac_nework(ip):
    answered_list = scapy.srp(scapy.Ether(dst='ff:ff:ff:ff:ff:ff') / scapy.ARP(pdst=ip), timeout=1, verbose=False)[0]
    clients_list = []
    for element in answered_list:
        clients_list.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})
    return clients_list
   
def get_getaway():
    #com = f'route PRINT 0* | find {get_ip()}'.split()
    #output = subprocess.Popen( com, stdout=subprocess.PIPE ).communicate()[0]
    #print(output)
    #print(check_output(com).decode('cp866').split()[2])
    com = f'route PRINT 0* | findstr {get_ip()}'
    result = subprocess.run(com, stdout=subprocess.PIPE, shell=True, text=True)
    print(result.stdout.split()[2])

def print_ip_mac(mac_ip_list):
    print(f"IP\t\t\t\t\tMAC-address\n{'-' * 41}")
    for client in mac_ip_list:
        print(f'{client["ip"]}\t\t{client["mac"]}')

if __name__ == "__main__":
    ip = get_ip()
    gateway = get_getaway()
    ip_mac_network = get_ip_mac_nework(f'{ip.split(".")[0]}.{ip.split(".")[1]}.{ip.split(".")[2]}.1/24')
    print(f'\n{ip}\n{gateway}')
    print_ip_mac(ip_mac_network)