import paramiko
import os
import glob

print("Starting SFTP transfer...")
try:
    transport = paramiko.Transport(('67.211.221.234', 22))
    transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    files = glob.glob('d:\\tokenizer\\*.py')
    for f in files:
        basename = os.path.basename(f)
        remote_path = f'/root/az-tokenizer/{basename}'
        print(f"Uploading {basename}...")
        sftp.put(f, remote_path)
        
    sftp.close()
    transport.close()
    print("All files uploaded successfully.")
except Exception as e:
    print(f"Error: {e}")
