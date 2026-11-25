# pyaubo_sdk 文档

## 1. 项目概述

pyaubo_sdk 是一个用于控制和管理 Aubo 机器人的 Python 软件开发工具包。它提供了丰富的 API，允许开发者通过 Python 语言与 Aubo 机器人进行交互，实现各种功能，如运动控制、力控制、IO 控制等。

## 2. 核心类和接口

### 2.1 基础类

#### AuboApi

AuboApi 是 pyaubo_sdk 的核心基类，提供了访问机器人各种功能模块的接口。

```python
class AuboApi(pybind11_builtins.pybind11_object):
    def getAxisInterface(self, arg0: str) -> arcs::common_interface::AxisInterface: ...
    def getAxisNames(self) -> List[str]: ...
    def getMath(self) -> pyaubo_sdk.Math: ...
    def getRegisterControl(self) -> pyaubo_sdk.RegisterControl: ...
    def getRobotInterface(self, arg0: str) -> pyaubo_sdk.RobotInterface: ...
    def getRobotNames(self) -> List[str]: ...
    def getRuntimeMachine(self) -> pyaubo_sdk.RuntimeMachine: ...
    def getSerial(self) -> pyaubo_sdk.Serial: ...
    def getSocket(self) -> pyaubo_sdk.Socket: ...
    def getSyncMove(self, arg0: str) -> pyaubo_sdk.SyncMove: ...
    def getSystemInfo(self) -> pyaubo_sdk.SystemInfo: ...
    def getTrace(self, arg0: str) -> pyaubo_sdk.Trace: ...
```

#### RpcClient

RpcClient 是 AuboApi 的子类，提供了通过 RPC 协议与机器人通信的功能。

```python
class RpcClient(AuboApi):
    def __init__(self) -> None: ...
    def connect(self, arg0: str, arg1: int) -> int: ...
    def disconnect(self) -> int: ...
    def hasConnected(self) -> bool: ...
    def hasLogined(self) -> bool: ...
    def login(self, arg0: str, arg1: str) -> int: ...
    def logout(self) -> int: ...
    def setLogHandler(self, arg0: Callable[[int, str, int, str], None]) -> None: ...
    def setRequestTimeout(self, arg0: int) -> int: ...
```

#### RtdeClient

RtdeClient 提供了通过 RTDE 协议与机器人通信的功能，适用于实时数据交换。

```python
class RtdeClient(pybind11_builtins.pybind11_object):
    def __init__(self) -> None: ...
    def connect(self, arg0: str, arg1: int) -> int: ...
    def disconnect(self) -> int: ...
    def getInputMaps(self) -> Dict[str, int]: ...
    def getOutputMaps(self) -> Dict[str, int]: ...
    def getProtocolVersion(self) -> int: ...
    def hasConnected(self) -> bool: ...
    def login(self, arg0: str, arg1: str) -> int: ...
    def logout(self) -> int: ...
    def publish(self, arg0: int, arg1: Callable[[arcs::aubo_sdk::OutputBuilder], None]) -> int: ...
    def subscribe(self, arg0: int, arg1: Callable[[arcs::aubo_sdk::InputParser], None]) -> int: ...
```

### 2.2 错误码

AuboErrorCodes 定义了 SDK 中使用的各种错误码。

```python
class AuboErrorCodes(pybind11_builtins.pybind11_object):
    AUBO_OK = 0
    AUBO_BAD_STATE = 1
    AUBO_QUEUE_FULL = 2
    AUBO_BUSY = 3
    AUBO_TIMEOUT = 4
    AUBO_INVL_ARGUMENT = 5
    AUBO_NOT_IMPLETEMENT = 6
    AUBO_NO_ACCESS = 7
    AUBO_CONN_REFUSED = 8
    AUBO_CONN_RESET = 9
    AUBO_INPROGRESS = 10
    # 更多错误码...
```

## 3. 运动控制

### 3.1 MotionControl

MotionControl 类提供了机器人运动控制的各种功能。

```python
class MotionControl(pybind11_builtins.pybind11_object):
    def __init__(self) -> None: ...
    def moveJoint(self, arg0: List[float], arg1: float, arg2: float, arg3: float, arg4: float) -> int: ...
    def moveLine(self, arg0: List[float], arg1: float, arg2: float, arg3: float, arg4: float) -> int: ...
    def moveCircle(self, arg0: List[float], arg1: List[float], arg2: float, arg3: float, arg4: float, arg5: float) -> int: ...
    def servoJoint(self, arg0: List[float], arg1: float, arg2: float, arg3: float, arg4: float, arg5: float) -> int: ...
    def servoCartesian(self, arg0: List[float], arg1: float, arg2: float, arg3: float, arg4: float, arg5: float) -> int: ...
    def stopJoint(self, arg0: float) -> int: ...
    def stopLine(self, arg0: float, arg1: float) -> int: ...
    # 更多方法...
```

### 3.2 运动控制示例

```python
from pyaubo_sdk import RpcClient, MotionControl

# 创建 RPC 客户端并连接
client = RpcClient()
client.connect("192.168.1.100", 8899)
client.login("username", "password")

# 获取机器人接口和运动控制
robot_interface = client.getRobotInterface("robot0")
motion_control = robot_interface.getMotionControl()

# 关节运动示例
joint_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 六个关节角度
motion_control.moveJoint(joint_positions, 0.5, 0.5, 0.5, 0.5)

# 直线运动示例
target_pose = [0.5, 0.0, 0.5, 0.0, 3.14, 0.0]  # x, y, z, rx, ry, rz
motion_control.moveLine(target_pose, 0.2, 0.2, 0.2, 0.2)

# 断开连接
client.logout()
client.disconnect()
```

## 4. 力控制

### 4.1 ForceControl

ForceControl 类提供了机器人力控制的各种功能。

```python
class ForceControl(pybind11_builtins.pybind11_object):
    def __init__(self) -> None: ...
    def fcEnable(self) -> int: ...
    def fcDisable(self) -> int: ...
    def setTargetForce(self, arg0: List[float], arg1: List[bool], arg2: List[float], arg3: List[float], arg4: arcs::common_interface::TaskFrameType) -> int: ...
    def setDamping(self, arg0: List[float], arg1: float) -> int: ...
    def setSupvForce(self, arg0: List[float], arg1: List[float]) -> int: ...
    def isFcEnabled(self) -> bool: ...
    # 更多方法...
```

### 4.2 力控制示例

```python
from pyaubo_sdk import RpcClient

# 创建 RPC 客户端并连接
client = RpcClient()
client.connect("192.168.1.100", 8899)
client.login("username", "password")

# 获取机器人接口和力控制
robot_interface = client.getRobotInterface("robot0")
force_control = robot_interface.getForceControl()

# 启用力控制
force_control.fcEnable()

# 设置目标力
# 力分量：[fx, fy, fz, tx, ty, tz]
target_force = [0.0, 0.0, 5.0, 0.0, 0.0, 0.0]  # 沿 z 轴施加 5N 的力
# 各轴使能：[fx_en, fy_en, fz_en, tx_en, ty_en, tz_en]
enable_axes = [False, False, True, False, False, False]
# 比例增益
kp = [100.0, 100.0, 100.0, 10.0, 10.0, 10.0]
# 积分增益
ki = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

force_control.setTargetForce(target_force, enable_axes, kp, ki, TaskFrameType.Tool)

# 断开连接
client.logout()
client.disconnect()
```

## 5. IO 控制

### 5.1 IoControl

IoControl 类提供了机器人 IO 控制的各种功能。

```python
class IoControl(pybind11_builtins.pybind11_object):
    def __init__(self) -> None: ...
    def getStandardDigitalInput(self, arg0: int) -> bool: ...
    def getStandardDigitalOutput(self, arg0: int) -> bool: ...
    def setStandardDigitalOutput(self, arg0: int, arg1: bool) -> int: ...
    def setStandardDigitalOutputPulse(self, arg0: int, arg1: bool, arg2: float) -> int: ...
    def getStandardAnalogInput(self, arg0: int) -> float: ...
    def setStandardAnalogOutput(self, arg0: int, arg1: float) -> int: ...
    # 更多方法...
```

### 5.2 IO 控制示例

```python
from pyaubo_sdk import RpcClient

# 创建 RPC 客户端并连接
client = RpcClient()
client.connect("192.168.1.100", 8899)
client.login("username", "password")

# 获取机器人接口和 IO 控制
robot_interface = client.getRobotInterface("robot0")
io_control = robot_interface.getIoControl()

# 设置数字输出
io_control.setStandardDigitalOutput(0, True)  # 设置第 0 个数字输出为高电平

# 设置数字输出脉冲
io_control.setStandardDigitalOutputPulse(1, True, 0.5)  # 第 1 个数字输出输出 0.5 秒的高电平脉冲

# 获取数字输入状态
input_state = io_control.getStandardDigitalInput(0)
print(f"Digital Input 0 state: {input_state}")

# 获取模拟输入值
analog_value = io_control.getStandardAnalogInput(0)
print(f"Analog Input 0 value: {analog_value}")

# 设置模拟输出
io_control.setStandardAnalogOutput(0, 5.0)  # 设置第 0 个模拟输出为 5.0V

# 断开连接
client.logout()
client.disconnect()
```

## 6. 机器人状态

### 6.1 RobotState

RobotState 类提供了获取机器人状态信息的各种方法。

```python
class RobotState(pybind11_builtins.pybind11_object):
    def __init__(self) -> None: ...
    def getJointPositions(self) -> List[float]: ...
    def getJointSpeeds(self) -> List[float]: ...
    def getJointState(self) -> List[arcs::common_interface::JointStateType]: ...
    def getTcpPose(self) -> List[float]: ...
    def getTcpSpeed(self) -> List[float]: ...
    def getRobotModeType(self) -> arcs::common_interface::RobotModeType: ...
    def getSafetyModeType(self) -> arcs::common_interface::SafetyModeType: ...
    def isPowerOn(self) -> bool: ...
    def isSteady(self) -> bool: ...
    def isCollisionOccurred(self) -> bool: ...
    # 更多方法...
```

### 6.2 获取机器人状态示例

```python
from pyaubo_sdk import RpcClient

# 创建 RPC 客户端并连接
client = RpcClient()
client.connect("192.168.1.100", 8899)
client.login("username", "password")

# 获取机器人接口和状态
robot_interface = client.getRobotInterface("robot0")
robot_state = robot_interface.getRobotState()

# 获取关节位置
joint_positions = robot_state.getJointPositions()
print(f"Joint positions: {joint_positions}")

# 获取 TCP 位姿
tcp_pose = robot_state.getTcpPose()
print(f"TCP pose: {tcp_pose}")

# 获取机器人模式
robot_mode = robot_state.getRobotModeType()
print(f"Robot mode: {robot_mode}")

# 检查机器人是否稳定
is_steady = robot_state.isSteady()
print(f"Is robot steady: {is_steady}")

# 检查是否发生碰撞
is_collision = robot_state.isCollisionOccurred()
print(f"Collision occurred: {is_collision}")

# 断开连接
client.logout()
client.disconnect()
```

## 7. 机器人管理

### 7.1 RobotManage

RobotManage 类提供了机器人管理的各种功能，如电源控制、模式切换等。

```python
class RobotManage(pybind11_builtins.pybind11_object):
    def __init__(self) -> None: ...
    def poweron(self) -> int: ...
    def poweroff(self) -> int: ...
    def freedrive(self, arg0: bool) -> int: ...
    def getOperationalMode(self) -> arcs::common_interface::OperationalModeType: ...
    def setOperationalMode(self, arg0: arcs::common_interface::OperationalModeType) -> int: ...
    def isSimulationEnabled(self) -> bool: ...
    def setSim(self, arg0: bool) -> int: ...
    # 更多方法...
```

### 7.2 机器人管理示例

```python
from pyaubo_sdk import RpcClient, OperationalModeType

# 创建 RPC 客户端并连接
client = RpcClient()
client.connect("192.168.1.100", 8899)
client.login("username", "password")

# 获取机器人接口和管理
robot_interface = client.getRobotInterface("robot0")
robot_manage = robot_interface.getRobotManage()

# 机器人上电
robot_manage.poweron()

# 设置为自动模式
robot_manage.setOperationalMode(OperationalModeType.Automatic)

# 进入自由驱动模式
robot_manage.freedrive(True)

# 退出自由驱动模式
robot_manage.freedrive(False)

# 机器人下电
robot_manage.poweroff()

# 断开连接
client.logout()
client.disconnect()
```

## 8. 机器人配置

### 8.1 RobotConfig

RobotConfig 类提供了机器人配置的各种功能。

```python
class RobotConfig(pybind11_builtins.pybind11_object):
    def __init__(self) -> None: ...
    def getRobotType(self) -> str: ...
    def getDof(self) -> int: ...
    def getHomePosition(self) -> List[float]: ...
    def setHomePosition(self, arg0: List[float]) -> int: ...
    def getPayload(self) -> Tuple[float, List[float], List[float], List[float]]: ...
    def setPayload(self, arg0: float, arg1: List[float], arg2: List[float], arg3: List[float]) -> int: ...
    def getTcpOffset(self) -> List[float]: ...
    def setTcpOffset(self, arg0: List[float]) -> int: ...
    # 更多方法...
```

### 8.2 机器人配置示例

```python
from pyaubo_sdk import RpcClient

# 创建 RPC 客户端并连接
client = RpcClient()
client.connect("192.168.1.100", 8899)
client.login("username", "password")

# 获取机器人接口和配置
robot_interface = client.getRobotInterface("robot0")
robot_config = robot_interface.getRobotConfig()

# 获取机器人类型
robot_type = robot_config.getRobotType()
print(f"Robot type: {robot_type}")

# 获取自由度
robot_dof = robot_config.getDof()
print(f"Robot DOF: {robot_dof}")

# 获取 TCP 偏移
tcp_offset = robot_config.getTcpOffset()
print(f"TCP offset: {tcp_offset}")

# 设置 TCP 偏移
new_tcp_offset = [0.0, 0.0, 0.1, 0.0, 0.0, 0.0]  # 工具长度增加 10cm
robot_config.setTcpOffset(new_tcp_offset)

# 获取负载参数
payload, cog, inertia, friction = robot_config.getPayload()
print(f"Payload: {payload} kg")
print(f"Center of gravity: {cog}")

# 设置负载参数
new_payload = 1.0  # 1kg
new_cog = [0.0, 0.0, 0.1]  # 重心在工具末端 10cm 处
new_inertia = [0.01, 0.01, 0.01, 0.0, 0.0, 0.0]  # 惯性矩阵
new_friction = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 摩擦力
robot_config.setPayload(new_payload, new_cog, new_inertia, new_friction)

# 断开连接
client.logout()
client.disconnect()
```

## 9. 机器人算法

### 9.1 RobotAlgorithm

RobotAlgorithm 类提供了机器人算法相关的功能，如正逆运动学计算、雅克比矩阵计算等。

```python
class RobotAlgorithm(pybind11_builtins.pybind11_object):
    def __init__(self) -> None: ...
    def calcJacobian(self, arg0: List[float], arg1: bool) -> Tuple[List[float], int]: ...
    def forwardKinematics(self, arg0: List[float]) -> Tuple[List[float], int]: ...
    def inverseKinematics(self, arg0: List[float], arg1: List[float]) -> Tuple[List[float], int]: ...
    # 更多方法...
```

### 9.2 机器人算法示例

```python
from pyaubo_sdk import RpcClient

# 创建 RPC 客户端并连接
client = RpcClient()
client.connect("192.168.1.100", 8899)
client.login("username", "password")

# 获取机器人接口和算法
robot_interface = client.getRobotInterface("robot0")
robot_algorithm = robot_interface.getRobotAlgorithm()

# 正向运动学计算
joint_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 关节位置
tcp_pose, error_code = robot_algorithm.forwardKinematics(joint_positions)
if error_code == 0:
    print(f"Forward kinematics result: {tcp_pose}")
else:
    print(f"Forward kinematics failed with error code: {error_code}")

# 逆向运动学计算
target_pose = [0.5, 0.0, 0.5, 0.0, 3.14, 0.0]  # 目标 TCP 位姿
seed_joint = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 种子关节位置
joint_solution, error_code = robot_algorithm.inverseKinematics(target_pose, seed_joint)
if error_code == 0:
    print(f"Inverse kinematics solution: {joint_solution}")
else:
    print(f"Inverse kinematics failed with error code: {error_code}")

# 计算雅克比矩阵
jacobian, error_code = robot_algorithm.calcJacobian(joint_positions, True)
if error_code == 0:
    print(f"Jacobian matrix: {jacobian}")
else:
    print(f"Jacobian calculation failed with error code: {error_code}")

# 断开连接
client.logout()
client.disconnect()
```

## 10. 数学工具

### 10.1 Math

Math 类提供了各种数学计算工具。

```python
class Math(pybind11_builtins.pybind11_object):
    def __init__(self) -> None: ...
    def poseAdd(self, arg0: List[float], arg1: List[float]) -> List[float]: ...
    def poseSub(self, arg0: List[float], arg1: List[float]) -> List[float]: ...
    def poseTrans(self, arg0: List[float], arg1: List[float]) -> List[float]: ...
    def quaternionToRpy(self, arg0: List[float]) -> List[float]: ...
    def rpyToQuaternion(self, arg0: List[float]) -> List[float]: ...
    def interpolatePose(self, arg0: List[float], arg1: List[float], arg2: float) -> List[float]: ...
    # 更多方法...
```

### 10.2 数学工具示例

```python
from pyaubo_sdk import RpcClient

# 创建 RPC 客户端并连接
client = RpcClient()
client.connect("192.168.1.100", 8899)
client.login("username", "password")

# 获取数学工具
math = client.getMath()

# 姿态插值
start_pose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
end_pose = [1.0, 1.0, 1.0, 0.0, 3.14, 0.0]
interpolated_pose = math.interpolatePose(start_pose, end_pose, 0.5)  # 50% 插值
print(f"Interpolated pose: {interpolated_pose}")

# 四元数转换为欧拉角
quaternion = [0.0, 0.0, 0.0, 1.0]  # 单位四元数
rpy = math.quaternionToRpy(quaternion)
print(f"Quaternion to RPY: {rpy}")

# 欧拉角转换为四元数
rpy = [0.0, 0.0, 3.14]  # 绕 z 轴旋转 180 度
quaternion = math.rpyToQuaternion(rpy)
print(f"RPY to quaternion: {quaternion}")

# 断开连接
client.logout()
client.disconnect()
```

## 11. 常见问题解答

### 11.1 如何连接到机器人？

使用 RpcClient 类的 connect 方法连接到机器人，需要指定机器人的 IP 地址和端口号。

```python
client = RpcClient()
client.connect("192.168.1.100", 8899)
client.login("username", "password")
```

### 11.2 如何处理错误？

SDK 中的方法通常返回错误码，可以通过 AuboErrorCodes 类来解释错误码。

```python
from pyaubo_sdk import AuboErrorCodes

result = motion_control.moveJoint(joint_positions, 0.5, 0.5, 0.5, 0.5)
if result == AuboErrorCodes.AUBO_OK:
    print("Move successful")
elif result == AuboErrorCodes.AUBO_BUSY:
    print("Robot is busy")
elif result == AuboErrorCodes.AUBO_INVL_ARGUMENT:
    print("Invalid argument")
else:
    print(f"Move failed with error code: {result}")
```

### 11.3 如何确保机器人运动完成？

可以使用 RobotState 类的 isSteady 方法检查机器人是否稳定。

```python
while not robot_state.isSteady():
    time.sleep(0.1)
print("Robot motion completed")
```

### 11.4 如何设置机器人的 TCP 偏移？

使用 RobotConfig 类的 setTcpOffset 方法设置 TCP 偏移。

```python
robot_config = robot_interface.getRobotConfig()
new_tcp_offset = [0.0, 0.0, 0.1, 0.0, 0.0, 0.0]  # 工具长度增加 10cm
robot_config.setTcpOffset(new_tcp_offset)
```

### 11.5 如何切换机器人的操作模式？

使用 RobotManage 类的 setOperationalMode 方法切换机器人的操作模式。

```python
from pyaubo_sdk import OperationalModeType

robot_manage = robot_interface.getRobotManage()
# 切换到自动模式
robot_manage.setOperationalMode(OperationalModeType.Automatic)
# 切换到手动模式
robot_manage.setOperationalMode(OperationalModeType.Manual)
```

## 12. 总结

pyaubo_sdk 提供了丰富的 API，允许开发者通过 Python 语言与 Aubo 机器人进行交互，实现各种功能。本文档介绍了 SDK 的核心类和接口，以及如何使用这些接口实现机器人的运动控制、力控制、IO 控制等功能。

通过本文档的学习，开发者应该能够快速上手使用 pyaubo_sdk 开发自己的机器人应用程序。