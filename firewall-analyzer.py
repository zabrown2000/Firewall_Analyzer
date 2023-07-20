#firewall-analyzer.py

import subprocess
import paramiko
import requests

import importlib

# Configuration for the victim machine where the firewall configurations are located
victim_host = "192.168.1.209"
victim_username = "kali"
victim_password = "kali"
# Configuration for the attacker machine where the attack scripts are located
attacker_host = "192.168.1.101"
attacker_username = "kali"
attacker_password = "kali"
firewall_configurations = [
    {
        "name": "iptables",
        "path": "/etc/iptables.rules.v4",
        "url": "http://192.168.1.209/",
        "bcmd": "",
        "acmd": "sudo iptables -F"
    }#,
    #{
    #    "name": "nginx",
    #    "path": "/etc/nginx/nginx_test.conf",
    #    "url": "http://192.168.1.209/",
    #    "bcmd": "sudo pkill -f nginx",
    #    "acmd": ""
    #}
]

firewall_commands = {
    "iptables": "sudo systemctl start netfilter-persistent",
    "nginx": "sudo nginx -c /etc/nginx/nginx_test.conf"
}
attacks = [
    {
        "name": "Insecure HTTP Methods",
        "module": "insecure-http",
    },
    {
        "name": "Clickjacking",
        "module": "clickjacking",
    },
    {
        "name": "MIME Sniffing",
        "module": "mime",
    },
    {
        "name": "Cross-Domain Requests",
        "module": "cross-domain",
    }
]
results = []
# Connect to the victim machine
victim_ssh = paramiko.SSHClient()
victim_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
victim_ssh.connect(victim_host, username=victim_username, password=victim_password)
# Loop through each firewall configuration ---------------------------will need to check if iptable first, and then before new nginx to kill old version and iptables
for config in firewall_configurations:
    #command to run before starting the current firewall
    victim_ssh.exec_command(f"{config['bcmd']}")
    # Load the firewall configuration on the victim machine
    print(f"Loading firewall configuration: {config['name']}")
    victim_ssh.exec_command(f"{firewall_commands[config['name']]}")
    
    # Loop through each attack
    for attack in attacks:
        attack_name = attack["name"]
        attack_module = importlib.import_module(attack["module"])
        success = attack_module.main()

        # Add the results to the list
        results.append({
            "configuration": config["name"],
            "attack_script": attack_name,
            "success": success
        })
    #command to run after the current firewall is done
    victim_ssh.exec_command(f"{config['acmd']}")
    print("-" * 50)
# Print the results
print("Final Results:\n")
for result in results:
    print(f"Configuration: {result['configuration']}")
    print(f"Attack Script: {result['attack_script']}")
    print(f"Success: {result['success']}")
    print()
# Close the connection to the victim machine
victim_ssh.close()
