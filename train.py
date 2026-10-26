import torch
from pathlib import Path

from lerobot.datasets.lerobot_dataset import LeRobotDataset

from lerobot.configs.default import DatasetConfig
from lerobot.policies.act.configuration_act import ACTConfig
from lerobot.policies.factory import make_policy

# from lerobot.scripts.train import train
from lerobot.scripts.lerobot_train import train
from lerobot.configs.train import TrainPipelineConfig


# =========================
# 設定
# =========================
DATASET_REPO_ID = "kourindayo/record-si_ball"
OUTPUT_DIR = "./outputs/train/trainByScript1"


# =========================
# dataset
# =========================
dataset = LeRobotDataset(DATASET_REPO_ID)

dataset_config = DatasetConfig(
    repo_id=DATASET_REPO_ID
)
# metadata取得（重要）
metadata = dataset.meta


# =========================
# policy
# =========================
policy_config = ACTConfig(
    # ここは最低限明示する（None回避）
    n_obs_steps=1,
    n_action_steps=1,
    repo_id=DATASET_REPO_ID
)

policy = make_policy(
    cfg=policy_config,
    ds_meta=metadata,
)


# =========================
# train config
# =========================
train_config = TrainPipelineConfig(
    dataset=dataset_config,
    policy=policy_config,

    output_dir=Path(OUTPUT_DIR),

    batch_size=16,
    steps=10000,

    num_workers=8,
    cudnn_deterministic=False,

    log_freq=100,
    save_freq=2000,
)


# =========================
# 学習
# =========================
if __name__ == "__main__":
    train(train_config)