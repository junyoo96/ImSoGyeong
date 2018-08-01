# -*- coding: utf-8 -*-

import platform
import numpy as np
import argparse
import cv2
import serial
import time
import sys

# -----------------------------------------------
def clock():
    return cv2.getTickCount() / cv2.getTickFrequency()
# -----------------------------------------------
def draw_str_height(dst, target, s, height):
    x, y = target
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, height, (0, 0, 0), thickness = 2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, height, (255, 255, 255), lineType=cv2.LINE_AA)
# -----------------------------------------------
def create_blank(width, height, rgb_color=(0, 0, 0)):

    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color

    return image
# -----------------------------------------------
def TX_data(serial, one_byte):  # one_byte= 0~255
    global Temp_count
    try:
        serial.write(chr(int(one_byte)))
    except:
        Temp_count = Temp_count  + 1
        print("Serial Not Open " + str(Temp_count))
        pass
# -----------------------------------------------
def RX_data(serial):
    global Temp_count
    try:
        if serial.inWaiting() > 0:
            result = serial.read(1)
            RX = ord(result)
            return RX
        else:
            return 0
    except:
        Temp_count = Temp_count + 1
        print("Serial Not Open " + str(Temp_count))
        return 0
        pass
# -----------------------------------------------
# **************************************************
# **************************************************
# **************************************************
if __name__ == '__main__':

    # -------------------------------------
    print ("-------------------------------------")
    print ("(2018-6-15) Serial Test Program.    MINIROBOT Corp.")
    print ("-------------------------------------")
    print ("")
    os_version = platform.platform()
    print (" ---> OS " + os_version)
    python_version = ".".join(map(str, sys.version_info[:3]))
    print (" ---> Python " + python_version)
    opencv_version = cv2.__version__
    print (" ---> OpenCV  " + opencv_version)
    print ("")
    
    Setting_screen_w = 320
    Setting_screen_h = 120
    img = create_blank(Setting_screen_w, Setting_screen_h, rgb_color=(0, 100, 100))

    Top_name = "Serial Test Program"
    cv2.namedWindow(Top_name)
    draw_str_height(img, (15, (Setting_screen_h/4)), 'MINIROBOT Corp.', 1.2)
    draw_str_height(img, (15, int(Setting_screen_h/1.6)), 'key 1~9 Press', 2.0)

    draw_str_height(img, (15, int(Setting_screen_h/1.1)), 'Exit:  ESC key ', 1.2)
    
    cv2.imshow(Top_name, img)
    # ---------------------------
    BPS =  4800  # 4800,9600,14400, 19200,28800, 57600, 115200
    
    serial_port = serial.Serial('/dev/ttyAMA0', BPS, timeout=0.001)
    serial_port.flush() # serial cls
    # ---------------------------
       
    # -------- Main Loop Start --------

    # 라파이에서 제어기로 연결 확인
    Send_data = 239
    TX_data(serial_port, Send_data)
    print("TX => " + str(Send_data))

    while True:
        # 제어기에서 라파이로 통신 연결 확인
        Read_RX = RX_data(serial_port)
        if Read_RX==239:
            print("  <= RX : " + str(Read_RX))
            break

    while True:

            # 키보드로 통신하기 위해 사용하는 코드
            key = 0xFF & cv2.waitKey(1)

            if key == 27:  # ESC  Key
                break
            elif key == ord('1'):

                #어떤 동작 시킬지
                Send_data = 100

                # 로봇 동작 반복문
                for i in range(0,3):

                    if i==0:
                        TX_data(serial_port, Send_data)
                        print("TX => " + str(Send_data))

                    else:
                        while True:
                            A_Old = RX_data(serial_port)

                            if A_Old==253:
                                print("  <= RX : " + str(A_Old))
                                Send_data=100
                                TX_data(serial_port, Send_data)
                                print("TX => " + str(Send_data))
                                break

                # 마지막 로봇 부분 동작 멈춤 확인
                while True:
                    A_Old = RX_data(serial_port)
                    if A_Old<>0:
                        print("  <= RX : " + str(A_Old))
                        break

                # 로봇 동작 완전히 멈추게하기
                Send_data = 240
                TX_data(serial_port, Send_data)
                print("TX => " + str(Send_data))

                #제어기에서 로봇 동작 완전히 멈췄다는 것 신호확인
                while True:
                    WaitAllStopSignal= RX_data(serial_port)
                    if WaitAllStopSignal==254:
                        print("로봇 동작 완전 멈춤 => " + str(WaitAllStopSignal))
                        break



    # cleanup the camera and close any open windows
    serial_port.close()

    cv2.destroyAllWindows()






