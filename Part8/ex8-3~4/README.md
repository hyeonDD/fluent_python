# 기본 복사는 얕은 복사
리스트나 대부분의 내장 가변 컬렉션을 복사하는 가장 손쉬운 방법은 그 자료형 자체의 내장 생성자를 사용하는 것이다. 다음 예를 보자.
- [내장 생성자를 이용한 복사](https://github.com/hyeonDD/fluent_python/blob/master/Part8/ex8-3~4/list_copy.py)
1. list(l1)은 l1의 사본을 생성한다.
2. 두 사본이 동일하다. 
3. 그러나 서로 다른 두 객체를 참조한다.
리스트 및 가변형 시퀀스의 경우 l2 = l1[:] 코드는 사본을 생성한다.

그러나 생성자나 [:]을 사용하면 **얕은 사본**을 생성한다. 즉, 최상위 컨테이너는 복제하지만 사본은 원래 컨테이너에 들어 있던 동일 객체에 대한 참조로 채워진다. 모든 항목이 불변형이면 이 방식은 메모리를 절약하며 아무런 문제를 일으키지 않는다. 그러나 가변 항목이 들어있을 때는 불쾌한 문제를 야기할 수도 있다.

아래 예제에서는 다른 리스트와 튜플을 담고 있는 리스트의 얕은 사본을 생성한 후 변경해서 참조된 객체에 어떻게 영향을 미치지는지 보여준다.
> 인터넷에 연결된 컴퓨터가 옆에 있다면 온라인 파이썬 튜터(http://www.pythontutor.com/)에서 아래 예제의 대화형 애니메이션을 확인해보기 바란다. 이 책을 쓰고 있는 현재 pythontutor.com에서 준비한 예제를 직접 바인딩하는 방법은 제대로 작동하지 않지만, 도구는 훌륭하다. 코드를 복사해서 붙여 넣고 애니메이션으로 확인할 가치가 충분히 있다.

```
다른 리스트를 담고 있는 리스트의 얕은 복사. 이 코드를 온라인 파이썬 튜터에 복사해서 애니메이션을 확인해보라.
l1 = [3, [66, 55, 44], (7, 8, 9)]
l2 = list(l1)       #1
l1.append(100)      #2
l1[1].remove(55)    #3
print('l1:', l1)    
print('l2:', l2)    
l2[1] += [33, 22]   #4
l2[2] += (10, 11)   #5
print('l1:', l1)
print('l2:', l2)
```
1. l2는 l1의 얕은 사본이다. 이 상태는 아래 그림 3과 같다.
2. l1에 100을 추가해도 l2에는 영향을 미치지 않는다.
3. 여기서는 내부 리스트 l1[1]에서 55를 제거한다. l2[1]이 l1[1]과 동일한 리스트에 바인딩되어 있으므로 이 코드는 l2에 영향을 미친다.
4. l2[1]이 참조하는 리스트처럼 가변 객체의 경우 += 연산자가 리스트를 그 자리에서 변경한다. 이 변경은 l2[1]의 별명인 l1[1]에도 반영된다.
5. 여기서 += 연산자는 새로운 튜플을 만들어서 l2[2]에 다시 바인딩한다. 이 코드는 l2[2] = l2[2] + (10, 11)과 동일하다. 이제 l1과 l2의 마지막에 있는 튜플은 더 이상 동일 객체가 아니다. 그림4를 참조하라.
```
위 코드의 실행 결과 (출력)이다.
l1: [3, [66, 44], (7, 8, 9), 100]
l2: [3, [66, 44], (7, 8, 9)]
l1: [3, [66, 44, 33, 22], (7, 8, 9), 100]
l2: [3, [66, 44, 33, 22], (7, 8, 9, 10, 11)]
```
![그림3](https://github.com/hyeonDD/fluent_python/blob/master/Part8/ex8-1~2/그림3.png)
![그림4](https://github.com/hyeonDD/fluent_python/blob/master/Part8/ex8-1~2/그림4.png)
이제 얕은 복사를 만들기 쉽다는 것은 잘 알겠지만, 얕은 복사를 원하지 않을 수도 있다. 다음 절에서는 깊게 복사하는 방법을 알아보자.

## 객체의 깊은 복사와 얕은 복사 
얕게 복사한다고 해서 늘 문제가 생기는 것은 아니지만, 내포된 객체의 참조를 공유하지 않도록 깊게 복사할 필요가 있는 경우가 종종 있다. copy 모듈이 제공하는 deepcopy()함수는 깊은 복사를, copy()함수는 얕은 복사를 지원한다.

copy()와 deepcopy()사용법을 예제를 통해 설명하기 위해 아래 예제는 노선을 따라가면서 승객을 태우거나 내리는 학교 버스를 나타내는 Bus 클래스를 간단히 정의한다.

- [Bus 클래스](https://github.com/hyeonDD/fluent_python/blob/master/Part8/ex8-3~4/bus_class.py)
이제 아래의 코드와 같이 대화형 콘솔(인터프립터를 이용해서 bus1 객체와 두개의 사본(bus2는 얕은 사본, bus3은 깊은 사본))을 만들어 bus1이 학생을 내릴 때 어떤 일이 생기는지 보자.
```
import copy
bus1 = Bus(['Alic', 'Bill', 'Claire', 'David'])
bus2 = copy.copy(bus1)
bus3 = copy.depcopy(bus1)
id(bus1), id(bus2), id(bus3)
bus1.drop('Bill')
bus2.passengers
```
1. copy()와 deepcopy()를 이용해서 세 개의 Bus 객체를 생성한다.
2. bus1이 'Bill'을 내리면 bus2에서도 'Bill'이 사라진다.
3. passengers 속성을 조사해보면 bus1과 bus2가 동일 리스트를 공유하는 것을 알 수 있다. bus2가 bus1의 얕은 사본이기 때문이다.
4. bus3는 bus1의 깊은 사본이므로, passengers 속성을 다른 리스트를 가리킨다.

일반적으로 깊은 사본을 만드는 일은 간단하지 않다는 점에 주의하라. 객체 안에 순환 참조가 있으면 단순한 알고리즘은 무한 루프에 빠질 수 있다. deepcopy()함수는 순환 참조를 제대로 처리하기 위해 이미 복사한 객체에 대한 참조를 기억하고 있다. 순환 참조를 깊게 복사하는 예는 아래와 같다.

```
a = [10,20]
b = [a,30]
a.append(b)
a
# [10, 20, [[...], 30]]
from copy import deepcopy
c = deepcopy(a)
c
# [10, 20, [[...], 30]]
```
게다가 깊은 복사가 너무 깊이 복사하는 경우도 잇다. 예를 들어 복사하면 안 되는 외부 리소스나 싱글턴을 객체가 참조하는 경우가 있다. copy 모듈 문서 (http://docs.python.org/3/library/copy.html)에 설명된 대로 __copy__()와 __deepcopy__() 특별 메서드를 구현해서 copy()와 deepcopy()의 동작을 제어할 수 있다.

별명을 통한 객체 공유 방식은 파이썬에서 매개변수 전달이 작동하는 방식과 가변 자료형을 매개변수 기본형으로 사용하는 문제도 설명할 수 있다. 이에 대해서 아래를 보자.

# 참조로서의 함수 매개변수
파이썬은 **공유로 호출**하는 매개변수 전달 방식만 지원한다. 이 방식은 루비, 스몰토크, 자바(자바 참조 자료형일 때만 동일하다. 기본 자료형은 값으로 호출하는 방식을 사용한다) 등 대부분의 객체지향 언어에서 사용하는 방식과 동일하다. 공유로 호출한다는 말은 함수의 각 매개변수가 인수로 전달받은 각 참조의 사본을 받는다는 의미다. 달리 말하면, 함수 안의 매개변수는 실제 인수의 별명이 된다.

이런 체계의 결과로서, 함수는 인수로 전달받은 모든 가변 객체를 변경할 수 있지만, 객체의 정체성 자체는 변경할 수 없다. 즉, 어떤 객체를 다른 객체로 바꿀 수는 없다. 아래 에제는 매개 변수 중 하나에 += 연산자를 사용하는 간단한 함수를 보여준다. 함수에 숫자, 리스트, 튜플을 전달하면, 전달받은 인수는 서로 다른 영향을 받는다.

- [전달받은 가변 객체 수정(함수)](https://github.com/hyeonDD/fluent_python/blob/master/Part8/ex8-3~4/change_arg_func.py)
1. 숫자 x는 변경되지 않는다.
2. 리스트a는 변경된다.
3. 튜플 t는 변경되지 않는다.

함수 매개변수와 관련된 또 다른 문제는 가변형 기본값을 사용하는 것과 관련 있다. 이에 대해서는 다음 절에서 설명한다.

## 가변형을 매개변수 기본값으로 사용하기:좋지 않은 생각
기본값을 가진 선택적 인수는 파이썬 함수 정의에서 아주 좋은 기능으로, 하위 호환성을 유지하며 API를 개선할 수 있게 해준다. 그러나 매개변수 기본값으로 가변 객체를 사용하는 것은 피해야 한다.


예를 들어 설명하기 위해 아래 예제에서는 [Bus 클래스](https://github.com/hyeonDD/fluent_python/blob/master/Part8/ex8-3~4/bus_class.py)의 Bus 클래스를 가져와서 __init__()메서드를 변경하고 HauntedBus 클래스를 정의한다. 여기서는 약간의 꾀를 부려 passengers의 기본값을 None 대신 []를 사용해서 이전 __init__() 메서드에서 if 절로 검사하던 부분을 생략할 수 있게 했다. 여기서는 제 꾀에 제가 넘어가는 경우가 발생한다.

- [가변형이 기본값이 될 때의 위험성을 보여주는 간단한 클래스](https://github.com/hyeonDD/fluent_python/blob/master/Part8/ex8-3~4/hunted_bus.py)
1. passengers 인수를 전달하지 않는 경우 이 매개변수는 기본밗인 빈 리스트에 바인딩된다.
2. 이 할당문은 self.passengers를 passengers에 대한 별명으로 만드므로, passengers 인수를 전달하지 않는 경우 self.passengers를 기본값인 빈 리스트에 대한 별명으로 설정한다.
3. self.passengers에 remove()와 append()메서드를 사용할 때, 실제로는 함수 객체의 속성인 가변형 기본 리스트를 변경하는 것이다.

아래는 HauntedBus의 기괴한 작동을 보여준다.
1. 1까지는 문제가 없다. bus1이 예상한 대로 작동한다.
2. bus2가 빈 리스트로 시작하므로, 기본값인 빈 리스트가 self.passengers에 할당된다.
3. bus3도 빈 리스트로 시작하므로, 여기서도 기본값인 빈 리스트가 self.passengers에 할당된다.
4. 기본값이 더 이상 비어 있지 않다!
5. 이제 bus3에 승차한 Dave가 bus2에 나타난다.
6. 문제는 bus2.passengers와 bus3.passengers가 동일한 리스트를 참조한다는 것이다.
7. 그러나 bus1.passengers는 별개의 리스트다.

결국 명시적인 승객 리스트로 초기화되지 않은 Bus 객체들이 승객 리스트를 공유ㅏㅎ게 되는 문제가 발생한다.

이런 버그는 찾아내기 쉽지 않다. 위 유령버스 예제 처럼 HauntedBus 객체를 passengers로 초기화하면 원하는 대로 작동한다. HauntedBus 객체가 빈 리스트로 시작할 때만 이상한 일이 발생한다. self.passengers가 passengers 매개변수 기본값의 별명이 되기 때문이다. 문제는 각 기본값이 함수가 정의될 때(즉, 일반적으로 모듈이 로딩될 때) 평가되고 기본값은 함수 객체의 속성이 된다는 것이다. 따라서 기본값이 가변 객체고, 이 객체를 변경하면 변경 내용이 향후에 이 함수의 호출에 영향을 미친다.

유령버스의 문장들을 실행한 후 HauntedBus.__init__객체를 조사하면 다음과 같이 __defaults__ 속성 안에 유령 학생이 들어 있는 것을 볼 수 있다.
```
>>> dir(HauntedBus.__init__)
['__annotations__', '__call__', ..., '__defaults__',...]
>>> HauntedBus.__init__.__defaults__
(['Carrie', 'Dave'],)
```
가변 기본값에 대한 이러한 문제 때문에, 가변 값을 받는 매개변수의 기본값으로 None을 주로 사용한다. 위 예제에서 __init__()메서드는 passengers 인수가 None인지 확인하고 새로만든 빈 리스트를 self.passengers에 할당한다. 다음 절에서 설명하는 것처럼, passengers인수가 None이 아니면 인수의 사본을 self.passengers에 할당하는 것이 올바른 방법이다. 좀더 자세히 살펴보자.

## 가변 매개변수에 대한 방어적 프로그래밍
가변 매개변수를 받는 함수를 구현할 때는, 전달된 인수가 변경될 것이라는 것을 호출자가 예상할 수 있는지 없는지 신중하게 고려해야 한다.

예를 들어 여러분이 구현하는 함수를 dict 객체를 받아서 처리하는 동안 그 dict 객체를 변경한다면, 함수가 반환된 후에도 변경 내용이 남아 있어야 할까 아닐까? 판단은 상황에 따라 다르다. 정말 중요한 것은 함수 구현자와 함수 호출자가 예상하는 것을 일치시키는 것이다.
이 장에서 마지막으로 구현할 버스 예제인 TwilightBus 클래스는 승객 리스트를 코드 호출자와 공유함으로써 어떻게 호출자가 예상치 못한 일이 발생하는지 보여준다. 클래스 구현에 앞서, 클래스 사용자의 입장에서 TwilightBus 클래스가 어떻게 작동해야 하는지 살펴보자.

```
>>> TwilightBus가 하차시킬 때 사라지는 승객들
>>> basketball_tema = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
>>> bus = TwilightBus(basketball_team)
>>> bus.drop('Tina')
>>> bus.drop('Pat')
>>> basketball_team
['Sue', 'Maya', 'Dina']
```
1. basketball_team에 학생 다섯 명이 있다.
2. TwilightBus가 팀을 태운다.
3. bus가 학생을 한 명을 내린 후 한명 더 내린다.
4. 내린 학생들이 농구팀에서 사라졌다!

TwilightBus 클래스는 인터페이스 디자인에서 가장 중요한 '최소 놀람의 법칙'을 어긴다. 학생이 버스에서 내린다고 해서 그 학생이 농구팀 출전 명단에서 빠진다는것은 분명 놀라운 일이다.

아래 예제는 TwilightBus 클래스 구현 코드며 문제의 원인을 알려준다.

- [받은 인수를 변경하는 위험성을 보여주는 간단한 클래스](https://github.com/hyeonDD/fluent_python/blob/master/Part8/ex8-3~4/twilight_bus_class.py)
1. passengers가 None일 때 빈 리스트를 새로 생성하는 신중함을 보여준다.
2. 그러나 이 할당문에 의해 self.passengers는 passengers에 대한 별명이 된다. 이때 passengers는 위 basketball_team 소스코드에서의 basketball_team처럼 __init__()에 전달된 인수의 별명이다.
3. self.passengers의 remove()나 append() 메서드를 사용하면, 생성자에 인수로 전달된 원래 리스트를 변경하게 된다.

여기서 문제는 bus가 생성자에 전달된 리스트의 별명이라는 점이다. 여기서는 TwilightBus객체 고유의 리스트를 유지해야 한다. 해결하는 방법은 __init__() 메서드가 passengers 인수를 받을 때 인수의 사본으로 self.passengers를 초기화하면 된다. 아래 절 '객체의 깊은 복사와 얕은 복사'의 list(l1)처럼 다음 소스는 제대로 구현했다.
```
def __init__(self, passengers=None):
    if passengers is None:
        self.passengers = []
    else:
        self.passengers = list(passengers) #1
```
1. passengers 리스트의 사본을 만들거나, passengers가 리스트가 아닐 때는 리스트로 변환한다.

이제 TwilightBus 객체 안에서 passenger 리스트를 변경해도 TwilightBus 객체를 초기화하기 위해 전달한 인수에는 아무런 영향을 미치지 않는다. 게다가 융통성도 향상된다. list() 생성자가 모든 반복 가능한 객체를 받으므로, 튜플은 물론 집합이나 데이터베이스 결과 등의 반복 가능한 객체는 모두 passengers 매개변수에 사용할 수 있다. 관리할 리스트를 자체적으로 생성하므로 pick()과 drop() 메서드 안에서 사용하는 remove()와 append() 메서드 지원을 보장할 수 있다.
> 인수로 받은 객체를 메서드가 변경할 것이라는 의도가 명백하지 않은 한 클래스 안에서 인수를 변수에 할당함으로써 인수 객체에 별명을 붙이는 것에 대해 주의할 필요가 있다. 불명확한 경우에는 사본을 만들어라. 여러분이 만든 클래스를 사용하는 프로그래머들의 행복도가 향상될 것이다.
