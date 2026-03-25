import paramiko

def run_fast_check():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        sftp.put('d:\\tokenizer\\fast_sample_check.py', '/root/az-tokenizer/fast_sample_check.py')
        
        cmd = "cd /root/az-tokenizer && source venv/bin/activate && python fast_sample_check.py"
        print("Running finalized 300k batch validation...")
        stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
        
        for line in iter(stdout.readline, ""):
            print(line, end="")
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run_fast_check()
