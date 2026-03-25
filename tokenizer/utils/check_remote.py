import paramiko

def check_remote():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        cmd = "ls -la /root/az-tokenizer && source /root/az-tokenizer/venv/bin/activate && python -c 'import transformers' 2>/dev/null && echo 'Environment Ready'"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        out = stdout.read().decode()
        err = stderr.read().decode()
        
        print("STDOUT:")
        print(out)
        print("STDERR:")
        print(err)
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_remote()
