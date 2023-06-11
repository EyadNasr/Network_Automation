from jinja2 import Environment, FileSystemLoader
import json, time, paramiko, concurrent.futures


targets = [str(i) for i in range(1,8)]
def mainCode(target):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=f"192.168.200.{target}", port=22, username="test123", password="huawei")
    env = Environment(loader=FileSystemLoader('Jinja_templates'))
    shell = ssh.invoke_shell()
    shell.send('screen-length 0 temporary\n')
    jinjafiles = ["CE_Routers.j2", "CE_Routers.j2", "PE_Routers.j2", "PE_Routers.j2","Backbone_Routers.j2", "PE_Routers.j2", "CE_Routers.j2"]
    jsonfiles = ["CE1_inputs.json", "CE2_inputs.json", "PE3_inputs.json", "PE4_inputs.json", "P5_inputs.json" , "PE6_inputs.json", "CE7_inputs.json"]
    temp = env.get_template(jinjafiles[int(target)-1])

    with open("JSON_Inputs/" + jsonfiles[int(target)-1]) as f:
        data = f.read()
        output = json.loads(data)
        commands = temp.render(config=output) + '\n'
        # print(commands)
        shell.send('system-view\n')
        for i in commands.split('\n'):
            shell.send(i+'\n')
            time.sleep(0.5)
        shell.send('return\nsave ' + jsonfiles[int(target) - 1].split('_')[0] + '.cfg\n')
        time.sleep(1)
        shell.send('y\n')
        time.sleep(3)
        shell_session = shell.recv(999999).decode()
        if shell_session.endswith(" exists, overwrite? (y/n)[n]:"):
            shell.send('y\n')
            time.sleep(3)
        shell.send('startup saved-configuration ' + jsonfiles[int(target) - 1].split('_')[0] + '.cfg\n')
        time.sleep(3)
        final_shell_session = shell.recv(999999).decode()
        time.sleep(3)
        print(shell_session + final_shell_session)


num_threads = len(targets)# multiprocessing.cpu_count()

# Create a thread pool executor with the desired number of threads
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    # Submit the slow function to the thread pool executor for each piece of data
    futures = [executor.submit(mainCode, remote) for remote in targets]
    # Wait for all the threads to complete
    results = [f.result() for f in futures]