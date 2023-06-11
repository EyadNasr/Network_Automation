# Network_Automation
Automating Hub &amp; Spokes MPLS L3VPN with python paramiko and netmiko modules on Huawei eNSP
![image](https://github.com/EyadNasr/Network_Automation/assets/62260537/7dfbe457-fbca-4a3f-92e3-420881c64c45)
All routers are initally configured with the following:
- Interface GE4/0/0 has an IP address from the subnet 192.168.200.0/24 (**.1** through **.7**) which is directly connected to the cloud network (local windows network adapter) which has the IP 192.168.200.254
- All routers are configured with ssh username: **test123** and a password: **huawei**

