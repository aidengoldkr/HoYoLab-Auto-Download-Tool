import json
import tkinter as tk
import tkinter.messagebox as messagebox
from download import download_imgs
import webbrowser

with open("text.json", "r", encoding="utf-8") as file:
    text_data = json.load(file)

window = tk.Tk()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
lang = "EN"

def open_github(event=None):
    webbrowser.open("https://github.com/Aidengoldkr")

def on_entry_click(default_text, entry):
    if entry.get() == default_text:
        entry.delete(0, tk.END)
        entry.config(fg="black")  

def on_focus_out(default_text, entry):
    if entry.get() == "":
        entry.insert(0, default_text)
        entry.config(fg="gray") 

def on_button_click():
    folder_path = entry_1.get()  # 폴더 경로 가져오기
    url = entry_2.get()  # URL 가져오기

    if folder_path == "" or folder_path == text_data[lang]["folder_index"]:
        messagebox.showerror("ERROR", text_data[lang]["folder_error_message"])
        return  

    if not url.startswith("https://www.hoyolab.com/article/"):
        messagebox.showerror("ERROR", text_data[lang]["url_error_message"])
        return  

    download_status = download_imgs(folder_path, url)
    if download_status == "Download ss":
        messagebox.showinfo("SUCCESS", text_data[lang]["success_message"])
    else:
        messagebox.showerror("ERROR", download_status)

def change_language(new_lang):
    global lang
    lang = new_lang
    # 언어 변경 후, 텍스트 갱신
    label.config(text=text_data[lang]["title"])
    # caution_label.config(text=text_data[lang]["caution"])
    step_label_1.config(text="STEP 1")
    step_label_2.config(text="STEP 2")
    step_label_3.config(text="STEP 3")
    entry_1.delete(0, tk.END)
    entry_1.insert(0, text_data[lang]["folder_index"])
    entry_2.delete(0, tk.END)
    entry_2.insert(0, text_data[lang]["url_index"])
    text_label_2.config(text=text_data[lang]["url_index_description"])
    download_button.config(text="Download")

window.title(text_data["EN"]["title"])
window.geometry(f"600x300+{screen_width//2-300}+{screen_height//2-150}")
window.resizable(False, False)

label = tk.Label(window, text=text_data[lang]["title"], font=("Noto Sans", 15, "bold"), pady=10)
label.pack()

frame_1 = tk.Frame(window)
frame_1.pack(anchor="w", padx=20, pady=(10, 0))

step_label_1 = tk.Label(frame_1, text="STEP 1", font=("Noto Sans", 8, 'bold'))
step_label_1.pack(side="left", padx=10)

entry_1 = tk.Entry(frame_1, width=67, fg="gray")
entry_1.insert(0, text_data[lang]["folder_index"])
entry_1.bind("<FocusIn>", lambda event: on_entry_click(text_data[lang]["folder_index"], entry_1))
entry_1.bind("<FocusOut>", lambda event: on_focus_out(text_data[lang]["folder_index"], entry_1))
entry_1.pack(side="left")

frame_2 = tk.Frame(window)
frame_2.pack(anchor="w", padx=20, pady=(10, 0))

step_label_2 = tk.Label(frame_2, text="STEP 2", font=("Noto Sans", 8, 'bold'))
step_label_2.pack(side="left", padx=10)

entry_2 = tk.Entry(frame_2, width=67, fg="gray")
entry_2.insert(0, text_data[lang]["url_index"])
entry_2.bind("<FocusIn>", lambda event: on_entry_click(text_data[lang]["url_index"], entry_2))
entry_2.bind("<FocusOut>", lambda event: on_focus_out(text_data[lang]["url_index"], entry_2))
entry_2.pack(side="left")

text_label_2 = tk.Label(window, text=text_data[lang]["url_index_description"], font=("Noto Sans", 8))
text_label_2.pack(anchor="w", padx=85, pady=(3))

# frame_3 수정: STEP 3과 버튼을 같은 행에 배치
frame_3 = tk.Frame(window)
frame_3.pack(padx=20, pady=(10, 0))

# STEP 3을 버튼 왼쪽에 배치
step_label_3 = tk.Label(frame_3, text="STEP 3", font=("Noto Sans", 8, 'bold'))
step_label_3.grid(row=0, column=0, padx=10, pady=5, sticky="w")  # STEP 3을 왼쪽에 배치

# 버튼 생성 부분 수정
download_button = tk.Button(frame_3, text="Download", font=("Noto Sans", 10, 'bold'), command=on_button_click, fg='green')
download_button.grid(row=0, column=1, pady=10, padx=10)  # 버튼을 STEP 3 옆에 배치

# caution_label = tk.Label(window, text=text_data[lang]["caution"], font=("Noto Sans", 8),fg='red', anchor="e")
# caution_label.pack()

# 언어 변경 버튼 (맨 아래에 배치, 왼쪽 정렬)
language_frame = tk.Frame(window)
language_frame.pack(side="bottom", pady=10, anchor="w")  # 왼쪽 정렬되도록 설정

languages_label = tk.Label(language_frame, text="Languages:", font=("Noto Sans", 8, 'bold'))
languages_label.pack(side="left", padx=10)

change_lang_en = tk.Button(language_frame, text="English", command=lambda: change_language("EN"))
change_lang_en.pack(side="left", padx=5)

change_lang_kr = tk.Button(language_frame, text="한국어", command=lambda: change_language("KR"))
change_lang_kr.pack(side="left", padx=5)

change_lang_zh = tk.Button(language_frame, text="中文", command=lambda: change_language("ZH"))
change_lang_zh.pack(side="left", padx=5)

made_by_label = tk.Label(language_frame, text="Made By ", font=("Noto Sans", 8), anchor="e")
made_by_label.pack(side="left", padx=(200,0))

github_link = tk.Label(language_frame, text="Aidengoldkr", fg="blue", cursor="hand2", font=("Noto Sans", 8))
github_link.pack(side="left", padx=(0.1,0))
github_link.bind("<Button-1>", open_github)

frame_3.grid_rowconfigure(0, weight=1)  # 첫 번째 행에 확장 비율 설정
frame_3.grid_rowconfigure(1, weight=1)  # 두 번째 행에 확장 비율 설정
frame_3.grid_columnconfigure(0, weight=1)  # 첫 번째 열에 확장 비율 설정

window.mainloop()
