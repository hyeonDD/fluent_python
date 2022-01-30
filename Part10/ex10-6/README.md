<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part10/ex10-6/UML_class_diagram.png)
 -->
# Vector 버전 #4: 해싱 및 더 빠른 ==
__hash__() 메서드를 구현하자. 기존 __eq__() 메서드와 함께 __hash__() 메서드를 구현하면 Vector 객체를 해시할 수 있게 된다.

9.8절의 __hash__()는 hash(self.x) ^ hash(self.y)를 이용해서 해시값을 계산했다.
이제는 hash(v[0]) ^ hash(v[1]) ^ hash(v[2]) ... 형태로 각 요소의 해시를 계산해서 연속해서 ^(XOR) 연산자를 적용하려고 한다. 바로 이런곳에 사용하기 위해 functools.reduce()함수가 있다. 앞에서 reduce()가 그리 인기 있지 않다고 설명했지만, 모든 벡터 요소의 해시를 계산하는 연산은 reduce()에 딱 맞는다. 

![reucde그림](https://github.com/hyeonDD/fluent_python/blob/master/Part10/ex10-6/reduce.png)

지금까지 functools.reduce()는 sum()으로 대체할 수 있다고 설명했지만, 이제 reduce()메서드를 제대로 살펴보자. 핵심은 일련의 값을 하나의 값으로 줄이는 것이다. reduce()가 받는 첫 번째 인수는 두 개의 인수를 받는 함수, 두 번째 인수는 반복형이다. 인수 두 개를 받는 함수 fn과 리스트 lst가 있다고 가정하자. reduce(fn, lst)를 호출하면 첫 번째 요소 쌍에 fn을 적용해서(즉, fn(lst[0], lst[1])) 첫 번째 결과 r1을 생성한다. 그러고 나서 r1과 다음 요소에 fn을 적용해서 (즉, fn(r1, lst[2])) 두번째 결과 r2를 생성한다. 이제 fn(r2, lst[3])을 호출해서 r3를 생성하고... 이 과정을 마지막 요소까지 반복하면 결국 rN이 반환된다.

다음은 reduce()를 이용해서 5!(5팩토리얼)을 계산하는 코드다.

```
2 * 3 * 4 * 5
# 120
import functools
functools.reduce(lamdbda a,b: a*b, range(1, 6))
# 120
```

다시 해시 문제로 돌아가자. 위 예제는 0에서 5까지의 숫자에 XOR을 누적 계산하는 세가지 방법을 보여준다. 첫 번째는 for 루프를, 두 번째와 세 번째는 reduce() 함수를 사용한다.

```
n = 0
for i in range(6): #1
    n ^= i
n
# 1
import functools
functools.reduce(lambda a, b: a^b, range(6)) #2
# 1
import operator
functools.reduce(operator.xor, range(6)) #3
# 1
```
1. for 루프와 변수를 이용해서 XOR 연산을 누적 적용한다.
2. 익명 함수를 이용해서 functools.reduce()를 호추랗ㄴ다.
3. 사용자 정의 람다를 operator.xor로 대체해서 functools.reduce()를 호출한다.

위 예제의 세 가지 방법 중 필자가 가장 좋아하는 것은 마지막 방법이고, 두 번째 좋아하는 것은 for 루프를 사용하는 것이다. 여러분은 어떤 것이 마음에 드는가?

5.10.1절 'operator 모듈'에서 설명한 것처럼 operator 모듈은 모든 파이썬 중위 연산자를 함수 형태로 제공해서 람다를 사용할 필요성을 줄여준다.

Vector.__hash__()를 필자가 좋아하는 스타일로 구현하려면 functools와 opeartor 모듈을 임포트 해야한다. 아래 예제는 관련된 변경사항을 보여준다.

- [vector_v4.py의 일부](https://github.com/hyeonDD/fluent_python/blob/master/Part10/ex10-6/vector_v4.py)
1. reduce()를 사용하기 위해 functools 모듈을 임포트한다.
2. xor 함수를 사용하기 위해 operator 모듈을 임포트한다.
3. __eq__()는 바뀌지 않았다. 여기에 포함시킨 이유는 __eq__()와 __hash__()가 밀접히 작동해야 하므로, 소스 코드 안에서 가까이 두는 습관을 들이는 것이 좋기 때문이다.
4. 각 요소의 해시를 느긋하게 계산하기 위해 제너레이터 표현식을 만든다.
5. xor 함수와 hashes를 전달해서 reduce() 함수를 호출함으로써 해시값들의 XOR을 구한다. 세 번째 인수인 0은 초기값이다(아래 참조구문 참조.)
> reduce()를 사용할 때는 세 번째 인수를 전달해서 reduce(<함수>, <반복형>, <초깃값>)형태로 호출하고 'TypeError: reduce() of empty sequence with no inital value' 예외가 발생하지 않게 예방하는 것이 좋다(훌륭한 메세지다. 문제를 설명하고 해결책을 제시한다). <초깃값>은 시퀀스가 비어 있을 때 반환되는 값이며, 리듀스 루프 안에서 첫 번째 인수로 사용된다. 따라서 함수에 대한 항등원을 사용해야 한다. 예를 들어 +, |, ^ 연산의 경우에는 <초깃값>이 0이 되어야 하지만, *, & 연산의 경우에는 <초깃값>이 1이 되어야 한다.

__hash__()메서드는 맵 - 리듀스 계산 에 딱 맞는 예다.

![reucde그림2](https://github.com/hyeonDD/fluent_python/blob/master/Part10/ex10-6/reduce2.png)

맵 단계에서는 각 요소에 대한 해시를 계산하고, 리듀스 단계에서는 모든 해시에 xor연산자를 적용한다. **제너레이터 표현식** 대신 **맵**을 사용하면 맵 단계가 훨씬 더 잘 드러난다.
```
def __hash__(self):
    hashes = map(hash, self._components)
    return functools.reduce(operator.xor, hashes)
```
> map()함수가 결과값을 가진 리스트를 새로 생성하는 파이썬 2에서는 map()을 이용한 방법의 효율이 떨어진다. 그러니 파이썬 3에서의 map()을 느긋하게 수행하여 필요할 때 결과를 산출하는 제너레이터를 생성한다. 따라서 위 코드의 __hash__()메서드에서 사용한 제너레이터 표현식과 마찬가지로 메모리를 절약해준다.

지금은 리듀스 함수에 대해 다루고 있지만, __eq__() 메서드를 간단히 수정해서 커다란 벡터를 더 빠르고 메모리를 적게 사용하도록 바꿔보자. 아래 예제에서 소개한 것처럼 현재 __eq__()메서드는 다음과 같이 구현되어 있다.
```
def __eq__(self, other):
    return tuple(self) == tuple(other)
```
이 코드는 Vector2d와 Vector 클래스 모두에 작동한다. 심지어 Vector([1,2])와 (1, 2)가 같다고 판단한다. 이것은 문제가 될 수 있지만, 지금은 무시하자. 그렇지만 수천 개의 요소를 가질 수 있는 Vector 객체의 경우, 이 코드는 상당히 비효율적이다. 단지 튜플형의 __eq__()메서드를 적용하기 위해 피연산자 전체를 복사해서 튜플 두 개를 만든다. 요소가 두 개 밖에 없는 Vector2d의 경우에는 나쁘지 않지만, 아주 큰 다차원 벡터의 경우에는 얘기가 다르다. Vector 객체를 다른 Vector 객체나 반복형과 비교할 때는 아래와 같이 구현하는 것이 좋다.

```
def __eq__(self, other):
    if len(self) != len(other): #1
        return False
    for a, b in zip(self, other): #2
        if a != b: #3
            return False
    return True #4
```
1. 두 객체의 길이가 다르면, 객체가 다르다.
2. zip() 함수는 반복형 인수의 항목으로 구성된 튜플의 제네레이터를 만든다. zip()이 생소하다면 다음쪽에 있는 '멋진 zip()함수'글상자를 참조하라. 위에서 len()함수로 길이를 먼저 검사해야 한다는 점에 주의하라. 입력 중 하나가 소진되자마자 zip()이 아무런 경고 없이 값 생산을 중단하기 때문이다.
3. 두 요소가 다르다는 것이 발견되자마자 False를 반환하면서 빠져나간다.
4. 그렇지 않으면 객체가 동일한 것이다.

위 코드의 효유리 높지만, all() 함수를 사용하면 for 루프와 동일한 계산을 단 한 줄에 할 수 있다. 해당 요소간의 비교가 모두 True면, 결과도 True다. 비교하는 도중에 다른 요소가 나오면, 즉 비교가 False면 all()은 바로 False를 반환한다. all() 함수를 이용해서 구현한 __eq__() 메서드는 아래와 같다.

```
def __eq__(self, other):
    return len(self) == len(other) and all(a == b for a, b in zip(self, other))
```
zip()은 가장 짧은 피연산자에서 멈추므로, 먼저 피연산자의 길이를 검사해야 하는 것을 잊지 말아야 한다.

아래의 __eq__()메서드를 vector_v4.py에 적용한다.

이 장은 Vector2d에서 구현한 __format__() 메서드를 Vector클래스로 가져오면서 마친다.

---
**_ 멋진 zip() 함수 _**

인덱스 변수를 조작하지 않으면서 항목들을 반환하는 for 루프가 있다는 것은 정말 멋지고 많은 버그를 예방하는 데 도움이 되지만, 몇 가지 특별 유틸리티 함수가 필요하다. 그중 하나가 zip()내장 함수다. zip()은 각 반복형에서 나온 항목들을 튜플로 묶음으로써 두 개 이상의 반복형을 병렬로 반복하기 쉽게 해준다. 튜플을 변수에 언패킹해서 각 변수에 병렬로 입력할 수 있다. 아래를 보자.

> zip() 함수의 이름은 지퍼 슬라이더에서 따온 것이다. 물리적인 지퍼 슬라이더는 지퍼 양쪽의 이빨 쌍을 맞물리게 한다. zip(lef, right)가 하는 일을 보면 비슷하다는 것을 쉽게 떠올릴 수 있을 것이다. 이 함수는 압축파일과는 상관이 없다.
---

내장된 zip()함수의 사용
```
zip(range(3), 'ABC') #1
# <zip object at 0x0000020F0CE07780>
list(zip(range(3), 'ABC')) #2
# [(0, 'A'), (1, 'B'), (2, 'C')]
list(zip(range(3), 'ABC', [0,0, 1.1, 2.2, 3.3])) #3
# [(0, 'A', 0), (1, 'B', 0), (2, 'C', 1.1)]
from itertools import zip_longest #4
list(zip_longest(range(3), 'ABC', [0.0, 1.1, 2.2, 3.3], fillvalue=-1))
# [(0, 'A', 0.0), (1, 'B', 1.1), (2, 'C', 2.2), (-1, -1, 3.3)]
```
1. zip() 함수는 요청에 따라 튜플을 생성하는 제네레이터를 반환한다.
2. 여기서는 리스트를 생성해서 출력한다. 일반적으로 제네레이터를 반복한다.
3. zip()함수는 놀라운 성질이 있다. 반복형 중 어느 것이라도 소진되면 경고 메세지 없이 중단한다.
4. itertools.zip_longest() 함수는 다르게 동작한다. 선택적인 fillvalue(기본값은 None이다)를 이용해서 빠진 값을 채워가면서 마지막 반복형이 소진될 때까지 튜플을 생성한다.

enumerate() 내장 함수도 인덱스 변수를 직접 조작할 필요 없이 for 루프 안에서 종종 사용되는 제네레이터 함수다. enumerate()가 낯설면서 반드시 '내장함수 문서 (http://bit.ly/1QOtsk8) 를 참조하기 바란다. zip()과 enumerate() 내장 함수는 14.9절 '표준 라이브러리의 제너레이터 함수'에서 여러 제네레이터 함수를 설명할 때 함께 설명한다.
