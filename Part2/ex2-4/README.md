# 고급 슬라이싱

* 슬라이스와 범위 지정시에 마지막 항목이 포함되지 않는 이유
    - 세 개의 항목을 생성하는 range(3)나 my_list[:3]처럼 중단점만 이용해서 슬라이스나 범위를 지정할때 길이를 계산하기 쉽다.
    - 시작점과 중단점을 모두 지정할 때도 길이를 계산하기 쉽다. 단지 중단점에서 시작점을 빼면 된다.
    - 다음 예제에서 보는 것처럼, x 인덱스를 기준으로 겹침 없이 시퀀스를 분할하기 쉽다. 단지 my_list[:x]와 my_list[x:]로 지정하면 된다.

    [슬라이싱 예제](https://github.com/hyeonDD/fluent_python/blob/master/Part2/ex2-4/ex_slicing.py "소스코드")

* 슬라이스 객체
    - 1장에서 사용한 deck[12::13] 와 같이 a:b:c표기법은 인덱스 연산을 수행하는 [] 안에서만 사용할수있다.
    - 10.4.1 슬라이싱 작동 방식 에서 설명하는것처럼 seq[start:stop:step] 표현식을 평가하기 위해 파이썬은 seq.__getitem__(slice(start,stop,step))을 호출한다. 슬라이스 객체 덕분에 슬라이스에 이름을 붙일 수 있다.

    [슬라이싱 이름붙이기 예제](https://github.com/hyeonDD/fluent_python/blob/master/Part2/ex2-4/named_slicing.py "소스코드")
    
    - 파이썬 에서의 세 개의 마침표(...) 은 하나의 토큰으로 인식된다. 이기호는 Ellipsis 객체의 별명으로서 하나의 ellipsis 클래스의 객체다. 생략 기호 객체는 f(a, ...,z)처럼 함수의 인수나, a[i:...]처럼 슬라이스의 한 부분으로 전달할 수 있다. NumPy는 다차원 배열을 슬라이싱할 때 생략 기호(...)를 사용한다.