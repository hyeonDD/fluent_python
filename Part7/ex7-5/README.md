# 클로저
<!-- 
- [지역 및 전역 변수를 읽는 함수](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-5/read_local_global_func.py)
 -->
블로그 글을 보다 보면 클로저를 익명 함수와 혼동하는 경우가 종종 있다. 아마도 익명 함수를 이용하면서 함수 안에 함수를 정의하는 방식이 보편화되었기 때문으로 생각된다.
그리고 클로저는 내포된 함수 안에서만 의미가 있다. 따라서 클로저와 익명 함수를 동일한 개념으로 생각하는 사람이 많은 것 같다.
실제로 클로저는 함수 본체에서 정의하지 않고 참조하는 비전역변수를 포함한 확장 범위를 가진 함수다. 함수가 익명 함수인지 여부는 중요하지 않다. 함수 본체 외부에 정의된 비전역 변수에 접근할 수 있다는 것이 중요하다.

이 개념은 이해하기 어려우므로, 예제를 통해 알아보는 것이 좋다.

avg() 함수가 점차 증가하는 일련의 값의 평균을 계산한다고 가정해보자. 예를 들어 전체 기간을 통틀어 어떤 상품의 종가 평균을 구하는 경우를 생각해보자. 매일 새로운 가격이 추가되고 지금까지의 모든 가격을 고려해서 평균을 구한다.

처음 avg()를 실행한 후 반복 실행하면 다음과 같다.

***
>>> avg(10)
10.0
>>> avg(11)
10.5
>>> avg(12)
11.0
***

avg()는 어떻게 이전 값을 기억하고 이쓴ㄴ 것일까? 먼저 클래스를 이용해서 구현하는 아래 예제를 보자.

- [average_oo.py](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-5/average_oo.py)

이제 고위 함수 make_averager()를 이용해서 구현한 아래 예제를 보자.

- [average.py](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-5/average.py)
호출되면 make_averager()는 average() 함수 객체를 반환한다. average() 함수는 호출될때마다 받은 인수를 series 리스트에 추가하고 현재까지의 평균을 계산해서 출력한다.

위 average_oo.py 의 클래스로 구현한 객체와 average.py의 고위 함수는 상당히 비슷하다. Averager()나 make_averager()를 호출해서 콜러블 객체인 avg가 반환되고, avg()는 series를 갱신하고 지금까지의 평균을 계산한다. averager_oo.py의 avg()는 Averager 클래스의 객체고, average.py의 avg()는 내부 함수인 average()다. 어쨋든 우리는 avg(n)을 호출해서 series에 추가하고 새로운 평균을 가져온다.

Averager 클래스의 avg()함수가 데이터를 보관하는 방법은 명확히 알 수 있다. 바로 self.series 객체 속성에 저장되기 때문이다. 그러나 두 번째 예제의 avg()함수는 어디에서 series를 찾을까?

make_averager() 함수 본체 안에서 series = []로 초기화하고 있으므로 series는 이 함수의 지역 변수다. 그렇지만 avg(10)을 호출할 때, make_averager()함수는 이미 반환했으므로 지역 범위도 이미 사라진 후다.

average 안에 있는 series는 **자유 변수**다. 자유 변수라는 말은 지역 범위에 바인딩되어 있지 않은 변수를 의미한다.
밑의 그림을 보자.
![def_averager그림](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-5/def_averager.png)
반환된 averager() 객체를 조사해보면 파이썬이 컴파일된 함수 본체를 나타내는 __code__속성 안에 어떻게 지역 변수와 자유 변수의 '이름'을 저장하는지 알 수 있다.

```
avg.__code__.co_varnames
('new_value', 'total')
avg.__code__.co_freevars
('series',)
```
series에 대한 바인딩은 반환된 avg() 함수의 __closure__ 속성에 저장된다. avg.__closure__의 각 항목은 avg.__code__.co_freevars의 이름에 대응된다. 이 항목은 cell 객체며, 이 객체의 cell_contents 속성에서 실제 값을 찾을 수 있다. 아래를 보자.

```
avg.__code__.co_freevars
('series',)
avg.__closure__
(<cell at 0x0000026B4B2688B0: list object at 0x0000026B4B22FA80>,)
avg.__closure__[0].cell_contents
[10, 11, 12]
```
지금까지 설명한 내용을 정리해보면, 클로저는 함수를 정의할 때 존재하던 자유 변수에 대한 바인딩을 유지하는 함수다. 따라서 함수를 정의하는 범위가 사라진 후에 함수를 호출해도 자유변수에 접근할 수 있다.

함수가 '비전역' 외부 변수를 다루는 경우는 그 함수가 다른 함수 안에 정의된 경우뿐이라는 점에 주의하라.
