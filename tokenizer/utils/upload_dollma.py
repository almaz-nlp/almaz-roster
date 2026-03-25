import paramiko
import os

print("Starting SFTP transfer for download_dollma.py...")
try:
    transport = paramiko.Transport(('67.211.221.234', 22))
    transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    local_file = 'd:\\tokenizer\\download_dollma.py'
    remote_path = '/root/az-tokenizer/download_dollma.py'
    sftp.put(local_file, remote_path)
        
    sftp.close()
    transport.close()
    print("File uploaded successfully.")
except Exception as e:
    print(f"Error: {e}")
