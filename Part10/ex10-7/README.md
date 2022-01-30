<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part10/ex10-1~4/UML_class_diagram.png)
 -->
# Vector 버전 #5: 포매팅
Vector의 __format__() 메서드는 Vector2d의 __format__()과 비슷하지만, 극좌표 대신 구면좌표를 사용한다. 구면좌표는 초구면좌표라고도 하는데, 4차원 이상에서의 구를 초구라고 하기 때문이다. 이에 따라 뒤에 붙는 포맷 코드를 'p'에서 'h'로 변경한다.
> 9.5절 '포맷된 출력'에서 설명한 것처럼, 포맷 명시 간이 언어 (https://docs.python.org/3/library/string.html#formatspec)를 확장하려면 내장 자료형에서 지원하는 포맷 코드를 다른 용도로 사용하지 않는 것이 좋다. 특히 우리가 확장한 포맷 간이 언어는 실수형 포맷코드 'eEfFgGn%'를 원래 의미대로 사용하므로, 이 포맷 코드는 반드시 피해야 한다. 정수형은 'bcdoxXn'을, 문자열은 's'를 사용하므로, Vector2d의 극좌표에서는 'p'를 사용했다. 초평면좌표를 나타내기 위해 'h'를 사용한 것은 탁월한 선택이다.

예를 들어 4차원 공간(len(v) ==4) 에 있는 Vector 객체에 대해 'h'코드는 <r, 1, 2, 3>를 출력한다. 이때 r은 크기 (abs(v))를 나타내고, 나머지 숫자는 각좌표 1,2,3을 나타낸다.

vector_v5.py 에서 4차원 구면 좌표에 대한 doctest 코드의 일부를 보면 다음과 같ㄴ다.

```
format(Vector([-1, -1, -1, -1]), 'h)

format(Vector([2, 2, 2, 2]), '.3eh')

format(Vector([0, 1, 0, 0]), '0.4fh)
```

__format__() 메서드를 수정하기 전에 몇 가지 지원 메서드를 구현해야 한다. angle(n)은 특정 좌표의 각좌표를 계산하고 (에를들면 1), angles()는 모든 각좌표의 반복형을 반환한다. 여기서는 구체적인 수학 공식은 설명하지 안흔다. Vector 요소 배열에 들어있는 직교좌표에서 구면좌표를 구하는 자세한 방법은 위키 백과의 '초구면 좌표계' (https://ko.wikipedia.org/wiki/초구면_좌표계) 를 참조하라.

- [vector_v5.py](https://github.com/hyeonDD/fluent_python/blob/master/Part10/ex10-1~4/vector_v5.py)
