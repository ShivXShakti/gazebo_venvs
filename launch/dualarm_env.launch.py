from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
from launch.actions import ExecuteProcess
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
def generate_launch_description():
    # Get the path to the package and the URDF file
    pkg_description = get_package_share_directory('gazebo_venvs')
    
    # Return the LaunchDescription
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_description, 'launch', 'spawn_table.launch.py'))
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_description, 'launch', 'spawn_bottle.launch.py'))
        ),

    ])

if __name__ == '__main__':
    generate_launch_description()