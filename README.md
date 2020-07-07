# Christan_FoodTable_Algorithem
[충격] [실화] 신학교의 식사는 매우 까다롭다. 규칙이 없으면 밥을 못먹는단다 그들이 밥을 먹울수 있도록 도와주자

# 문제 정의
신학교에는 1학년~ 7학년 총 7개의 학년이 있다. 이 모두가 화합을 이루도록 서로 소통하기 위해 만찬을 여는대 이 만찬의 자리배치가 여간 까다로운것이 아니다.

프로그램을 만들어 그들의 자리배치를 할수 있게 하자

자리배치 조건
1. 신학교에는 총 7개의 학년이 있다.

2. 테이블의 개수는 7개의 학년중 가장 많은 학생을 가진 학년을 기준이다.
ex) 1학년: 20명, 2학년 30명, 3학년 25명, 4학년 24명, 5학년 20명, 6학년 15명 7학년 10명
이 경우 테이블의 개수는? 2학년 30명 -> 30개

3. 하나의 테이블에는 최대 6명까지 앉을수 있다.

4. 하나의 테이블에 같은 학년이 겹쳐지면 안된다. 
ex) 하나의 테이블에 같은 1학년이 2명 있을수는 없다.
또한 최대 6명인 테이블임으로 7개중 하나의 학년은 빠져야 한다.

5. 각 학생은 소속된 교회가 있으며 같은 교회 사람들끼지는 같은 테이블에 앉지 못한다.

6. 학생중 부장을 맡은 사람들은 자리가 고정되어 있다. 6학년 10명과 7학년 3명의 자리를 지정할수 있어야 한다.

7. 해당 만찬 이전 8번 까지의 만찬의 자리 배치동안 같은 테이블에 앉았던 사람과는 중복이 될수 없다.

이 모든 조건을 만족해서 자리 배치를 해야한다. 

추가 조건 
1. 해당 프로그램은 종료후 다시 실행해도 이전의 사람와 중복이 되어서는 안된다.

2. 컴퓨터에 무지한 사람이 쓰는것임으로 GUI로 사용하기 편하게 만들어야 한다.

3. 해당 결과를 액셀 파일로 해당 양식에 맞추어서 내보낼수 있어야 한다.
