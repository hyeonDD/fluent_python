<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-1/UML_class_diagram.png)
 -->
# 스레드와 코루틴 비교

스레드 및 GIL에 대해 설명하면서 미셸 시미오나토는 장시간 연산이 실행되는 동안 multiprocessing 패키지를 이용해서 콘솔에 '|/-\' 아스키 문자로 스피너 애니메이션을 보여주는 간단하고 재미있는 예제 (http://bit.ly/1Ox3vWA) 를 올렸다.

필자는 시미오나토의 예제를 살짝 수정했다. 먼저 threading 모듈의 스레드를 이용해서 구현한 후 다시 asyncio 모듈의 코루틴을 이용해서 구현함으로써 스레드 없이 코루틴이 동시 동작을 어떻게 하는지 코드를 비교해서 볼 수 있게 했다.

아래 spinner_thread.py 와 spinner_asyncio.py 스크립트를 실행하면 애니메이션을 볼 수 있으므로, 이 코드가 어떻게 작동하는지 알아보려면 실제로 코드를 실행해보는 것이 좋다. 만약 지하철에서 이 책을 보고 있다면 (혹은 와이파이로 연결되어 있지 않다면), 아래 그림을 보고 'thinking!'단어 앞의 \ 막대가 돌아가는 것을 상상해보라.

![spinner실행화면](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-1/spinner.png)

먼저 spinner_thread.py 스크립트를 살펴보자

- [spinner_thread.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-1/spinner_thread.py)
1. 이 클래스는 외부에서 스레드를 제어하기 위해 사용할 go 속성 하나만 있는 간단한 가변 객체를 정의한다.
2. 이 함수는 별도의 스레드에서 실행된다. signal 인수는 바로 앞에서 정의한 Signal 클래스의 객체를 받는다.
3. itertools.cycle()은 주어신 시퀀스를 순환하면서 끝없이 항목을 생성하므로, 이 for 루프는 사실상 무한 루프다.
4. 텍스트 모드 애니메이션 기법으로서, 문자열의 길이만큼 백스페이스 문자(\08)를 반복해서 커서를 앞으로 이동시킨다.
5. go 속성이 True가 아니면 루프를 빠져나온다.
6. 공백 문자로 덮어쓰고 다시 커서를 처음으로 이동해서 메시지 출력 행을 청소한다.
7. 실행에 시간이 오래 걸리는 함수라고 생각하자.
8. 주 스레드에서 sleep() 함수를 호출할 때 GIL이 해제되므로 두 번째 스레드가 진행된다.
9. 이 함수는 두 번째 스레드를 만들고, 스레드 객체를 출력하고, 시간이 오래 걸리는 연산을 수행하고 나서 스레드를 제거한다.
10. 두 번째 스레드 객체를 출력한다. <Thread(Thread-1, initial)>과 같은 형태로 출력된다.
11. 두 번째 스레드를 실행한다.
12. slow_function() 함수를 실행한다. 그러면 주 스레드가 블로킹되고, 그 동안 두 번째 스레드가 텍스트 스피너 애니메이션 만을 보여준다.
13. signal의 상태를 변경한다. 그러면 spin() 함수 안의 for 루프가 중단된다.
14. spinner 스레드가 끝날 때까지 기다린다.
15. supervisor() 함수를 실행한다.

파이썬에는 스레드를 종료시키는 API가 정의되어 있지 않음에 주의하라. 스레드에 메시지를 보내 종료시켜야 한다. 여기서는 signal.go 속성을 사용했다. 주 스레드가 이 속성을 False로 설정하면, spinner 스레드가 이 값을 확인하고 깔끔하게 종료한다.

이제 스레드 대신 @asyncio.coroutine을 이용해서 동일한 동작을 어떻게 구현할 수 있는지 알아보자.
> 16.10절 '요약'에서 설명한 것처럼 asyncio는 '코루틴'을 더욱 엄격히 정의한다. asyncio API에 사용할 코루틴은 본체 안에서 yield가 아니라 yield from을 사용해야 한다. 그리고 asyncio 코루틴은 yield from으로 호출하는 호출자에 의해 구동되거나, 이 장에서 설명할 asyncio.async() 등의 함수에 전달해서 구동해야 한다. 마지막으로, 예제에서 보여주는 것처럼 @asyncio.corutine 데커레이터를 코루틴에 적용해야 한다.

- [spinner_asyncio.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-1/spinner_asyncio.py)
1. asyncio에 사용할 코루틴은 @asyncio.coroutine으로 데커레이트해야 한다. 반드시 해야 하는 것은 아니지만, 되도록 사용하라고 권장한다. 코드 설명을 마친 뒤 이 데커레이터에 대해 알아본다.
2. 여기에서는 spinner_thread.py의 spin()함수에서 스레드를 종료하기 위해 사용했던 signal 인수가 필요 없다.
3. 이벤트 루프를 블로킹하지 않고 잠자기 위해 time.sleep(.1) 대신 yield from asyncio.sleep(.1)을 사용한다.
4. spin()이 깨어난 후 asyncio.CancelledError 예외가 발생하면, 취소가 요청된 것이므로 루프를 종료한다.
5. slow_function()은 이제 코루틴으로서, 코루틴이 잠자면서 입출력을 수행하는 체 하는 동안 이벤트 루프가 진행될 수 있게 하기 위해 yield from을 사용한다.
6. yield from asyncio.sleep(3) 표현식은 메인 루프의 제어 흐름을 처리하는데, 메인 루프는 잠자고 난후에 코루틴을 계속 실행한다.
7. 이제는 supervisor()도 코루틴이므로, yield from을 이용해서 slow_function()을 구동할 수 있다.
8. asyncio.async()는 spin() 코루틴의 실행을 스케줄링하고 Task 객체 안에 넣어, Task 객체를 즉시 반환한다.
9. Task 객체를 출력한다. <Task pending coro=<spin() running at spinner_asyncio.py:12>>와 같은 메시지와 출력한다.
10. slow_function() 함수를 구동해서 완료되면 반환된 값을 가져온다. 그러는 동안 이벤트 루프는 게속 실행된다. slow_function()이 궁극적으로 yield from asyncio.sleep(3)을 실행해서 메인 루프로 제어권을 넘기기 때문이다.
11. Task 객체는 cancel() 메서드를 호출해서 취소할 수 있다. 그러면 코루틴이 중단된 곳의 yield from에서 asyncio.CancelledError 예외가 발생한다. 코루틴은 예외를 잡아서 지연시키거나 취소 요청을 거부할 수 있다.
12. 이벤트 루프에 대한 참조를 가져온다.
13. supervisor() 코루틴을 구동해서 완료한다. 코루틴의 반환값은 run_until_complete() 메서드의 반환값이 된다.
> 주 스레드를 블로킹해서 이벤트 루프를 중단시키고 그래서 애플리케이션 전체를 멈추고 싶은 경우가 아니라면, 결코 asyncio 코루틴 안에서 time.sleep()을 호출하지 말라. 코루틴 안에서는 아무 것도 안 하고 잠시 시간을 보내고 싶으면 yield from asyncio.sleep(<초>)를 사용해야 한다.

반드시 @asyncio.coroutine 데커레이터를 사용해야 하는 것은 아니지만, 되도록이면 사용하라고 강력히 권고한다. @asyncio.coroutine은 코루틴을 일반 함수와 다르게 보이도록 만들며, 코루틴이 yield from되지 않고 (즉, 일부 작업이 완료되지 않았ㅇ므ㅡ로, 버그가 발생할 가능성이 높다) 가비지 컬렉트되는 경우 경고 메시지를 출력하므로 디버깅에 도움이 된다.
@asyncio.coroutine은 데커레이트된 제너레이터를 자동으로 기동하지 않는다.

spinner_thread.py와 spinner_asyncio.py의 소스 코드 길이가 거의 비슷하다는 점에 주목하라. supervisor()함수는 이 예제의 핵심이다. 이제부터 이 함수를 자세히 비교해보자ㅏ. 아래 예제는 스레드 예제에서 supervisor()함수만 가져온 것이다.
```
# spinner_thread.py: 스레드화된 supervisor() 함수
def supervisor():
    signal = Signal()
    spinner = threading.Thread(targer=spin,
                                args=('thinking!', signal))
    print('spinner object:', spinner)
    spinner.start()
    result = slow_function()
    signal.go = False
    spinner.join()
    return result
```

이와 비교하기 위해 아래 예제에서는 supervisor() 코루틴만 가져왔다.

```
#spinner_asyncio.py:비도기 supervisor() 코루틴
def supervisor():
    spinner = asyncio.ensure_future(spin('thinking!'))
    print('spinner object:', spinner)
    result = yield from slow_function()
    spinner.cancel()
    return result
```
이 두 supervisor() 함수의 주요 차이점을 정리하면 다음과 같다.
* asyncio.Task는 threading.Thread와 거의 대등하다. 이 장의 특별 테크니컬 리뷰어인 빅터 스터너에 의하면 Task는 gevent 같은 협업적 멀티태스킹을 구현하는 라이브러리에서의 그린 스레드와 같다.
* Task는 코루틴을 구동하고, Thread는 콜러블을 호출한다.
* task 객체는 직접 생성하지 않고, 코루틴을 asyncio.async()나 loop.create_task()에 전달해서 가져온다.
* Task 객체를 가져오면, 이 객체는 이미 asyncio.async()등에 의해 실행이 스케줄링되어 있다. Thread객체는 start() 메서드를 호출해서 실행하라고 명령해야 한다.
* 스레드화된 supervisor()에서 slow_function()은 평범한 함수로서, 스레드에 의해 직접 호출된다. 비동기 supervisor()에서 slow_function()은 yield from으로 구동하는 코루틴이다.
* 스레드는 외부에서 API를 이용해서 중단시킬 수 없다. 스레드는 아무 때나 중단시키면 시스템 상태의 무결성이 훼손되기 때문이다. Task에는 코루틴 안에서 CancelledError를 발생시키는 Task.cancel() 객체 메서드가 있다. 코루틴은 중단되었던 yield 문에서 예외를 잡아서 처리할 수 있다.
* supervisor() 코루틴은 main() 함수 안에서 loop.run_until_complete()로 실행해야 한다.

이렇게 익숙한 threading 모듈과 하나하나 비교하면, asyncio가 동시성 작업을 어떻게 지휘하는지 이해하는 데 도움디 된다.

스레드와 코루틴의 비교와 관련해서 마짐가으로 한 가지만 더 이야기하자. 스레드로 복잡한 프로그램을 구현해봤다면 스케줄러가 언제든 스레드를 중단시킬 수 있으므로 프로그램을 분석하는 작업이 얼마나 힘든지 잘 알 것이다. 프로그램의 크리티컬 섹션을 보호하기 위해 락을 잠그고, 여러 단계의 작업을 수행하는 도중에 인터럽트되지 않게 해야 한다. 크리티컬 섹션 도중에 인터럽트되면 데이터가 잘못된 상태에 놓일 수 있기 때문이다.

코루틴의 경우, 모든 것이 기본적으로 인터럽트로부터 보호된다. 명시적으로 yield를 실행해야 프로그램의 다른 부분이 실행된다. 여러 스레드의 연산을 동기화하기 위해 락을 잠그는 대신, 언제든 실행되고 있는 코루틴 중 하나만 사용하면 된다. 그리고 제어권을 넘겨주고 싶을 때는 yield나 yield from을 이용해서 스케줄러에 넘겨줄 수 있다. 그렇기 때문에 코루틴은 안전하게 취소할 수 있다. 코루틴은 yield 지점에서 중단되었을 때만 취소할 수 있다고 정의되어 있으므로, 단지 CancelledError 예외를 처리해서 마무리하면 된다.

이제 asyncio.Future 클래스가 17장에서 본 concurrent.futures.Future 클래스와 어떻게 다른지 알아보자.

## asyncio.Future: 논블로킹 설계
asyncio.Future와 concurrent.futures.Future 클래스는 인터페이스와 거의 같지만, 다르게 구현되어 있으므로 서로 바꿔 쓸 수 없다. 'PEP-3156 - 비동기 입출력 지원 재시동: asyncio 모듈' (https://www.python.org/dev/peps/pep-3156/) 은 이런 불행한 상황에 대해 다음과 같이 이야기한다.

**언젠가 concurrent.futures.Future에 __iter__() 메서드를 추가해서 yield from에 사용할 수 있게 하는 등 asyncio.Future와 concurrent.futures.Future를 통합할 수도 있다.**

17.1.3절 'Future는 어디에 있나?'에서 이야기한 것처럼 Future는 실행할 코드를 스케줄링해야 생성한다. asyncio에서 BaseEventLoop.create_task() 메서드는 코루틴을 받아서 실행하기 위해 스케줄링하고, asyncio.Task 객체를 반환한다. Task는 코루틴을 래핑하기 위해 설계된 Future의 서브클래스이므로, Task 객체는 Future 객체이기도 하다. 이 과정은 Executor.submit()을 호출해서 concurrent.futures.Future 객체를 생성하는 방법과 비슷하다.

단짝인 concurrent.futures.Future 클래스와 마찬가지로 asyncio.Future 클래스도 done(), add_done_callback(), result() 등의 메서드를 제공한다. 앞의 두 메서드는 17.1.3절 'Future는 어디에 있나?'에서 설명한 대로 작동하지만, result()는 아주 다르다.

asyncio.Future에서 result() 메서드는 인수를 받지 않으므로 시간초과를 지정할 수 없다. 그리고 아직 실행이 완료되지 않은 Future 객체의 result() 메서드를 호출하면, 결과를 기다리느라 블로킹되는 대신 asyncio.InvalidStateError 예외가 발생한다.

그러나 asyncio.Future에서 결과를 가져오기 위해서는 [예제 18-8]처럼 일반적으로 yield from을 이요한다.

Future 객체에 yield from을 호출하면 이벤트 루프를 블로킹하지 않고 작업 완료를 기다리는 과정을 자동으로 처리해준다. asyncio에서 yield from은 이벤트 루프에 제어권을 넘겨주기 위해 사용하기 때문이다. Future 객체에 yield from을 사용하는 것은 코루틴에 add_done_callback() 함수를 호출하는 것과 비슷하다. 콜백을 호출하지 않고 지연된 작업이 완료되면, 이벤트 루프는 Future 객체의 결과를 설정하고 yield from 표현식은 지연된 코루틴 내부에서 반환된 값을 생성하고 실행을 계속 진행한다.

정리하면, asyncio.Future는 yield from과 함께 사용하도록 설계되었으므로 다음과 같은 메서드가 필요 없다.
* 코루틴 안에서 my_future가 실행을 완료한 다음에 수행할 작업은 단순히 yield from my_future 뒤에 넣으면 되므로 my_future.add_done_callback()을 호출할 필요가 없다. 이것은 중단했다가 재개할 수 있는 함수라는 코루틴의 커다란 장점이다.
* my_future에 대한 yield from 표현식의 값이 result가 되므로(예를 들면 result = yield from my_future) my_future.result()를 호출할 필요 없다.

물론 done(), add_done_callback(), result() 메서드가 필요한 경우도 있지만, 일반적으로 asyncio의 Future 객체는 이런 메서드를 호출하지 않고, yield from으로 구동된다.

이제 yield from과 asyncio API가 Future, Task, 코루틴을 어떻게 통합하는지 알아보자.

## Future, Task, 코루틴에서 생성하기
asyncio에서는 yield from을 이용해서 asyncio.Future 객체의 결과를 가져올 수 있으므로 Future와 코루틴의 고나계는 밀접하다. 이는 foo()가 코루틴 함수거나(즉, 호출되면 코루틴 객체를 반환한다), Future나 Task 객체를 반환하는 일반 함수면, res = yield from foo() 코드가 작동한다는 것을 의미한다.

그렇기 때문에 asyncio API에서 코루틴과 Future 객체를 바꿔가면서 쓸 수 있는 경우가 많다.

실행하려면 반드시 코루틴을 스케줄링해야 하며, 그러고 나서 코루틴이 asyncio.Task 객체 안에 래핑된다. 코루틴을 받아서 Task 객체를 가져오기 위해서는 주로 다음과 같은 두 가지 방법을 사용한다.

---

**asyncio.async(coro_or_futre,*,loop=None)**
이 함수는 코루틴과 Future 객체를 통합한다. 첫 번째 인수로는 둘 중 아무거나 올 수 있다. Future나 Task 객체면 그대로 반환한다. 코루틴이면 async()가 loop.create_task()를 호출해서 Task를 생성한다. loop 키워드 인수에 이벤트 루프를 전달할 수도 있다. 생략하면 async()가 asyncio.get_event_loop()를 호출해서 루프 객체를 가져온다.

**BaseEventLoop.create_task(coro)**
이 메서드는 코루틴을 실행하기 위해 스케줄링하고 asyncio.Task 객체를 반환한다. Tornado 등의 외부 라이브러리에서 제공하는 BaseEventLoop의 서브클래스에 호출하면, 외부 라이브러리에서 제공하는 Task와 호환되는 클래스의 객체가 반환될 수도 있다.

---

> BaseEventLoop.create_task() 는 파이썬 3.4.2부터 사용할 수 있다. 파이썬 3.3이나 3.4등 이전 버전의 파이썬을 사용하고 있다면 asyncio.async()를 사용하거나, PyPI (https://pypi.python.org/pypi/asyncio) 에서 asyncio 최신 버전을 설치해야 한다.

내부적으로 asyncio.async()를 이용해서 받은 코루틴을 자동으로 asyncio.Tsak 객체 안에 래핑하는 asyncio 함수들이 많이 있다. 그중 대표적인 것이 BaseEventLoop.run_until_complete()다.

파이썬 콘솔이나 간단한 테스트에서 Future 객체나 코루틴을 실험하고 싶다면 다음 코드를 사용한다.
```
import asyncio
def run_sync(coro_or_future):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro_or_future)

a = run_sync(some_coroutine())
```
코루틴, Future, Task의 관계는 asyncio 문서의 18.5.3절 '테스크와 코루틴 (https://docs.python.org/3/library/asyncio-task.html) 에서 다음과 같이 설명하고 있다.

**이 문서에는 Future 객체를 반환하는 평범한 파이썬 함수임에도 불구하고 코루틴이라고 부르는 메서드들이 종종 있다. 이것은 의도적인 것으로서, 향후에 이 함수들의 구현을 변경할 여지를 남겨두고자 한 것이다.**

기본적인 사항을 어느 정도 설명했으니, 이제[예제 17-1]에서 순차 및 스레드 풀 스크립트와 함계 테스트했던,비동기식으로 국기 이미지를 내려받는 flags_asyncio.py 스크립트의  소스코드를 살펴보자.