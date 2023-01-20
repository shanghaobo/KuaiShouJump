"""
自动识别兔子坐标版，考虑透视计算
"""
import os
import sys
import json
import pyautogui
from pynput import keyboard
import time
from pynput.mouse import Button, Controller

# 长按一秒跳跃的像素距离，越低跳的越远（可按实际修改配置）
SECOND_DISTANCE = 528
# 单次完成后延时秒数（可按实际修改配置）
FINISHED_DELAY = 2
# 横纵坐标偏移量
X_DV = 7
Y_DV = 69


# 不需要修改
x1, y1 = 0, 0
x2, y2 = 0, 0


def resource_path(relative_path):
    """将相对路径转为exe运行时资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS  # 只有通过exe运行时才会进入这个分支，它返回的是exe运行时的临时目录路径
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 获取兔子坐标
def get_person_point():
    p = pyautogui.locateCenterOnScreen(resource_path('img/rabbitRight.png'), confidence=0.75)
    if not p:
        p = pyautogui.locateCenterOnScreen(resource_path('img/rabbitLeft.png'), confidence=0.75)
    if not p:
        return None, None
    # 偏移调整
    return p.x + X_DV, p.y + Y_DV


# 重置为默认
def reset():
    print('-----新一轮开始-----')
    global x1
    global y1
    global x2
    global y2
    x1, y1 = 0, 0
    x2, y2 = 0, 0

    x1, y1 = get_person_point()
    if not x1 and not y1:
        print('未获取到兔子坐标')
        print('等待1秒继续')
        time.sleep(1)
        reset()
        return
    print(f'已自动获取到兔子坐标：{x1},{y1}')
    print('等待按右Ctrl标记跳跃地')


# 执行跳一跳
def run_jump(x1, y1, x2, y2):
    if not all([x1, y1, x2, y2]):
        return
    # 计算距离
    distance = ((x2 - x1) ** 2 + ((y2 - y1) * (2 ** 0.5)) ** 2) ** 0.5
    print(f'距离:{distance}')
    tm = round(distance / SECOND_DISTANCE, 3)
    print(f'长按时间：{tm}秒')
    print('开始自动执行')
    mouse = Controller()
    print('开始点击')
    mouse.press(Button.left)
    time.sleep(tm)
    print('开始松手')
    mouse.release(Button.left)
    print('-----本次完成-----')
    print(f'延时{FINISHED_DELAY}秒')
    time.sleep(FINISHED_DELAY)
    reset()


# 监听按键
def on_press(key):
    if key == keyboard.Key.ctrl_r:
        print('已按下右Ctrl')
        global x2, y2
        x2, y2 = pyautogui.position()
        print(f'获取到坐标2：{x2},{y2}')
        run_jump(x1, y1, x2, y2)


def init_config():
    try:
        with open('config.json', 'r') as f:
            config_text = f.read()
            config = json.loads(config_text)
            global SECOND_DISTANCE, FINISHED_DELAY, X_DV, Y_DV
            SECOND_DISTANCE = config.get('second_distance')
            FINISHED_DELAY = config.get('finish_delay')
            X_DV = config.get('x_dv')
            Y_DV = config.get('y_dv')
    except:
        pass


if __name__ == "__main__":
    init_config()
    reset()
    with keyboard.Listener(on_press=on_press) as lsn:
        lsn.join()
