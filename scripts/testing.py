from pathlib import Path

from src.focusstack.pipeline import run

import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Input / output
# ---------------------------------------------------------------------

# determine which root path to use based on existence of local or server path
ROOT_LOCAL = Path(
    "O:/Data-Work/22_Plant_Production-CH/224_Digitalisation"
    "/Jonas_Anderegg_Files/B_Data/04_DL_datasets_updates"
)
ROOT_SERVER = Path(
    "/agroscope/Data-Work-CH/22_Plant_Production-CH/224_Digitalisation"
    "/Jonas_Anderegg_Files/B_Data/04_DL_datasets_updates"
)
if ROOT_LOCAL.exists():
    ROOT = ROOT_LOCAL
elif ROOT_SERVER.exists():
    ROOT = ROOT_SERVER
else:
    raise FileNotFoundError("Could not find root directory.")

base_dir  = Path(ROOT / "focus/focus_stacks")
base_meta_dir = Path(ROOT / "symptoms")

dfs = []
for batch_dir in base_meta_dir.iterdir():
    if batch_dir.is_dir() and batch_dir.name.startswith("batch"):
        path = batch_dir / "img" / "source.txt"

        df_batch = pd.read_csv(path, header = None)
        df_batch["batch_id"] = batch_dir.name
        df_batch["filename"] = df_batch[0].apply(lambda x: Path(x).name)

        dfs.append(df_batch)
df = pd.concat(dfs, ignore_index=True)

# iterate over all image directories
img_dirs = sorted([d for d in base_dir.iterdir() if d.is_dir()])
for img_dir in img_dirs:

    # directories
    stack_dir = img_dir
    out_dir = stack_dir / "out"
    debug_dir = stack_dir / "debug_noalign"
    out_dir.mkdir(parents=True, exist_ok=True)
    debug_dir.mkdir(parents=True, exist_ok=True)

    # find input images
    inputs = sorted(stack_dir.glob("*.JPG"))

    # Run focus stacking
    run(
        inputs=[str(path) for path in inputs],
        output=str(
            out_dir / "stacked_noalign.png"
        ),
        method="perband",
        align=False,
        focus_method="content_aware",
        normalize_exposure=False,
        debug_dir=str(debug_dir),
        verbose=True,
    )

    # Get all JPG images in the directory and sort them
    images = sorted(
        [p for p in img_dir.iterdir() if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg"}]
    )
    img_names = [p.name for p in images]

    # get all focus masks in the directory and sort them
    focus_masks = sorted(
        [p for p in debug_dir.iterdir() if p.is_file() and "_mask_" in p.stem]
    )

    # Find target image position in stack
    filename = img_dir.name + ".JPG"
    try:
        image_idx = img_names.index(filename)
    except ValueError:
        raise FileNotFoundError(
            f"{filename} was not found in {img_dir}"
        )

    # get relevant focus masks
    masks = []
    if image_idx not in (1, 15):
        for i in range(image_idx-1, image_idx + 1 + 1):
            mask = cv2.imread(str(focus_masks[i]), cv2.IMREAD_COLOR)
            mask = cv2.medianBlur(mask, 21)
            masks.append(mask)

    # get image
    img = cv2.imread(images[image_idx], cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # ------------------------------------------------------------
    # OVERLAY
    # ------------------------------------------------------------
    # RGB = pink / magenta
    overlay_colour1 = np.array([255, 0, 0], dtype=np.uint8)
    overlay_colour2 = np.array([255, 0, 255], dtype=np.uint8)
    alpha = 1

    # combined focus masks
    focus1 = masks[1] > 0
    focus2 = (masks[0] > 0) | (masks[2] > 0)

    # change to grid points
    grid_spacing = 20
    focus1_grid = np.zeros_like(focus1, dtype=bool)
    focus1_grid[::grid_spacing, ::grid_spacing] = (
        focus1[::grid_spacing, ::grid_spacing]
    )
    kernel1 = np.ones((5, 5), np.uint8)
    focus1_points = cv2.dilate(
        focus1_grid.astype(np.uint8),
        kernel1
    ) > 0

    focus2_grid = np.zeros_like(focus2, dtype=bool)
    focus2_grid[::grid_spacing, ::grid_spacing] = (
        focus2[::grid_spacing, ::grid_spacing]
    )
    kernel2 = np.ones((3, 3), np.uint8)
    focus2_points = cv2.dilate(
        focus2_grid.astype(np.uint8),
        kernel2
    ) > 0

    # overlay grid
    result = img.copy()
    focus1_mask = focus1_points.any(axis=2)
    focus2_mask = focus2_points.any(axis=2)
    result[focus1_mask] = (
        img[focus1_mask] * (1 - alpha)
        + overlay_colour1 * alpha
    ).astype(np.uint8)
    result[focus2_mask] = (
        result[focus2_mask] * (1 - alpha)
        + overlay_colour2 * alpha
    ).astype(np.uint8)

    # plt.figure(figsize=(16, 10))
    # plt.imshow(result)
    # plt.axis("off")
    # plt.show()

    # crop to the annotation patch
    batch_id = df.loc[df["filename"] == filename, "batch_id"].iloc[0]
    patch_coords = pd.read_csv(base_meta_dir / batch_id / "control" / (img_dir.name + "_coords.csv"), index_col=0).loc[str(img_dir.name) + ".png"]
    out = result[patch_coords["y1"]:patch_coords["y2"], patch_coords["x1"]:patch_coords["x2"], :]

    # write out
    cv2.imwrite(out_dir / (img_dir.name + ".png"), cv2.cvtColor(out, cv2.COLOR_RGB2BGR))
