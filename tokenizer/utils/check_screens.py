import paramiko

def check_status():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        print("--- SCREEN LS ---")
        stdin, stdout, stderr = client.exec_command("screen -ls")
        print(stdout.read().decode())
        
        print("--- LOG FILE TAIL ---")
        stdin, stdout, stderr = client.exec_command("tail -n 20 /root/az-tokenizer/dollma_download.log")
        print(stdout.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_status()
