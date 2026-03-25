import paramiko

def enforce_15k():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        sftp.put('d:\\tokenizer\\filter_tokens.py', '/root/az-tokenizer/filter_tokens.py')
        sftp.close()
        
        cmd = "cd /root/az-tokenizer && source venv/bin/activate && python filter_tokens.py && echo '---' && rm -rf ./qwen3_tokenizer_azerbaijani && python integrate_tokens.py"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err.strip():
            print("STDERR:", err)
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    enforce_15k()
