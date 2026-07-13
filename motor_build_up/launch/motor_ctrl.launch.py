from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    temp_node = Node(
        package = 'motor_temp',
        executable  = 'temp_pub',
        name = 'temperature_publisher',
        output = 'screen'
    )
    ctrl_node = Node(
        package = "motor_ctrl",
        executable = 'ctrl_signal',
        name = 'control_node',
        output = 'screen'

    )
    hmi_node = Node(
        package = "motor_state",
        executable = 'hmi',
        name = 'hmi_node',
        output = 'screen'
    )
    return LaunchDescription([
        temp_node,
        ctrl_node,
        hmi_node
    ])