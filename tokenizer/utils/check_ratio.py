import paramiko

def check_ratio():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        stdin, stdout, stderr = client.exec_command("tail -n 10 /root/az-tokenizer/corpus_results.txt")
        out = stdout.read().decode()
        if out:
            print(out)
        else:
            print("The log file is empty or hasn't updated yet.")
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_ratio()
