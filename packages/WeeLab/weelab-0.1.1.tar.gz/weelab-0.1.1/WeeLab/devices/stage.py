import time

from WeeLab.connections.base import InstrumentConnection

default_mictosteps = 8
default_steps_per_rotation = 200
default_screw_pitch = 5
default_max_speed = 5
default_acceleration = 2


class Stage:
    tries_to_save = 3

    def __init__(self, conn: InstrumentConnection):
        self.conn = conn
        self.init()

    def __del__(self):
        if self.conn is not None:
            self.save_state()
            self.close()
        else:
            print("No stage to disconnect. Quitting...")

    def init(self):
        self.connected = False
        self.enabled = False
        self.current_position = None
        self.isrunning = (False, False)
        self.speed = (0, 0)
        self.limiters = ((False, False), (False, False))
        # self.connect()
        self.configure()

    def enable(self, en_state):
        self.conn.write(f"en {en_state} ")
        line = self.conn.read()
        if "En changed " not in line:
            raise Exception("Could not enable stage")
        self.enabled = line.decode().split()[3] == "1"

    def configure(self):
        self.steps_per_rotation = default_steps_per_rotation  # steps
        self.screw_pitch = default_screw_pitch  # mm
        self.microsteps = default_mictosteps  # steps

        self.max_speed = default_max_speed  # mm/s
        self.acceleration = default_acceleration  # mm/s^2

        self.steps_per_mm = self.steps_per_rotation * self.microsteps / self.screw_pitch
        self.max_speed_steps = self.max_speed * self.steps_per_mm
        self.acceleration_steps = self.acceleration * self.steps_per_mm

        self.conn.write(f"setvmax {self.max_speed_steps} {self.max_speed_steps} ")
        self.conn.write(f"setacc {self.acceleration_steps} {self.acceleration_steps} ")

        self.conn.write(f"currpos ")
        line = self.conn.read()
        self.current_position = int(line.split()[1]), int(line.split()[2])

    def set_vmax(self, vmax_x):
        if vmax_x is None:
            return
        self.max_speed = vmax_x
        self.max_speed_steps = self.max_speed * self.steps_per_mm
        self.conn.write(f"setvmax {self.max_speed_steps} {self.max_speed_steps} ")

    def set_acc(self, acc_x):
        if acc_x is None:
            return
        self.acceleration = acc_x
        self.acceleration_steps = self.acceleration * self.steps_per_mm
        self.conn.write(f"setacc {self.acceleration_steps} {self.acceleration_steps} ")

    def set_microsteps(self, microsteps):
        if microsteps is None:
            return
        if microsteps not in [
            1,
            2,
            4,
            8,
            16,
            32,
            64,
            128,
            5,
            10,
            20,
            25,
            40,
            50,
            100,
            125,
        ]:
            return
        self.microsteps = microsteps
        self.steps_per_mm = self.steps_per_rotation * self.microsteps / self.screw_pitch
        self.max_speed_steps = self.max_speed * self.steps_per_mm
        self.acceleration_steps = self.acceleration * self.steps_per_mm
        self.conn.write(f"setvmax {self.max_speed_steps} {self.max_speed_steps} ")
        self.conn.write(f"setacc {self.acceleration_steps} {self.acceleration_steps} ")

    def move(self, x, y, mode="mm"):
        self.current_target = (x, y)
        self.this_init_positon = self.current_position
        if mode == "mm":
            x = int(x * self.steps_per_mm)
            y = int(y * self.steps_per_mm)
        elif mode == "steps":
            x = int(x)
            y = int(y)
        self.conn.write(f"move {x} {y} ")

    def move_axis(self, axis, value, mode="mm"):
        self.this_init_positon = self.current_position
        if axis == "x":
            self.current_target = (value, self.current_position[1])
            command = "xmove"
        elif axis == "y":
            self.current_target = (self.current_position[0], value)
            command = "ymove"

        if mode == "mm":
            value = int(value * self.steps_per_mm)
        elif mode == "steps":
            value = int(value)

        self.conn.write(f"{command} {value} ")

    def ask_position(self):
        line = self.conn.query("currpos ")
        # self.current_position = int(line.decode().split()[1]), int(line.decode().split()[2])
        self.current_position = (
            int(line.split()[1]) / self.steps_per_mm,
            int(line.split()[2]) / self.steps_per_mm,
        )
        return self.current_position

    def refresh_status(self):
        self.conn.write(f"status ")
        line = self.conn.read()
        messages = line.split("|")
        # print(line)
        if len(messages) < 5:
            return
        self.enabled = messages[0].split()[1] == "1"
        self.isrunning = (messages[1].split()[1] == "1", messages[1].split()[2] == "1")
        self.current_position = (
            int(messages[2].split()[1]) / self.steps_per_mm,
            int(messages[2].split()[2]) / self.steps_per_mm,
        )
        self.speed = (
            float(messages[3].split()[1]) / self.steps_per_mm,
            float(messages[3].split()[2]) / self.steps_per_mm,
        )
        self.limiters = (
            (messages[4].split()[1] == "1", messages[4].split()[2] == "1"),
            (messages[4].split()[3] == "1", messages[4].split()[4] == "1"),
        )
        # print(self.enabled, self.isrunning, self.current_position, self.speed, self.limiters)

    def print_status(self):
        self.refresh_status()
        print(f"Enabled: {self.enabled}")
        print(f"Is running: {self.isrunning}")
        print(f"Current position: {self.current_position}")
        print(f"Speed: {self.speed}")
        print(f"Limiters: {self.limiters}")

    def set_position(self, axis=None, position=(0, 0)):
        if axis == "x":
            self.conn.write(f"setxcurpos {position*self.steps_per_mm}")
        elif axis == "y":
            self.conn.write(f"setycurpos {position*self.steps_per_mm}")
        else:
            self.conn.write(f"setxcurpos {position[0]*self.steps_per_mm}")
            self.conn.write(f"setycurpos {position[1]*self.steps_per_mm}")
        return self.current_position

    def save_state(self):
        for i in range(self.tries_to_save):
            self.conn.write(f"save ")
            line = self.conn.read()
            if "saved" in line:
                print("State saved successfully")
                return
            else:
                print("Error saving state")
        return

    def stop(self):
        # self.ser.write(f"xstop ".encode())
        # self.ser.write(f"ystop ".encode())
        self.conn.write(f"stop ")

    def close(self):
        self.conn.close()

    def wait_arrived(self):
        self.refresh_status()
        time.sleep(0.5)
        while self.isrunning[0] or self.isrunning[1]:
            self.refresh_status()
            time.sleep(0.5)


# stage = Stage("COM4")
