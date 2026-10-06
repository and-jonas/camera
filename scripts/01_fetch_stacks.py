from pathlib import Path
import pandas as pd
import shutil


def copy_image_block(image_path, block_size=15):
    image_path = Path(image_path)

    # Directory containing the target image
    image_dir = image_path.parent

    # Get all JPG images in the directory and sort them
    images = sorted(
        [
            p for p in image_dir.iterdir()
            if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg"}
        ]
    )

    # Find target image position (0-based)
    try:
        image_idx = images.index(image_path)
    except ValueError:
        raise FileNotFoundError(
            f"{image_path.name} was not found in {image_dir}"
        )

    # Determine the 15-image block
    block_start = (image_idx // block_size) * block_size
    block_end = min(block_start + block_size, len(images))

    block_paths = images[block_start:block_end]

    # Create folder named after the target image, without extension
    output_dir = OUTPUT_ROOT / image_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    # Copy images
    for source_path in block_paths:
        destination_path = output_dir / source_path.name
        shutil.copy2(source_path, destination_path)

    print(
        f"{image_path.name}: "
        f"image {image_idx + 1} → "
        f"copied images {block_start + 1}-{block_end} "
        f"to {output_dir}"
    )


# # fetch stacks batch1
# OUTPUT_ROOT = Path(
#     r"O:/Data-Work/22_Plant_Production-CH/224_Digitalisation"
#     r"/Jonas_Anderegg_Files/B_Data/04_DL_datasets_updates/focus/batch1/focus_stacks"
# )
# img_paths = pd.read_csv(r"O:/Data-Work/22_Plant_Production-CH/224_Digitalisation/Jonas_Anderegg_Files/B_Data/04_DL_datasets_updates/focus/batch1/src.txt", header=None)[0].tolist()
# for image_path in img_paths:
#     copy_image_block(image_path)

# fetch stacks batch2
OUTPUT_ROOT = Path(
    r"O:/Data-Work/22_Plant_Production-CH/224_Digitalisation"
    r"/Jonas_Anderegg_Files/B_Data/04_DL_datasets_updates/focus/batch2/focus_stacks"
)

img_paths = pd.read_csv(r"O:/Data-Work/22_Plant_Production-CH/224_Digitalisation/Jonas_Anderegg_Files/B_Data/04_DL_datasets_updates/focus/batch2/src.txt", header=None)[0].tolist()
for image_path in img_paths:
    copy_image_block(image_path)
