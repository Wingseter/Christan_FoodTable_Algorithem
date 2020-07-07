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
student = list()

student.append({'Name': "김철수1", 'grade': 1, 'church': "양영1"})
student.append({'Name': "김철수1", 'grade': 1, 'church': "양영1"})
student.append({'Name': "김철수1", 'grade': 1, 'church': "양영1"})
student.append({'Name': "김철수2", 'grade': 2, 'church': "양영2"})
student.append({'Name': "김철수3", 'grade': 3, 'church': "양영3"})
student.append({'Name': "김철수4", 'grade': 4, 'church': "양영4"})
student.append({'Name': "김철수5", 'grade': 5, 'church': "양영5"})
student.append({'Name': "김철수6", 'grade': 6, 'church': "양영6"})
student.append({'Name': "김철수7", 'grade': 7, 'church': "양영7"})

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