<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-5~6/UML_class_diagram.png)
 -->
# 코루틴 종료와 예외 처리

코루틴 안에서 발생한 예외를 처리하지 않으면, next()나 send()로 코루틴을 호출한 호출자에 예외가 전파된다. 아래예제는 [coroaverager1.py](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-5~6/coroaverager1.py)의 데커레이트된 averager 코루틴을 사용한 예를 보여준다.

```
# 처리하지 않은 예외에 의한 코루틴 종료
from coroaverager1 import averager
coro_avg = averager()
coro_avg.send(40) #1
# 40.0
coro_avg.send(50)
# 45.0
coro_avg.send('spam') #2
"""
Traceback (most recent call last):
 ...
TypeError: unsupported operand type(s) for += 'float' and 'str'
"""
coro_avg.send(60) #3
"""
Traceback (most recent call last):
 File "<stdin>", line 1, in <module>
StopIteration
"""
```
1. @coroutine으로 데커레이트된 averager()를 사용하므로, 코루틴에 바로 값을 보낼 수 있다.
2. 비수치형 값을 보내면 코루틴 안에서 예외가 발생한다.
3. 코루틴 안에서 예외를 처리하지 않으므로 코루틴이 종료된다. 이후에 코루틴을 다시 활성화하려면 StopIteration 예외가 발생한다.

코루틴의 total 변수에 더할 수 없는 'spam'이라는 문자열을 전송했으므로 에러가 발생했다.

위 예제를 보면 종료하라고 코루틴에 알려주는 구분 표시를 전송해서 코루틴을 종료할 수 있음을 알 수 있다. None이나 Ellipsis와 같은 내장된 싱글턴 상수는 구분 표시로 사용하기 좋다. Ellipsis는 데이터 스트림에서 상당히 보기 드문 표시라는 장점도 있다. 그리고 필자는 StopIteration을 사용하기도 한다(객체가 아니라 클래스 자체를 사용한다). 즉, my_coro.send(StopIteration) 형태로 사용한다.

파이썬 2.5이후 제너레이터 객체는 호출자가 코루틴에 명시적으로 예외를 전달할 수 있게 해주는 thrwo()와 close() 메서드를 제공한다.

---

**generator.throw(exc_type[,exc_value[, traceback]])**
제너레이터가 중단한 곳의 yield 표현식에 예외를 전달한다. 제너레이터가 예외를 처리하면, 제어흐름이 다음 yield 문까지 진행하고, 생성된 값은 generator.throw() 호출 값이 된다. 제너레이터가 에외를 처리하지 않으면 호출자까지 예외가 전파된다.

**generator.close()**
제너레이터 실행을 중단한 yield 표현식이 GeneratorExit 예외를 발생시키게 만든다. 제너레이터가 예외를 처리하지 않거나 StopIteration 예외 (일반적으로 제너레이터가 실행을 완료할 때 발생한다)를 발생시키면, 아무런 에러도 호출자에 전달되지 않는다. GeneratorExit 예외를 받으면 제너레이터는 아무런 값도 생성하지 않아야 한다. 아니면 RuntimeError 예외가 발생한다. 제너레이터에서 발생하는 다른 예외는 모두 호출자에 전달된다.

---
> 제너레이터 객체 메서드에 대한 공식 문서는 파이썬 언어 깊은 곳 (6.2.9.1절 '제너레이터-반복자 메서드' 문서 (https://docs.python.org/3/reference/expressions.html#generator-iterator-methods))에 숨어 있다.

이제 close()와 throw()가 어떻게 코루틴을 제어하는지 알아보자. 아래예제는 잠시 후에 나올 에제에 사용할 demo_exc_handling() 함수를 보여준다.

- [coro_exc_demo.py](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-5~6/coro_exc_demo.py)
1. DemoException 예외를 따로 처리한다.
2. 예외가 발생하지 않으면 받은 값을 출력한다.
3. 이 코드는 결코 실행되지 않는다.

위 예제의 마지막 행은 도달할 수 없다. 위에 나온 무한 루프는 처리되지 않은 예외에 의해서만 중단될 수 있으며, 예외를 처리하지 않으면 코루틴의 실행이 중단되기 때문이다.

demo_exc_handling()의 일반적인 연산은 아래와 코드와 같다.
```
exc_coro = demo_exc_handling()
next(exc_coro)
# -> coroutine started
exc_coro.send(11)
# -> coroutine received: 11
exc_coro.send(22)
# -> corutine received: 22
exc_coro.close()
from inspect import getgeneratorstate
getgeneratorstate(exc_coro)
# 'GEN_CLOSED'
```
DemoException을 코루틴 안으로 던지면, 이 예외가 처리되어 demo_exc_handling() 코루틴은 아래 예제와 같이 계속 실행된다.

```
# DemoException을 demo_exc_handling() 안에 던져도 종료되지 않는다.
exc_coro = demo_exc_handling()
next(exc_coro)
# -> coroutine started
exc_coro.send(11)
# -> coroutine recevied: 11
exc_coro.throw(DemoException)
# *** DemoException handled. Countinuing...
getgeneratorstate(exc_coro)
# 'GEN_SUSPENDED'
```
한편 처리되지 않는 예외를 코루틴 안으로 던지면 아래 코드와 같이 코루틴이 중단되고, 코루틴의 상태는 'GEN_CLOSED'가 된다.
```
#자신에게 던져진 예외를 처리할 수 없으면 코루틴이 종료된다.
exc_coro = demo_exc_handling()
next(exc_coro)
# -> coroutine started
exc_coro.send(11)
# -> coroutine recevied: 11
exc_coro.throw(ZeroDivisionError)
"""
Traceback (most recent call last):
 ...
ZeroDivisionError
"""
getgeneratorstate(exc_coro)
# 'GEN_CLOSE'
```
코루틴이 어떻게 종료되든 어떤 정리 코드를 실행해야 하는 경우에는 아래에제 에서처럼 try/finally 블록 안에 코루틴의 해당 코드를 넣어야 한다.

- [coro_finally_demo.py](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-5~6/coro_finally_demo.py)
yield from 구조체가 파이썬 3.3에 추가된 이유 중 하나는 중첩된 코루틴에 예외를 던지는 것과 관련 있다. 그리고 코루틴에서 값을 좀 더 편리하게 반호나할 수 있게 하기 위한 이유도 있다.
다음 절에서 설명이 이어진다.

# 코루틴에서 값 반환하기
아래예제는 averager() 코루틴을 변형해서 값을 반환한다. 이 코루틴은 활성화할 때마다 이동 평균을 생성하지는 않는다. 의미 있는 값을 생성하지는 않지만 최후에 어떤 의미 있는 값을 반환하는(예를 들면 최중 합계를 반환하는 경우) 코루틴도 있음을 설명하기 위해서다.

아래예제의 averager()가 반환하는 결과는 namedtuple로서, 항목 수 (count)와 평균(averager)을 담고 있다. 그냥 average 값만 변환할 수도 있었지만, 튜플을 반환해서 누적된 데이터(항목 수)도 반환할 수 있음을 보여주고 싶었다.

- [coroaverager2.py](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-5~6/coroaverager2.py)
1. 값을 반환하려면 코루틴이 정상적으로 종료되어야 한다. 그렇기 때문에 이 averager 버전에서는 루프를 빠져나오는 조건을 검사한다.
2. count와 avaerger를 가진 namedtuple을 반환한다. 제너레이터 함수가 값을 반환하므로 파이썬 3.3 이전 버전에서는 이 구문에서 에러가 발생한다.

새로 만든 averager()가 어떻게 작동하는지 알아보기 위해 아래처럼 콘솔에서 실행해 볼 수 있다.
```
coro_avg = averager()
next(coro_avg)
coro_avg.send(10) #1
coro_avg.send(30)
coro_avg.send(6.5)
coro_avg.send(None) #2
"""
Traceback (most recent call last):
 ...
Stopiteration: Result(count=3, avaerge=15.5)
```
1. 이 버전은 값을 생성하지 않는다.
2. None을 보내면 루프를 빠져나오고 코루틴이 결과를 반환하면서 종료하게 된다. 일반적인 제너레이터 객체와 마찬가지로 StopIteration 예외가 발생한다. 예외 객체의 value 속성에는 반환된 값이 들어 있다.

return 문이 반환하는 값은 StopIteration 예외의 속성에 담겨 호출자에 밀반임됨에 주의하라. 약간 꼼수를 부렸지만, 실행이 완료되면 StopIteration 예외를 발생시키는 기존 제너레이터 객체의 작동 방식을 유지한다.

아래 에제는 코루틴이 반환한 값을 가져오는 방법을 보여준다.
```
coro_avg = averager()
next(coro_avg)
coro_avg.send(10)
coro_avg.send(30)
coro_avg.send(6.5)
try:
    coro_avg.send(None)
except StopIteration as exc:
    result = exc.value


result
# Result(count=3, average=15.5)
```
이 방법이 PEP 380에 정의되어 있고 yield from 구성체가 StopIteration 예외를 내부적으로 잡아서 자동으로 처리한다는 사실을 깨닫는다면, 코루틴에서 반환값을 가져오는 우회적인 방법이 타당하다는 생각이 들 것이다. 이것은 for 루프 안에서 StopIteration을 사용하는 방법과 비슷하다. 예외가 발생했다는 사실을 사용자가 모르도록 루프가 깔끔하게 처리한다. yield from의 경우 인터프리터가 StopIteration 예외를 처리할 뿐만 아니라 value 속성이 yield from 표현식의 값이 된다. 불행히도 이 과정은 콘솔에서 대화식으로 테스트할 수 없다. 함수 외부에서 yield from이나 yield를 사용하면 구문 에러가 발생하기 때문이다.

다음 절에서는 PEP 380에서 의도한 대로 결과를 생성하기 위해 averager() 코루틴을 yield from과 함께 사용하는 예를 보여준다.