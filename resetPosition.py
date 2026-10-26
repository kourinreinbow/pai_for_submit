from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
import numpy as np
import copy
import sys

defaultAngles = {
    'shoulder_pan.pos' : -1.19 ,
    'shoulder_lift.pos' : -90.33 ,
    'elbow_flex.pos' : 88.92 ,
    'wrist_flex.pos' : 66.81 ,
    'wrist_roll.pos' : -0.22 ,
    'gripper.pos' : 1.25
}



config = SO101FollowerConfig(
    port="COM7",
    use_degrees=True
)

robot = SO101Follower(config)

robot.connect()
print("connected")

robot.bus.write("Goal_Velocity", "shoulder_pan", 300)
robot.bus.write("Goal_Velocity", "shoulder_lift", 300)
robot.bus.write("Goal_Velocity", "elbow_flex", 300)
robot.bus.write("Goal_Velocity", "wrist_flex", 300)
robot.bus.write("Goal_Velocity", "wrist_roll", 300)
robot.bus.write("Goal_Velocity", "gripper", 300)

try:
    while True:
        try:
            obs = robot.get_observation()
        
            for ob_key in obs.keys():
                print(f"'{ob_key}' : {obs[ob_key]:.2f}", end=" , ")
            
            # print(", values :", obs.values())
            print("")

            send_obs = copy.deepcopy(obs)
            
            send_obs['shoulder_pan.pos'] = defaultAngles['shoulder_pan.pos']
            send_obs['shoulder_lift.pos'] = defaultAngles['shoulder_lift.pos']
            send_obs['elbow_flex.pos'] = defaultAngles['elbow_flex.pos']
            send_obs["wrist_flex.pos"] = defaultAngles["wrist_flex.pos"]
            send_obs["wrist_roll.pos"] = defaultAngles["wrist_roll.pos"]
            send_obs["gripper.pos"] = defaultAngles["gripper.pos"]

            robot.send_action(send_obs) # ロボットアームに制御情報を送る

        except KeyboardInterrupt:
            robot.send_action(obs)
            break
finally:
    robot.disconnect()
    # print(obs)
    print("disconnected")