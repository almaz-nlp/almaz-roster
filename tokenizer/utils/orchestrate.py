import paramiko
import sys

def run_orchestration():
    print("Connecting to server via SSH...")
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        # Command sequence
        cmd = """
        export DEBIAN_FRONTEND=noninteractive
        apt-get update -y
        apt-get install -y python3-venv screen
        cd /root/az-tokenizer
        python3 -m venv venv || python3.10 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip
        pip install transformers sentencepiece huggingface_hub datasets torch
        
        echo "Starting Tokenizer Download..."
        python download_tokenizer.py
        
        echo "Starting DOLLMA corpus download inside GNU screen..."
        screen -d -m -S tokenizer bash -c 'source venv/bin/activate && python download_dollma.py > dollma_download.log 2>&1'
        
        echo "Orchestration successfully kicked off!"
        """
        
        print(f"Executing commands...")
        stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
        
        # Stream output line by line
        for line in iter(stdout.readline, ""):
            print(line, end="")
            
        client.close()
    except Exception as e:
        print(f"Error during orchestration: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_orchestration()
