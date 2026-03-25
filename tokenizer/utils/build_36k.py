import paramiko

def build_36k_model():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Backup the current 20k model
        cmd_backup = "cd /root/az-tokenizer && mv qwen3_tokenizer_azerbaijani qwen3_tokenizer_az_20k"
        client.exec_command(cmd_backup)
        
        # Upload the unrestricted filter
        sftp.put('d:\\tokenizer\\filter_tokens.py', '/root/az-tokenizer/filter_tokens.py')
        
        # Run the full pipeline
        cmd_run = "cd /root/az-tokenizer && source venv/bin/activate && python filter_tokens.py && rm -rf ./qwen3_tokenizer_azerbaijani && python integrate_tokens.py && python final_check.py > final_results_36k.txt 2>&1 && cat final_results_36k.txt"
        
        print("Building full unrestricted 36k token model...")
        stdin, stdout, stderr = client.exec_command(cmd_run)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err.strip():
            print("Errors:", err)
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    build_36k_model()
