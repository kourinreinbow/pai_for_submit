import pandas as pd
from pathlib import Path

datasetPath = Path("C:/Users/kouma/.cache/huggingface/lerobot/kourindayo/record-si_ball_forcus")

parquetPath = datasetPath / Path("./data/chunk-000/file-000.parquet")
# parquetPath = datasetPath / Path("./meta/episodes/chunk-000/file-000.parquet")

df = pd.read_parquet(str(parquetPath))
print(df[['timestamp', 'frame_index', 'episode_index', 'index', 'task_index']].iloc[30000])
# print(df.head())
print(df.columns.to_list())