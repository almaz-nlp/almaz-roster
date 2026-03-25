import paramiko

def build_20k_model():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Backup the current 14k model
        cmd_backup = "cd /root/az-tokenizer && cp -r qwen3_tokenizer_azerbaijani qwen3_tokenizer_az_14k"
        client.exec_command(cmd_backup)
        
        # Upload the new strict-20k filter
        sftp.put('d:\\tokenizer\\filter_tokens.py', '/root/az-tokenizer/filter_tokens.py')
        
        # Run the full pipeline
        cmd_run = "cd /root/az-tokenizer && source venv/bin/activate && python filter_tokens.py && rm -rf ./qwen3_tokenizer_azerbaijani && python integrate_tokens.py && python final_check.py > final_results_20k.txt 2>&1 && cat final_results_20k.txt"
        
        print("Building strict 20k token model...")
        stdin, stdout, stderr = client.exec_command(cmd_run)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err.strip():
            print("Errors:", err)
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    build_20k_model()
