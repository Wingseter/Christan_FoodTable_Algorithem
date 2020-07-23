from tkinter import *
import tkinter.ttk as ttk

root = Tk()
root.title("자리 배치 v1.0")
root.geometry("1080x720")

def menucmd1():
    print("menu command")

# 파일 불러오기
def add_file():
    pass

# 선택 삭제

# 상단 메뉴
menu = Menu(root)

# 메뉴->파일 
menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label="파일 불러오기", command=menucmd1)
menu_file.add_command(label="파일 내보내기", state="disable")
menu_file.add_command(label="끝내기", command = root.quit)
menu.add_cascade(label="파일", menu=menu_file)

# 메뉴->편집
menu_edit = Menu(menu, tearoff=0)
menu_edit.add_radiobutton(label = "op1")
menu_edit.add_radiobutton(label = "op2")
menu_edit.add_radiobutton(label = "op3")
menu.add_cascade(label="편집", menu=menu_edit)

# 메인창 ->하단-> 편집창
brain_frame = LabelFrame(root, text="권능", relief="solid", bd = 1, padx = 1, pady = 1)
brain_frame.pack(side="bottom", fill="both", padx = 5)
Button(brain_frame, text = "btn2").pack()
 

# 메인창-> 우측 -> 전채 학생 목록
all_frame = LabelFrame(root, text="전채 학생", relief="solid", bd = 1, padx = 1, pady = 1)
all_frame.pack(side="right", fill="both", padx = 5, pady = 5)

# 전체 학생 리스트 박스
all_student_list = Listbox(all_frame, selectmode="extended", height=50)

for i in range(1, 32):
    all_student_list.insert(END, str(i))
    
all_student_list.pack(side="left")

# 메인창-> 가운데측 -> 자리배치 가능한 목록
available_frame = LabelFrame(root, text="가능한 학생", relief="solid", bd = 1, padx = 1, pady = 1)
available_frame.pack(side="right", fill="both", padx = 5, pady = 5)

# 자리배치 가능한 학생 리스트 박스
available_student_list = Listbox(available_frame, selectmode="extended", height=50)

for i in range(1, 32):
    available_student_list.insert(END, str(i))
    
available_student_list.pack(side="left")


# 메인창->좌측->테이블 목록
##############################################################
# 스크롤 옵션
def scroll_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=1000,height=800)
##############################################################

table_frame=Frame(root,relief=GROOVE, bd=1, padx = 1, pady = 1)
table_frame.pack(side="right", fill="x", expand=True, padx = 5, pady = 5)

canvas=Canvas(table_frame)
t_frame=Frame(canvas)
table_scroll=Scrollbar(table_frame,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=table_scroll.set)

table_scroll.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((0,0),window=t_frame,anchor='nw')
t_frame.bind("<Configure>",scroll_configure)

# 테이블 목록들
for j in range(1, 33):
    # 테이블 목록 5개씩 1줄
    if j % 5 == 1:
        each_five_table = LabelFrame(t_frame, text = "test", relief="flat")
    listbox_temp = Listbox(each_five_table, selectmode="extended", height=10)

    # ToDo 총 테이블 개수마다
    for i in range(1, 32):
        listbox_temp.insert(END, str(i))
        
    listbox_temp.pack(side="left")
    each_five_table.pack(side="top")

# root.resizable(False, False)

root.config(menu=menu)
root.mainloop()