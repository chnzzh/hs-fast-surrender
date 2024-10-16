import win32gui
import json
import cv2
import numpy as np
import pyautogui
import keyboard
import time

window_name = "炉石传说"
distance_threshold = 30  # 根据需要调整该值


reg_x, reg_y, width, height = 0, 0, 0, 0  # 初始化监控区域的位置和大小
db = {}  # 用于保存特征点的数据库
regions = {}
orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


# 获取窗口句柄
def get_window_info(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        raise Exception(f"未找到名称为'{window_name}'的窗口")

    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]  # 左上角X坐标
    y = rect[1]  # 左上角Y坐标
    width = rect[2] - rect[0]  # 窗口宽度
    height = rect[3] - rect[1]  # 窗口高度
    return x, y, width, height

def get_feature(image_path):
    if image_path in db:
        return False
    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.resize(template, (0, 0), fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    #template = cv2.equalizeHist(template)
    #template = cv2.GaussianBlur(template, (3, 3), 0)

    kp1, des1 = orb.detectAndCompute(template, None)

    px, py = template.shape[:2]
    if des1 is None:
        print(f"未检测到 {image_path} 中的任何特征点")
        return False
    print(f"检测到 {image_path} 中的 {len(kp1)} 个特征点")

    return (kp1, des1, px, py)

def insert_feature(image_path):
    f = get_feature(image_path)
    if f:
        db[image_path] = f
        return True
    return False

def detect_pos(image_path, pos):
    """image_path必须是已经插入到数据库中的图片"""

    kp1, des1, px, py = db[image_path]

    base_reg_x, base_reg_y, base_width, base_height = pos

    screenshot = pyautogui.screenshot(region=pos)

    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    img = cv2.resize(img, (0, 0), fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

    kp2, des2 = orb.detectAndCompute(img, None)
    if des2 is None:
        print("\033[91m目标位置未检测到任何特征点，请检查配置\033[0m")
        return None

    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    if len(matches) == 0:
        print("未找到匹配点")
        return None

    best_match = matches[0] if matches[0].distance < distance_threshold else None

    if best_match is not None:
        # 获取匹配点的坐标
        x, y = kp2[best_match.trainIdx].pt
        x, y = base_reg_x + x/2, base_reg_y + y/2
        print(f"{image_path} 匹配到的位置: ({x}, {y})")
        return (x, y)

    return None

if __name__ == "__main__":
    reg_x, reg_y, width, height = get_window_info(window_name)
    if width * height < 10000:
        raise Exception("窗口太小，请重新选择")

    # 读json文件
    with open("frames.json", "r") as f:
        frames_info = json.load(f)
        for frame in frames_info:
            regions[frame['color']] = (frame['x'] + reg_x, frame['y'] + reg_y, frame['width'], frame['height'])

    if not insert_feature("start.png") or not insert_feature("surrender.png") or not insert_feature(
            "search.png") or not insert_feature(
            "continue.png"):
        print("未检测到特征点，程序退出")
        exit(0)

    stage = 0
    while True:
        time.sleep(0.5)
        if keyboard.is_pressed('alt'):
            print("退出程序")
            break

        if stage == 0:
            pos_start = detect_pos("start.png", regions['lightgreen'])
            pos_surrender = detect_pos("surrender.png", regions['lightpink'])
            pos_continue = detect_pos("continue.png", regions['lightblue'])
            if pos_start:
                stage = 1
                continue
            elif pos_surrender:
                stage = 2
                continue
            elif pos_continue:
                stage = 3
                continue
            else:
                stage = 1
                continue

        if stage == 1:
            pos_start = detect_pos("start.png", regions['lightgreen'])
            if pos_start:
                time.sleep(0.6)
                pyautogui.click(pos_start)
                stage = 2
                continue
            print("未检测到'开始'按钮")
        elif stage == 2:
            pos_surrender = detect_pos("surrender.png", regions['lightpink'])
            if pos_surrender:
                pyautogui.click(pos_surrender)
                stage = 3
                continue
            keyboard.press_and_release('esc')
        elif stage == 3:
            pos_continue = detect_pos("continue.png", regions['lightblue'])
            if pos_continue:
                pyautogui.click(pos_continue)
                continue
            pos_start = detect_pos("start.png", regions['lightgreen'])
            if pos_start:
                stage = 1
                continue
