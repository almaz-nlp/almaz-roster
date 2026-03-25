import paramiko

def run_deep_remote():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        sftp.put('d:\\tokenizer\\deep_validate_all.py', '/root/az-tokenizer/deep_validate_all.py')
        
        # Run in a background screen so it's guaranteed to finish even if connection drops
        cmd = "screen -wipe ; screen -d -m -S deep_val bash -c 'cd /root/az-tokenizer && source venv/bin/activate && python deep_validate_all.py > deep_val.log 2>&1'"
        client.exec_command(cmd)
        
        print("Deep validation started in detached screen 'deep_val'.")
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run_deep_remote()
