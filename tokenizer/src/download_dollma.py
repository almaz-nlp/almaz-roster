import os
import sys
from datasets import load_dataset
import traceback

def main():
    token = "YOUR_HF_TOKEN_HERE"
    configs = ['anl-news', 'azwiki', 'bhos', 'elite-blogs', 'elite-books', 'eqanun', 'mediocore-books', 'translated-enwiki']
    
    os.makedirs("data", exist_ok=True)
    out_file = "data/az_corpus.txt"
    
    print("Starting DOLLMA dataset download...")
    try:
        written_lines = 0
        
        # Open in append mode so we can resume or append configs sequentially
        with open(out_file, "w", encoding="utf-8") as f:
            for config in configs:
                print(f"\\n--- Downloading config: {config} ---")
                try:
                    ds = load_dataset("allmalab/DOLLMA", config, split="train", token=token)
                    
                    config_lines = 0
                    for item in ds:
                        text = item.get("text", "")
                        if text:
                            # Split by newline and strip spaces
                            lines = text.split("\\n")
                            for line in lines:
                                line = line.strip()
                                if line:
                                    f.write(line + "\\n")
                                    written_lines += 1
                                    config_lines += 1
                                    
                                    if written_lines % 500000 == 0:
                                        print(f"Written {written_lines} lines total...")
                                        f.flush()
                    print(f"Finished {config} ({config_lines} lines).")
                except Exception as inner_e:
                    print(f"Error on config {config}: {inner_e}", file=sys.stderr)
                    
        print(f"\\nDone downloading DOLLMA. Total lines: {written_lines}")
    except Exception as e:
        print(f"Fatal error: {e}\\n{traceback.format_exc()}", file=sys.stderr)

if __name__ == "__main__":
    main()
