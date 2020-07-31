idSearchSql = ("""
    SELECT id FROM student WHERE name = ? AND grade = ? AND church = ?
""")


def printkiller():
    print(idSearchSql)

printkiller()