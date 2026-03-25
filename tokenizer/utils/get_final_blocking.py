import paramiko
import sys

def check_results():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        cmd = "cd /root/az-tokenizer && source venv/bin/activate && python final_check.py"
        print(f"Running: {cmd}")
        stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
        
        for line in iter(stdout.readline, ""):
            print(line, end="")
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_results()
