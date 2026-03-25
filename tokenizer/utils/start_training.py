import paramiko

def run_training():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        # Start unigram training safely inside a background screen
        cmd = "screen -wipe ; screen -d -m -S unigram_train bash -c 'cd /root/az-tokenizer && source venv/bin/activate && python -u train_unigram.py > unigram.log 2>&1'"
        client.exec_command(cmd)
        
        print("Training successfully started.")
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run_training()
