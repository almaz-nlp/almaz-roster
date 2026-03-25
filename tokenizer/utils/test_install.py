#!/usr/bin/env python3
"""
=== test_install.py ===
Step 1: Verify all dependencies are installed.
"""

import sentencepiece
import transformers
import torch

print(f"sentencepiece: {sentencepiece.__version__}")
print(f"transformers:  {transformers.__version__}")
print(f"torch:         {torch.__version__}")
print("All good!")
