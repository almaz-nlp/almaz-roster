import paramiko

def fast_eval_file():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        sftp.put('d:\\tokenizer\\micro_eval_direct.py', '/root/az-tokenizer/micro_eval_direct.py')
        
        cmd = "cd /root/az-tokenizer && source venv/bin/activate && python micro_eval_direct.py && cat micro_eval_results.txt"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err: print("ERR:", err)
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    fast_eval_file()
