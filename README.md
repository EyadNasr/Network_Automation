1- Before downloading the folder, insure that these modules are installed:
   - pip install paramiko
   - pip install netmiko
   - pip install jinja2

2- Add a loopback adapter as shown here https://forum.huawei.com/enterprise/en/connect-pc-to-ensp/thread/628999-861
   - After restarting your pc, configure the loopback adapter with this IP **192.168.200.254**
    ![image](https://github.com/EyadNasr/Network_Automation_hub-spoke/assets/62260537/a7e0f88b-e70f-4765-b7bb-13bbb8506bf0)
   - Download the lab and bind the cloud with the adapter as shown in the link above
    ![image](https://github.com/EyadNasr/Network_Automation_hub-spoke/assets/62260537/3bc6c576-4026-4000-a0ef-702916fd89a4)

3- Run the python script main_paramiko.py or main_netmiko.py to configure the hub & spoke topology
   - To confirm that the topology is configured successfully, ping **172.16.0.1** from **Spoke-CE1** and ping **192.168.1.1** from **Spoke-CE2**

# Network_Automation
Automating Hub &amp; Spokes MPLS L3VPN with python paramiko and netmiko modules on Huawei eNSP

![image](https://github.com/EyadNasr/Network_Automation/assets/62260537/7dfbe457-fbca-4a3f-92e3-420881c64c45)

All routers are initally configured with the following:
- Interface GE4/0/0 has an IP address from the subnet 192.168.200.0/24 (**.1** through **.7**) which is directly connected to the cloud network (local windows network adapter) which has the IP 192.168.200.254
- All routers are configured with ssh username: **test123** and a password: **huawei**
- No other configuration is done on the routers

