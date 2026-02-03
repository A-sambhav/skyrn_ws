from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    robot_description = {
        'robot_description': Command([
            'xacro ',
            os.path.join(
                get_package_share_directory('skyrn_description'),
                'urdf',
                'skyrn_description.urdf.xacro'
            ),
            ' is_ignition:=false'
        ])
    }

    controllers_yaml = os.path.join(
        get_package_share_directory('skyrn_controller'),
        'config',
        'skyrn_controllers.yaml'
    )

    return LaunchDescription([robot_description, controllers_yaml,

        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[
                robot_description,
                controllers_yaml,
                {'use_sim_time': True}
            ],
            output='screen'
        ),

        ExecuteProcess(
            cmd=['ros2', 'run', 'controller_manager', 'spawner',
                 'joint_state_broadcaster'],
            output='screen'
        ),

        ExecuteProcess(
            cmd=['ros2', 'run', 'controller_manager', 'spawner',
                 'propeller_velocity_controller'],
            output='screen'
        ),
    ])
