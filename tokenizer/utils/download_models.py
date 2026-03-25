import paramiko
import tarfile
import os

def download_models():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # 1. Compress folders on server
        print("Compressing tokenizers on server...")
        cmd_tar = "cd /root/az-tokenizer && tar -czf exported_models.tar.gz qwen3_tokenizer_az_14k qwen3_tokenizer_az_20k qwen3_tokenizer_azerbaijani new_tokens.tsv"
        stdin, stdout, stderr = client.exec_command(cmd_tar)
        stdout.channel.recv_exit_status() # wait for tar to finish
        
        # 2. Download the compressed file
        local_path = "d:\\\\tokenizer\\\\exported_models.tar.gz"
        remote_path = "/root/az-tokenizer/exported_models.tar.gz"
        print("Downloading to D:\\\\tokenizer...")
        sftp.get(remote_path, local_path)
        
        # 3. Extract locally
        print("Extracting files...")
        with tarfile.open(local_path, "r:gz") as tar:
            tar.extractall(path="d:\\\\tokenizer")
            
        print("Download and extraction complete.")
        
        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    download_models()
