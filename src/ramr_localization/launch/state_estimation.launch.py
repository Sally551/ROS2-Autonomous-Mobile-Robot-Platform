import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_dir = get_package_share_directory('ramr_localization')
    ekf_config = os.path.join(package_dir, 'config', 'ekf.yaml')

    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config],
        remappings=[
            ('/odometry/filtered', '/odom_combined')
        ]
    )

    return LaunchDescription([
        ekf_node
    ])
