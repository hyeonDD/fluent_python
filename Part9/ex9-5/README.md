<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part9/ex9-1/UML_class_diagram.png)
 -->
# 포맷된 출력

format() 내장 함수와 str.format() 메서드는 실제 포맷 작업을 __format__(format_spec)메서드에 위임한다. format_spec은 포맷 명시자로서, 다음 두 가지 방법 중 하나를 통해 지정한다.
* format(my_obj, format_spec)의 두 번째 인수
* str.format()에 사용된 포맷 문자열 안에 {}로 구분한 대체 필드 안에서 콜론 뒤의 문자열

예를 들어 다음과 같이 사용한다.

```
brl = 1/2.43
brl
format(brl, '0.4f')
'1 BRl = {rate:0.2f} USD'.format(rate=brl)
```
1. '0.4f'가 포맷 명시자다.
2. '0.2f'가 포맷 명시자다. 대체 필드 안에 있는 'rate' 문자열을 필드명이라고 한다. 이 문자열은 포맷 명시자와 상관 없지만, format()인수 중 어느 인수가 대체 필드에 들어갈 것인지 결정한다.

여기서 2번 항목에 주의하라. '{0.mass:5.3e}'와 같은 포맷 문자열은 실제로는 두 가지 표기법을 사용한다. 콜론의 왼쪽에 있는 '0.mass'는 대체 필드 구문에서 필드명(field_name)에 해당하는 부분이며, 콜론의 오른쪽에 있는 '5.3e'가 포맷 명시자다. 포맷 명시자에 사용된 표기법을 '포맷 명시 간이 언어' (http://bit.ly/1Gt4vJF) 라고 한다.
> 강의해본 경험을 돌이켜보면, format()과 str.format()을 처음 접하는 경우, 먼저 포맷 명시 간이 언어 (http://bit.ly/1Gt4vJF) 만 사용하는 format() 함수를 공부하는 것이 좋다. 어느 정도 핵심을 파악한 후에는 str.format() 메서드에 사용되는 {:} 형태의 대체 필드 표기법에 사용되는 포맷 문자열 구문 (http://bit.ly/23gMGI2) 을 공부하면서 !s, !r, !a와 같은 변환 플래그까지 공부하는 것이 좋다.

몇몇 내장 자료형은 포맷 명시 간이 언어에 자신만의 고유한 표현 코드를 가지고 있다. 예를 들어 int형의 경우 이진수를 나타내는 'b', 16진수를 나타내는 'x'코드를 지원하며, float 형의 경우 고정소수점을 나타내는 'f', 백분율을 나타내는 '%' 코드를 지원한다.

```
format(42,'b)
format(2/3, '.1%')
```
각 클래스가 format_spec 인수를 자신이 원하는 대로 해석해서 포맷 명시 간이 언어를 확장할 수 있다. 예를 들어 datetime 모듈의 클래스들은 자신의 __format__() 메서드에서 strftime() 함수와 동일한 포맷 코드를 사용한다. 다음 코드에서 format() 내장 함수와 str.format() 메서드를 실행하는 예를 보자.

```
from datetime import datetime
now = datetime.now()
format(now, '%H:%M:%S')
"It's now {:%I:%M %p}".format(now)
```

클래스에서 __format__() 메서드를 정의하지 않으면, object에서 상속받은 메서드가 str(my_object)를 반환한다. Vector2d는 __str__()을 정의하고 있으므로, 다음과 같이 실행된다.

```
v1 = Vector2d(3, 4)
format(v1)
```
그러나 이대 포맷 명시자를 사용하면 object.__format__()은 TypeError를 발생한다.
```
format(v1, '.3f')
Traceback (most recent call last):
...
TypeError: non-empty format string passed to object.__format__
```
Vector2d 클래스 자체의 포맷 간이 언어를 구현하면 이 문제를 해결할 수 있다. 먼저 사용자가 제공하는 포맷 명시자를 벡터의 각 float 형 요소를 포맷하기 위한 것이라고 가정하자. 즉, 다음과 같은 결과가 나오기를 원한다고 가정하자.

```
# Vector2d 클래스 내부
def __format__(self, fmt_spec=''):
    components = (format(c, fmt_spec) for c in self) #1
    return '({, {})'.format(*components) #2
```
1. 벡터의 각 요소에 fmt_spec 포맷을 적용하기 위해 format()내장 함수를 호출하고, 포맷된 문자열의 반복형을 생성한다.
2. 포맷된 문자열을 '(x,y)' 형식으로 만든다.

이제 Vector2d의 간이 언어에 포맷 코드를 추가해보자. 포맷 명시자가 'p'로 끝나면 벡터를 극좌표 <r, 0>로 표현한다. 여기서 r은 벡터의 크기, 세타(0)는 라디안으로 표현된 각을 나타낸다.'p'앞에 오는 나머지 포맷 명시자는 이전과 동일하게 사용된다.

> 필자는 포맷 코드를 추가할 때 다른 자료형에서 사용하는 코드와 중복되지 안흔ㄴ 코드를 선택한다. 포맷 명시자간이 언어 (http://bit.ly/1Gt4vJF) 를 보면, 정수형은 'bcdoxXn'을, 실수형은 'eEfFgGn%'를, 문자열은 's'를 사용함을 알 수 있다. 그래서 극좌표에 대한 포맷 코드로 'p'를 선택했다. 각 클래스에서 이 코드를 독립적으로 해석하므로 새로운 자료형에 대해 기존 포맷 코드를 재사용해도 에러가 발생하지는 않지만, 사용자가 혼동할 우려가 있다.

이제 극좌표를 생성해보자. 크기를 생성하는 __abs__() 메서드는 이미 있으며, 각을 구하기 위해 math.atan2()함수를 사용하는 angle() 메서드를 다음과 같이 간단히 구현한다. 
```
# Vector2d 클래스 내부
def angle(self):
    return math.atan2(self.y, self.x)
```
필요한 코드를 모두 갖추었으니, 이제 __format__() 메서드가 극좌표를 생성하도록 수정해보자

```
# Vector2d.format(), 버전 2

def __format__(self, fmt_spec=''):
    if fmt_spec.endswith('p): #1
        fmt_spec = fmt_spec[:-1] #2
        coords = (abs(self), self.angle()) #3
        outer_fmt = '<{}, {}>' #4
    else:
        coords = self #5
        outer_fmt = '({},{})' #6
    components = (format(c, fmt_spec) for c in coords) #7
    return outer_fmt.format(*components) #8
```
1. 포맷 명시자가 'p'로 끝나면 극좌표를 사용한다.
2. fmt_spec의 마지막에 있는 'p'를 떼어낸다.
3. (크기,각)으로 극좌표 튜플을 만든다.
4. 꺾쇠괄호를 이용해서 바깥쪽 포맷을 구성한다.
5. 그렇지 않으면 self의 x,y요소를 이용해서 직교좌포를 만든다.
6. 괄호를 이용해서 바깥쪽 포맷을 구성한다.
7. 요소들을 포맷해서 반복형을 만든다.
8. 포맷된 문자열을 바깥쪽 포맷에 적용한다.

