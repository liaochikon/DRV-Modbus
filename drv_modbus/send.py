from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
from drv_modbus import request

MovP = 0
MovL = 1

def Go_Position(c, x, y, z, rx, ry, rz, speed = 20, mov = 0, block = True):
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    builder.add_32bit_int(int(x  * 1000))
    builder.add_32bit_int(int(y  * 1000))
    builder.add_32bit_int(int(z  * 1000))
    builder.add_32bit_int(int(rx * 1000))
    builder.add_32bit_int(int(ry * 1000))
    builder.add_32bit_int(int(rz * 1000))
    payload = builder.to_registers()
    c.write_register(0x0324, speed, 2)
    c.write_registers(0x0330, payload, 2)

    if mov == MovP:
        print("MovP")
        c.write_register(0x0300, 301, 2)   
    if mov == MovL:
        print("MovL")
        c.write_register(0x0300, 302, 2)   

    print("Start moving...")
    if block == False:
        return

    pos_flag = 2
    while pos_flag != 1:
        pos_flag = request.Get_Pose_Flag(c)
    print("Move done!")

def Suction_ON(c):
    c.write_register(0x02FE, 1, 2)   

def Suction_OFF(c):
    c.write_register(0x02FE, 0, 2)   

def Jog_Position(c, x, y, z, rx, ry, rz):
    if x > 0:
        c.write_registers(0x0300, 601, 2)
    if x < 0:
        c.write_registers(0x0300, 602, 2)

    if y > 0:
        c.write_registers(0x0300, 603, 2)
    if y < 0:
        c.write_registers(0x0300, 604, 2)

    if z > 0:
        c.write_registers(0x0300, 605, 2)
    if z < 0:
        c.write_registers(0x0300, 606, 2)

    if rx > 0:
        c.write_registers(0x0300, 607, 2)
    if rx < 0:
        c.write_registers(0x0300, 608, 2)

    if ry > 0:
        c.write_registers(0x0300, 609, 2)
    if ry < 0:
        c.write_registers(0x0300, 610, 2)

    if rz > 0:
        c.write_registers(0x0300, 611, 2)
    if rz < 0:
        c.write_registers(0x0300, 612, 2)

def Jog_Stop(c):
    c.write_registers(0x0300, 0, 2)