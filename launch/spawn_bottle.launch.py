from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-entity', 'bottle',
                '-file', '/home/kd/Documents/dual_arm_ws/src/gazebo_venvs/models/bottle/model.sdf',
                '-x', '0.7',
                '-y', '-0.2',
                '-z', '1.2'
            ],
            output='screen'
        )
    ])
