import subprocess
import sys
from pathlib import Path

def run_all(pdf_path):
    paper_name = Path(pdf_path).stem
    # The output folder created by the 'extract' script
    target_folder = f"markdown_output/{paper_name}"

    print(f"--- Starting Full Workflow for: {pdf_path} ---")
    
    # 1. Extract
    print("Step 1: Extracting...")
    subprocess.run(["phd-deepread", "extract", pdf_path], check=True)
    
    # 2. Generate
    print("Step 2: Generating Literature Note...")
    subprocess.run(["phd-deepread", "generate", target_folder], check=True)
    
    # 3. Canvas
    print("Step 3: Creating Visual Canvas...")
    subprocess.run(["phd-deepread", "canvas", target_folder], check=True)

    print(f"--- Workflow Complete! Check the {target_folder} directory. ---")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: phd-deepread run <file.pdf>")
    else:
        run_all(sys.argv[1])