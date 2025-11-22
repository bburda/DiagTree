# Copyright 2025 mfaferek93
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Get package directory
    pkg_dir = get_package_share_directory('ros2_medkit_gateway')

    # Path to default config file
    default_config = os.path.join(pkg_dir, 'config', 'gateway_params.yaml')

    # Declare launch arguments for easy overriding
    declare_host_arg = DeclareLaunchArgument(
        'server_host',
        default_value='127.0.0.1',
        description='Host to bind REST server (127.0.0.1 or 0.0.0.0)'
    )

    declare_port_arg = DeclareLaunchArgument(
        'server_port',
        default_value='8080',
        description='Port for REST API'
    )

    declare_refresh_arg = DeclareLaunchArgument(
        'refresh_interval_ms',
        default_value='2000',
        description='Cache refresh interval in milliseconds'
    )

    # Gateway node with parameters
    gateway_node = Node(
        package='ros2_medkit_gateway',
        executable='gateway_node',
        name='ros2_medkit_gateway',
        output='screen',
        parameters=[
            default_config,  # Load from YAML first
            {  # Override with launch arguments
                'server.host': LaunchConfiguration('server_host'),
                'server.port': LaunchConfiguration('server_port'),
                'refresh_interval_ms': LaunchConfiguration('refresh_interval_ms'),
            }
        ],
        arguments=['--ros-args', '--log-level', 'info']
    )

    return LaunchDescription([
        declare_host_arg,
        declare_port_arg,
        declare_refresh_arg,
        gateway_node
    ])
