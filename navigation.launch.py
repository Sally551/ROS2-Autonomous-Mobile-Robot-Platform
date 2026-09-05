import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    ramr_navigation_dir = get_package_share_directory('ramr_navigation')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    map_file = os.path.expanduser('~/ramr_ws/maps/my_map.yaml')
    params_file = os.path.join(
        ramr_navigation_dir,
        'config',
        'nav2_params.yaml'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            default_value=map_file,
            description='Full path to map yaml file'
        ),
        DeclareLaunchArgument(
            'params_file',
            default_value=params_file,
            description='Full path to Nav2 parameter file'
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    nav2_bringup_dir,
                    'launch',
                    'bringup_launch.py'
                )
            ),
            launch_arguments={
                'map': LaunchConfiguration('map'),
                'params_file': LaunchConfiguration('params_file'),
                'use_sim_time': 'false',
                'autostart': 'true',
                'slam': 'false'
            }.items()
        )
    ])