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
    while True:
  
        # 제어기에서 로봇 동작 명령 받기
        Read_RX = RX_data(serial_port)
        if Read_RX <> 0:
            print("  <= RX : " + str(Read_RX))
       
        key = 0xFF & cv2.waitKey(1)
        
        if key == 27:  # ESC  Key
            break
        elif key == ord('1'):

            Send_data = 100

            for i in range(0,4):

                if i==0:
                    TX_data(serial_port, Send_data)
                    print("TX => " + str(Send_data))

                else:
                    while True:
                        A_Old = RX_data(serial_port)
                        print("  <= RX : " + str(A_Old))
                        if A_Old==253:
                            Send_data=100
                            TX_data(serial_port, Send_data)
                            break

            Send_data = 240
            TX_data(serial_port, Send_data)
            break







            # for i in range(0,5):
            #
            #     print("come in!")
            #     while True:
            #
            #         if i == 0:
            #             TX_data(serial_port, Send_data)
            #             print("TX => " + str(Send_data))
            #             break
            #
            #         else:
            #             while True:
            #                 A_Old= RX_data(serial_port)
            #                 if A_Old<>0:
            #                     print("  <= RX : " + str(A_Old))
            #                     break
            #
            #             if A_Old == 38:
            #                 TX_data(serial_port, Send_data)
            #                 print("TX => " + str(Send_data))
            #                 break

            # Send_data = 240
            # TX_data(serial_port, Send_data)
            # print("TX => " + str(Send_data))

        elif key == ord('2'):
            Send_data = 102
            TX_data(serial_port,Send_data)
            print("TX => " + str(Send_data))
        # elif key == ord('3'):
        #     Send_data = 103
        #     TX_data(serial_port,Send_data)
        #     print("TX => " + str(Send_data))
        # elif key == ord('4'):
        #     Send_data = 104
        #     TX_data(serial_port,Send_data)
        #     print("TX => " + str(Send_data))
        # elif key == ord('5'):
        #     Send_data = 105
        #     TX_data(serial_port,Send_data)
        #     print("TX => " + str(Send_data))
        # elif key == ord('6'):
        #     Send_data = 106
        #     TX_data(serial_port,Send_data)
        #     print("TX => " + str(Send_data))
        # elif key == ord('7'):
        #     Send_data = 107
        #     TX_data(serial_port,Send_data)
        #     print("TX => " + str(Send_data))
        # elif key == ord('8'):
        #     Send_data = 108
        #     TX_data(serial_port,Send_data)
        #     print("TX => " + str(Send_data))
        # elif key == ord('9'):
        #     Send_data = 109
        #     TX_data(serial_port,Send_data)
        #     print("TX => " + str(Send_data))


    # cleanup the camera and close any open windows
    serial_port.close()

    cv2.destroyAllWindows()






