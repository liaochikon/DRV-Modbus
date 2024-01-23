from pynput import keyboard
from drv_modbus import send
from drv_modbus import request
from pymodbus.client import ModbusTcpClient
import time

c = ModbusTcpClient(host="192.168.1.1", port=502, unit_id=2)
c.connect()
x , y , z , rx, ry, rz = request.Get_TCP_Pose(c)

def on_press(key):
    try:
        print(request.Get_TCP_Pose(c))
        if key == keyboard.Key.up:#-x
            send.Jog_Position(c, -1 , 0 , 0 , 0, 0, 0)
        if key == keyboard.Key.down:#+x
            send.Jog_Position(c, 1 , 0 , 0 , 0, 0, 0)
        if key == keyboard.Key.left:#-y
            send.Jog_Position(c, 0 , -1 , 0 , 0, 0, 0)
        if key == keyboard.Key.right:#+y
            send.Jog_Position(c, 0 , 1 , 0 , 0, 0, 0)
        if key == keyboard.Key.ctrl_l:#-z
            send.Jog_Position(c, 0 , 0 , -1 , 0, 0, 0)
        if key == keyboard.Key.shift_l:#+z
            send.Jog_Position(c, 0 , 0 , 1 , 0, 0, 0)
        
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    #print('{0} released'.format(key))
    if key == keyboard.Key.up:#-x
        send.Jog_Stop(c)
    if key == keyboard.Key.down:#+x
        send.Jog_Stop(c)
    if key == keyboard.Key.left:#-y
        send.Jog_Stop(c)
    if key == keyboard.Key.right:#+y
        send.Jog_Stop(c)
    if key == keyboard.Key.ctrl_l:#-z
        send.Jog_Stop(c)
    if key == keyboard.Key.shift_l:#+z
        send.Jog_Stop(c)
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

