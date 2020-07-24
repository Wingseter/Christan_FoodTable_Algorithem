from tkinter import *
import tkinter.ttk as ttk

root = Tk()
root.title("자리 배치 v1.0")
root.geometry("1480x820")

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
brain_frame.pack(side="bottom", fill="both", padx = 5, pady = (0, 10))
Label(brain_frame)

dest_path_txt = Entry(brain_frame)
dest_path_txt.pack(side="left", fill="x", expand = True, ipady = 4)
Button(brain_frame, text = "파일 불러오기").pack(side = "left", padx=(10, 0))
Button(brain_frame, text = "파일 내보내기", state="disable").pack(side = "left", padx = (10,100))

Button(brain_frame, text = "자동 생성 주사위").pack(side = "left", padx = 10)
Button(brain_frame, text = "최종 결정 및 저장").pack(side = "left", padx = 10)
progressbar = ttk.Progressbar(brain_frame, maximum=100, mode = "determinate")
progressbar.pack(side = "right", padx = 10)
 
  
# 메인창-> 우측 -> 히스토리
history_frame = LabelFrame(root, text="과거 히스토리", relief="solid", bd = 1, padx = 1, pady = 1)
history_frame.pack(side="right", fill="both", padx = 5, pady = 5)

# 히스토리 리스트 박스
history_scroll_bar = Scrollbar(history_frame)
history_scroll_bar.pack(side="right", fill="y")
history_date_list = Listbox(history_frame, selectmode="extended", height=30, yscrollcommand = history_scroll_bar.set)
history_scroll_bar.config(command=history_date_list.yview)
history_date_list.pack(side="top")

 
load_history_btn = Button(history_frame, text="불러오기", padx = 5, pady = 3, width = 7)
delete_history_btn = Button(history_frame, text="기록 삭제", padx = 5, pady = 3, width = 7)
load_history_btn.pack(side="top")
delete_history_btn.pack(side="top")

# 메인창-> 우측 -> 전채 학생 목록
all_frame = LabelFrame(root, text="전채 학생", relief="solid", bd = 1, padx = 1, pady = 1)
all_frame.pack(side="right", fill="both", padx = 5, pady = 5)

# 전체 학생 리스트 박스
all_scroll_bar = Scrollbar(all_frame)
all_scroll_bar.pack(side="right", fill="y")
all_student_list = Listbox(all_frame, selectmode="extended", height=30, yscrollcommand = all_scroll_bar.set)
all_scroll_bar.config(command=all_student_list.yview)
all_student_list.pack(side="top")

for i in range(1, 32):
    all_student_list.insert(END, str(i))

# 학생 추가 삭제
name_text = Entry(all_frame, width = 17)
grade_values = list(range(1,9))
grade_text = ttk.Combobox(all_frame, width = 14, height=8, values = grade_values)
grade_text.set("학년 선택")
church_text = Entry(all_frame, width = 17)
 
student_add_btn = Button(all_frame, text="학생 추가", padx = 5, pady = 3, width = 7)
student_del_btn = Button(all_frame, text="학생 삭제", padx = 5, pady = 3, width = 7)

Label(all_frame, text = "이름").pack(side="top")
name_text.pack(side="top")
Label(all_frame, text = "학년").pack(side="top")
grade_text.pack(side="top")
Label(all_frame, text = "교회").pack(side="top")
church_text.pack(side="top")
student_add_btn.pack(side="left")
student_del_btn.pack(side="right")

    
# 메인창-> 가운데측 -> 자리배치 가능한 목록
available_frame = LabelFrame(root, text="가능한 학생", relief="solid", bd = 1, padx = 1, pady = 1)
available_frame.pack(side="right", fill="both", padx = 5, pady = 5)

# 자리배치 가능한 학생 리스트 박스
available_scroll_bar = Scrollbar(available_frame)
available_scroll_bar.pack(side="right", fill="y")
available_student_list = Listbox(available_frame, selectmode="extended", height=30, yscrollcommand = available_scroll_bar.set)
available_scroll_bar.config(command=available_student_list.yview)
available_student_list.pack(side="top")

insert_stu_btn = Button(available_frame, text="학생 배치", padx = 5, pady = 3, width = 7)
insert_stu_btn.pack(side="top")


Label(available_frame, text = "선택된 테이블: ").pack(side="left")
Label(available_frame, text = "1").pack(side="left")
Label(available_frame, text = "번").pack(side="left")


# Todo 삭제
for i in range(1, 32):
    available_student_list.insert(END, str(i))
    

# 메인창->좌측->테이블 목록
##############################################################
# 스크롤 옵션
def scroll_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=2000,height=1800)
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

table_list = list()

# 테이블 목록들
for j in range(1, 33):

    # 테이블 목록 5개씩 1줄
    if j % 5 == 1:
        each_five_table = LabelFrame(t_frame, text = str(j) + "번 ~" + str(j + 4) + "번 테이블", relief="ridge")

        each_five_table.pack(side="top")
       


    listbox_temp = Listbox(each_five_table, selectmode="extended", height=7)
    
    # ToDo 총 테이블 개수마다
    for i in range(1, 8):
        listbox_temp.insert(END, str(i))

    select_table_btn = Button(each_five_table, text=str(j) +"번", width = "3")
    select_table_btn.pack(side="left", ipady="40")
    
    table_list.insert(j, listbox_temp)
    listbox_temp.pack(side="left", padx = (0,10))
    

root.resizable(False, False)
# print(len(table_list))
root.config(menu=menu)
root.mainloop()