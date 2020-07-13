from tkinter import *

root = Tk()
root.title("자리 배치 v1.0")
root.geometry("1280x720")

def menucmd1():
    print("menu command")

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
 
# 메인창-> 좌측 -> 자리배치 가능한 목록
available_frame = LabelFrame(root, text="가능한 학생", relief="solid", bd = 1, padx = 1, pady = 1)
available_frame.pack(side="right", fill="both", padx = 5, pady = 5)
Button(available_frame, text = "btn2").pack()

# 메인창->우측->테이블 목록
table_frame = LabelFrame(root, text="테이블", relief="solid", bd = 1, padx = 1, pady = 1)
table_frame.pack(side="right", fill="both", expand=True, padx = 5, pady = 5)
Button(table_frame, text = "btn2").pack()



# root.resizable(False, False)

root.config(menu=menu)
root.mainloop()