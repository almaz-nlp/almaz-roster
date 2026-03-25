import paramiko
import sys

def fast_ratio():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Upload patched script
        sftp.put('d:\\tokenizer\\corpus_ratio.py', '/root/az-tokenizer/corpus_ratio.py')
        
        # Execute natively and stream output
        cmd = "cd /root/az-tokenizer && source venv/bin/activate && python -u corpus_ratio.py"
        print("Running accurate sampling...")
        stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)
        
        for line in iter(stdout.readline, ""):
            print(line, end="")
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    fast_ratio()
