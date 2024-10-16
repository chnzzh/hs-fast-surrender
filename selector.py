import tkinter as tk
import win32gui
import json

def get_window_info(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        print(f"未找到名称为'{window_name}'的窗口")
        return None
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]  # 左上角X坐标
    y = rect[1]  # 左上角Y坐标
    width = rect[2] - rect[0]  # 窗口宽度
    height = rect[3] - rect[1]  # 窗口高度
    return x, y, width, height


class DraggableResizableBox:
    def __init__(self, x, y, width, height):
        self.root = tk.Tk()
        self.root.title("画图")
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.configure(bg='gray')
        self.root.wm_attributes("-alpha", 0.7)
        self.root.resizable(width=False, height=False)

        self.frames = []

        # 退出事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # 在中间生成三个可以调整大小的框
        paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=1)

        try:
            with open("frames.json", "r") as f:
                frames_info = json.load(f)
                for frame_info in frames_info:
                    self.create_draggable_resizable_frame(frame_info['width'], frame_info['height'],
                                                          frame_info['color'], frame_info['x'], frame_info['y'])
        except :
            self.create_draggable_resizable_frame(200, 200, 'lightpink', 100, 100)
            self.create_draggable_resizable_frame(200, 200, 'lightblue', 400, 100)
            self.create_draggable_resizable_frame(200, 200, 'lightgreen', 700, 100)

    def create_draggable_resizable_frame(self, width, height, color, x, y):
        frame = DraggableResizableFrame(self.root, width=width, height=height, bg=color)
        frame.place(x=x, y=y)
        self.frames.append(frame)

    def on_close(self):
        frames_info = []
        for frame in self.frames:
            frame_info = {
                'x': frame.winfo_x(),
                'y': frame.winfo_y(),
                'width': frame.winfo_width(),
                'height': frame.winfo_height(),
                'color': frame.cget('bg')  # 记录颜色
            }
            frames_info.append(frame_info)
        # 保存框的位置和大小为json文件
        with open("frames.json", "w") as f:
            json.dump(frames_info, f)
        self.root.destroy()

class DraggableResizableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Button-1>", self.on_left_click)  # 左键点击
        self.bind("<B1-Motion>", self.on_drag)  # 左键拖动
        self.bind("<Button-3>", self.on_right_click)  # 右键点击
        self.bind("<B3-Motion>", self.on_resize)  # 右键拖动

        self._drag_data = {"x": 0, "y": 0}
        self._resize_data = {"x": 0, "y": 0, "width": 0, "height": 0}

    # 左键点击事件，记录点击位置
    def on_left_click(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    # 左键拖动事件，移动框
    def on_drag(self, event):
        x = self.winfo_x() - self._drag_data["x"] + event.x
        y = self.winfo_y() - self._drag_data["y"] + event.y
        self.place(x=x, y=y)

    # 右键点击事件，记录初始大小和位置
    def on_right_click(self, event):
        self._resize_data["x"] = event.x
        self._resize_data["y"] = event.y
        self._resize_data["width"] = self.winfo_width()
        self._resize_data["height"] = self.winfo_height()

    # 右键拖动事件，调整大小
    def on_resize(self, event):
        new_width = max(100, self._resize_data["width"] + (event.x - self._resize_data["x"]))
        new_height = max(100, self._resize_data["height"] + (event.y - self._resize_data["y"]))
        self.config(width=new_width, height=new_height)


# 创建一个 DraggableResizableBox 实例并运行
if __name__ == "__main__":
    x, y, width, height = get_window_info("炉石传说")
    box = DraggableResizableBox(x, y, width, height)
    box.root.mainloop()
