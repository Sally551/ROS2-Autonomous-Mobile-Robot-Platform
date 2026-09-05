# ROS2 Autonomous Mobile Robot Platform Commands
## Task 1：启动机器人
```bash
cd ~/ramr_ws
source /opt/ros/humble/setup.bash
source ~/wheeltec_ws/install/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch ramr_bringup robot_bringup.launch.py
```
## Task 2：键盘控制
保持Task 1运行，新终端执行：
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
检查速度指令：
```bash
ros2 topic echo /cmd_vel
```
紧急停止：
```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```
## Task 3：传感器与TF验证
启动雷达：
```bash
ros2 launch turn_on_wheeltec_robot wheeltec_lidar.launch.py
```
检查雷达：
```bash
ros2 topic hz /scan
ros2 topic echo /scan --once
```
启动摄像头：
```bash
ros2 run usb_cam usb_cam_node_exe --ros-args \
-p video_device:=/dev/video1 \
-p pixel_format:=mjpeg2rgb \
-p image_width:=640 \
-p image_height:=480 \
-p framerate:=30.0 \
-p frame_id:=camera_link
```
显示图像：
```bash
ros2 run rqt_image_view rqt_image_view
```
检查IMU与里程计：
```bash
ros2 topic hz /imu/data_raw
ros2 topic hz /odom
```
检查TF：
```bash
ros2 run tf2_ros tf2_echo odom_combined base_footprint
ros2 run tf2_ros tf2_echo base_footprint laser
ros2 run tf2_ros tf2_echo base_link camera_link
ros2 run tf2_tools view_frames
```
## Task 4：状态估计与传感器融合

```bash
ros2 launch ramr_bringup robot_bringup.launch.py
```
```text
/odom ───────────┐
                 ├── ekf_filter_node ──→ /odom_combined
/imu/data_raw ───┘
```
检查EKF：
```bash
ros2 node info /ekf_filter_node
ros2 topic info /odom -v
ros2 topic info /imu/data_raw -v
ros2 topic info /odom_combined -v
ros2 topic hz /odom_combined
```
系统中应只有一个EKF：
```bash
ps -ef | grep '[e]kf_node'
```
## Task 5：SLAM建图

终端 1：基础系统
source /opt/ros/humble/setup.bash
source ~/wheeltec_ws/install/setup.bash
source ~/ramr_ws/install/setup.bash
ros2 launch ramr_bringup robot_bringup.launch.py

终端 2：启动雷达：

```bash
source /opt/ros/humble/setup.bash
source ~/wheeltec_ws/install/setup.bash
source ~/ramr_ws/install/setup.bash
ros2 launch turn_on_wheeltec_robot wheeltec_lidar.launch.py
```

确认雷达正常：

```bash
ros2 topic hz /scan
```

终端 3：启动 SLAM Toolbox 和 RViz：

```bash
source /opt/ros/humble/setup.bash
source ~/wheeltec_ws/install/setup.bash
source ~/ramr_ws/install/setup.bash
ros2 launch ramr_localization slam.launch.py
```
RViz 设置：

```text
Fixed Frame: map
Map Topic: /map
LaserScan Topic: /scan
```
```text
/scan + /odom_combined + /tf → SLAM Toolbox → /map
```
## Task 6：地图保存与管理
当 RViz 里已经出现地图后，新开终端执行：

```bash
source /opt/ros/humble/setup.bash
source ~/wheeltec_ws/install/setup.bash
source ~/ramr_ws/install/setup.bash
mkdir -p ~/ramr_ws/maps
ros2 run nav2_map_server map_saver_cli -f ~/ramr_ws/maps/my_map
```

成功后会生成：

```text
~/ramr_ws/maps/my_map.pgm
~/ramr_ws/maps/my_map.yaml
```

## Task 7：Nav2定位与自主导航
待完成。
```text
地图 + 雷达 + 里程计 + TF → Nav2 → /cmd_vel → 底盘
```
## Task 8：真机导航参数优化
待完成，主要调整速度、机器人轮廓、膨胀半径、障碍物层和目标容差。
## Task 9：动态避障与复杂环境导航
待完成，主要实现动态障碍物环境下的规划与避障。
## Task 10：视觉感知与智能导航
待完成，计划扩展YOLO、AprilTag、视觉辅助导航和VLM/VLA。
## Git
```bash
cd ~/ramr_ws
git status
git add .
git commit -m "Complete state estimation and robot bringup"
git push origin main
```