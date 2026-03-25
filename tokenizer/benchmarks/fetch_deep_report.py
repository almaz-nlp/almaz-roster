import paramiko

def fetch_report():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        remote = "/root/az-tokenizer/deep_validation_report.txt"
        local = "d:\\\\tokenizer\\\\deep_validation_report.txt"
        sftp.get(remote, local)
        sftp.close()
        client.close()
        
        with open(local, "r") as f:
            print("=== LOCAL REPORT READ ===")
            print(f.read())
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    fetch_report()
