import paramiko

def show_results():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        print("Checking clean.log...")
        stdin, stdout, stderr = client.exec_command("cat /root/az-tokenizer/clean.log")
        print(stdout.read().decode())
        
        print("\\nChecking baseline_results.txt...")
        stdin, stdout, stderr = client.exec_command("cat /root/az-tokenizer/baseline_results.txt")
        print(stdout.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    show_results()
