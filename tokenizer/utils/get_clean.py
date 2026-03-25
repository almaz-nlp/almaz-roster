import paramiko
import sys

def get_clean_results():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        _, stdout, _ = client.exec_command("grep -A 5 'Total lines read:' /root/az-tokenizer/clean.log")
        print("--- CLEAN LOG ---")
        print(stdout.read().decode())
        
        _, stdout, _ = client.exec_command("grep -A 2 'AVERAGE FERTILITY' /root/az-tokenizer/baseline_results.txt")
        print("--- BASELINE LOG ---")
        print(stdout.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    get_clean_results()
