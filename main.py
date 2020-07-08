import sqlite3
import openpyxl
import random

# sqlite 데이터베이스 연결하기
dbpath = "foodTable.db"
conn = sqlite3.connect(dbpath)

# 테이블 생성하고 데이터 넣기
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS student(
	"id" INTEGER,
	"name" TEXT,
	"church" TEXT,
	"grade" INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
)
""")

cur.executescript("""
CREATE TABLE IF NOT EXISTS student(
	"id" INTEGER,
	"date" TEXT,
	"stu_id" INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
)
""")




all_grade = list()

grade_1 = list()
grade_2 = list()
grade_3 = list()
grade_4 = list()
grade_5 = list()
grade_6 = list()
grade_7 = list()

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

stuInsertSql = ("""
INSERT INTO student(name , grade, church)
SELECT ?, ?, ?
WHERE NOT EXISTS(SELECT 1 FROM student WHERE name = ? AND grade = ? AND church = ?);
""")

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
        cur.execute(stuInsertSql, (name, grade, church, name, grade, church))
        student.append({'Name': name, 'grade': grade, 'church': church})

conn.commit()

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

count_grade = list()

for i, grade in enumerate(all_grade):
    count_grade.append(len(grade))
# 테이블 개수
table_count = max(count_grade)

# 테이블 분류
all_table = list()
for count in range(table_count):
    all_table.append(list())

# TODO db로 대체
past = list()

# 과거의 중복이 되었나?
def timeMachine(stuHash, students):

    return list()

# 같은 교회 출신인가
def churchChecker(stuHash, table, students):
    assert(len(stuHash) == len(students))
    tempList = stuHash[:]
    for i, student in zip(tempList, students):
        for member in table:
            if student['church'] == member['church']:
                stuHash.pop(i)

    return stuHash

# 가능한 모든 학생을 반환
def availableStudent(table, student):
    stuHash = list()
    for i in range(len(student)):
        stuHash.append(i)

    churchChecker(stuHash, table, student)
    return stuHash

# 학생 섞기
for i, grade in enumerate(all_grade):
    random.shuffle(grade)

# TODO 삭제
cur = conn.cursor()
cur.execute("SELECT id, name, grade, church FROM student")
stu_db_list = cur.fetchall()

for it in stu_db_list:
    print(it)
print(len(stu_db_list))

conn.close()