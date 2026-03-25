import paramiko
import os
import glob
import sys

def upload_all():
    print("Connecting to SFTP...", flush=True)
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Ensure remote directory exists
        try:
            sftp.stat('/root/az-tokenizer')
        except IOError:
            sftp.mkdir('/root/az-tokenizer')
            
        try:
            sftp.stat('/root/az-tokenizer/data')
        except IOError:
            sftp.mkdir('/root/az-tokenizer/data')
            
        files = glob.glob('d:/tokenizer/*.py')
        print(f"Found {len(files)} files to upload.", flush=True)
        
        for f in files:
            bn = os.path.basename(f)
            # Skip the paramiko upload scripts from going to the remote
            if bn in ('upload.py', 'upload_dollma.py', 'remote_exec.py', 'run_setup.py', 'check_remote.py', 'upload_all.py'):
                continue
            remote_path = f'/root/az-tokenizer/{bn}'
            print(f"Uploading {bn}...", flush=True)
            sftp.put(f, remote_path)
            
        print("Uploads complete.", flush=True)
        sftp.close()
        transport.close()
        
    except Exception as e:
        print(f"SFTP Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    upload_all()
