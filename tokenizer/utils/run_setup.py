import paramiko
import sys

def setup():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        print("Connected.")
        
        # We use get_pty=True so commands like apt-get and screen don't buffer/hang
        cmd = """
        export DEBIAN_FRONTEND=noninteractive
        apt-get update -y
        apt-get install -y python3.10-venv python3-venv screen
        mkdir -p /root/az-tokenizer
        cd /root/az-tokenizer
        python3 -m venv venv
        source venv/bin/activate
        pip install transformers sentencepiece huggingface_hub datasets torch
        python download_tokenizer.py
        """
        
        stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
        
        for line in iter(stdout.readline, ""):
            print(line, end="")
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    setup()
