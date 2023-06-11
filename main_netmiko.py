from jinja2 import Environment, FileSystemLoader
import json, concurrent.futures
from netmiko import Netmiko

targets = [str(i) for i in range(1,8)]
def mainCode(target):
    host = {"host": f"192.168.200.{target}", "username":"test123","password":"huawei","device_type":"huawei"}#,"global_delay_factor":0.1}
    env = Environment(loader=FileSystemLoader('Jinja_templates'))
    shell = Netmiko(**host)
    jinjafiles = ["CE_Routers.j2", "CE_Routers.j2", "PE_Routers.j2", "PE_Routers.j2","Backbone_Routers.j2", "PE_Routers.j2", "CE_Routers.j2"]
    jsonfiles = ["CE1_inputs.json", "CE2_inputs.json", "PE3_inputs.json", "PE4_inputs.json", "P5_inputs.json" , "PE6_inputs.json", "CE7_inputs.json"]
    temp = env.get_template(jinjafiles[int(target)-1])

    with open("JSON_Inputs/" + jsonfiles[int(target)-1]) as f:
        data = f.read()
        output = json.loads(data)
        commands = 'system-view\n' + temp.render(config=output)
        for index, cmd in enumerate(commands.split('\n')):
            # print(index)
            tempo = shell.send_config_set(cmd,read_timeout=0.1, terminator=']', exit_config_mode=False, enter_config_mode=False)
            # print(tempo, end='')
        tempo = shell.send_config_set("return", read_timeout=0.1, exit_config_mode=False,enter_config_mode=False)
        savetrial = shell.save_config('save ' + jsonfiles[int(target) - 1].split('_')[0] + '.cfg')
        if savetrial.endswith("overwrite? (y/n)[n]:"):
            save = shell.save_config('y',confirm=True, confirm_response="")
        else:
            save = ''
        startup = shell.send_config_set('startup saved-configuration ' + jsonfiles[int(target) - 1].split('_')[0] + '.cfg\n', enter_config_mode=False, exit_config_mode=False)
        print(shell.send_command("display currrent-configuration"), savetrial, save, startup, sep='\n')




num_threads = len(targets)# multiprocessing.cpu_count()

# Create a thread pool executor with the desired number of threads
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    # Submit the slow function to the thread pool executor for each piece of data
    futures = [executor.submit(mainCode, remote) for remote in targets]
    # Wait for all the threads to complete
    results = [f.result() for f in futures]