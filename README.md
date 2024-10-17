# hs-fast-surrender

## 简介

某个游戏的自动快速投降脚本，非进程注入的纯视觉实现。

*仅限测试本地游戏稳定性，请勿在实际对局中使用*

![演示](https://github.com/user-attachments/assets/7962847e-bee2-42ec-a0ed-5cb68f9fcd47)

## 依赖项

请确保已安装以下依赖：

- Python 3.x
- OpenCV
- pyautogui
- keyboard
- pywin32

可以使用以下命令安装依赖项：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 使用方法

1. 调整游戏为窗口模式，大小为 1920x1080，并进入开始位置。

2. 运行 `main.py` 脚本，开始监控指定窗口内的按钮。

```bash
python main.py
```

3. 长按 `Q` 键退出程序。

## 文件说明

- `main.py`：主脚本，负责监控窗口并执行自动点击操作。
- `selector.py`：用于创建和调整识别框的位置和大小，并保存到 `frames.json` 文件中。
- `frames.json`：保存框的位置和大小信息（默认1920x1080）。
- `*.png`：识别的模板图片

## 注意事项

- 请确保目标窗口名称正确，并且窗口在运行时可见。
- 程序会影响鼠标和键盘的操作，请确保在运行时不要操作鼠标和键盘。

## 实现方式

![图片](https://github.com/user-attachments/assets/32ad4d0a-3d2a-401d-80a0-76321a175837)

