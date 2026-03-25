import paramiko
import sys

def check_unigram_log():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        print("Checking unigram.log...")
        stdin, stdout, stderr = client.exec_command("tail -n 15 /root/az-tokenizer/unigram.log")
        out = stdout.read().decode()
        print(out if out.strip() else "Log is empty or hasn't started writing yet.")
        
        stdin, stdout, stderr = client.exec_command("ls -la /root/az-tokenizer/*.model 2>/dev/null")
        out = stdout.read().decode()
        if out.strip():
            print("\\nFound trained models:\\n", out)
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_unigram_log()
