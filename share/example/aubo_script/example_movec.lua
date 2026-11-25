--[[
    功能：圆弧运动
    步骤：
        第一步：通过计算获取圆弧轨迹的3个路点
        第二步：以直线运动的方式到达第一个路点
        第三步：执行圆弧运动
]]
local aubo = require('aubo')
local sched = sched or aubo.sched
local math = aubo.math or math

local sleep = sched.sleep
local thread = sched.thread
local sync = sched.sync
local run = sched.run
local kill = sched.kill
function p_example_movec()
    setDigitalInputActionDefault()
    setDigitalOutputRunstateDefault()
    setPayload(0, {0,0,0}, {0,0,0}, {0,0,0,0,0,0})
    setTcpOffset({0.0003,0.0001,0.00066,0,0,0})
    Base = {0,0,0,0,0,0}
    Tool = {0,0,0,0,0,0}
    
    function waitForMotionComplete()
        while (getQueueSize() > 0) or (isSteady() == false) do
            sync()
        end
    end
    
    local function calculate_point_to_move_towards(feature, direction, position_distance)
      local posDir={direction[1], direction[2], direction[3]}
      if (math.norm(posDir) < 1e-6) then
          return getTargetTcpPose()
      end
      local direction_vector_normalized=math.normalize(posDir)
      local displacement_pose={direction_vector_normalized[1] * position_distance,direction_vector_normalized[2] * position_distance,direction_vector_normalized[3] * position_distance,0,0,0}

      local wanted_displacement_in_base_frame=poseSub(poseTrans(feature, displacement_pose), feature)
      return poseAdd(getTargetTcpPose(), wanted_displacement_in_base_frame)
    end
    setPlanContext(0, 1, "Program")
    setPlanContext(0, 2, "example_movec.lua")
    -- 获取圆弧轨迹的路点
    -- 根据 (x-0.12294)^2 + (y-0.54855)^2 + (z-0.26319)^2 = 0.2^2 来计算
    z1 = 0.26319
    y1 = 0.7
    x1 = math.sqrt(math.pow(0.2, 2) - math.pow(y1 - 0.54855, 2) - math.pow(z1 - 0.26319, 2))
    waypoint1 = {x1, y1, z1, 3.14, 0.00, 3.14}
        
    z2 = 0.26319
    y2 = 0.55
    x2 = math.sqrt(math.pow(0.2, 2) - math.pow(y2 - 0.54855, 2) - math.pow(z2 - 0.26319, 2))
    waypoint2 = {x2, y2, z2, 3.14, 0.00, 3.14}
        
    z3 = 0.26319
    y3 = 0.35
    x3 = math.sqrt(math.pow(0.2, 2) - math.pow(y3 - 0.54855, 2) - math.pow(z3 - 0.26319, 2))
    waypoint3 = {x3, y3, z3, 3.14, 0.00, 3.14}
    -- 直线运动到圆弧运动的路点1   
    moveLine(waypoint1, 1, 1, 0, 0)
    sleep(1)
    -- 圆弧运动
    -- 对应AUBOPE move_track(MoveTrackType.ARC_CIR, true)
    moveCircle(waypoint2, waypoint3, 1, 1, 0, 0)
end

local plugin = {
  PRIORITY = 1000, -- set the plugin priority, which determines plugin execution order
  VERSION = "0.1",
  VENDOR = "Aubo Robotics",
}

function plugin:start_robot1()
  print("start_robot1---")
  -- 配置脚本环境
  local env = self.api:loadf(1)
  setmetatable(env, { __index = _G })
  env = require'aubo.scheduler'.trackGlobals(env) or env
  require('compat_env').setfenv(p_example_movec, env)
  p_example_movec()
end

function plugin:start(api)
  --
  self.api = api
  print("start---")
  self:start_robot1()
end

function plugin:robot_error_handler(name, err)
  --
  print("An error hanppen to robot "..name)
end

-- return our plugin object
return plugin
