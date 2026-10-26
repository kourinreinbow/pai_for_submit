from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
import numpy as np
import copy
import sys

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

robot.bus.write("Goal_Velocity", "shoulder_pan", 100)
robot.bus.write("Goal_Velocity", "shoulder_lift", 100)
robot.bus.write("Goal_Velocity", "elbow_flex", 100)
robot.bus.write("Goal_Velocity", "wrist_flex", 100)
robot.bus.write("Goal_Velocity", "wrist_roll", 100)
robot.bus.write("Goal_Velocity", "gripper", 100)

try:
    while True:
        try:
            obs = robot.get_observation()
        
            for ob_key in obs.keys():
                print(f"'{ob_key}' : {obs[ob_key]:.2f}", end=" , ")
            
            # print(", values :", obs.values())
            print("")

            send_obs = copy.deepcopy(obs)
            
            send_obs['shoulder_pan.pos'] = 0
            send_obs['shoulder_lift.pos'] = 0
            send_obs['elbow_flex.pos'] = 0
            send_obs["wrist_flex.pos"] = 0
            send_obs["wrist_roll.pos"] = 0
            send_obs["gripper.pos"] = 0

            # robot.send_action(send_obs) # ロボットアームに制御情報を送る

        except KeyboardInterrupt:
            robot.send_action(obs)
            break
finally:
    robot.disconnect()
    # print(obs)
    print("disconnected")