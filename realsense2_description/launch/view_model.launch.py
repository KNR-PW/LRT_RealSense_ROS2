import os
import launch
from launch_ros.actions import Node
import sys
from ament_index_python.packages import get_package_share_directory

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from launch_utils import to_urdf

def generate_launch_description():
    package_path = get_package_share_directory('realsense2_description')
    urdf_dir = os.path.join(package_path, 'urdf')
    
    default_model = 'test_d455_camera.urdf.xacro'
    
    available_urdf_files = [f for f in os.listdir(urdf_dir) if f.startswith('test_')]

    params = dict([aa for aa in [aa.split(':=') for aa in sys.argv] if len(aa) == 2])

    if 'model' not in params or params['model'] not in available_urdf_files:
        print(f"Using default model: {default_model}")
        params['model'] = default_model

    xacro_path = os.path.join(urdf_dir, params['model'])

    urdf = to_urdf(xacro_path, {'use_nominal_extrinsics': 'true', 'add_plug': 'true'})

    rviz_config_dir = os.path.join(package_path, 'rviz', 'urdf.rviz')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_dir],
        parameters=[{'use_sim_time': False}]
    )
    
    model_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='model_node',
        output='screen',
        arguments=[urdf]
    )

    return launch.LaunchDescription([rviz_node, model_node])
