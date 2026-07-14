#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from motor_interfaces.msg import MotorState
class MotorControllerNode(Node):
    def __init__(self):
        super().__init__('motor_contoller_node')
        self.ctrl_pub_ = self.create_publisher(MotorState, '/ctrl_signal', 20)
        self.temp_ = self.create_subscription(MotorState, '/motor_temp', self.control_callback, 10)
        self.ctrl_sig_ = 0

    def control_callback(self,msg: MotorState):
        if msg.motor_temp > 45.0:
            if self.ctrl_sig_ == 0:
                self.get_logger().info("The motor is in off state")
            else:
                self.get_logger().warn("Turning Off the motor as its overheating")
            self.ctrl_sig_ = 0
        else:
            if self.ctrl_sig_ == 1:
                self.get_logger().info("The motor is in on state")
            else:
                self.get_logger().info("Turning on the motor")
            self.ctrl_sig_ = 1
        signal = MotorState()
        signal.ctrl_signal = self.ctrl_sig_
        self.ctrl_pub_.publish(signal)


def main(args = None):
    rclpy.init(args = args)
    node = MotorControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()