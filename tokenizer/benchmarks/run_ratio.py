import paramiko

def run_ratio():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        cmd = "screen -wipe ; screen -d -m -S corpus_verify bash -c 'cd /root/az-tokenizer && source venv/bin/activate && python -u corpus_ratio.py > corpus_results.txt 2>&1'"
        client.exec_command(cmd)
        
        print("Corpus ratio validation sequence running.")
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run_ratio()
