import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    wheeltec_dir = get_package_share_directory('turn_on_wheeltec_robot')
    localization_dir = get_package_share_directory('ramr_localization')

    base_serial_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                wheeltec_dir,
                'launch',
                'base_serial.launch.py'
            )
        )
    )

    robot_description_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                wheeltec_dir,
                'launch',
                'robot_mode_description.launch.py'
            )
        )
    )

    state_estimation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                localization_dir,
                'launch',
                'state_estimation.launch.py'
            )
        )
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen'
    )

    return LaunchDescription([
        base_serial_launch,
        joint_state_publisher_node,
        robot_description_launch,
        state_estimation_launch
    ])
