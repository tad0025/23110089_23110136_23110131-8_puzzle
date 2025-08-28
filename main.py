import tkinter as tk
import random, time

# Lấy text
def get_text(value):
    return str(value) if value != "" else ""

# Lấy màu
def get_color(value):
    return colors[value - 1] if value != "" else empty_color

# Kiểm tra tính khả thi
def ktra_giai(btn):
    temp = [x for x in btn if x != ""]
    dem = 0
    for i in range(len(temp)):
        for j in range(i+1, len(temp)):
            if temp[i] > temp[j]: dem += 1
    return dem % 2 == 0

# Kiểm tra hai ô có cạnh nhau không
def canh_nhau(idx1, idx2):
    row1, col1 = divmod(idx1, 3)
    row2, col2 = divmod(idx2, 3)
    return (abs(row1 - row2) == 1 and col1 == col2) or (abs(col1 - col2) == 1 and row1 == row2)

# Xử lý khi nhấn nút
def button_click(idx):
    global buttons, buttons_goc, empty_pos, move_count
    if canh_nhau(idx, empty_pos):
        buttons[idx], buttons[empty_pos] = buttons[empty_pos], buttons[idx]
        buttons_goc[idx]['text'] = get_text(buttons[idx])
        buttons_goc[empty_pos]['text'] = get_text(buttons[empty_pos])
        buttons_goc[idx]['bg'] = get_color(buttons[idx])
        buttons_goc[empty_pos]['bg'] = get_color(buttons[empty_pos])
        empty_pos = idx

        move_count += 1
        move_label.config(text=f"Lượt: {move_count}")
        if buttons == [1, 2, 3, 4, 5, 6, 7, 8, ""]: restart_game()

def update_timer():
    if running:
        elapsed = int(time.time() - start_time)
        minutes, seconds = divmod(elapsed, 60)
        time_label.config(text=f"{minutes:02}:{seconds:02}")
        root.after(1000, update_timer)

def restart_game():
    global restart_btn, running
    running = False
    restart_btn = tk.Button(frame, text="Chơi lại", font=("Arial", 18, "bold"), bg="red", fg="white", command=start_game)
    restart_btn.place(relx=0.5, rely=0.5, anchor="center")

def start_game():
    global buttons, buttons_goc, empty_pos, colors, empty_color, start_time, running, move_count
    for widget in frame.winfo_children(): widget.destroy()
    move_count = 0
    move_label.config(text="Lượt: 0")
    time_label.config(text="00:00")
    start_time = time.time()
    running = True
    update_timer()

    buttons = [1, 2, 3, 4, 5, 6, 7, 8, ""]
    while True:
        random.shuffle(buttons)
        if ktra_giai(buttons): break
    buttons_goc = []
    empty_pos = buttons.index("")
    colors = ["#FFC0CB", "#ADD8E6", "#90EE90", "#FFD700", "#FFA07A", "#20B2AA", "#BA55D3", "#87CEEB"]
    empty_color = "lightgray"

    # Tạo nút
    for i in range(3):
        for j in range(3):
            index = i*3 + j
            btn = tk.Button(frame, text=get_text(buttons[index]), font=("Arial", 24), width=5, height=2, bg=get_color(buttons[index]), command=lambda idx=index: button_click(idx))
            btn.grid(row=i, column=j, sticky="nsew")
            buttons_goc.append(btn)
            
    # Căn đều các hàng và cột
    for i in range(3):
        frame.rowconfigure(i, weight=1)
        frame.columnconfigure(i, weight=1)
        
# Begin
root = tk.Tk()
root.title("8 ô chữ")
# icon = tk.PhotoImage(file="./image/icon.png")
# root.iconphoto(False, icon)

size = 400
x = (root.winfo_screenwidth() - size) // 2
y = (root.winfo_screenheight() - size) // 2
root.geometry(f"{size}x{size}+{x}+{y}")
root.resizable(False, False)

# Layout chính
main_frame = tk.Frame(root, bg="white")
main_frame.pack(expand=True, fill="both")

# Thanh thông tin trên cùng
top_frame = tk.Frame(main_frame, bg="white")
top_frame.pack(side="top", fill="x")

move_label = tk.Label(top_frame, text="Lượt: 0", font=("Arial", 12, "bold"), fg="black", bg="white")
move_label.pack(side="left", padx=20, pady=5)

time_label = tk.Label(top_frame, text="00:00", font=("Arial", 12, "bold"), fg="black", bg="white")
time_label.pack(side="right", padx=20, pady=5)

# Khung game bên dưới
frame = tk.Frame(main_frame, bg="blue")
frame.pack(expand=True, fill="both")

# Nút bắt đầu
start_btn = tk.Button(frame, text="Bắt đầu", font=("Arial", 18, "bold"),
                      bg="orange", fg="white", command=start_game)
start_btn.pack(expand=True)

root.mainloop()