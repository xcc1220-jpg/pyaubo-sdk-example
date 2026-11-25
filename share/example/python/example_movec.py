#! /usr/bin/env python
# coding=utf-8

"""
机械臂圆弧运动

步骤:
第一步: 连接到 RPC 服务
第二步: 机械臂登录
第三步: 圆弧运动
"""

import time
import math
import pyaubo_sdk

def waitArrival(impl):
    cnt = 0
    while impl.getMotionControl().getExecId() == -1:
        cnt += 1
        if cnt > 5:
            print("Motion fail!")
            return -1
        time.sleep(0.05)
        print("getExecId: ", impl.getMotionControl().getExecId())
    id = impl.getMotionControl().getExecId()
    while True:
        id1 = impl.getMotionControl().getExecId()
        if id != id1:
            break
        time.sleep(0.05)
robot_ip = "192.168.117.128"  # 服务器 IP 地址
robot_port = 30004  # 端口号
M_PI = 3.14159265358979323846
robot_rpc_client = pyaubo_sdk.RpcClient()

waypoint1 = []  # 圆弧轨迹的起始路点（位姿）
waypoint2 = []  # 圆弧轨迹的中间路点（位姿）
waypoint3 = []  # 圆弧轨迹的终止路点（位姿）

# 获取圆弧轨迹的路点
# 依据 (x-0.12294)^2 + (y-0.54855)^2 + (z-0.26319)^2 = 0.2^2 来计算
def get_circle_waypoint():
    global waypoint1
    global waypoint2
    global waypoint3

    # 球心坐标
    center_x = 0.12294
    center_y = 0.54855
    center_z = 0.26319
    radius = 0.2
    
    # 计算第一个点
    z1 = 0.26319
    y1 = 0.7
    # 计算x坐标，确保结果非负
    temp_value = pow(radius, 2) - pow(y1 - center_y, 2) - pow(z1 - center_z, 2)
    if temp_value < 0:
        temp_value = 0
    x1 = center_x + math.sqrt(temp_value)
    waypoint1 = [x1, y1, z1, 3.14, 0.00, 3.14]

    # 计算第二个点
    z2 = 0.26319
    y2 = 0.55
    temp_value = pow(radius, 2) - pow(y2 - center_y, 2) - pow(z2 - center_z, 2)
    if temp_value < 0:
        temp_value = 0
    x2 = center_x + math.sqrt(temp_value)
    waypoint2 = [x2, y2, z2, 3.14, 0.00, 3.14]

    # 计算第三个点
    z3 = 0.26319
    y3 = 0.35
    temp_value = pow(radius, 2) - pow(y3 - center_y, 2) - pow(z3 - center_z, 2)
    if temp_value < 0:
        temp_value = 0
    x3 = center_x + math.sqrt(temp_value)
    waypoint3 = [x3, y3, z3, 3.14, 0.00, 3.14]

# 圆弧运动
def example_movec(robot_name):
    get_circle_waypoint()
    robot_rpc_client.getRobotInterface(robot_name).getMotionControl()\
        .moveJoint([0,0,0,0,0,0], 180 * (M_PI / 180), 180 * (M_PI / 180), 0, 0)  # 接口调用: 关节运动
    res = robot_rpc_client.getRobotInterface(robot_name).getRobotAlgorithm().inverseKinematics([0,0,0,0,0,0], waypoint1)
    print("逆解函数返回值:", res[1])
    print("逆解得到的关节角:", res[0])
    robot_rpc_client.getRobotInterface(robot_name).getMotionControl()\
        .moveJoint(res[0], 180 * (M_PI / 180), 180 * (M_PI / 180), 0, 0)  # 接口调用: 关节运动
    waitArrival(robot_rpc_client.getRobotInterface(robot_name))

    ret = robot_rpc_client.getRobotInterface(robot_name).getMotionControl()\
        .moveCircle(waypoint2, waypoint3, 180 * (M_PI / 180), 180 * (M_PI / 180), 0, 0) # 接口调用: 圆弧运动

    if ret == 0:
        print("圆弧运动成功!")
    else:
        print("圆弧运动失败！错误码:%d", ret)


if __name__ == '__main__':
    robot_rpc_client.connect(robot_ip, robot_port)  # 接口调用: 连接 RPC 服务
    if robot_rpc_client.hasConnected():
        print("Robot rcp_client connected successfully!")
        robot_rpc_client.login("aubo", "123456")  # 接口调用: 机械臂登录
        if robot_rpc_client.hasLogined():
            print("Robot rcp_client logined successfully!")
            robot_name = robot_rpc_client.getRobotNames()[0]  # 接口调用: 获取机器人的名字
            example_movec(robot_name)  # 圆弧运动
