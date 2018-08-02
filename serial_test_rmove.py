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
# 내가 만든 동작 호출 함수
def robot_action(send_data,retryNum):
    # 로봇 동작 반복문
    for i in range(0, retryNum):

        if i == 0:
            TX_data(serial_port, send_data)
            print("로봇 동작 명령=> : " + str(send_data))

        else:
            while True:
                A_Old = RX_data(serial_port)

                if A_Old == 253:
                    print("<=로봇 부분 동작 종료 : " + str(A_Old))
                    TX_data(serial_port, send_data)
                    print("로봇 동작 명령=> : " + str(send_data))
                    break

    # 마지막 로봇 부분 동작 멈춤 확인
    while True:
        A_Old = RX_data(serial_port)
        if A_Old <> 0:
            print("  <= 로봇 마지막 부분 동작 종료 : " + str(A_Old))
            break

    # 로봇 동작 완전히 멈추게하기
    send_data = 240
    TX_data(serial_port, send_data)
    print("로봇 동작 완전히 종료 명령 => : " + str(send_data))

    # 제어기에서 로봇 동작 완전히 멈췄다는 것 신호확인
    while True:
        waitAllStopSignal = RX_data(serial_port)
        if waitAllStopSignal == 254:
            print("<= 로봇 동작 완전 멈춤 : " + str(waitAllStopSignal))
            break



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
    send_data = 239
    TX_data(serial_port, send_data)
    print("라파이에서제어기연결체크 => : " + str(send_data))

    while True:
        # 제어기에서 라파이로 통신 연결 확인
        Read_RX = RX_data(serial_port)
        if Read_RX==239:
            print("  <= 제어기에서라파이연결됨: " + str(Read_RX))
            break

    while True:

            # 키보드로 통신하기 위해 사용하는 코드
            key = 0xFF & cv2.waitKey(1)

            if key == 27:  # ESC  Key
                break
            elif key == ord('1'):

                #어떤 동작 시킬지
                send_data = 121
                robot_action(send_data,3)

            elif key == ord('2'):

                # 어떤 동작 시킬지
                send_data = 122
                robot_action(send_data, 3)

            elif key == ord('3'):

                # 어떤 동작 시킬지
                send_data = 123
                robot_action(send_data, 3)

            elif key == ord('4'):

                # 어떤 동작 시킬지
                send_data = 130
                robot_action(send_data, 1)

            elif key == ord('5'):

                # 어떤 동작 시킬지
                send_data = 131
                robot_action(send_data, 1)

            elif key == ord('6'):

                # 어떤 동작 시킬지
                send_data = 135
                robot_action(send_data, 1)

            elif key == ord('7'):

                # 어떤 동작 시킬지
                send_data = 136
                robot_action(send_data, 1)

            elif key == ord('8'):

                # 어떤 동작 시킬지
                send_data = 137
                robot_action(send_data, 1)

            elif key == ord('9'):

                # 어떤 동작 시킬지
                send_data = 138
                robot_action(send_data, 1)

            elif key == ord('q'):

                # 어떤 동작 시킬지
                send_data = 139
                robot_action(send_data, 1)

            elif key == ord('w'):

                # 어떤 동작 시킬지
                send_data = 145
                robot_action(send_data, 1)

            elif key == ord('r'):

                # 어떤 동작 시킬지
                send_data = 146
                robot_action(send_data, 3)

            elif key == ord('s'):

                # 어떤 동작 시킬지
                send_data = 147
                robot_action(send_data, 1)






    # cleanup the camera and close any open windows
    serial_port.close()

    cv2.destroyAllWindows()






