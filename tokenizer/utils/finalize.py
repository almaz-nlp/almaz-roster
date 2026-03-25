import paramiko

def finalize():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        cmd = "cd /root/az-tokenizer && source venv/bin/activate && python filter_tokens.py && echo '---' && python integrate_tokens.py"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print("STDOUT:")
        out = stdout.read().decode()
        print(out)
        
        err = stderr.read().decode()
        if err.strip():
            print("STDERR:")
            print(err)
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    finalize()
