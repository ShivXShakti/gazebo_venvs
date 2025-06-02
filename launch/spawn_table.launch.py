from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-entity', 'simple_table',
                '-file', '/home/cstar/Documents/dual_arm_ws/src/gazebo_venvs/models/table/model.sdf',
                '-x', '1.3',
                '-y', '0.0',
                '-z', '0.0'
            ],
            output='screen'
        )
    ])
