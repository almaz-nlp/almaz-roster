import paramiko

def update_and_run():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Upload the fixed python script
        sftp.put('d:\\tokenizer\\download_dollma.py', '/root/az-tokenizer/download_dollma.py')
        sftp.close()
        
        # Relaunch the screen properly
        cmd = "screen -wipe ; screen -d -m -S dollma_dl bash -c 'cd /root/az-tokenizer && source venv/bin/activate && python -u download_dollma.py > dollma_download.log 2>&1'"
        client.exec_command(cmd)
        
        print("Updated download_dollma.py uploaded and running.")
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    update_and_run()
