<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-1/UML_class_diagram.png)
 -->
# 코루틴은 제너레이터에서 어떻게 진화했는가?
코루틴의 기반 구조는 파이썬 2.5(2006년)에 구현된 'PEP 342 - 향상된 제너레이터를 통한 코루틴' 제안서 (https://www.python.org/dev/peps/pep-0342/) 에 설명되어 있다. 이때부터 yield 키워드를 표현식에 사용할 수 있게 되었으며, send()메서드가 제너레이터 API에 추가되었다. 제너레이터의 호출자는 send()를 이용해서 제너레이터 함수 내부의 yield 표현식의 값이 될 데이터를 전송할 수 있다. 이렇게 제너레이터가 호출자에 데이터를 생성해주고 호출자로부터 데이터를 받으면서 호출자와 협업하는 프로시저인 코루틴이 된다.

PEP 342는 send() 메서드 외에 throw()와 close()를 추가했다. throw() 메서드는 제너레이터 내부에서 처리할 예외를 호출자가 발생시킬 수 있게 해주며, close() 메서드는 제너레이터가 종료되도록 만든다. 이 기능은 다음 절과 16.5절 '코루틴 종료와 예외 처리'에서 설명한다.

최근 코루틴으로의 혁신적인 진화는 파이썬 3.3(2012년)에서 구현된 'PEP 380 - 하위 제너레이터에 위임하기 위한 구문' 제안서 (https://www.python.org/dev/peps/pep-0380/) 에 기술되어 있다. PEP 380은 제너레이터 함수에 다음과 같이 두 가지 구문 변경을 정의해서 훨씬 더 유용하게 코루틴으로 사용할 수 있도록 만들었다.
* 제너레이터가 값을 반환할 수 있다. 이전에는 제너레이터에서 return 문으로 값을 반환하면 SytaxError가 발생했다.
* 기존 제너레이터가 하위 제너레이터에 위임하기 위해 필요했던 수많은 판에 박힌 코드를 사용할 필요 없이, yield from 구문을 이용해서 복잡한 제너레이터를 더 작은 내포된 제너레이터로 리팩토링할 수 있게 한다.

최신 변경 내용은 16.6절 '코루틴에서 값 반환하기'와 16.7절 'yield from 사용하기'에서 자세히 설명한다.

이제 이 책의 확고한 전통을 따라 먼저 기본적인 사실을 설명하고, 예제를 보여준 후, 점점 더 어려운 특징으로 넘어가보자.

# 코루틴으로 사용되는 제너레이터의 기본 동작

아래 에제는 코루틴의 동작을 보여준다.
```
def simple_coroutine(): #1
    print('-> corutine started')
    x = yield #2
    print('-> coroutine received:', x)

my_coro = simple_coroutine()
my_coro #3
# <generator object simple_coroutine at 0x100c2be10>
next(my_coro) #4
# -> coroutine started
my_coro.send(42) #5
# -> corotine recevied: 42
"""
Traceback (most recent call last): #6
 ...
StopIteration
```
1. 코루틴은 자신의 본체 안에 yield 문을 가진 일종의 제너레이터 함수로 정의된다.
2. yield를 표현식에 사용한다. 단지 호출자에서 데이터를 받도록 설계하면 yield는 값을 생성하지 않는다. yield 키워드 뒤에 아무런 표현식이 없을 때 값을 생성하지 않으려는 의도를 암묵적으로 표현한다.
3. 일반적인 제너레이터와 마찬가지로 함수를 호출해서 제너레이터 객체를 가져온다.
4. 제너레이터가 아직 실행되지 않았으므로 yield 문에서 대기하지 않는다. 따라서 먼저 next()를 호출해서 제너레이터를 yield 문까지 실행함으로써 데이터를 전송할 수 있는 상태를 만든다.
5. 제너레이터의 send() 메서드를 호출해서 코루틴 본체 안의 yield 문의 값을 42로 만든다. 이제 코루틴이 실행을 재개해서 다음 yield 문이 나오거나 종료될 때까지 실행한다.
6. 여기서는 제어 흐름이 코루틴 본체의 끝에 도달하므로, 일반적인 제너레이터와 마찬가지로 StopIteration예외를 발생시킨다.

코루틴은 네 가지 상태를 가진다. inspect.getgeneratorstate() 함수를 이용해서 현재 상태를 알 수 있다(이 함수는 네 가지 상태 중 하나를 반환한다).

---

**'GEN_CREATED'**
실행을 시작하기 위해 대기하고 있는 상태

**'GEN_RUNNING'**
현재 인터프리터가 실행하고 있는 상태

**'GEN_SUSPENDE'**
현재 yield 문에서 대기하고 있는 상태

**'GEN_CLOSED'**
실행이 완료된 상태

---

send() 메서드에 전달한 인수가 대기하고 있는 yield 표현식의 값이 되므로, 코루틴이 현재 대기 상태에 있을 때는 my_coro.send(42)와 같은 형태로만 호출할 수 있다. 그러나 코루틴이 아직 기동되지 않은 상태(즉, 'GEN_CREATE' 상태)인 경우에는 send() 메서드를 호출할 수 없다. 그래서 코루틴을 처음 활성화하기 위해 next(my_coro)를 호출한다 (이 상태에서는 my_coro.send(None)을 호출해도 효과가 동일하다).

코루틴 객체를 생성하고 난 직후에 바로 None이 아닌 값을 전달하려고 하면 다음과 같은 오류가 발생한다.
```
my_coro = simple_coroutine()
my_coro.send(1729)
"""
Traceback (most recnet call last):
    File "<stdin>", line 1, in <module>
TypeError: can't send non-None value to a just-started generator
"""
```

에러 메세지를 통해 원인을 명확히 알 수 있다.

처음 next(my_coro)를 호출할 때, 코루틴을 '기동'한다고도 표현한다. 즉, 코루틴이 호출자로부터 값을 받을 수 있도록 처음 나오는 yield문까지 실행을 진행하는 것이다.

yield 문을 한 번 이상 호출하는 코드를 보면, 코루틴의 동작을 좀 더 명확히 이해할 수 있다. [예제 16-2]를 보자.

```
# 두 번 생성하는 코루틴
def simple_coro2(a):
    print('-> Started: a =', a)
    b = yield a
    print('-> Recevied: b =', b)
    c = yield a + b
    print('-> Received: c =', c)


my_coro2 = simple_coro2(14)
from inspect import getgeneratorstate
getgeneratorstate(my_coro2) #1
# 'GEN_CREATE'
next(my_coro2) #2
# -> Started: a = 14
# 14
getgeneratorstate(my_coro2) #3
'GEN_SUSPENDED'
my_coro2.send(28) #4
# -> Received: b = 28
# 42
my_coro2.send(99) #5
# -> Received: c = 99
"""
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
StopIteration
"""
getgeneratorstate(my_coro2) #6
# 'GEN_CLOSED'
```
1. inspect.getgeneratorstate()가 'GEN_CREATED'를 반환하므로 아직 실행되지 않았음을 알 수 있다.
2. 첫 번째 yield 문까지 진행하면서 '-> Started: a = 14' 메시지를 출력하고 a의 값을 생성한 후 b에 값이 할당될 때까지 대기한다.
3. inspect.getgeneratorstate()가 'GEN_SUSPENDED'를 반환한다. 즉, 코루틴이 yield 문에서 대기하고 있는 상태다.
4. 중단된 코루틴에 28이라는 숫자를 보낸다. yield 문의 값이 28로 평가되고 이 값은 b에 할당된다. '-> Received: b = 28' 메시지가 출력되고, a + b의 값(42)이 생성된다. 그리고 코루틴은 c에 할당할 값을 기다리기 위해 중단한다.
5. 중단된 코루틴에 숫자 99를 보낸다. yield 문은 99로 평가되어 c 변수에 바인딩된다. '-> Received: c = 99'메시지를 출력하고 나서 코루틴이 종료되므로 제너레이터 객체가 StopIteration 예외를 발생시킨다.
6. inspect.getgeneratorstate()가 'GEN_ClOSED'를 반환하므로 코루틴 실행이 완료된 상태다.

코루틴 실행은 yield 키워드에서 중단됨을 잘 알고 있어야 한다. 앞에서 설명한 것처럼 할당문에서는 실제 값을 할당하기 전에 = 오른쪽 코드를 실행한다. 즉, b = yield a와 같은 코드에서는 나중에 호출자가 값을 보낸 후에야 변수 b가 설정된다. 이러한 방식에 익숙해지려면 신경을 더 써야 하지만, 이 방식을 제대로 알고 있어야 뒤에서 설명할 비동기 프로그래밍에서 yield의 용법을 이해할 수 있다.

아래 그림에서 보는 것처럼 simple_coro2 코루틴의 실행은 세 단계로 나눌 수 있다.

1. next(my_coro2)는 첫 번째 메시지를 출력하고 yield a까지 실행되어 숫자 14를 생성한다.
2. my_coro2.send(28)은 28을 b에 할당하고, 두 번째 메시지를 출력하고, yield a + b까지 실행되어 숫자 42를 반환한다.
3. my_coro2.send(99)는 99를 c에 할당하고, 세 번째 메시지를 출력하고, 코루틴을 끝까지 실행시킨다.

![simple_coro2](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-1~2/simple_coro2.png)