
import sys, paramiko


hostnames = ['192.168.0.101','192.168.0.102','192.168.0.103','192.168.0.104']
passwords = ['AKZCobotUR3','AKZCobotUR5','AKZGravierer','0ctoPr!nt']
#hostname = "192.168.0.103"
#password = "AKZGravierer"
command = "sudo shutdown -h now"

username = "pi"
port = 22

for key,val in enumerate(hostnames):
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())

        client.connect(hostnames[key], port=port, username=username, password=passwords[key])
        # client.connect(hostname, port=port, username=username, password=password, pkey=None, key_filename="gcp_public")

        stdin, stdout, stderr = client.exec_command(command)
        # print(stdout.read())

    except:
        print("Error connecting to server!")

    finally:
        client.close()

