# ROS2 Autonomous Mobile Robot Platform Commands

## 环境配置

每个新终端先运行：

```bash
source /opt/ros/humble/setup.bash
source ~/ramr_ws/install/setup.bash
```

## 编译

首次编译底层基础包：

```bash
cd ~/ramr_ws
source /opt/ros/humble/setup.bash

colcon build --symlink-install \
  --base-paths src/vendor src/vendor/depend \
  --packages-select \
  serial \
  wheeltec_robot_msg \
  wheeltec_robot_urdf \
  turn_on_wheeltec_robot

source install/setup.bash
```

后续修改自己的功能包时，只编译对应功能包，例如：

```bash
cd ~/ramr_ws
source /opt/ros/humble/setup.bash
source install/setup.bash

colcon build --symlink-install \
  --packages-select ramr_navigation

source install/setup.bash
```

查看当前工作区识别到的 ROS 2 包：

```bash
cd ~/ramr_ws
colcon list
```

## Task 1：真机底盘驱动接入

检查底盘串口：

```bash
ls -l /dev/wheeltec_controller
```

启动底盘：

```bash
ros2 launch turn_on_wheeltec_robot turn_on_wheeltec_robot.launch.py
```

正常情况下应能看到底盘串口成功打开相关日志。

## Task 2：键盘控制与运动验证

保持底盘驱动运行，新终端执行：

```bash
source /opt/ros/humble/setup.bash
source ~/ramr_ws/install/setup.bash

ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

检查控制指令：

```bash
ros2 topic echo /cmd_vel
```

检查 `/cmd_vel` 发布者和订阅者：

```bash
ros2 topic info /cmd_vel
```

紧急发送一次零速度指令：

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

## Task 3：LiDAR、IMU、Odometry 与 TF 验证

查看当前 Topic：

```bash
ros2 topic list
```

### LiDAR

查找激光雷达 Topic：

```bash
ros2 topic list | grep scan
```

检查激光数据：

```bash
ros2 topic echo /scan
ros2 topic hz /scan
```

### IMU

查找 IMU Topic：

```bash
ros2 topic list | grep imu
```

确认实际 Topic 名称后，再检查数据和频率：

```bash
ros2 topic echo <imu_topic>
ros2 topic hz <imu_topic>
```

### Odometry

查找里程计 Topic：

```bash
ros2 topic list | grep odom
```

检查里程计数据：

```bash
ros2 topic echo /odom
ros2 topic hz /odom
```

### TF

检查 TF 发布频率：

```bash
ros2 topic hz /tf
```

检查 `odom -> base_link`：

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

生成 TF 树：

```bash
ros2 run tf2_tools view_frames
```

## Task 4：状态估计与传感器融合

待完成。

计划验证编码器里程计与 IMU 数据，并通过状态估计获得稳定的机器人位姿信息。

## Task 5：SLAM 建图

待完成。

计划使用 SLAM Toolbox 完成真机环境建图。

## Task 6：地图保存与管理

待完成。

计划保存和管理：

```text
map.yaml
map.pgm
```

## Task 7：Nav2 定位与自主导航

待完成。

主要数据链路：

```text
Map + LiDAR + Odometry + TF
              ↓
             Nav2
              ↓
          /cmd_vel
              ↓
         Robot Driver
```

## Task 8：真机导航参数优化

待完成。

重点优化：

- 机器人速度
- footprint
- inflation radius
- cost scaling factor
- obstacle layer
- goal tolerance
- controller

## Task 9：动态避障与复杂环境导航

待完成。

重点研究动态障碍物环境下的局部规划、避障和运动控制。

## Task 10：视觉感知与智能导航

待完成。

计划逐步扩展：

- Camera
- YOLO
- AprilTag
- 视觉辅助导航
- VLM / VLA

## Git

查看状态：

```bash
git status
```

添加修改：

```bash
git add .
```

提交：

```bash
git commit -m "Update ROS2 autonomous mobile robot platform"
```