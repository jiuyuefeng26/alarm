import tkinter as tk
import pyttsx3
import time
import threading
from datetime import datetime


def speak(text):
    """在独立线程中播放语音，避免阻塞界面"""
    def _run():
        try:
            engine = pyttsx3.init()
            # 可选：调整语速、音量
            engine.setProperty('rate', 160)   # 语速，默认约200
            engine.setProperty('volume', 1.0) # 音量 0.0 ~ 1.0
            # 中文语音（Windows 上通常有 "Microsoft Huihui Desktop" 或 "Microsoft Yaoyao"）
            # 若你的系统没有中文语音，可注释掉下面两行
            for v in engine.getProperty('voices'):
                if 'Chinese' in v.name or 'Huihui' in v.name or 'Yaoyao' in v.name:
                    engine.setProperty('voice', v.id)
                    break
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("语音播放失败:", e)

    t = threading.Thread(target=_run, daemon=True)
    t.start()


def main():
    root = tk.Tk()
    root.title('alarm')
    root.attributes('-fullscreen', True)
    root.overrideredirect(True)      #隐藏标题栏
    root.attributes("-topmost", True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}')
    root.configure(bg="#000000")

    # 防止启动瞬间的鼠标/键盘事件误关窗口
    start_time = time.time()
    LOCK_SECONDS = 2.0

    def can_close():
        return (time.time() - start_time) > LOCK_SECONDS

    def on_close(_event=None):
        if can_close():
            root.destroy()

    date = time.strftime("%Y/%m/%d")
    tk.Label(root, text=date, bg="#000000", fg='#FFFFFF',
             font=("Microsoft YaHei UI", 50)).place(x=50, y=50)

    def gettime():
        dstr.set(time.strftime("%H:%M:%S"))
        root.after(1000, gettime)

    dstr = tk.StringVar()
    lb = tk.Label(root, textvariable=dstr, bg="#000000", fg='#FFFFFF',
                  font=("Microsoft YaHei UI", 200))
    lb.place(x=100, y=200)

    root.bind('<Key>', on_close)
    root.bind('<Motion>', on_close)
    root.bind('<Button>', on_close)
    root.bind('<Escape>', on_close)

    gettime()

    # 画面出现的同时开始播报
    speak("稀饭煮好了，记得趁热吃啊")

    root.mainloop()


if __name__ == "__main__":
    main()
