# ROS2 Autonomous Mobile Robot Platform Commands

Task1:启动
每个新终端依次运行：

```bash
cd ~/ramr_ws
source /opt/ros/humble/setup.bash
source ~/wheeltec_ws/install/setup.bash
colcon build --symlink-install
source ~/ramr_ws/install/setup.bash
```

```bash
ros2 launch ramr_bringup robot_bringup.launch.py
```



## 5. Task 2：键盘控制与运动验证

保持基础系统运行，新终端执行：

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

检查速度指令：

```bash
ros2 topic echo /cmd_vel
```

紧急发送一次零速度指令：

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

测试期间应确保机器人周围空间安全。

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

### 主要 Topic

| Topic | 发布者 | 订阅者 |

|---|---|---|

| `/odom` | `/wheeltec_robot` | `/ekf_filter_node` |

| `/imu/data_raw` | `/wheeltec_robot` | `/ekf_filter_node` |

| `/odom_combined` | `/ekf_filter_node` | SLAM、Nav2等 |

### Topic检查命令

```bash

ros2 topic info /odom -v

ros2 topic info /imu/data_raw -v

ros2 topic info /odom_combined -v

```

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

      /cmd\_vel

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

```还有这个

下面是整理后的完整 COMMANDS.md。重点修正了环境加载顺序，并将现在推荐的统一启动方式放在前面。

# ROS2 Autonomous Mobile Robot Platform Commands

## 1. 环境配置

每个新终端依次运行：

```bash
source /opt/ros/humble/setup.bash
source ~/wheeltec_ws/install/setup.bash
source ~/ramr_ws/install/setup.bash
```

加载顺序不能颠倒：

```text
ROS 2 Humble → WHEELTEC厂家工作空间 → RAMR项目工作空间
```

后续会将这三条命令写入统一环境脚本。

## 2. 编译项目

编译全部自定义功能包：

```bash
cd ~/ramr_ws
source /opt/ros/humble/setup.bash
source ~/wheeltec_ws/install/setup.bash

colcon build --symlink-install
source ~/ramr_ws/install/setup.bash
```

只编译状态估计和统一启动包：

```bash
cd ~/ramr_ws

colcon build --symlink-install \
  --packages-select ramr_localization ramr_bringup

source ~/ramr_ws/install/setup.bash
```

## 3. 当前推荐启动方式

启动前确认没有旧的EKF进程：

```bash
ps -ef | grep '[e]kf_node'
```

统一启动底盘、机器人模型、关节状态和EKF：

```bash
ros2 launch ramr_bringup robot_bringup.launch.py
```

该启动文件包含：

```text
base_serial.launch.py
robot_mode_description.launch.py
joint_state_publisher
state_estimation.launch.py
```

它不包含厂家的 `wheeltec_ekf.launch.py`，因此系统中只会运行自己的一个EKF。

不要同时运行：

```bash
ros2 launch turn_on_wheeltec_robot turn_on_wheeltec_robot.launch.py
```

否则厂家EKF和自己的EKF可能同时启动。

## 4. Task 1：真机底盘驱动接入

单独调试底盘驱动时运行：

```bash
ros2 launch turn_on_wheeltec_robot base_serial.launch.py
```

检查底盘控制接口：

```bash
ros2 topic info /cmd_vel
```

如果显示至少一个订阅者，说明底盘节点可以接收速度指令。

检查底盘设备：

```bash
ls -l /dev/wheeltec_controller
```

## 5. Task 2：键盘控制与运动验证

保持基础系统运行，新终端执行：

```bash
source /opt/ros/humble/setup.bash
source ~/wheeltec_ws/install/setup.bash
source ~/ramr_ws/install/setup.bash

ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

检查速度指令：

```bash
ros2 topic echo /cmd_vel
```

检查发布者和订阅者：

```bash
ros2 topic info /cmd_vel -v
```

紧急发送一次零速度指令：

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

测试期间应确保机器人周围空间安全。

## 6. Task 3：传感器与TF验证

### 6.1 检查设备

检查底盘和雷达串口：

```bash
ls -l /dev/wheeltec_controller
ls -l /dev/wheeltec_lidar
```

查看摄像头设备：

```bash
v4l2-ctl --list-devices
```

摄像头设备编号可能是 `/dev/video0` 或 `/dev/video1`，应以实际查询结果为准。

### 6.2 启动激光雷达

```bash
ros2 launch turn_on_wheeltec_robot wheeltec_lidar.launch.py
```

检查雷达：

```bash
ros2 topic info /scan -v
ros2 topic hz /scan
ros2 topic echo /scan --once
```

正常频率约为10 Hz。

在RViz2中显示：

```bash
rviz2
```

推荐设置：

```text
Fixed Frame：base_footprint
Display：LaserScan
Topic：/scan
```

如果TF尚未启动，可以临时将 `Fixed Frame` 设置为雷达消息中的实际坐标系。

### 6.3 启动摄像头

以下命令以 `/dev/video1` 为例：

```bash
ros2 run usb_cam usb_cam_node_exe --ros-args \
  -p video_device:=/dev/video1 \
  -p pixel_format:=mjpeg2rgb \
  -p image_width:=640 \
  -p image_height:=480 \
  -p framerate:=30.0 \
  -p frame_id:=camera_link
```

显示ROS 2图像：

```bash
ros2 run rqt_image_view rqt_image_view
```

选择：

```text
/image_raw
```

检查图像频率：

```bash
ros2 topic hz /image_raw
```

### 6.4 检查IMU

```bash
ros2 topic info /imu/data_raw -v
ros2 topic echo /imu/data_raw --once
ros2 topic hz /imu/data_raw
```

### 6.5 检查编码器里程计

```bash
ros2 topic info /odom -v
ros2 topic echo /odom --once
ros2 topic hz /odom
```

### 6.6 检查TF

检查融合里程计到机器人底盘：

```bash
ros2 run tf2_ros tf2_echo odom_combined base_footprint
```

检查底盘到雷达：

```bash
ros2 run tf2_ros tf2_echo base_footprint laser
```

如果实际雷达坐标系为 `laser_link` 或 `radar`，使用：

```bash
ros2 run tf2_ros tf2_echo base_footprint laser_link
ros2 run tf2_ros tf2_echo base_footprint radar
```

检查相机TF：

```bash
ros2 run tf2_ros tf2_echo base_link camera_link
```

生成完整TF树：

```bash
ros2 run tf2_tools view_frames
```

结果保存在当前目录的 `frames.pdf`。

## 7. Task 4：状态估计与传感器融合

当前数据链路：

```text
/odom ───────────┐
                 ├── ekf_filter_node ──→ /odom_combined
/imu/data_raw ───┘
```

主要Topic：

| Topic | 发布者 | 订阅者 |
|---|---|---|
| `/odom` | 底盘驱动 | `ekf_filter_node` |
| `/imu/data_raw` | IMU驱动 | `ekf_filter_node` |
| `/odom_combined` | `ekf_filter_node` | SLAM、Nav2等 |

检查EKF节点：

```bash
ros2 node info /ekf_filter_node
```

确认系统中只有一个EKF：

```bash
ros2 node list | grep ekf
ps -ef | grep '[e]kf_node'
```

检查输入与输出：

```bash
ros2 topic info /odom -v
ros2 topic info /imu/data_raw -v
ros2 topic info /odom_combined -v
```

正确状态：

```text
/odom：发布者1，订阅者1
/imu/data_raw：发布者1，订阅者1
/odom_combined：发布者1
```

检查融合频率：

```bash
ros2 topic hz /odom_combined
```

当前正常频率约为10 Hz。

查看一条融合结果：

```bash
ros2 topic echo /odom_combined --once
```

检查融合TF：

```bash
ros2 run tf2_ros tf2_echo odom_combined base_footprint
```



## 8. Task 5：SLAM建图

待完成。

计划使用SLAM Toolbox完成实机环境建图。

主要输入：

```text
/scan
/odom_combined
/tf
/tf_static
```

## 9. Task 6：地图保存与管理

待完成。

计划保存：

```text
map.yaml
map.pgm
```

地图将统一存放在项目的地图目录中。

## 10. Task 7：Nav2定位与自主导航

待完成。

主要数据链路：

```text
地图 + 雷达 + 里程计 + TF
              ↓
             Nav2
              ↓
          /cmd_vel
              ↓
           底盘驱动
```

## 11. Task 8：真机导航参数优化

待完成。

重点参数包括：

- 机器人速度与加速度
- 机器人轮廓
- 障碍物膨胀半径
- 代价衰减系数
- 障碍物层
- 目标容差
- 局部控制器

## 12. Task 9：动态避障与复杂环境导航

待完成。

重点研究动态障碍物环境下的局部规划、避障和运动控制。

## 13. Task 10：视觉感知与智能导航

待完成。

计划逐步扩展：

- YOLO目标检测
- AprilTag识别与定位
- 视觉辅助导航
- 视觉语言模型
- 视觉语言动作模型

## 14. 常用诊断命令

查看全部节点：

```bash
ros2 node list
```

查看全部Topic：

```bash
ros2 topic list
```

查看Topic连接：

```bash
ros2 topic info <topic_name> -v
```

查看Topic频率：

```bash
ros2 topic hz <topic_name>
```

查看一条消息：

```bash
ros2 topic echo <topic_name> --once
```

查看指定节点：

```bash
ros2 node info <node_name>
```

## 15. Git

查看修改：

```bash
cd ~/ramr_ws
git status
```

添加修改：

```bash
git add .
```

提交：

```bash
git commit -m "Complete state estimation and robot bringup"
```

推送：

```bash
git push origin main
```