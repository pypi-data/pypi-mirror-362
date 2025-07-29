import sys
from pathlib import Path

# Input string, e.g., "Hello_Alice"
input_str = sys.argv[1]

# Create a file with name derived from input
output_path = Path(f"{input_str}.txt")
output_path.write_text(f"This is step 1 content for {input_str}.\n")
