import paramiko

def run_fix():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        cmd = "screen -wipe && screen -d -m -S dollma_dl bash -c 'cd /root/az-tokenizer && source venv/bin/activate && python download_dollma.py > dollma_download.log 2>&1'"
        client.exec_command(cmd)
        print("Screen session 'dollma_dl' started.")
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run_fix()
