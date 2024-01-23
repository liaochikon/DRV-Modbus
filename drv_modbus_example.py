from drv_modbus import send
from drv_modbus import request
from pymodbus.client import ModbusTcpClient
import time

c = ModbusTcpClient(host="192.168.1.1", port=502, unit_id=2)
c.connect()

home = [408.285, 0.0, 680.0120000000001, 178.969, -0.241, -103.145]

#x : 388.442, y : -73.33200000000001, z : 325.693, rx: 179.987, ry: -0.004, rz: -106.121
#x : 637.4350000000001, y : 221.607, z : 322.593, rx: 179.987, ry: -0.004, rz: -106.121
#z : 324.796

#send.Suction_ON(c)
#time.sleep(1)
#send.Suction_OFF(c)

#send.Go_Position(c, 353.208, -48.09, 680.0, 179.987, -0.004, -106.121, 50) #home
#send.Go_Position(c, 388.442+100, -73.332+100, 680.0-200, 179.987, -0.004, -106.121, 50)

while True:
    x , y , z , rx, ry, rz = request.Get_TCP_Pose(c)

    print("x : " + str(x ), end=", ")
    print("y : " + str(y ), end=", ")
    print("z : " + str(z ), end=", ")
    print("rx: " + str(rx), end=", ")
    print("ry: " + str(ry), end=", ")
    print("rz: " + str(rz))

    time.sleep(0.2)

c.close()