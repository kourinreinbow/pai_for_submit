import pandas as pd
from pathlib import Path
import glob
import cv2
import random

datasetPath = Path("C:/Users/kouma/.cache/huggingface/lerobot/kourindayo/record-si_ball")
# saveDatasetPath = Path("C:/Users/kouma/.cache/huggingface/lerobot/kourindayo/record-si_ball_forcus")

videosPath = datasetPath / Path("./videos/*/*/*.mp4") # observation.images.front
videosPath = glob.glob(str(videosPath))
videosPath = [path for path in videosPath if "_gen" not in path ]

CLIP_RATE = 0.9 # 切り取り後のフレームのshape （切り取り前のフレームに対する割合）
SHIFT_MIN_TIME = 10 # シフトする最短時間
SHIFT_RATE = 0.5 # シフトする最短時間を超過後、シフトする確率
ARM_HEAD_NAME = "side"
MOVE_TIME = 10 # フレームを徐々に動かす時間

finishFlag = False
skipRate = 10 # 早送り用

# todo: configから、動画内のエピソードを抽出し、各エピソードごとにシフトの初期化を行う。めんどくさいからランダムなタイミングで位置を変えるようにしようか…
for videoPath in videosPath:
    cap = cv2.VideoCapture(videoPath)
    FPS = cap.get(cv2.CAP_PROP_FPS)

    # 動画保存用
    # saveMoviePath = videoPath.replace(".mp4", "_gen.mp4")
    saveMoviePath = videoPath.replace("record-si_ball", "record-si_ball_forcus")
    saveWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    saveHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    forcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(saveMoviePath, forcc, FPS, (saveWidth, saveHeight), True)
    print(f"save to {saveMoviePath}")

    i = 0
    frameCount = 0
    waitFrame = 0
    moveBeginFrameCount = 0 # 徐々にフレームを動かす動作を始めたフレームカウント
    moveBeginX, moveBeginY = 0, 0
    dx, dy = 0, 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break
        
        # ループ開始時のみ決定する
        if i == 0:
            clippedShape = int(frame.shape[0] * CLIP_RATE), int(frame.shape[1] * CLIP_RATE)
            shiftMax = (frame.shape[0] - clippedShape[0], frame.shape[1] - clippedShape[1])
            tarY = random.randint(0, shiftMax[0])
            tarX = random.randint(0, shiftMax[1])
            waitFrame = FPS * (SHIFT_MIN_TIME + random.random()*5)
            # print(waitFrame, waitFrame / FPS)
            moveBeginFrameCount = frameCount
            dx, dy = 0, 0

        # アームのカメラについては、シフトは行わない。(名前はindexによって変わるので、それを考慮する)
        if ARM_HEAD_NAME in videoPath:
            tarX, tarY = 0, 0

        dx += (tarX - moveBeginX) / (MOVE_TIME*FPS)
        dy += (tarY - moveBeginY) / (MOVE_TIME*FPS)

        if (dx < 0 and dx+moveBeginX > tarX) or (dx > 0 and dx+moveBeginX < tarX):
            clipped = frame[int(moveBeginY+dy):int(moveBeginY+dy+clippedShape[0]), int(moveBeginX+dx):int(moveBeginX+dx+clippedShape[1])]
        else:
            clipped = frame[int(tarY):int(tarY+clippedShape[0]), int(tarX):int(tarX+clippedShape[1])]
            moveBeginX = tarX
            moveBeginY = tarY

        # 表示だけ早送りする
        # if i == 0 or i == 1:        
        #     cv2.imshow("frame", frame)
        #     cv2.imshow("clipped", clipped)
        #     if cv2.waitKey(int(1000/FPS)) & 0xFF == ord('q'):
        #         # finishFlag = True
        #         break
        # cv2.imshow("clipped", clipped)
        # cv2.imshow("frame", frame)
        # if cv2.waitKey(int(1000/FPS)) & 0xFF == ord('q'):
        #     break
        
        if frameCount >= waitFrame:
            i = 0
            frameCount = 0
        else:
            i = i % skipRate + 1 # 1 ～ skipRate （i % skipRateだと、0～skipRate-1）
            frameCount += 1

        # アームヘッドのカメラ → 別視点のカメラ となった場合に、初期化させるために0に戻す。
        if ARM_HEAD_NAME in videoPath:
            i = i % skipRate

        clipped = cv2.resize(clipped, dsize=(saveWidth, saveHeight))
        out.write(clipped)
        
        
    cv2.destroyAllWindows()
    cap.release()

    if finishFlag:
        break

# print(videosPath)