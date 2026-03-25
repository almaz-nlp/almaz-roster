import paramiko
import time

def get_report():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        print("Waiting for deep_val to finish...", flush=True)
        for _ in range(60):
            stdin, stdout, stderr = client.exec_command("cat /root/az-tokenizer/deep_validation_report.txt 2>/dev/null")
            out = stdout.read().decode()
            if "DEEP STATISTICAL VALIDATION" in out:
                print("\\n--- REPORT FOUND ---\\n")
                print(out)
                client.close()
                return
            time.sleep(5)
            
        print("Report not found after 5 minutes.")
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    get_report()
