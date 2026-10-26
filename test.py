import subprocess
import pyautogui
import time
import shutil
import os
import sys

# cmd = 'lerobot-record --robot.type=so101_follower --robot.port=COM7 --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}, head: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}, side: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}}" --display_data=false --dataset.repo_id=kourindayo/eval_si_ball3 --dataset.single_task="Grap the si_ball" --dataset.push_to_hub=false --dataset.num_episodes=1 --dataset.episode_time_s=30 --dataset.reset_time_s=0 --policy.path=kourindayo/policy-si_ball3'
args = [
    "lerobot-record",
    "--config", "testconfig.yaml",
    "--policy.path=kourindayo/policy-si_ball3"
    ]

saveFolderPath = "C:/Users/kouma/.cache/huggingface/lerobot/kourindayo/eval_temp"

if os.path.exists(saveFolderPath):
    shutil.rmtree(saveFolderPath)

# subprocess.run(cmd, shell=True)

print("start")
# subprocess.run(args)
proc = subprocess.Popen(args)

try:
    while True:
        t = input(">>")
        if t == "s":
            # pyautogui.press('esc')
            pyautogui.hotkey('ctrl', 'c')
            break

    # proc.terminate()
except KeyboardInterrupt:
    pass

proc.wait()
print("stop")