from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
import numpy as np
import math
import copy
import sys

def EstimateTipPosition(_targetAngles):
    targetRads = list(map(math.radians, _targetAngles))

    # ワールド座標系 → 計算上の座標系 への変換
    q1 = targetRads[0]
    q2 = math.pi/2 - targetRads[1]
    # q2 = -targetRads[1]
    q3 = -targetRads[2]
    q4 = -targetRads[3]
    q5 = targetRads[4] # アームの向き（使わない）

    x0 = R0 * math.cos(q1)
    y0 = R0 * math.sin(q1)
    
    r = L2*math.cos(q2) + L3*math.cos(q2+q3) + L4*math.cos(q2+q3+q4)
    x = r*math.cos(q1) + x0
    y = r*math.sin(q1) + y0
    z = L1 + L2*math.sin(q2) + L3*math.sin(q2+q3) + L4*math.sin(q2+q3+q4)
    
    resVector = np.array([x, z, y], np.float32)

    return resVector

# yawはradian
def calculateKI(_targetPosi, yaw) -> np.ndarray:
    targetPosi = _targetPosi - basePosi;

    # Unity上の座標をtargetPosiとして受け取るため、計算を行う座標系に変換する
    x = targetPosi[0]
    y = targetPosi[2]
    z = targetPosi[1] # 高さ
    yaw = -yaw

    # これ以降は、縦（高さ成分）はz

    q1 = math.atan2(y, x)

    r = math.sqrt(math.pow(x,2) + math.pow(y,2)) - R0

    x -= R0 * math.cos(q1)
    y -= R0 * math.sin(q1)
    z -= L1

    r = r - L4 * math.cos(yaw)
    z = z - L4 * math.sin(yaw)

    # 基準点と目標座標との距離
    d = math.sqrt(math.pow(r, 2) + math.pow(z, 2))
    q3 = - math.acos((math.pow(d,2) - math.pow(L2,2) - math.pow(L3,2)) / (2*L2*L3))

    # Debug.Log((math.Pow(d,2) - math.Pow(L2,2) - math.Pow(L3,2)) / (2*L2*L3))
    theta = math.atan2(z, r)

    q2 = theta + math.acos((math.pow(d,2) + math.pow(L2,2) - math.pow(L3,2)) / (2*d*L2))

    q4 = yaw - q2 - q3

    q2 = math.pi/2 - q2 # q2' → q2 への変換（q2がtargetRad）
    q3 = -q3
    q4 = -q4
    # q2 = - q2
    pred_q1 = math.degrees(q1)
    pred_q2 = math.degrees(q2)
    pred_q3 = math.degrees(q3)
    pred_q4 = math.degrees(q4)
    
    # Debug.Log("q1 : " + pred_q1 + ", q2 : " + pred_q2 + ", q3 : " + pred_q3 + ", q4 : " + pred_q4)

    # yaw = q2 + q3 + q4 の条件を満たす必要がある。

    predAngles = np.array([pred_q1, pred_q2, pred_q3, pred_q4, 0, 0], np.float32)
    return predAngles

config = SO101FollowerConfig(
    port="COM7",
    use_degrees=True
)

robot = SO101Follower(config)

robot.connect()
print("connected")

# print(robot.bus.model_ctrl_table["sts3215"].keys()) # sts3215で操作できるパラメータを取得
# robot.disconnect()

# robot.bus.disable_torque() # サーボの値を取得するため、サーボにトルクを与えない

robot.bus.write("Goal_Velocity", "shoulder_pan", 300)
robot.bus.write("Goal_Velocity", "shoulder_lift", 300)
robot.bus.write("Goal_Velocity", "elbow_flex", 300)
robot.bus.write("Goal_Velocity", "wrist_flex", 300)
robot.bus.write("Goal_Velocity", "wrist_roll", 300)
robot.bus.write("Goal_Velocity", "gripper", 300)

# ==== パラメータ ====
# アームの長さ(m*/10)
L1 = 0.8
L2 = 1.1885
L3 = 1.35
L4 = 0.6
R0 = 0.25

basePosi = np.array([0.7, 0, 0], np.float32) 
# targetPosi = np.array([2.5 ,2.5 , 0], np.float32)]
targetPosi = np.array([1.0 ,0.8 , -1.8], np.float32)

targetAngleOffsets = np.zeros(6)
tAngle = math.atan2(0.3, 1.15)
# targetAngleOffsets[1] = 90 - math.degrees(tAngle)
# targetAngleOffsets[2] = -(180 - math.degrees(tAngle))
targetAngleOffsets[1] = - math.degrees(tAngle)
targetAngleOffsets[2] = math.degrees(tAngle) - 90
yaw = 90 

try:
    while True:
        try:
            obs = robot.get_observation()
        
            # for ob_key in obs.keys():
            #     print(f"'{ob_key}' : {obs[ob_key]:.2f}", end=" , ")
            
            # print(", values :", obs.values())
            print("")

            send_obs = copy.deepcopy(obs)

            pred_angles = calculateKI(targetPosi, math.radians(yaw))
            send_angles = pred_angles + targetAngleOffsets

            send_obs['shoulder_pan.pos'] = send_angles[0]
            send_obs['shoulder_lift.pos'] = send_angles[1]
            send_obs['elbow_flex.pos'] = send_angles[2]
            send_obs["wrist_flex.pos"] = send_angles[3]
            send_obs["wrist_roll.pos"] = send_angles[4]
            send_obs["gripper.pos"] = send_angles[5]

            for ob_key in send_obs.keys():
                print(f"'{ob_key}' : {send_obs[ob_key]:.2f}", end=" , ")

            robot.send_action(send_obs) # ロボットアームに制御情報を送る

        except KeyboardInterrupt:
            robot.send_action(obs)
            break
finally:
    robot.disconnect()
    # print(obs)
    print("disconnected")