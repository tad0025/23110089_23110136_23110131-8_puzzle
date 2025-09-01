import tkinter as tk
from idlelib.configdialog import font_sample_text
from tkinter import ttk
import random
from debugpy.common.sockets import close_socket
from win32cryptcon import dwFORCE_KEY_PROTECTION_USER_SELECT

root = tk.Tk()
root.title("Two 8x8 Boards - 8 Queens")      # Khởi tạo cửa sổ chính
root.geometry("1200x770")
root.rowconfigure(0, weight=1)     # cho phép stretch nếu cần
root.columnconfigure(0, weight=1)

main = ttk.Frame(root, padding= 8) #Container để giữ layout
main.grid(sticky="nsew")

#Tạo 2 bảng, Board A (trống) và Board B (Có sẵn)
left_side = ttk.LabelFrame(main, text ="Board A", padding = 6)
left_side.grid(row = 0, column=0, padx= 6, pady= 6)
right_side = ttk.LabelFrame(main, text ="Board B", padding = 6)
right_side.grid(row = 0, column=1, padx= 6, pady= 6)
# cho 2 cột tỉ lệ mở rộng nếu resize
main.columnconfigure(0, weight =1)
main.columnconfigure(1, weight =1)

#Cấu hình
TILE = 56
N = 8
BOARD = N * TILE

# Tạo 2 bảng 8x8
boardA = tk.Canvas(left_side, width = BOARD, height = BOARD, bg = "White")
boardA.grid(row = 0, column = 0)
boardB = tk.Canvas(right_side, width= BOARD, height=BOARD, bg = "White")
boardB.grid(row =0, column = 0)

rect_id_lf = [[None]*N for i in range(N)]
queen_id_lf = [[None]*N for i in range(N)]

rect_id_right = [[None]*N for i in range(N)]
queen_id_right = [[None]*N for i in range(N)]
## dùng cho board B (Có sẵn) dễ hiển thị: queen_cols_right[row] = col hoặc -1

queen_cols_right = [-1]*N


queens= [-1] *N

#khai báo cols để lưu cột đang bị hậu chiếm
cols= [0]*N

# khai báo cross1 để lưu đường chéo chính đang bị hậu chiếm

cross1 = [0] * (2*N-1)

# khai báo cross2 để lưu đường chéo phụ đang bị hậu chiếm
cross2 = [0] * (2*N-1)


#Vẽ lưới ô
for r in range(N):
    for c in range(N):
        x1 = c *TILE
        y1 = r *TILE
        x2 = x1 + TILE
        y2 = y1 + TILE
        color = "#EEEED2" if (r+c) % 2 == 0 else "#769656" # Lấy 2 maàu khác nhau
        rid= boardA.create_rectangle(x1,y1,x2,y2, fill = color, outline="")
        rect_id_lf[r][c] =rid
        boardA.addtag_withtag(f"l_{r}_{c}", rid)
        rid2= boardB.create_rectangle(x1,y1,x2,y2, fill= color, outline="")
        rect_id_right[r][c] =rid2
        boardB.addtag_withtag(f"l_{r}_{c}", rid2)

def BoardA_Click(event, row, col):
    #row,col xác định ô đã click
    if queen_id_lf[row][col] is None:
        cx = col*TILE + TILE//2
        cy = row*TILE + TILE//2
        qid= boardA.create_text(cx, cy, text="♛", font=("Arial", int(TILE*0.8)))
        queen_id_lf[row][col] =qid
    else:
        #Xóa queen
        boardA.delete(queen_id_lf[row][col])
        queen_id_lf[row][col] = None

# gán event cho mỗi ô (dùng tag để truyền row/col cố định trong lambda)
for r in range(N):
    for c in range(N):
        boardA.tag_bind(f"l_{r}_{c}", "<Button-1>", lambda e, rr = r, cc= c: BoardA_Click(e, rr, cc))

def draw_queens_inBoardB(sol):
    #Xóa taất cả queen cũ
    for r in range(N):
        for c in range(N):
            if queen_id_right[r][c] is not None:
                boardB.delete(queen_id_right[r][c])
                queen_id_right[r][c] = None

    #Vẽ mới
    for r,c in enumerate(sol):
        if c is not None and c >= 0:
            cx = c * TILE + TILE // 2
            cy = r * TILE + TILE // 2
            qid = boardB.create_text(cx, cy, text="♛", font=("Arial", int(TILE * 0.8)))
            queen_id_right[r][c] = qid

# ví dụ format đơn giản: "0,4,7,5,2,6,1,3" (mỗi phần tử là col index cho row tương ứng)
def parse_pos(s):
    # Loại space
    parts = s.strip().split(",")
    if len(parts) != N:
        raise ValueError("N phải là 8 số!!")
    cols= []
    for p in parts:
        p = p.strip()
        if p =="":
            cols.append(-1) # cho phép -1 nếu ô trống
        else:
            cols.append(int(p))
    return cols
# khi user bấm nút "Load", gọi parse_positions(input_text) rồi gán vào queen_cols_right, sau đó draw_queens_inBoardB(...)
ctrl = ttk.Frame(main,padding = 4)
ctrl.grid(row = 1, column= 0, columnspan=2, sticky="ew")


def load_entry():
    pass

def random_preset():
    pass

def clear_boards():
    for r in range(N):
        for c in range(N):
            if queen_id_right[r][c] is not None:
                boardB.delete(queen_id_right[r][c])
                queen_id_right[r][c] = None


def start_solve():
    # RESET trạng thái trước khi tìm
    for i in range(N):
        queens[i] = -1
        cols[i] = 0
    for i in range(2*N - 1):
        cross1[i] = 0
        cross2[i] = 0
    def dfs(row):
        if row == N:
            draw_queens_inBoardB(queens)  # vẽ lên board B
            return True # dừng lại sau 1 nghiệm

        for col in range(N):
            d1 = row - col + (N + 1)
            d2 = row + col
            # nếu cột hoặc đường chéo đã bị chiếm thì bỏ qua
            if cols[col] or cross1[d1] or cross2[d2]:
                continue

            queens[row]= col
            cols[col] = 1
            cross1[d1] = 1
            cross2[d2] = 1

            # đệ quy sang hàng tiếp theo; nếu tìm được nghiệm thì bubble up True để dừng
            if dfs(row + 1):
                return True

            # backtrack: bỏ đặt
            queens[row] = -1
            cols[col] = 0
            cross1[d1] = 0
            cross2[d2] = 0
        return False
    dfs(0)


btnClear = ttk.Button(ctrl, text="Clear board", width=50, command=lambda : clear_boards())
btnClear.pack(expand=True, padx=6, pady=6)
btnStart = ttk.Button(ctrl, text="Solve", width=50, command=lambda :start_solve())
btnStart.pack(expand=True, padx=6, pady=6)

root.mainloop()
