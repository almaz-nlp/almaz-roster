import paramiko

def prep_steps():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        # We start cleaning & measuring baseline directly on the server
        cmd = "cd /root/az-tokenizer && source venv/bin/activate && python clean_corpus.py > clean.log 2>&1 && python measure_baseline.py > baseline_results.txt 2>&1"
        client.exec_command(cmd)
        
        print("Cleaning and Baseline Measurement kicked off.")
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    prep_steps()
