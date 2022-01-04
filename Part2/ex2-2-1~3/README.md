# 내장 시퀀스 개요

* 컨테이너 시퀀스
    - 서로 다른 자료형의 항목들을 담을수 있음 list, tuple, collections.deque 형.

* 균일 시퀀스
    - 단 하나의 자료형만 담을 수 있는 str, bytes, bytearry, memoryview, arrary.array 형. 

# 지능형 리스트 (listcomp)

* 지능형 리스트
    - 구문이 두 줄 이상 넘어가는 경우에는 코드를 분할 또는 for문을 이용해 작성하는것이 나음.
> 파이선 2에서는 i='dummy' , dummy = [i for i in 'ABC'] , print(a) # 결과 C  와같이 처음 i에 설정된 값이 사라지는 메모리 누수가 있었지만 파이썬 3에서는 함수처럼 고유한 지역 범위를 가지게됨.

    - 내장된 map() filter() 를 조합한 방법이 지능형 리스트보다 무조건 빠르진 않다.
> [비교소스](https://github.com/hyeonDD/fluent_python/blob/master/Part2/ex2-2-1~3/listcomp_speed.py "비교소스")
    
    - 지능형 리스트는 오로지 리스트만 만든다.




