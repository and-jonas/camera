from pathlib import Path
import re
import shutil

batch = "batch2"


# copy the patches with overlay for visual confirmation of congruency
ROOT = Path(
    "O:/Data-Work/22_Plant_Production-CH/224_Digitalisation"
    "/Jonas_Anderegg_Files/B_Data/04_DL_datasets_updates/focus" / batch / "focus_stacks"
)
DIRS = sorted([d / "out" for d in ROOT.iterdir() if d.is_dir() and re.fullmatch(r"[A-Za-z0-9]{8}", d.name)])

OUTPUT_DIR = ROOT.parent / "patches_with_overlay_control"
OUTPUT_DIR.mkdir(exist_ok=True)

for dir in DIRS:
    for patch in dir.glob("*.png"):
        shutil.copy(patch, OUTPUT_DIR / patch.name)


# also copy patches without overlay for visual confirmation of congruency
ROOT = Path("O:/Data-Work/22_Plant_Production-CH/224_Digitalisation/Jonas_Anderegg_Files/B_Data/04_DL_datasets_updates/symptoms")
DIRS = sorted([d / "patches" for d in ROOT.iterdir() if d.is_dir() and re.fullmatch(r"batch\d+", d.name)])

sample_names = [p.stem for p in (OUTPUT_DIR).glob("*.png")]
for dir in DIRS:
    for patch in dir.glob("*.png"):
        if patch.stem in sample_names:
            shutil.copy(patch, OUTPUT_DIR / (patch.stem + "_nooverlay.png"))



# copy the patches with overlay for CVAT upload
ROOT = Path(
    "O:/Data-Work/22_Plant_Production-CH/224_Digitalisation"
    "/Jonas_Anderegg_Files/B_Data/04_DL_datasets_updates/focus" / batch / "focus_stacks"
)
DIRS = sorted([d / "out" for d in ROOT.iterdir() if d.is_dir() and re.fullmatch(r"[A-Za-z0-9]{8}", d.name)])

OUTPUT_DIR = ROOT.parent / "patches_with_overlay"
OUTPUT_DIR.mkdir(exist_ok=True)

for dir in DIRS:
    for patch in dir.glob("*.png"):
        shutil.copy(patch, OUTPUT_DIR / patch.name)