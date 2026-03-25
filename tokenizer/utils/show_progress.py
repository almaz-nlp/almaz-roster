import paramiko

def show_progress():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        cmd = "tail -n 15 /root/az-tokenizer/dollma_download.log"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        out = stdout.read().decode()
        print(out)
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    show_progress()
