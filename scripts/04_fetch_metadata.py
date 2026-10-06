
import pandas as pd
from collections import Counter

# meta data for all annotated patches
all_meta = pd.read_csv(r"O:/Data-Work/22_Plant_Production-CH/224_Digitalisation/Jonas_Anderegg_Files/B_Data/04_DL_datasets_updates/symptoms/meta/merged_metadata.csv")

# subset: only meta data for the patches with focus annotations
used_samples = pd.read_csv(r"O:/Data-Work/22_Plant_Production-CH/224_Digitalisation/Jonas_Anderegg_Files/B_Data/04_DL_datasets_updates/focus/batch1/src.txt", header=None)[0].tolist()
sub_meta = all_meta[all_meta['full_path'].isin(used_samples)]
sub_meta = sub_meta.drop_duplicates(subset="full_path")  # three duplicate samples!? :/

# save meta data 
sub_meta.to_csv(r"O:/Data-Work/22_Plant_Production-CH/224_Digitalisation/Jonas_Anderegg_Files/B_Data/04_DL_datasets_updates/focus/meta/merged_metadata.csv", index=False)