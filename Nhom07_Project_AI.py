import tkinter as tk
from gc import enable

from tkinter import ttk

from stack_data.utils import frame_and_lineno
from win32comext.adsi.adsicon import ADS_RIGHT_GENERIC_ALL

# ====== MAIN WINDOW ======
root = tk.Tk()
root.title("Graph Search Algorithm Visualizer")
root.geometry("1220x880")

# ====== LAYOUT SETUP ======
root.grid_rowconfigure(0, weight= 1)
root.grid_columnconfigure(0, weight=0, minsize=200)
root.grid_columnconfigure(1, weight=3)  # frame_mid rộng hơn
root.grid_columnconfigure(2, weight=1, minsize=300)

# ----- LEFT PANE (Thuật toán) -----
frame_left = tk.Frame(root, bd=2, relief= "groove")
frame_left.grid(row= 0, column=0, sticky="nswe")
frame_left.grid_propagate(False)


label_algo = tk.Label(frame_left, text="CÁC THUẬT TOÁN", font=("Arial", 14, "bold"))
label_algo.grid(row=0, column=0, columnspan=2,pady=5)

algos = ["BFS", "DFS", "UCS", "DLS", "IDS",
         "Greedy Search", "A* Search",
         "Hill Climbing Search", "Beam Search"]

for i, algo in enumerate(algos, start=1):
    ttk.Button(frame_left, text=algo).grid(row=i, column=0, padx=6, pady=6, sticky="ew")


# ----- MIDDLE PANE (Chính) -----
frame_mid = tk.Frame(root, bd=2, relief="groove")
frame_mid.grid(row=0, column=1, sticky="nsew")

frame_mid.grid_columnconfigure(0, weight=0)
frame_mid.grid_columnconfigure(1, weight=1)

frame_graph = tk.Frame(frame_mid, bd=2, relief="sunken", bg="white")
frame_graph.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)



label_name = tk.Label(frame_mid,text="Tên thuật toán", font=("Arial", 14, "bold"))
label_name.grid(row =0, column=0, columnspan=2, padx=10, pady= 10)


labelStartNode = tk.Label(frame_mid, text="Start Node:", font=("Arial",20))
labelStartNode.grid(row= 2, column=0, padx=6, pady=6, sticky="w")
TxtboxStartNode = tk.Entry(frame_mid, font=("Arial", 12), width= 25)
TxtboxStartNode.grid(row=2, column=1, padx=6, pady=6, sticky="w")
labelGoalNode = tk.Label(frame_mid, text="Goal Node:", font=("Arial",20))
labelGoalNode.grid(row= 3, column=0, padx=6, pady=6, sticky="w")
TxtboxGoalNode = tk.Entry(frame_mid, font=("Arial", 12), width= 25)
TxtboxGoalNode.grid(row=3, column=1, padx=6, pady=6, sticky="w")

frame_buttons = tk.Frame(frame_mid)
frame_buttons.grid(row=4, column=0, columnspan=2, pady=10, sticky="w")

btnRun = tk.Button(frame_buttons, text="Run Algorithm", font=("Arial", 12), width=20, command=lambda: RunCode_window())
btnRun.pack(side="left", padx=5)

btnViewCode = tk.Button(frame_buttons, text="View Algorithm-Code", font=("Arial", 12), width=20, command=lambda: ViewCode_window())
btnViewCode.pack(side="left", padx=5)

def RunCode_window():
    # Tạo cửa sổ con
    new_win = tk.Toplevel(root)
    new_win.title("Run Code")
    new_win.geometry("1200x900")

    # Nội dung trong cửa sổ con
    lbl = tk.Label(new_win, text="Đây là cửa sổ mới", font=("Arial", 14))
    lbl.pack(pady=20)

    btn_close = tk.Button(new_win, text="Đóng", command=new_win.destroy)
    btn_close.pack()

def ViewCode_window():
    # Tạo cửa sổ con
    new_win = tk.Toplevel(root)
    new_win.title("View Code")
    new_win.geometry("1200x900")

    # Nội dung trong cửa sổ con
    lbl = tk.Label(new_win, text="Đây là cửa sổ mới", font=("Arial", 14))
    lbl.pack(pady=20)

    btn_close = tk.Button(new_win, text="Đóng", command=new_win.destroy)
    btn_close.pack()


# ----- RIGHT PANE (Log) -----
frame_right = tk.Frame(root, bd=2, relief="groove")
frame_right.grid(row=0, column=2, sticky="nswe")

LblLogHistory = tk.Label(frame_right, text="Log History", font=("Arial", 14, "bold"))
LblLogHistory.grid(row=1, column=0, columnspan=2, pady=5)
txtboxtHistory = tk.Text(frame_right, font=("Arial", 12), width= 40, height= 20)
txtboxtHistory.grid(row=2, column=0, columnspan=2, padx= 5, pady=5, sticky="nsew")
txtboxtHistory.insert("1.0", "Kết quả thuật toán...\nNode path: A → B → C")
txtboxtHistory.config(state="disabled")









root.mainloop()