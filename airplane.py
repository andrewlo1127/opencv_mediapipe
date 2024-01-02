from codrone_edu.drone import *
import video_pose
import keyboard
drone = Drone()

drone.pair()
def up():
    for i in range(1):
        # 上升
        drone.takeoff()
        drone.set_throttle(25)
        drone.move(1)

def back():
    # 後退
    drone.set_pitch(-30)
    drone.move(2)

# #前進
def straight():
    drone.set_pitch(30)
    drone.move(2)

#右移
def move_right():
    drone.set_roll(50)
    drone.move(2) # move command executes the movement for 1 second
#前進
    drone.set_pitch(30)
    drone.move(2)

def turn_right():
#右旋
    drone.set_yaw(50)
    drone.move(2)
#後退
    drone.set_pitch(-30)
    drone.move(1)
def land():
#下降
    print("fuck")
    drone.set_throttle(-25)
    drone.move(2)
    drone.land()
    print("land")

# drone.land()
def stop():
    while True:
        if keyboard.read_key()=="a":
            print("強制停止")
            drone.stop_motors()

# up()
land()