import sqlite3
import openpyxl

# sqlite 데이터베이스 연결하기
dbpath = "foodTable.db"
conn = sqlite3.connect(dbpath)

# 테이블 생성하고 데이터 넣기
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS student(
    stu_id INTERGER PRIMARY KEY,
    name TEXT,
    church TEXT,
    grade INTEGER
)
""")

all_grade = list()
count_grade = list()

grade_1 = list()
grade_2 = list()
grade_3 = list()
grade_4 = list()
grade_5 = list()
grade_6 = list()
grade_7 = list()


# TODO: 엑셀에서 가져올 것이다
filename = "명부샘플.xlsx"
std_book = openpyxl.load_workbook(filename, read_only=True)
std_sheet = std_book.worksheets[0]

#  색상 학년 변환기
def ColorConvert(color_hex):
    color_dic = {
        'FFCBCBFF': 1, #연보라
        'FFD8FFD8': 2, #연초록
        'FFFFFFCB': 3, #연노랑
        'FFFFDEB2': 4, #연주황
        'FFFFCBCB': 5, #연빨강
        '00000000': 6, #하양
        'FFFFD8FF': 7, #핑크
        'FFFFFFFF': 6
    }
    return(color_dic[color_hex])

student = list()

# 시트의 각행 순서대로 추출해서 추가
for i, row in enumerate(std_sheet.iter_rows()):
    if i == 0:
        continue
    for cell in row :
        original_text = str(cell.value)
        if original_text == "None" or cell.fill is None:
            continue
        if original_text.find('(') == -1:
            name = original_text
            church = "없음"
        else:
            name = original_text[:original_text.find('(')]
            church = original_text[original_text.index('(')+1:original_text.index(')')]
        
        grade = ColorConvert(cell.fill.start_color.index) 
        student.append({'Name': name, 'grade': grade, 'church': church})

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
    else:
        print("error")

all_grade.append(grade_1)
all_grade.append(grade_2)
all_grade.append(grade_3)
all_grade.append(grade_4)
all_grade.append(grade_5)
all_grade.append(grade_6)
all_grade.append(grade_7)

for i, item in enumerate(all_grade):
    count_grade.append(len(item))

# 테이블 개수
table_count = max(count_grade)

# 테이블 분류
all_table = list()
for table in range(table_count):
    all_table.append(list())

# TODO 삭제
all_table[0].append(student[0])
all_table[0].append(student[1])
all_table[0].append(student[2])
all_table[1].append(student[3])
all_table[1].append(student[4])
all_table[2].append(student[5])
print(all_table[0])
print(all_table[1])
print(all_table[2])

conn.close()