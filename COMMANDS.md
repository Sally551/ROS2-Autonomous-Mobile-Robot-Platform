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

## Task 1：真机底盘驱动接入
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

## Task 3：各种传感器与状态数据验证

本任务用于验证激光雷达、IMU、摄像头、里程计和 TF 是否正常工作。

当前设备对应关系应为：

```text
/dev/wheeltec_controller -> /dev/ttyACM1
/dev/wheeltec_lidar -> /dev/ttyACM0
Integrated Webcam -> /dev/video0
```
### 启动机器人

```bash
cd ~/ramr_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch turn_on_wheeltec_robot turn_on_wheeltec_robot.launch.py
```

### 启动雷达

如果机器人启动文件没有自动启动雷达：

```bash
source /opt/ros/humble/setup.bash
source ~/ramr_ws/install/setup.bash
ros2 launch turn_on_wheeltec_robot wheeltec_lidar.launch.py
```

在 RViz2 中显示雷达：

```bash
rviz2
```

将 `Fixed Frame` 设置为 `laser`，添加 `LaserScan`，Topic 选择 `/scan`。

### 启动摄像头

```bash
source /opt/ros/humble/setup.bash
source ~/ramr_ws/install/setup.bash
ros2 run usb_cam usb_cam_node_exe --ros-args -p video_device:=/dev/video0 -p frame_id:=camera_link
```

另开终端显示 ROS2 图像：

```bash
source /opt/ros/humble/setup.bash
source ~/ramr_ws/install/setup.bash
ros2 run rqt_image_view rqt_image_view
```

选择 `/image_raw`。

直接显示摄像头画面：

```bash
ffplay -f v4l2 -i /dev/video0
```

### 检查 IMU

```bash
ros2 topic list | grep -i imu
ros2 topic echo /imu/data_raw --once
ros2 topic hz /imu/data_raw
```

### 检查里程计

```bash
ros2 topic echo /odom --once
ros2 topic hz /odom
```

### 检查 TF

```bash
ros2 run tf2_ros tf2_echo odom_combined base_footprint
ros2 run tf2_ros tf2_echo base_footprint laser
ros2 run tf2_ros tf2_echo base_link camera_link
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