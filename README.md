# Firewall_Analyzer

NOTE: This project was deployed in a contained environment on a Kali Linux machine. If this code is used, be sure to protect your machine.

## Attacker Machine Instructions:
  1. You'll need to do pip install paramiko
  2. Ping the victim machine to ensure machines are connected
  3. Start ssh - sudo systemctl start ssh
  4. Make sure attack module scripts are located in the same directory as the analyzer
  5. Update attacker and victim machine info in firewall-analyzer.py for ssh functionality
  6. Once the victim machine is set up, run firewall-analyzer.py
  7. Make sure to change all IP addresses in the file to be your victim machine's IP
## Victim Machine Instructions:
  1. Start ssh - sudo systemctl start ssh
  2. When using no firewall or iptables, for any test to work correctly the default nginx configuration has to be running
     1. Sudo systemctl start nginx
     2. Ensure nginx is running - ps aux | grep nginx (nginx.conf should be running)
  4. Iptables
     1. Run sudo iptables -F to get rid of any existing rules
     2. Open conf file with - sudo nano /etc/iptables/rules.v4
     3. Put in the rules below and save
  6. Save the rules to the system - sudo iptables-save > /etc/iptables/rules.v4
  7. Run sudo iptables -L and check that rules added to file are outputted
  8. When switching to the next firewall
     1. Run sudo iptables -F
     2. Stop iptables - sudo systemctl restart netfilter-persistent
 
### This is just a proof of concept and can be scaled up to include any number of attacks and different firewall configurations, for example firewalld, nginx, etc
