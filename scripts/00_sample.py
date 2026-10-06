
import pandas as pd
from pathlib import Path
import random
import csv

# patches for batch1 for visually selected

# sample patches for batch2 randomly, excluding samples already contained in batch1
DIR = Path("O:/Data-Work/22_Plant_Production-CH/224_Digitalisation/Jonas_Anderegg_Files/B_Data/04_DL_datasets_updates/focus")
img_paths = pd.read_csv(DIR / "batch1/src.txt", header=None)[0].tolist()
img_paths = [Path(p) for p in img_paths]

# for batch2, we want to sample 100 images randomly from the source.txt files in the batch directories, 
# excluding any images that are already in batch1.
ROOT = Path(
    "O:/Data-Work/22_Plant_Production-CH/224_Digitalisation/"
    "Jonas_Anderegg_Files/B_Data/04_DL_datasets_updates/symptoms"
)
source_files = sorted(ROOT.glob("batch*/img/source.txt"))
source_paths = [
    Path(line.strip().strip('"').strip("'"))
    for source_file in source_files
    for line in source_file.read_text().splitlines()
    if line.strip()
]
remaining = [p for p in source_paths if p not in img_paths]

random.seed(42)
sampled_paths = random.sample(remaining, 100)
output_csv = DIR / "batch2/src.txt"
output_csv.parent.mkdir(parents=True, exist_ok=True)

with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    
    for p in sampled_paths:
        writer.writerow([str(p)])
