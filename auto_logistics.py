from cgitb import reset
from time import sleep
import cv2 as cv
import os
import subprocess
import random
import argparse

#连接mumu模拟器
opt=argparse.ArgumentParser()
opt.add_argument('-a','--address',help='指定设备地址,默认mumu模拟器',default=r'127.0.0.1:7555')
args=opt.parse_args()
connect_command='adb connnect '+args.address
os.system(connect_command)
#打开样本图片
sample=cv.imread("./sample.png")

def clear_screen():
    os.system('cls')

clear_screen()

def get_screenshot():
    subprocess.check_output('adb shell /system/bin/screencap -p /sdcard/screencap.png', shell=True)
    subprocess.check_output('adb pull /sdcard/screencap.png ./screenshots/screencap.png', shell=True)
    screenshot=cv.imread('./screenshots/screencap.png')
    clear_screen()
    print('已截图')
    sleep(2)
    return screenshot
def compare(target,sample):
    clear_screen()
    print('开始寻找目标')
    sleep(2)
    result=cv.matchTemplate(target,sample,cv.TM_CCORR_NORMED)
    min_val,max_val,min_loc,max_loc=cv.minMaxLoc(result)
    if max_val>=0.95:
        clear_screen()
        print('找到目标')
        sleep(4)
        mat_top,mat_left=max_loc
        sp_h,sp_w,sp_ch=sample.shape
        bottom_right=(mat_top+sp_w,mat_left+sp_h)
        cv.rectangle(target,(mat_top,mat_left),bottom_right,(31,30,51),3)
        cv.imwrite('./outputs/testoutput.png',target)
        return True
    else:
        clear_screen()
        print('未找到目标,开始等待')
        return False

#1207 742 1371 777
#760 531 906 570
times=0
while True:
    p_x=random.randint(1207,1371)
    p_y=random.randint(742,777)
    p_x_2=random.randint(760,906)
    p_Y_2=random.randint(531,570)
    adbcommand_1='adb shell input tap %d %d'%(p_x,p_y)
    adbcommand_2='adb shell input tap %d %d'%(p_x_2,p_Y_2)
    if compare(target=get_screenshot(),sample=sample):
        os.system(adbcommand_1)
        sleep(2)
        os.system(adbcommand_2)
        times+=1
        sleep(1)
        print('已收获',times,'次')
    else:
        clear_screen()
        print('等待60s')
        print('当前已收获',times,'次')
        i=60
        while (i!=0):
            print('当前剩余',i,'秒',end='\r')
            i-=1
            sleep(1)