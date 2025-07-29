import sys
from pathlib import Path

# Input file path
input_path = Path(sys.argv[1])
output_file = Path.cwd() / (input_path.stem + "_processed.txt")
# Process content
text = input_path.read_text()
output_file.write_text(f"Processed {input_path.stem} step")
