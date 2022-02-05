<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-8/UML_class_diagram.png)
 -->
# 또 다른 예제: 등차수열 제너레이터
전통적인 반복자 패턴은 모두 데이터 구조체를 뒤져서 항목들을 나열하기 위한 것이다. 그러나 수열에서 다음 항목을 가져오는 메서드에 기반한 표준 인터페이스는 컬렉션에서 항목을 가져오는 대신 실행 도중에 항목을 생성하는 경우에도 유용하게 사용할 수 있다. 예를 들어 내장 함수 range()는 정수로 구성된 유한 등차수열을 생성하며, itertools.count() 함수는 무한 등차수열을 생성한다.

itertools.count()는 다음 절에서 다시 설명하지만, 특정 자료형의 숫자로 구성된 유한 등차수열을 생성하려면 어떻게 해야 할까?

아래예제는 잠시 후에 설명할 ArithmeticProgression 클래스를 콘솔에서 테스트한 결과를 보여준다. 이 예제에서 사용한 생성자 시그너처는 ArithmeticProgression(begin, step[, end])다. range() 함수가 여기에서 사용한 ArithmeticProgression 클래스와 비슷하지만, range() 함수의 전체 시그너처는 range(start, stop[, step])이다. 등차수열에서는 tep이 필수고, end가 선택이므로 여기서는 다른 시그너처를 사용하기로 결정했다. 그리고 start와 stop 인수명도 begin과 end로 바꿔서 시그너처가 다름을 명백히 보여주고자 했다. 아래예제에서는 테스트할 때마다 생성된 값들을 조사하기 위해 반한된 결과에 list() 생성자를 적용했다.

```
# ArithmeticProgression 사용 예
ap = ArithmeticProgression(0, 1, 3)
list(ap)
# [0, 1, 2]
ap = ArithmeticProgression(1, .5, 3)
list(ap)
# [1.0, 1.5, 2.0, 2.5]
ap = ArithmeticProgression(0, 1/3, 1)
list(ap)
# [0.0, 0.33333333, 0.6666666]
from fractions import Fraction
ap = ArithmeticProgression(0, Fraction(1, 3), 1)
list(ap)
# [Fraction(0, 1), Fraction(1, 3), Fraction(2, 3)]
from decimal import Decimal
ap = ArithmeticProgression(0, Decimal('.1'), .3)
list(ap)
# [Decimal('0.0'), Decimal('0.1'), Decimal('0.2')]
```
등차수열로 생성된 숫자들의 자료형이 파이썬 산술의 수치형 강제 변환 규칙에 의해 begin이나 step의 자료형을 따름에 주의하라. 위 예제에서는 int, float, Fraction, Decimal형 숫자들의 리스트를 보여주었다.

아래 예제는 ArithmeticProgression 클래스를 구현한 것이다.
- [arithmetic_progression.py](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-8/arithmetic_progression.py)
1. __init__() 메서드에서 begin과 step은 필수 인수며, end는 선택 인수다. end가 None이면 무한 수열이다.
2. 여기서는 self.begin과 같은 값이 결과가 되지만, 이후에 더할 값에 맞춰 자료형을 강제로 변환한다.
3. 가독성을 높이기 위해 self.end 속성이 None이면 forever 플래그를 True로 설정한다. 그러면 무한 등차수열을 생성한다.
4. forever 값에 따르거나 result가 self.end보다 작은 동안 루프를 실행한다. 이 루프를 빠져나가면 함수도 빠져나가게 된다.
5. 현재 result를 생성한다.
6. 다음에 가져올 result를 미리 계산한다. 다음번에 while 루프를 빠져나오면 이 값을 생성하지 않을 수도 있다.

위 arithmetic_progression.py의 마지막 줄에서는 실수로 작업할 때의 오차 누적을 줄이기 위해 단순히 result값을 self.step만큼 증가시키는 대신 index 값을 self.step에 곱해서 self.begin에 더했다.

위 ArithmeticProgression 클래스는 원하는 대로 작동하며, __iter__() 특별메서드를 구현하는 제너레이터 함수를 사용하는 예를 잘 보여준다. 그러나 이 클래스의 목적이 __iter__()를 구현함으로써 제너레이터를 생성하는 것이였다면, 클래스를 단지 하나의 제너레이터 함수로 만들 수도 있었을 것이다. 결국 제너레이터 함수도 일종의 제너레이터 팩토리이기 때문이다.

아래에제에서는 더 적은 양의 코드로 ArithmeticProgression 클래스와 동일한 작업을 수행하는 aritprog_gen()이라는 제너레이터 함수를 구현했다. ArithmeticProgression()대신 aritprog_gen()을 호출하면 ArithmeticProgression 사용 예 의 테스트를 모두 통과한다.
```
# aritprog_gen() 제너레이터 함수
def ariprog_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index
```
위 코드는 상당히 멋있지만, 표준 라이브러리에는 바로 사용할 수 있는 제너레이터가 아주 많음을 잊지 말아야 한다. 다음 절에서는 itertools 모듈을 이용해서 훨씬 더 멋있게 구현하는 방법을 설명한다.

## itertools를 이용한 등차수열
파이썬 3.4의 itertools 모듈에는 다양하고 재미있게 조합할 수 있는 제너레이터 함수가 19개 들어 있다.

예를 들어 itertools.count() 함수는 숫자를 생성하는 제너레이터를 반환한다. 인수를 지정하지 않으면 0에서 시작하는 수열을 생성한다. 그러나 start와 stop 인수를 지정하면 앞에서 구현한 aritprog_gen() 함수와 아주 비슷한 결과를 낼 수 있다.
```
import itertools
gen = itertools.count(1, .5)
next(gen)
# 1
next(gen)
# 1.5
next(gen)
# 2.0
next(gen)
# 2.5
```
그러나 itertools.count()는 끝이 없다. 따라서 list(count())를 실행하면, 파이썬 인터프리터는 사용할 수 있는 메모리보다 큰 리스트를 만들려고 시도하면서 잠시 후에 실패한다.

그리고 itertools.takewhile()이라는 함수도 있다. 이 함수는 다른 제너레이터를 소비하면서 주어진 조건식이 False가 되면 중단되는 제너레이터를 생성한다. 이 두 개의 제너레이터를 결합해서 다음과 같이 구현할 수 있다.
```
gen = itertools.takewhile(lambda n: n < 3, itertools.count(1, .5))
list(gen)
# [1, 1.5, 2.0, 2.5]
```
아래 예제는 takewhile()과 count()를 활용해서 aritprog_gen()을 짧고 멋지게 구현한다.
```
import itertools

def aritprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is not None:
        ap_gen = itertools.takewhile(lambda n: n < end, ap_gen)
    return ap_gen
```
위 예제의 aritprog_gen()은 본체 안에 yield 문이 없으므로 제너레이터 함수가 아님에 주의하라. 그러나 제너레이터를 반환하므로, 다른 제너레이터 함수와 마찬가지로 일종의 제너레이터 팩토리처럼 작동한다.

위에서 설명하고자 하는 것은 제너레이터를 구현할 때 표준 라이브러리에서 어떤 것이 제공되고 있는지 확인하라는 것이다. 표준 라이브러리를 확인하지 않으면 기존에 구현된 것을 다시 구현하게 될 수도 있다. 그러므로 다음 절에서는 바로 사용할 수 있는 여러 제너레이터 함수를 살펴본다.