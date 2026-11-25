from pyaubo_sdk import RpcClient, AuboErrorCodes
import time

def connect_to_arcs_simulation(ip="192.168.1.100", port=30004, username="aubo", password="your_password", timeout=5000):
    """
    连接到VMware中运行的arcs仿真环境
    
    参数:
        ip: arcs仿真环境的IP地址
        port: arcs仿真环境的端口号
        username: 登录用户名
        password: 登录密码
        timeout: 连接超时时间（毫秒）
    
    返回:
        client: 已连接的RPC客户端实例，失败返回None
    """
    print(f"\n===== 连接到arcs仿真环境 =====")
    print(f"目标: {ip}:{port}")
    
    # 创建RPC客户端
    client = RpcClient()
    
    # 设置请求超时时间
    client.setRequestTimeout(timeout)
    
    # 连接到仿真环境
    print("正在建立连接...")
    connect_result = client.connect(ip, port)
    if connect_result != AuboErrorCodes.AUBO_OK:
        print(f"❌ 连接失败，错误代码: {connect_result}")
        print("请检查：")
        print("  1. VMware网络配置（推荐使用桥接模式）")
        print("  2. arcs仿真环境是否正在运行")
        print("  3. IP地址和端口是否正确")
        return None
    
    print("✅ 连接成功")
    
    # 添加更安全的登录处理，处理版本兼容性问题
    print(f"正在登录，用户名: {username}")
    try:
        # 尝试登录
        login_result = client.login(username, password)
        
        if login_result != AuboErrorCodes.AUBO_OK:
            print(f"❌ 登录失败，错误代码: {login_result}")
            print("请检查：")
            print("  1. 用户名和密码是否正确")
            print("  2. pyaubo_sdk版本是否与arcs环境兼容")
            print("  3. 尝试使用不同版本的SDK或arcs环境")
            client.disconnect()
            return None
        
        print("✅ 登录成功")
        return client
    except Exception as e:
        print(f"❌ 登录时发生异常: {str(e)}")
        print("可能的原因：")
        print("  1. pyaubo_sdk与arcs环境版本不兼容")
        print("  2. arcs环境可能需要特定版本的SDK")
        print("  3. JSON解析错误通常表示协议不匹配")
        client.disconnect()
        return None

def enable_simulation_mode(robot_interface):
    """
    启用机器人仿真模式
    
    参数:
        robot_interface: 机器人接口实例
    
    返回:
        bool: 启用是否成功
    """
    try:
        # 获取机器人管理接口
        robot_manage = robot_interface.getRobotManage()
        
        # 检查当前是否已启用仿真模式
        if robot_manage.isSimulationEnabled():
            print("✅ 仿真模式已启用")
            return True
        
        # 启用仿真模式
        print("正在启用仿真模式...")
        sim_result = robot_manage.setSim(True)
        if sim_result != AuboErrorCodes.AUBO_OK:
            print(f"❌ 启用仿真模式失败，错误代码: {sim_result}")
            return False
        
        print("✅ 成功启用仿真模式")
        # 等待系统初始化
        time.sleep(2)
        return True
    except Exception as e:
        print(f"❌ 启用仿真模式时发生错误: {str(e)}")
        return False

def basic_motion_example(robot_interface):
    """
    基础运动控制示例
    
    参数:
        robot_interface: 机器人接口实例
    
    返回:
        bool: 运动是否成功
    """
    try:
        # 获取运动控制接口
        motion_control = robot_interface.getMotionControl()
        robot_state = robot_interface.getRobotState()
        
        print("\n===== 基础运动示例 =====")
        
        # 简单关节运动示例
        target_joints = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        print(f"移动到目标关节位置: {target_joints}")
        print("参数: 速度=0.5, 加速度=0.5, 减速度=0.5, 平滑度=0.5")
        
        result = motion_control.moveJoint(target_joints, 0.5, 0.5, 0.5, 0.5)
        if result != AuboErrorCodes.AUBO_OK:
            print(f"❌ 运动命令失败，错误代码: {result}")
            return False
        
        print("✅ 运动命令已发送，等待完成...")
        # 等待运动完成
        start_time = time.time()
        timeout = 10.0  # 10秒超时
        
        while not robot_state.isSteady():
            if time.time() - start_time > timeout:
                print("❌ 运动超时")
                return False
            time.sleep(0.1)
        
        print("✅ 运动完成")
        return True
    except Exception as e:
        print(f"❌ 运动控制时发生错误: {str(e)}")
        return False

def main():
    # VMware中arcs仿真环境配置
    simulation_config = {
        "ip": "192.168.117.128",
        "port": 30004,
        "username": "aubo",
        "password": ""
    }
    
    client = None
    
    try:
        # 1. 连接到arcs仿真环境
        client = connect_to_arcs_simulation(**simulation_config)
        if not client:
            print("\n❌ 无法连接到arcs仿真环境，程序退出")
            return
        
        # 2. 获取机器人列表
        print("\n===== 查找可用机器人 =====")
        robot_names = client.getRobotNames()
        print(f"可用机器人列表: {robot_names}")
        
        # 3. 处理机器人列表情况
        if not robot_names:
            print("❌ 未找到可用机器人")
            print("可能原因：")
            print("  1. 机器人未启动")
            print("  2. 仿真环境未正确配置")
            print("  3. 权限不足")
            
            # 尝试检查和启用仿真模式
            print("\n===== 尝试启用仿真模式 =====")
            try:
                # 尝试获取默认机器人接口（即使列表为空）
                print("尝试获取默认机器人接口 'robot0'...")
                robot_interface = client.getRobotInterface("robot0")
                print("✅ 成功获取默认机器人接口")
                
                # 启用仿真模式
                if enable_simulation_mode(robot_interface):
                    # 重新获取机器人列表
                    print("重新获取机器人列表...")
                    robot_names = client.getRobotNames()
                    print(f"更新后的机器人列表: {robot_names}")
                    
                    # 如果现在有机器人了，可以继续操作
                    if robot_names:
                        print("✅ 仿真模式启用后找到了机器人！")
            except Exception as e:
                print(f"❌ 获取默认机器人接口时发生错误: {str(e)}")
                print("提示：在某些arcs仿真环境中，可能需要先手动创建或启动仿真机器人实例")
            
            print("\n===== 故障排除建议 =====")
            print("1. 确保arcs仿真环境正在运行")
            print("2. 检查VMware网络配置是否正确（推荐使用桥接模式）")
            print("3. 确认防火墙没有阻止连接")
            print("4. 尝试重启arcs仿真环境")
            print("5. 在arcs界面中手动检查并启动机器人实例")
        else:
            # 找到了机器人，可以进行控制操作
            print("✅ 发现可用机器人")
            
            # 获取第一个机器人的接口
            robot_name = robot_names[0]
            print(f"\n===== 控制机器人 '{robot_name}' =====")
            robot_interface = client.getRobotInterface(robot_name)
            
            # 启用仿真模式（即使机器人列表非空，也确保仿真模式已启用）
            enable_simulation_mode(robot_interface)
            
            # 获取机器人状态信息
            robot_state = robot_interface.getRobotState()
            print("\n===== 机器人状态信息 =====")
            print(f"机器人名称: {robot_name}")
            print(f"机器人模式: {robot_state.getRobotModeType()}")
            print(f"机器人是否稳定: {robot_state.isSteady()}")
            print(f"是否发生碰撞: {robot_state.isCollisionOccurred()}")
            
            # 获取并显示关节位置
            joint_positions = robot_state.getJointPositions()
            print(f"当前关节位置: {joint_positions}")
            
            # 获取并显示TCP位姿
            tcp_pose = robot_state.getTcpPose()
            print(f"当前TCP位姿: {tcp_pose}")

            # # 获取机器人配置接口并获取TCP偏移量
            robot_config = robot_interface.getRobotConfig()
            tcp_pose_offset = robot_config.getTcpOffset()
            print(f"当前TCP位姿偏移量: {tcp_pose_offset}")
            # 让机器人运动到指定角度
            print("\n===== 机器人关节运动 =====")
            try:
                # 获取运动控制接口
                motion_control = robot_interface.getMotionControl()
                
                # 设置目标关节角度（示例：六个关节的角度值，单位：弧度）
                target_joints = [0,0,0,0,0,0]  # 可根据需要修改这些值
                print(f"移动到目标关节角度: {target_joints}")            
                # 执行关节运动
                result = motion_control.moveJoint(target_joints, 0.05, 0.05, 0.5, 0.5)
                if result != AuboErrorCodes.AUBO_OK:
                    print(f"❌ 运动命令失败，错误代码: {result}")
                else:
                    print("✅ 运动命令已发送，等待完成...")
                    
                    # 等待运动完成
                    start_time = time.time()
                    timeout = 10.0  # 10秒超时
                    
                    while not robot_state.isSteady():
                        if time.time() - start_time > timeout:
                            print("❌ 运动超时")
                            break
                        time.sleep(0.1)
                    else:
                        print("✅ 运动完成")
                        
                        # 显示运动后的关节位置
                        new_joint_positions = robot_state.getJointPositions()
                        print(f"运动后的关节位置: {new_joint_positions}")
                        
            except Exception as e:
                print(f"❌ 运动控制时发生错误: {str(e)}")
            
            # 运行基础运动示例（可选，取消注释启用）
            # print("\n是否运行基础运动示例? (注释掉下面一行可以禁用)")
            # basic_motion_example(robot_interface)
              
    except Exception as e:
        print(f"\n❌ 发生异常: {str(e)}")
        print("请检查错误信息并尝试解决问题")
    finally:
        # 4. 断开连接
        print("\n===== 断开连接 =====")
        if client and client.hasLogined():
            print("正在登出...")
            client.logout()
            print("✅ 已登出")
        if client and client.hasConnected():
            print("正在断开连接...")
            client.disconnect()
            print("✅ 已断开连接")
    
    print("\n===== 程序执行完成 =====")

if __name__ == "__main__":
    main()
