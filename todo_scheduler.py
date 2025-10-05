import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import winsound #Windows環境限定
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  #DPIスケーリング有効
except:
     pass


# ----- メインウィンドウ設定 ----- #
root = tk.Tk()
root.title("ToDoスケジュールツール")
root.geometry("700x900")
dark_mode = False   #ダークモード状態


# ----- 現在時刻の表示ラベル ----- #
current_time_label = ttk.Label(root, text="現在時刻：--:--:--", font=("Meiryo", 12))
current_time_label.pack(pady=10)

def update_time():
    now = datetime.now().strftime("%H:%M:%S")
    current_time_label.config(text=f"現在時刻：{now}")
    root.after(1000, update_time)

update_time()


# ----- タスクリスト用のフレーム ----- #
task_frame_container = ttk.Frame(root)
task_frame_container.pack(fill="both", expand=True)
task_frame = ttk.Frame(task_frame_container)
task_frame.pack(pady=10)

#中央寄せのためのカラムを配置
task_frame.grid_columnconfigure(0, weight=1)


# ----- タスク追加フォーム ----- #
form_frame = ttk.Frame(root)
form_frame.pack(pady=10)

task_name_entry = ttk.Entry(form_frame, width=20)
task_name_entry.grid(row=0, column=0, padx=5)

start_entry = ttk.Entry(form_frame, width=6)
start_entry.grid(row=0, column=1)
ttk.Label(form_frame, text="～").grid(row=0, column=2)
end_entry = ttk.Entry(form_frame, width=6)
end_entry.grid(row=0, column=3)


# ----- タスク管理リスト（通知済タスク記録付き） ----- #
#要素：{'name':..., 'start':..., 'end':..., 'notified':False}
tasks = []


# ----- タスク追加関数 ----- #
def add_task():
    name = task_name_entry.get().strip()
    start = start_entry.get().strip()
    end = end_entry.get().strip()

    if not name or not start or not end:
        return  #未入力なら無視
    
    #タスク完了時に表記をグレーアウトする関数
    def toggle_task_done():
        if done_var.get():
            task_label.config(foreground="gray")    #グレーアウト
            time_label.config(foreground="gray")
        else:
            task_label.config(foreground="black")   #未完了時は黒（デフォルト）
            time_label.config(foreground="black")
    
    #タスクの行
    row = ttk.Frame(task_frame)
    row.pack(fill="x", pady=2)

    #完了フラグ
    done_var = tk.BooleanVar(value=False)
    done_cb = ttk.Checkbutton(row, variable=done_var, command=toggle_task_done)
    done_cb.pack(side="left", padx=5)

    #タスク名
    task_label = ttk.Label(row, text=name, width=20, anchor="w", font=("Meiryo", 10))
    task_label.pack(side="left", padx=5)

    #時間帯
    time_label = ttk.Label(row, text=f"{start}～{end}", width=12, font=("Meiryo", 10))
    time_label.pack(side="left", padx=5)

    #削除ボタン
    delete_btn = ttk.Button(row, text="❌", width=3, command=lambda: row.destroy())
    delete_btn.pack(side="right", padx=5)

    #タスクデータを記録（通知済フラグ付き）
    task_data = {
        'name': name,
        'start': start,
        'end': end,
        'notified': False,
        'done_var': done_var}
    tasks.append(task_data)


    #入力フォーム初期化
    task_name_entry.delete(0, tk.END)
    start_entry.delete(0, tk.END)
    end_entry.delete(0, tk.END)


# ----- アラームチェック処理（10秒ごと） ----- #
def check_alarms():
    now = datetime.now().strftime("%H:%M")  #分単位で比較

    for task in tasks:
        if not task['notified'] and task['start'] == now:
            #通知実行処理
            messagebox.showinfo("タスク開始！", f"{task['name']}開始の時間です。")
            #winsound.Beep(800, 500)     #ビープ音（周波数, 時間ms）

            if 'done_var' in task:
                task['done_var'].set(False)

            task['notified'] = True     #通知済みにする
    
    root.after(10000, check_alarms)     #10秒ごとに再チェック

check_alarms()


def toggle_dark_mode():
    global dark_mode
    style = ttk.Style()

    if not dark_mode:
        #ダークモードON
        root.configure(bg="#222222")
        style.configure("TFrame", background="#222222")
        style.configure("TLabel", background="#222222", foreground="#FFFFFF")
        style.configure("TButton", background="#444444", foreground="#000000")
        style.configure("TCheckbutton", background="#222222", foreground="#000000")
        style.configure("TEntry", fieldbackground="#333333", foreground="#000000")
        dark_mode = True
    else:
        # ライトモード（デフォルト）ON
        root.configure(bg="#f0f0f0")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", foreground="#000000")
        style.configure("TButton", background="#f0f0f0", foreground="#000000")
        style.configure("TCheckbutton", background="#f0f0f0", foreground="#000000")
        style.configure("TEntry", fieldbackground="#ffffff", foreground="#000000")

        theme_button.config(text="テーマ切替")
        dark_mode = False


# ----- 追加ボタン ----- #
add_button = ttk.Button(form_frame, text="追加", command=add_task)
add_button.grid(row=0, column=4, padx=5)


# ----- ダークモード切替ボタン ----- #
theme_button = ttk.Button(root, text="テーマ切替", command=toggle_dark_mode)
theme_button.pack(pady=5)


# ----- メインループ ----- #
root.mainloop()