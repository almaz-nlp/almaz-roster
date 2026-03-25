import paramiko
import sys
import time

def run_remote(command):
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        print(f"Executing: {command}")
        stdin, stdout, stderr = client.exec_command(command)
        
        exit_status = stdout.channel.recv_exit_status()
        out = stdout.read().decode()
        err = stderr.read().decode()
        
        print("STDOUT:", out)
        if err:
            print("STDERR:", err)
        print("Exit Status:", exit_status)
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    with open('cmd.txt', 'r') as f:
        cmd = f.read().strip()
    run_remote(cmd)
