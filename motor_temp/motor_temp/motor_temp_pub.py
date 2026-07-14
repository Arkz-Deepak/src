#!/usr/bin/env python3

import rclpy
import random
from rclpy.node import Node
from motor_interfaces.msg import MotorState

class MotorTempPublisher(Node):
    def __init__(self):
        super().__init__('motor_temp_publisher')
        self.current_temp = 0
        self.pub_ = self.create_publisher(MotorState, '/motor_temp', 10)
        self.timeer_ = self.create_timer(4.0, self.temp_callback)

    def temp_callback(self):
        self.current_temp = random.uniform(0,50)
        if self.current_temp >= 45:
            self.get_logger().warn(f"Current Temperature is {self.current_temp}deg C")
        else:
            self.get_logger().info(f"Current Temperature is {self.current_temp}deg C")
        msg = MotorState()
        msg.motor_temp = self.current_temp
        self.pub_.publish(msg)

def main(args = None):
    rclpy.init(args = args)
    node = MotorTempPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()