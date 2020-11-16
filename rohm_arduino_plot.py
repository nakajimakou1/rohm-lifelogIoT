# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pygame
from pygame.locals import *
import serial
import sys
import math

def main():
    xscale = 1000
    ser = serial.Serial("COM7", 115200)  # COMポート(Arduino接続)
    temps = np.array([0]*xscale)         # 温度格納
    myakus= np.array([0]*xscale)
    presss= np.array([0]*xscale)
    magxys= np.array([0]*xscale)
    accxs= np.array([0]*xscale)
    accys= np.array([0]*xscale)
    acczs= np.array([0]*xscale)
    
    t = np.arange(0,xscale,1)
    plt.ion()
    pygame.init()                # Pygameを初期化
    screen = pygame.display.set_mode((200, 200))   # 画面作成(100×100)
    pygame.display.set_caption("傾斜角度")         # タイトルバー
    font = pygame.font.Font(None, 50)              # 文字の設定
    
    # print("[*] temps:", temps)
    # print("[*] t:", t)

    # 描画領域を取得
    fig, ax = plt.subplots(1, 1)

    """
    bm1383aglv.get_val(&press, &press_temp);// 気圧センサ
    bd1020.get_val(&temp);	// 温度センサ
    bm1422agmv.get_val(mag);// 地磁気センサ
    bh1790glc.get_val(val);	// 脈波センサ
    kx224.get_val(acc);		// 加速度センサ
    sprintf(str,"%d,%d,%s,%s,%s,%s,%s,%s,%s,%s,%s\n", val[0], val[1], tempbuf, mag0buf, mag1buf, mag2buf, pressbuf, presstempbuf, acc0buf, acc1buf, acc2buf);
    sprintf(str,"%d,%d,%s,%s,%s,%s,%s,%s,%s,%s,%s\n", val[0], val[1], tempbuf, mag[x] , mag[y] , mag[z] , pressbuf, presstempbuf, acc[x] , acc[y] , acc[z] );
    """
    ser.flush()
    while True:
        stemp = ser.readline().rstrip().decode(encoding='utf-8').replace(' ','') # \nまで読み込む
        temp = stemp.split(",") #.decode(encoding='utf-8')
        # print("[*] len(temp):",len(temp))
        if(len(temp) == 11) :
            print("[*1] temp:", temp)
        else:
            print("[*1] temp:+")
            continue
        
        text = font.render(str(float(temp[2])/10) + "[C]", False, (255,255,255))    # 表示する文字の設定
        screen.blit(text, (10, 10))     # レンダ，表示位置
        pygame.display.flip()           # 画面を更新して、変更を反映
        # 温度データのリスト更新
        temps  = np.append(float(temp[2]), temps)    # np.array
        temps  = np.delete(temps, len(temps) - 1)
        myakus = np.append(int(temp[0])+50, myakus)  
        myakus = np.delete(myakus, len(myakus) - 1)
        presss = np.append((float(temp[6])-1009.2)*100, presss)  
        presss = np.delete(presss, len(presss) - 1)
        magxys = np.append(math.degrees(math.atan2((float(temp[3])+30), (float(temp[4])+20))), magxys)  # 
        magxys = np.delete(magxys, len(magxys) - 1)
        accxs  = np.append(float(temp[8])*50, accxs)
        accxs  = np.delete(accxs, len(accxs) - 1)
        accys  = np.append(float(temp[9])*50, accys)
        accys  = np.delete(accys, len(accys) - 1)
        acczs  = np.append(float(temp[10])*50, acczs)
        acczs  = np.delete(acczs, len(acczs) - 1)
        print("[*1] temp:", temp, magxys[0])

        # グラフ表示設定
        plt.title("Real-time temperature")
        plt.xlabel("Time [s]")
        plt.ylabel("Temperature [Celsius]")
        plt.legend("t")
        plt.grid()
        plt.xlim([1,xscale])
        plt.ylim([0,150])
        
        line,  = ax.plot(t, temps, color='blue')   # 温度更新
        line2, = ax.plot(t, myakus, color='red')   # 脈波更新
        line3, = ax.plot(t, presss, color='green') # 気圧更新
        #line4, = ax.plot(t, accxs, color='yellow') # ACC X軸更新
        line5, = ax.plot(t, acczs, color='purple') # ACC Z軸更新
        line6, = ax.plot(t, magxys, color='black') # MAG XYRotate軸更新

        plt.draw()
        plt.pause(0.001)

        # グラフをクリア
        line.remove()
        line2.remove()
        line3.remove()
        #line4.remove()
        line5.remove()
        line6.remove()
        
        for event in pygame.event.get():
        # 終了ボタンが押されたら終了処理
            if event.type == QUIT:
                pygame.quit()
                ser.close()
                plt.close()
                sys.exit()


if __name__ == '__main__':
    main()
