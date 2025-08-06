# -*-coding:utf-8-*-
from machine import Pin

MOTOR1_CHANNEL1 = 4
MOTOR1_CHANNEL2 = 5
MOTOR2_CHANNEL1 = 6
MOTOR2_CHANNEL2 = 7

PERIOD = 20


class MotorsController:
    """
    A singleton class to control two DC motors using PWM signals.

    This class provides a simple interface to control the speed and direction
    of two DC motors. It initializes the PWM pins for each motor channel and
    provides methods to set the motor speed, stop the motors, and configure
    the forward/reverse speed and offset parameters for each motor.
    Example:
        >>> motors = MotorsController()
        >>> # Set motor 1 to forward at half speed
        >>> motors.set_speed(1, 1024)
        >>> # Set motor 2 to reverse at quarter speed
        >>> motors.set_speed(2, -512)
        >>> # Stop motor 1
        >>> motors.stop(1)
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MotorsController, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the MotorsController instance.
        """
        # Ensure __init__ only initializes once
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True

        self.motor1_1 = Pin(MOTOR1_CHANNEL1, Pin.OUT)
        self.motor1_2 = Pin(MOTOR1_CHANNEL2, Pin.OUT)
        self.motor2_1 = Pin(MOTOR2_CHANNEL1, Pin.OUT)
        self.motor2_2 = Pin(MOTOR2_CHANNEL2, Pin.OUT)

        self.motor1_1_duty = 0
        self.motor1_2_duty = 0
        self.motor2_1_duty = 0
        self.motor2_2_duty = 0

        self.motor_params = {
            1: {'forward_speed': 100, 'reverse_speed': 100, 'offset': 0},
            2: {'forward_speed': 100, 'reverse_speed': 100, 'offset': 0}
        }

        self.period_cnt = 0

        self.motor1_1.on()
        self.motor1_2.on()
        self.motor2_1.on()
        self.motor2_2.on()

    def motors_period_cb(self):
        """
        Updates the duty cycles of the motors based on the current motor duty.
        This method simulates PWM
        by turning the motors on and off in intervals,
        adjusting the duty cycles based on the PWM timing signal.

        This method should be called periodically to update motor speed.
        Example:
            >>> motors.motors_period_cb()  # Periodically update motor speed
        """
        self.period_cnt = (self.period_cnt + 1) % PERIOD

        if self.motor1_1_duty == 0 and self.motor1_2_duty == 0:
            self.motor1_1.on()
            self.motor1_2.on()
        else:
            if self.period_cnt >= self.motor1_1_duty:
                self.motor1_1.off()
            else:
                self.motor1_1.on()

            if self.period_cnt >= self.motor1_2_duty:
                self.motor1_2.off()
            else:
                self.motor1_2.on()

        if self.motor2_1_duty == 0 and self.motor2_2_duty == 0:
            self.motor2_1.on()
            self.motor2_2.on()
        else:
            if self.period_cnt >= self.motor2_1_duty:
                self.motor2_1.off()
            else:
                self.motor2_1.on()

            if self.period_cnt >= self.motor2_2_duty:
                self.motor2_2.off()
            else:
                self.motor2_2.on()

    def set_speed(self, motor_idx, speed):
        """
        Sets the speed of a motor.

        This method sets the speed of a specified motor by adjusting the duty \
            cycles of its channels.
        The speed is controlled using a simulated PWM (Pulse Width Modulation)\
            signal, where the duty cycle
        determines the effective speed of the motor.
        The speed value can range from -2048 to 2048, where \
            positive values indicate forward movement, \
                negative values indicate reverse movement, and zero \
                    indicates no movement.

        Args:
            motor_idx (int): Index of the motor (1 or 2).
            speed (int): Speed value to set for the motor,\
                ranging from -2048 to 2048.
        Returns:
            None
        Example:
            >>> # Set motor 1 to move forward at half speed
            >>> set_speed(1, 1024)
            >>> # Set motor 2 to move reverse at a quarter speed
            >>> set_speed(2, -512)
        """
        if motor_idx == 1:
            self.motor1_1_duty, self.motor1_2_duty = self._speed_handler(speed)
        elif motor_idx == 2:
            self.motor2_1_duty, self.motor2_2_duty = self._speed_handler(speed)
        else:
            print("[motors]Invalid motor index. Must be between 1 and 2.")

    def stop(self, motor_idx):
        """
        Stops a motor by setting its duty cycles to 0.

        Args:
            motor_idx (int): Index of the motor (1 or 2).
        Raises:
            ValueError: If the motor index is not 1 or 2.
        Example:
            >>> motors.stop(1)  # Stop motor 1
            >>> motors.stop(2)  # Stop motor 2
        """
        if motor_idx == 1:
            self.motor1_1_duty = 0
            self.motor1_2_duty = 0
            self.motor1_1.on()
            self.motor1_2.on()
        elif motor_idx == 2:
            self.motor2_1_duty = 0
            self.motor2_2_duty = 0
            self.motor2_1.on()
            self.motor2_2.on()
        else:
            raise ValueError(
                "[motors]Invalid motor index. Must be between 1 and 2.")

    def set_forward_rate(self, motor_idx, val):
        """
        Sets the maximum forward speed for the specified motor.
        The speed value must be between 0 and 100, \
            where 100 indicates maximum speed.

        Args:
            motor_idx (int): Index of the motor (1 or 2).
            val (int): The forward speed, in the range [0, 100].

        Raises:
            ValueError: If the value is outside the acceptable range.
        Example:
            >>> # Set motor 1 to 80% forward speed
            >>> motors.set_forward_rate(1, 80)
        """
        if motor_idx in self.motor_params:
            if 0 <= val <= 100:
                self.motor_params[motor_idx]['forward_speed'] = val
            else:
                print("[motors]Parameter value out of range (0-100).")
        else:
            print("[motors]Invalid motor index or parameter.")

    def set_reverse_rate(self, motor_idx, val):
        """
        Sets the maximum reverse speed for the specified motor.

        Args:
            motor_idx (int): Index of the motor (1 or 2).
            val (int): The reverse speed, in the range [0, 100].

        Raises:
            ValueError: If the value is outside the acceptable range.
        Example:
            >>> # Set motor 2 to 50% reverse speed
            >>> motors.set_reverse_rate(2, 50)
        """
        if motor_idx in self.motor_params:
            if 0 <= val <= 100:
                self.motor_params[motor_idx]['reverse_speed'] = val
            else:
                print("[motors]Parameter value out of range (0-100).")
        else:
            print("[motors]Invalid motor index or parameter.")

    def set_offset(self, motor_idx, val):
        """
        Sets the offset for the specified motor.

        Args:
            motor_idx (int): Index of the motor (1 or 2).
            val (int): The offset value, in the range [-100, 100].

        Raises:
            ValueError: If the value is outside the acceptable range.
        Example:
            >>> motors.set_offset(1, 20)  # Set motor 1 offset to 20
        """
        if motor_idx in self.motor_params:
            if -100 <= val <= 100:
                self.motor_params[motor_idx]['offset'] = val
            else:
                print("[motors]Parameter value out of range (-100-100).")
        else:
            print("[motors]Invalid motor index or parameter.")

    # Getter methods for motor parameters

    def get_forward_rate(self, motor_idx):
        """
        Gets the maximum forward speed for the specified motor.

        Args:
            motor_idx (int): Index of the motor (1 or 2).

        Returns:
            int: The forward speed of the motor, in the range [0, 100].
            If the motor index is invalid, returns None.
        Example:
            >>> # Returns 100 (default forward speed for motor 1)
            >>> motors.get_forward_rate(1)
            >>> # Returns 80 (if motor 2's forward speed is set to 80)
            >>> motors.get_forward_rate(2)
    """
        if motor_idx in self.motor_params:
            return self.motor_params[motor_idx]['forward_speed']
        else:
            print("[motors] Invalid motor index.")
            return None

    def get_reverse_rate(self, motor_idx):
        """
        Gets the maximum reverse speed for the specified motor.

        Args:
            motor_idx (int): Index of the motor (1 or 2).
            If the motor index is invalid, returns None.

        Returns:
            int: The reverse speed of the motor, in the range [0, 100].
        Example:
            >>> # Returns 100 (default reverse speed for motor 1)
            >>> motors.get_reverse_rate(1)
            >>> # Returns 80 (if motor 2's reverse speed is set to 80)
            >>> motors.get_reverse_rate(2)
    """
        if motor_idx in self.motor_params:
            return self.motor_params[motor_idx]['reverse_speed']
        else:
            print("[motors] Invalid motor index.")
            return None

    def get_offset(self, motor_idx):
        """
        Gets the offset value for the specified motor.

        Args:
            motor_idx (int): Index of the motor (1 or 2).

        Returns:
            int: The offset value of the motor, in the range [-100, 100].
        Example:
            >>> # Returns 0 (default offset for motor 1)
            >>> motors.get_offset(1)
            >>> # Returns 10 (if motor 2's offset is set to 10)
            >>> motors.get_offset(2)
        """
        if motor_idx in self.motor_params:
            return self.motor_params[motor_idx]['offset']
        else:
            print("[motors] Invalid motor index.")
            return None

    def _speed_handler(self, speed):
        """
        Converts a speed value to duty cycle values for two motor channels.

        Args:
            speed (int): Speed value to convert.
        Returns:
            tuple: A tuple containing the duty cycle values for \
                the two motor channels.
        """
        if speed > 0:
            pwm1 = int(speed * PERIOD / 2048)
            pwm2 = 0
        elif speed < 0:
            pwm1 = 0
            pwm2 = int(-speed * PERIOD / 2048)
        else:
            pwm1 = 0
            pwm2 = 0
        return pwm1, pwm2
