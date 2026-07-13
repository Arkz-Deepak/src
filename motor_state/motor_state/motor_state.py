#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int16

class MotorStateHMI(Node):
    # Define our 4 states as integers (0, 1, 2, 3)
    STATE_OFF = 0
    STATE_SPINNING_UP = 1
    STATE_ON = 2
    STATE_SPINNING_DOWN = 3

    def __init__(self):
        super().__init__('motor_state_HMI')
        
        # 1. State Variables (The Memory)
        self.current_state = self.STATE_OFF
        self.delay_timer = None     # Placeholder for our one-shot timer
        
        self.create_subscription(Int16, '/ctrl_signal', self.motor_state_callback, 10)

    def motor_state_callback(self, msg: Int16):
        command = msg.data

        # --- TURN ON COMMAND ---
        if command == 1:
            if self.current_state == self.STATE_OFF:
                self.get_logger().info("Starting the motor...")
                self.current_state = self.STATE_SPINNING_UP
                
                # Start a 2.0-second timer pointing to the spin-up completion function
                self.delay_timer = self.create_timer(2.0, self.spin_up_complete_callback)
            
            # If state is already 'ON' or 'SPINNING_UP', we do nothing and let it ride.

        # --- TURN OFF COMMAND ---
        elif command == 0:
            if self.current_state == self.STATE_ON or self.current_state == self.STATE_SPINNING_UP:
                self.get_logger().info("Stopping the motor...")
                self.current_state = self.STATE_SPINNING_DOWN
                
                # CRITICAL: If the motor was currently spinning up, cancel that timer instantly!
                if self.delay_timer is not None and not self.delay_timer.is_canceled():
                    self.delay_timer.cancel()
                
                # Start a 1.5-second timer pointing to the spin-down completion function
                self.delay_timer = self.create_timer(1.5, self.spin_down_complete_callback)

    # 2. Timer Callbacks (The Execution)
    def spin_up_complete_callback(self):
        self.get_logger().info("Started Roundy Round!!")
        self.current_state = self.STATE_ON
        
        # Cancel the timer so this function doesn't run again in 2 seconds
        self.delay_timer.cancel()

    def spin_down_complete_callback(self):
        self.get_logger().info("Motor has fully stopped.")
        self.current_state = self.STATE_OFF
        
        # Cancel the timer so this function doesn't run again in 1.5 seconds
        self.delay_timer.cancel()


def main(args=None):
    rclpy.init(args=args)
    node = MotorStateHMI()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()