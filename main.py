from tkinter import Tk, Menu, PhotoImage, Label, Frame, LabelFrame, Button, Entry, Scrollbar, Listbox, GROOVE, Canvas, END
import tkinter.ttk as ttk
import sqlite3
import openpyxl
import random
import tkinter.messagebox as msgbox
from tkinter import filedialog
import copy

root = Tk()

root.title("자리 배치 v1.3-beta")
root.geometry("1480x750")



##################################################################################################################################################
##################################################################################################################################################
# 변수 목록
##################################################################################################################################################
##################################################################################################################################################

student = list() # 전체 학생
available_student = list() # 가능한 학생
count_grade = list() # 각 학년의 학생수
table_list_box = list() # 테이블 전체 리스트 박스 모음
all_table = list()  # 모든 테이블 전체 데이터
is_student_loaded = False # 학생 로딩
all_grade = list() # 모든 학년
table_list_frame = list() # 테이블 리스트 박스 프레임
table_list_btn = list() # 테이블 리스트 박스 버튼

# DB 연결 목록
dbpath = "foodTable.db"
conn = sqlite3.connect(dbpath)
cur = conn.cursor()

# 백업
super_backup_student = list()
super_backup_count_grade = list()
super_backup_all_table = list()
super_backup_all_grade = list()

##################################################################################################################################################
##################################################################################################################################################
# 기타 기능 모음  #################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################

# 모두 초기화
def reset_all():
    count_grade.clear
    clear_available_student_list()
    clear_all_student_list()
    for btn in table_list_btn:
        btn.pack_forget()
    for frame in table_list_frame:
        frame.pack_forget()
    for table_list in table_list_box:
        table_list.delete(0, END)
    for listbox in table_list_box:
        listbox.pack_forget()

    table_list_btn.clear
    table_list_frame.clear
    table_list_box.clear

    student.clear
    available_student.clear
    for grade in all_grade:
        grade.clear
    all_grade.clear

    selected_table.configure(text="?")


# 학생이 있는가??
def insert_student_first():
    if(len(student) == 0):
        msgbox.showinfo("작업 실패", "작업할 학생이 없습니다")
        return 0
    else:
        return 1

# 테이블을 선택 했는가?
def select_table_first():
    if(selected_table.cget("text") == "?"):
        msgbox.showinfo("작업 실패", "테이블을 먼저 선택하세요")
        return 0
    else:
        return 1

# 전체 학생 삭제
def clear_all_student_list():
    all_student_list.delete(0, END)
    student.clear()

# 가능한 학생 삭제
def clear_available_student_list():
    available_student_list.delete(0, END)


def available_student_insert():
    if insert_student_first() == 0:
        return
    if select_table_first() == 0:
        return
    student
    all_table
    count_grade
    all_grade

    table_num = int(selected_table.cget("text")) - 1
    # 예외 처리
    if table_list_box[table_num].size() > 6:
        msgbox.showinfo("배치 불가", "7명이 넘었어요!")
        return
    student_selected = available_student_list.curselection()[0]
    insert = available_student_list.get(student_selected)
    table_list_box[table_num].insert(END, insert)

    index = all_student_list.get(0, END).index(insert)

    # 카운터 업데이트
    grade_selection = student[index]['grade']
    count_grade[grade_selection - 1] -= 1
    for i, grade in enumerate(all_grade[grade_selection - 1]):
        if student[index]['id'] == grade['id']:
           all_grade[grade_selection-1].pop(i)

    all_table[table_num].append(student.pop(index))
    all_student_list.delete(index)

    available_student_action()

# 강제 삽입
def force_student_insert():
    pass

def clear_table():
    table_num = int(selected_table.cget("text")) - 1
    table_list_box[table_num].delete(0, END)

#  색상 학년 변환기
def ColorConvert(color_hex):
    color_dic = {
        'FFCBCBFF': 1,  # 연보라
        'FFD8FFD8': 2,  # 연초록
        'FFFFFFCB': 3,  # 연노랑
        'FFFFDEB2': 4,  # 연주황
        'FFFFCBCB': 5,  # 연빨강
        '00000000': 6,  # 하양
        'FFFFD8FF': 7,  # 핑크
        'FFFFFFFF': 6,  # 엑셀 실수 방지용 하얀색
        'FFFF0000': 8   # 간부만 쓸수 있는 빨강색
    }
    picked = color_dic[color_hex]
    if not str(picked).isdigit:
        msgbox.showinfo("엑셀 오류", "엑셀 색상을 수정하고 다시 실행하세요")
        picked = 8
    return picked

def add_file_dialog():
    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요", \
        filetype=(("Excel 파일", "*.xlsx"), ("모든 파일", "*.*")), \
        initialdir="C:/")
    return files
##################################################################################################################################################
##################################################################################################################################################
# SQL Collection #################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################


# 학생 테이블 만들기
studentTableCreateSql = ("""
    CREATE TABLE IF NOT EXISTS student(
        "id" INTEGER,
        "name" TEXT,
        "church" TEXT,
        "grade" INTEGER,
        PRIMARY KEY("id" AUTOINCREMENT)
    )
""")

# 자리 테이블 만들기
seatTableCreateSql = ("""
    CREATE TABLE IF NOT EXISTS seat(
        "id" INTEGER,
        "date" INTEGER,
        "seat" INTEGER,  
        "stu_id" INTEGER,
        PRIMARY KEY("id" AUTOINCREMENT)
    )
""")

# 날자 저장 테이블 만들기
dateTableCreateSql = ("""
    CREATE TABLE IF NOT EXISTS date(
        "id" INTEGER,
        "date" TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
    )
""")

# 학생 입력하기
stuInsertSql = ("""
    INSERT INTO student(name , grade, church)
    SELECT ?, ?, ?
    WHERE NOT EXISTS(SELECT 1 FROM student WHERE name = ? AND grade = ? AND church = ?);
""")

# id 가져오기
idSearchSql = ("""
    SELECT id FROM student WHERE name = ? AND grade = ? AND church = ?
""")


# 자리 추가
seatInsertSql = ("""
INSERT INTO seat(date ,seat, stu_id)
VALUES(?, ?, ?);
""")

# 자리 빼기
deleteInsertSql = ("""
DELETE FROM seat WHERE date = ? AND seat = ? AND stu_id = ?
""")

# 과거 같이 했던 사람들 찾기
pastSearchSql = ("""
SELECT stu_id FROM seat WHERE (seat.date, seat.seat) IN (
    SELECT date, seat FROM seat WHERE stu_id = ? 
);
""")

# 날짜 저장 
createDateSql = ("""
INSERT INTO date(date)
SELECT ?
WHERE NOT EXISTS(SELECT 1 FROM date WHERE date = ?);
""")

# 날짜의 ID 찾기
getDateIdSql = ("""
SELECT id FROM date WHERE date = ?
""")

# 모든 날짜 반환
getAllDateSql = ("""
SELECT date FROM date
""")

# 해당 날짜의 모든 자리 목록 불러오기
# getStudentInDateSql=("""
# SELECT seat.seat, student.id, name, grade, church FROM seat INNER JOIN student on seat.stu_id = student.id WHERE student.id = (
#     SELECT stu_id FROM seat WHERE seat.date = (
#         SELECT id FROM date WHERE date = ?
#     )
# );
# """)
getStudentInDateSql=("""
    SELECT seat, student.id, name, grade, church FROM student LEFT OUTER JOIN seat ON student.id = seat.stu_id WHERE seat.date = 
        (SELECT id FROM date WHERE date = ?);
""")

# 해당 날짜의 모든 데이터 삭제하기
deleteAllDateInfoSql=("""
DELETE FROM seat WHERE seat.date IN
(SELECT id FROM date WHERE date = ?);
""")

# 해당 날짜 삭제하기
deleteDateInfoSql=("""
DELETE FROM date WHERE date = ?
""")

cur.executescript(studentTableCreateSql)

cur.executescript(seatTableCreateSql)

cur.executescript(dateTableCreateSql)


# 데이터 저장하기
def save_seat_to_db():
    all_table

    save_date = save_date_txt.get()
    if save_date == "":
        msgbox.showinfo("어라라?", "저장할 이름 입력 안했눈뎅")
        return

    cur.execute(getDateIdSql, (save_date,))
    find = cur.fetchall()

    if len(find) != 0:
        msgbox.showinfo("중복 불가", "이미 존재하는 이름입니다.")
        return

    cur.execute(createDateSql, (save_date, save_date))
    cur.execute(getDateIdSql, (save_date,))
    date_id = cur.fetchall()

    for i, table in enumerate(all_table): 
        for people in table:
            cur.execute(seatInsertSql, (date_id[0][0], i+1, people['id'][0]))

    history_date_list.insert(END, save_date)
    conn.commit()

# 데이터 불러오기
def load_seat_from_db():
    select = history_date_list.get(history_date_list.curselection())
    cur.execute(getStudentInDateSql, (select,))
    stu_data = cur.fetchall()

    if len(student) != 0:
        answer = msgbox.askquestion("초기화 경고", "모든 데이터가 날라갑니다. 정말로 불러올까요?")

        if answer == 'no':
            return

    reset_all()
    for stu in stu_data:
        student.append({'id': stu[1], 'Name': stu[2], 'grade': stu[3], 'church': stu[4]})
    
    all_grade

    grade_1 = list() # 1학년
    grade_2 = list() # 2학년
    grade_3 = list() # 3학년
    grade_4 = list() # 4학년
    grade_5 = list() # 5학년
    grade_6 = list() # 6학년
    grade_7 = list() # 7학년
    grade_8 = list() # 간부

    # 학년별로 분류
    for item in student:
        if item['grade'] == 1:
            grade_1.append(item)
        elif item['grade'] == 2:
            grade_2.append(item)
        elif item['grade'] == 3:
            grade_3.append(item)
        elif item['grade'] == 4:
            grade_4.append(item)
        elif item['grade'] == 5:
            grade_5.append(item)
        elif item['grade'] == 6:
            grade_6.append(item)
        elif item['grade'] == 7:
            grade_7.append(item)
        elif item['grade'] == 8:
            grade_8.append(item)
        else:
            print("error")

    all_grade.append(grade_1)
    all_grade.append(grade_2)
    all_grade.append(grade_3)
    all_grade.append(grade_4)
    all_grade.append(grade_5)
    all_grade.append(grade_6)
    all_grade.append(grade_7)
    all_grade.append(grade_8)

    for i, grade in enumerate(all_grade):
        count_grade.append(len(grade))
    # 테이블 개수
    table_count = max(count_grade)

    # 테이블 분류
    all_table

    for count in range(table_count):
        all_table.append(list())

    table_list_box
    table_list_frame
    table_list_btn

    # 테이블 목록들
    for j in range(1, table_count+1):

        # 테이블 목록 5개씩 1줄
        if j % 5 == 1:
            each_five_table = LabelFrame(t_frame, text=str(
                j) + "번 ~" + str(j + 4) + "번 테이블", relief="ridge")

            each_five_table.pack(side="top")
            table_list_frame.append(each_five_table)

        listbox_temp = Listbox(
            each_five_table, selectmode="extended", height=7)

        select_table_btn = Button(
            each_five_table, text=str(j) + "번", width="3")
        select_table_btn.configure(command=lambda button=select_table_btn: table_button_action(button))
        select_table_btn.pack(side="left", ipady="40")
        table_list_btn

        table_list_box.insert(j, listbox_temp)
        listbox_temp.pack(side="left", padx=(0, 10))
    
    # 테이블에 집어넣기
    for stu in stu_data:
        temp = student.pop(0)
        table_list_box[stu[0] - 1].insert(END, str(temp['grade']) + "/" +temp['Name'] + "/"+ temp['church'])
    
    for grade in all_grade:
        grade.clear()
    student.clear()
    all_grade.clear()

    

# 데이터 삭제하기
def delete_history():
    select = history_date_list.get(history_date_list.curselection())
    history_date_list.delete(history_date_list.curselection())
    cur.execute(deleteAllDateInfoSql, (select,))
    cur.execute(deleteDateInfoSql, (select,))
    conn.commit()
    
# def edit_history():
#     pass

##################################################################################################################################################
##################################################################################################################################################
# 엑셀 데이터 불러오기 ############################################################################################################################
##################################################################################################################################################
##################################################################################################################################################

def load_excel_data():
    if len(student) != 0:
        answer = msgbox.askquestion("초기화 경고", "모든 데이터가 날라갑니다. 파일을 새로 로딩할까요?")

        if answer == 'yes':
            reset_all()
            load_excel_data()
            return
    else:
        reset_all()
    
    filename = add_file_dialog()

    if filename == "":
        return
    dest_path_txt.delete(0, END)
    dest_path_txt.insert(0, str(filename[0]))
    std_book = openpyxl.load_workbook(str(filename[0]), read_only=True)

    std_sheet = std_book.worksheets[0]

    clear_all_student_list()
    student

    # 시트의 각행 순서대로 추출해서 추가
    for i, row in enumerate(std_sheet.iter_rows()):
        if i == 0:
            continue
        for cell in row:
            original_text = str(cell.value)
            if original_text == "None" or cell.fill is None:
                continue
            if original_text.find('(') == -1:
                name = original_text
                church = "없음"
            else:
                name = original_text[:original_text.find('(')]
                church = original_text[original_text.index(
                    '(')+1:original_text.index(')')]

            grade = ColorConvert(cell.fill.start_color.index)
            cur.execute(stuInsertSql, (name, grade, church, name, grade, church))

            # 바로 데이터 가져오기
            cur.execute(idSearchSql, (name, grade, church))
            stu_id = cur.fetchall()
            student.append(
                {'id': stu_id[0], 'Name': name, 'grade': grade, 'church': church})

    for stu in student:
        all_student_list.insert(END, str(stu['grade']) + "/" +stu['Name'] + "/"+ stu['church'])

    all_grade

    grade_1 = list() # 1학년
    grade_2 = list() # 2학년
    grade_3 = list() # 3학년
    grade_4 = list() # 4학년
    grade_5 = list() # 5학년
    grade_6 = list() # 6학년
    grade_7 = list() # 7학년
    grade_8 = list() # 7학년

    # 학년별로 분류
    for item in student:
        if item['grade'] == 1:
            grade_1.append(item)
        elif item['grade'] == 2:
            grade_2.append(item)
        elif item['grade'] == 3:
            grade_3.append(item)
        elif item['grade'] == 4:
            grade_4.append(item)
        elif item['grade'] == 5:
            grade_5.append(item)
        elif item['grade'] == 6:
            grade_6.append(item)
        elif item['grade'] == 7:
            grade_7.append(item)
        elif item['grade'] == 8:
            grade_7.append(item)
        else:
            print("error")

    all_grade.append(grade_1)
    all_grade.append(grade_2)
    all_grade.append(grade_3)
    all_grade.append(grade_4)
    all_grade.append(grade_5)
    all_grade.append(grade_6)
    all_grade.append(grade_7)

    for i, grade in enumerate(all_grade):
        count_grade.append(len(grade))
    # 테이블 개수
    table_count = max(count_grade)

    # 테이블 분류
    all_table

    for count in range(table_count):
        all_table.append(list())

    table_list_box
    table_list_frame
    table_list_btn

    # 테이블 목록들
    for j in range(1, table_count+1):

        # 테이블 목록 5개씩 1줄
        if j % 5 == 1:
            each_five_table = LabelFrame(t_frame, text=str(
                j) + "번 ~" + str(j + 4) + "번 테이블", relief="ridge")

            each_five_table.pack(side="top")
            table_list_frame.append(each_five_table)

        listbox_temp = Listbox(
            each_five_table, selectmode="extended", height=7)

        select_table_btn = Button(
            each_five_table, text=str(j) + "번", width="3")
        select_table_btn.configure(command=lambda button=select_table_btn: table_button_action(button))
        select_table_btn.pack(side="left", ipady="40")
        table_list_btn

        table_list_box.insert(j, listbox_temp)
        listbox_temp.pack(side="left", padx=(0, 10))
    conn.commit()
####################################################################################################################################################
####################################################################################################################################################
# 가능한 학생 계산기#################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################

# 과거의 중복이 되었나?
def timeMachine(stuHash, table, students):
    for member in table: # for-1
        cur.execute(pastSearchSql, (member['id'][0],))
        past_db_list = cur.fetchall()

        for past in past_db_list: # for-2
            for stu in students: # for-3
                try:
                    if stu['grade'] == 8:
                        pass
                    elif stu['id'][0] == past[0]:
                        stuHash.remove(past[0])
                except Exception:
                    continue
    return stuHash

# 같은 학년인가?
def gradeChecker(stuHash, table, students):
    for stu in students:
        for member in table:
            try:
                if stu['grade'] == 8:
                    pass
                elif stu['grade'] == member['grade']:
                    stuHash.remove(stu['id'][0])
            except Exception:
                continue

    return stuHash

# 같은 교회 출신인가
def churchChecker(stuHash, table, students):
    for stu in students:
        for member in table:
            if stu['grade'] == 8:
                pass
            elif stu['church'] == member['church']:
                try:
                    stuHash.remove(stu['id'][0])
                except Exception:
                    continue
    return stuHash

# 가능한 모든 학생을 반환
def availableStudent(table, student):
    stuHash = list()
    for it in student:
        stuHash.append(it['id'][0])
    assert(len(stuHash) == len(student))
    churchChecker(stuHash, table, student)
    gradeChecker(stuHash, table, student)
    timeMachine(stuHash, table, student)
    return stuHash


def table_button_action(button):
    student
    all_table

    table_num = button.cget("text")
    table_num = table_num[:table_num.index("번")]
    selected_table.configure(text=table_num)
    available = availableStudent(all_table[int(table_num)-1], student)
    
    clear_available_student_list()
    for stu in student:
        for pick in available: 
            if stu['id'][0] == pick:
                available_student_list.insert(END, str(stu['grade']) + "/" +stu['Name'] + "/"+ stu['church'])

def available_student_action():
    student
    number = int(selected_table.cget("text")) -1
    available = availableStudent(all_table[number], student)
    clear_available_student_list()
    for stu in student:
        for pick in available: 
            if stu['id'][0] == pick:
                available_student_list.insert(END, str(stu['grade']) + "/" +stu['Name'] + "/"+ stu['church'])

def menucmd1():
    print("menu command")


def backup_precess():
    clear_available_student_list()
    clear_all_student_list()
    global table_list_box
    
    for table_list in table_list_box:
        table_list.delete(0, END)


    global student
    global count_grade
    global all_table
    global all_grade
    global super_backup_all_grade
    global super_backup_student
    global super_backup_all_table
    global super_backup_count_grade

    available_student.clear
    student.clear
    count_grade.clear
    all_table.clear
    all_grade.clear

    student = copy.deepcopy(super_backup_student)
    count_grade = copy.deepcopy(super_backup_count_grade)
    all_table = copy.deepcopy(super_backup_all_table)
    all_grade = copy.deepcopy(super_backup_all_grade)

    for stu in student:
        all_student_list.insert(END, str(stu['grade']) + "/" +stu['Name'] + "/"+ stu['church'])

    for i, table in enumerate(all_table):
        for stu in table:
            table_list_box[i].insert(END, str(stu['grade']) + "/" +stu['Name'] + "/"+ stu['church'])

# 자동 편성 주사위
def super_seat_dice_rolling():
    if insert_student_first() == 0:
        return
    count_grade
    student
    table_list_box
    all_table
    all_grade
    global super_backup_all_table
    global super_backup_all_grade
    global super_backup_student
    global super_backup_count_grade
    
    super_backup_all_table = copy.deepcopy(all_table)
    super_backup_count_grade = copy.deepcopy(count_grade)
    super_backup_student = copy.deepcopy(student)
    super_backup_all_grade = copy.deepcopy(all_grade)

    
    # 모든 테이블에 돌아가면서
    for table_num, each_table in enumerate(all_table):
        if count_grade.count(max(count_grade)) == 7:
            number_in_table =7
        elif max(count_grade) - min(count_grade) >= 5: 
            number_in_table =5
        else:
            number_in_table = 6 

        # 학년 중복 방지용
        no_duplicater = [1,2,3,4,5,6,7]

        # 기존 입력 학생 중복 방지
        for stu in each_table:
            no_duplicater.pop(no_duplicater.index(stu['grade']))

        if len(student) == 0 or max(count_grade) == 0:
            break
        # 각 테이블 자리를 채운다
        for i in range(int(number_in_table-len(each_table))):
            max_finder = list()
            # 학년 중복 방지용
            for pin in no_duplicater:
                max_finder.append(count_grade[pin - 1])
            grade_to_insert = no_duplicater.pop(max_finder.index(max(max_finder)))

            
            grade_pick = all_grade[grade_to_insert - 1]

            if not grade_pick:
                return

            available_search = availableStudent(each_table, grade_pick)

            if (len(available_search) == 0):
                print(all_grade)
                backup_precess()
                super_seat_dice_rolling()
                return

            random_pick = available_search[random.randint(0,len(available_search)-1)]

            for stu in student:
                if stu['id'][0] == random_pick:
                    pick = str(stu['grade']) + "/" +stu['Name'] + "/"+ stu['church']
                    index = all_student_list.get(0, END).index(pick)
                    # 카운터 업데이트
                    grade_selection = student[index]['grade']
                    count_grade[grade_selection - 1] -= 1
                    for k, grade in enumerate(all_grade[grade_selection -1]):
                        if student[index]['id'] == grade['id']:
                            all_grade[grade_selection-1].pop(k)
                    # 리스트 박스 업데이트
                    table_list_box[table_num].insert(END, pick)
                    each_table.append(student.pop(index))
                    all_student_list.delete(index)
    clear_available_student_list()
 

    


##################################################################################################################################################
##################################################################################################################################################
# 그래픽 관련 코드#################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
menu = Menu(root)

fondo = PhotoImage(file="background.png")
background_label = Label(root, image=fondo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


# 메뉴->파일
menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label="파일 불러오기", command=load_excel_data)
menu_file.add_command(label="파일 내보내기", state="disable")
menu_file.add_command(label="끝내기", command=root.quit)
menu.add_cascade(label="파일", menu=menu_file)

def show_maker():
    msgbox.showinfo("프로그램 정보", "자리배치 ver 1.3\n CopyRight(c) 2020 Wingseter and 전태영 All Right Reserved")

# 메뉴->편집
menu_edit = Menu(menu, tearoff=0)
menu_edit.add_command(label="프로그램 정보", command=show_maker)
menu.add_cascade(label="도움말", menu=menu_edit)

# 메인창 ->하단-> 편집창
brain_frame = LabelFrame(
    root, text="권능", relief="solid", bd=1, padx=1, pady=1)
brain_frame.pack(side="bottom", fill="both", padx=5, pady=(0, 10))
Label(brain_frame)

dest_path_txt = Entry(brain_frame)
dest_path_txt.pack(side="left", fill="x", expand=True, ipady=4)
Button(brain_frame, text="파일 선택", command=load_excel_data).pack(side="left", padx=(10, 0))
Button(brain_frame, text="파일 내보내기", state="disable").pack(
    side="left", padx=(10, 100))

Button(brain_frame, text="자동 생성 주사위" , command=super_seat_dice_rolling).pack(side="left", padx=10)
progressbar = ttk.Progressbar(
    brain_frame, maximum=100, mode="determinate")
progressbar.pack(side="right", padx=10)

# 메인창-> 우측 -> 히스토리
history_frame = LabelFrame(
    root, text="과거 히스토리", relief="solid", bd=1, padx=1, pady=1)
history_frame.pack(side="right", fill="both", padx=5, pady=5)

# 히스토리 리스트 박스
history_scroll_bar = Scrollbar(history_frame)
history_scroll_bar.pack(side="right", fill="y")
history_date_list = Listbox(
    history_frame, selectmode="extended", height=30, yscrollcommand=history_scroll_bar.set)
history_scroll_bar.config(command=history_date_list.yview)
history_date_list.pack(side="top")

save_date_txt = Entry(history_frame)
save_date_txt.pack(side="top", ipady= 2)
Button(history_frame, text="최종 결정 및 저장", command=save_seat_to_db).pack(side="top", padx=10)

load_history_btn = Button(
    history_frame, text="불러오기", width=7, command = load_seat_from_db)
delete_history_btn = Button(
    history_frame, text="기록 삭제", width=7, command = delete_history)
# edit_history_btn = Button(
#     history_frame, text="수정하기", width=7, command = edit_history)
load_history_btn.pack(side="top", padx=5, pady=(10, 3))
delete_history_btn.pack(side="top", padx=5, pady=3, )
# edit_history_btn.pack(side="top", padx = 5, pady = 4,)

# 히스토리 창 초기화
cur.execute(getAllDateSql)
date_list = cur.fetchall()
for date in date_list:
    history_date_list.insert(END, date[0])

# 메인창-> 우측 -> 전채 학생 목록
all_frame = LabelFrame(
    root, text="남은 전채 학생", relief="solid", bd=1, padx=1, pady=1)
all_frame.pack(side="right", fill="both", padx=5, pady=5)

# 전체 학생 리스트 박스
all_scroll_bar = Scrollbar(all_frame)
all_scroll_bar.pack(side="right", fill="y")
all_student_list = Listbox(
    all_frame, selectmode="extended", height=40, yscrollcommand=all_scroll_bar.set)
all_scroll_bar.config(command=all_student_list.yview)
all_student_list.pack(side="top")

# student_add_btn = Button(
#     all_frame, text="강제 삽입", padx=5, pady=3, width=7, command=force_student_insert)
# student_add_btn.pack()


# 메인창-> 가운데측 -> 자리배치 가능한 목록
available_frame = LabelFrame(
    root, text="가능한 학생", relief="solid", bd=1, padx=1, pady=1)
available_frame.pack(side="right", fill="both", padx=5, pady=5)

# 자리배치 가능한 학생 리스트 박스
available_scroll_bar = Scrollbar(available_frame)
available_scroll_bar.pack(side="right", fill="y")
available_student_list = Listbox(
    available_frame, selectmode="extended", height=30, yscrollcommand=available_scroll_bar.set)
available_scroll_bar.config(command=available_student_list.yview)
available_student_list.pack(side="top")

insert_stu_btn = Button(
    available_frame, text="학생 배치", padx=5, pady=3, width=7, command=available_student_insert)
insert_stu_btn.pack(side="top")

Label(available_frame, text="선택된 테이블: ").pack(side="left")
selected_table = Label(available_frame, text="?")
selected_table.pack(side="left")
Label(available_frame, text="번").pack(side="left")


# 메인창->좌측->테이블 목록
##############################################################
# 스크롤 옵션

def scroll_configure(event):
    canvas.configure(scrollregion=canvas.bbox(
        "all"), width=2000, height=1800)
##############################################################

table_frame = Frame(root, relief=GROOVE, bd=1, padx=1, pady=1)
table_frame.pack(side="right", fill="x", expand=True, padx=5, pady=5)

canvas = Canvas(table_frame)
t_frame = Frame(canvas)
table_scroll = Scrollbar(
    table_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=table_scroll.set)

table_scroll.pack(side="right", fill="y")
canvas.pack(side="left")
canvas.create_window((0, 0), window=t_frame, anchor='nw')
t_frame.bind("<Configure>", scroll_configure)



##################################################################################################################################################
##################################################################################################################################################
# 그래픽 관련 코드 끝 #################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################

root.config(menu=menu)

root.mainloop()

conn.commit()
conn.close()


