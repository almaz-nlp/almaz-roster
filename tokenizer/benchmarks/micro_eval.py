import paramiko

def fast_eval():
    try:
        transport = paramiko.Transport(('67.211.221.234', 22))
        transport.connect(username='root', password='YOUR_SERVER_PASSWORD_HERE')
        client = paramiko.SSHClient()
        client._transport = transport
        
        # Prepare 2000 line sample locally
        print("Preparing fast sample test...")
        cmd_prep = "cd /root/az-tokenizer && head -n 4000 corpus_clean.txt > sample_test.txt"
        client.exec_command(cmd_prep)
        
        # Override the target file in the python string quickly via sed or directly run a Python snippet
        python_script = """
from transformers import AutoTokenizer

old_tok = AutoTokenizer.from_pretrained("./qwen3_tokenizer_original")
new_tok = AutoTokenizer.from_pretrained("./qwen3_tokenizer_azerbaijani")

total_old = total_new = total_words = lines = 0

with open("sample_test.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        words = line.split()
        total_words += len(words)
        total_old   += len(old_tok.tokenize(line))
        total_new   += len(new_tok.tokenize(line))
        lines += 1

old_r = total_old / total_words
new_r = total_new / total_words
delta = ((old_r - new_r) / old_r) * 100

print(f"\\n--- FAST SAMPLE RESULTS (4000 sentences) ---")
print(f"Lines Evaluated: {lines:,}")
print(f"Total Words:     {total_words:,}")
print(f"Original Qwen:   {old_r:.3f} tokens/word")
print(f"Azerbaijani Tok: {new_r:.3f} tokens/word")
print(f"Improvement:     {delta:.1f}%")
print("------------------------------------------")
"""
        # Run it directly
        cmd_run = f"cd /root/az-tokenizer && source venv/bin/activate && python -c '{python_script}'"
        stdin, stdout, stderr = client.exec_command(cmd_run, get_pty=True)
        
        for line in iter(stdout.readline, ""):
            print(line, end="")
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    fast_eval()
