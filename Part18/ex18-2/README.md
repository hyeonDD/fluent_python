<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-2/UML_class_diagram.png)
 -->
# asyncio와 aiohttp로 내려받기

파이썬 3.4에서 asyncio는 TCP와 UDP만 직접 지원한다. HTTP 등의 프로토콜을 지원하려면 서드파티 패키지가 필요하다. 현재 비동기 HTTP 클라이언트/서버를 구현하는 사람들은 모두 aiohttp를 사용하는 것 같다.

아래예제는 국기 이미지를 내려받는 flags_asyncio.py 스크립트의 전체 소스 코드다. 코드의 전반적인 흐름은 다음과 같다.
1. download_one()을 호출해서 생성된 여러 코루틴 객체를 이벤트 루프에 넣어 download_many() 안에서 프로세스를 시작한다.
2. asyncio 이벤트 루프는 각각의 코루틴을 차례대로 활성화한다.
3. get_flag() 등의 클라이언트 코루틴이 aiohttp.request() 등의 라이브러리 코루틴에 위임하기 위해 yield from을 사용하면, 제어권이 이벤트 루프로 넘어가서, 이벤트 루프가 이전에 스케줄링된 다른 코루틴을 실행할 수 있게 된다.
4. 블로킹된 연산이 완료되었을 때 통지받기 위해, 이벤트 루프는 콜백에 기반한 저수준 API를 사용한다.
5. 연산이 완료되면 메인 루프는 결과를 중단된 코루틴에 보낸다.
6. 그러고 나면 코루틴이 예를 들면 get_flag()의 yield from resp.read()와 같은 다음 yield from문으로 넘어간다. 이제 이벤트 루프가 다시 제어권을 가져오고, 종료될 때까지 4, 5, 6단계를 반복한다.

이 과정은 16.9.2절 '택시 집단 시뮬레이션'에서 메인 루프가 여러 택시 프로세스를 차례대로 실행했던 예제와 비슷하다. 각 택시 프로세스가 yield를 실행하면, 메인 루프는 그 택시에 대한 다음 이벤트를 스케줄링하고, 계속해서 큐에 들어 있는 다음 택시를 활성화한다. 택시 시뮬레이션은 훨씬 더 단순하므로 메인 루프를 쉽게 이해할 수 있다. 그러나 전체 흐름은 asyncio에서도 동일하다. 단지 메인 루프가 큐에 들어 있는 코루틴을 하나씩 활성화하는 단일 스레드 프로그램일 뿐이다. 각 코루틴이 몇 단계 진행하고 나서, 메인 루프에 제어권을 넘기고, 그러고 나면 메인 루프가 큐에 들어 있는 다음 코루틴을 활성화한다.

이제 아래소스코드의 코드를 하나하나 살펴보자.

- [flags_asyncio.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-2/flags_asyncio.py)
1. aiohttp는 기본 라이브러리에 들어 있지 않으므로 별도로 설치해야 한다.
2. flags 모듈(에제 17-2)에서 구현한 일부 함수를 재사용한다.
3. 코루틴은 @asyncio.coroutine으로 데커레이트해야 한다.
4. 블로킹 연산은 코루틴으로 구현되었고, yield from을 이용해서 이 코루틴에 위임하면, 코루틴이 비동기식으로 실행한다.
5. 응답 내용을 읽는 것은 별도의 비동기 연산에서 구현한다.
6. yield from을 사용하는 download_one() 함수도 코루틴이어야 한다.
7. 단어들을 yield from으로 가져온다는 것이 순차 버전의 download_one()과의 유일한 차이점이다. 이 함수의 나머지 부분은 기존과 완전히 동일하다.
8. 하위 이벤트 루프 구현에 대한 참조를 가져온다.
9. 국기 이미지를 가져올 때마다 download_one() 함수를 호출해서 제너레이터 객체 리스트를 생성한다.
10. 이름에도 불구하고 wait()는 블로킹 함수가 아니다. 일종의 코루틴으로서 자신에게 전달된 코루틴들이 모두 완료되면 완료된다(이것이 바로 wait()의 기본 작동 방식이다. 소스 코드 설명을 마치고 나서 자세히 설명한다).
11. wait_coro()가 완료될 때까지 이벤트 루프를 실행한다. 이 부분은 이벤트 루프가 실행하는 동안 블로킹된다.
12. 이벤트 루프를 종료한다.
> 이벤트 루프 객체가 콘텍스트 관리자면 with 블록을 이용해서 이벤트 루프 종료를 보장할 수 있으므로 좋을 것이다. 그러나 호출자 코드가 이벤트 루프를 직접 생성하지 않고 asyncio.get_event_loop()를 호출해서 이벤트 루프에 대한 참조를 가져오므로 상황이 복잡하다. 때로는 호출 코드가 이벤트 루프를 '소유'하지 않을 수도 있으므로 종료하면 안된다. 예를 들어 Qumash 패키지 (https://pypi.python.org/pypi/Quamash/) 를 이용해서 외부 GUI 이벤트 루프를 사용하는 경우에는 애플리케이션을 종료할 때 Qt 라이브러리가 이벤트 루프를 닫아야 한다.

asyncio.wait() 코루틴은 Future 객체나 코루틴의 반복형을 받고, wait()는 각 코루틴을 Task 안에 래핑한다. 결국 wait()가 관리하는 모든 객체는 Future 객체가 된다. wait()는 코루틴 함수이기 때문에 이를 호출하면 코루틴/제너레이터 객체가 반환된다. wait_coro 변수에 들어 있는 게 바로 wait()가 반환한 코루틴 제너레이터 객체다. 이 코루틴을 구동하기 위해 그것을 loop.run_until_complete()에 전달한다.

loop.run_until_complete() 함수는 Future 객체나 코루틴을 받는다. 코루틴을 받으면 wait()가 하는 것과 비슷하게 run_until_complete()도 코루틴을 Task 안에 래핑한다. 코루틴, Future, Task는 모두 yield from으로 구동할 수 있으며, 이것이 바로 wait()가 반환한 wait_coro 객체에 run_until_complete()가 하는 일이다. wait_coro는 실행이 완료되면 (<실행 완료된 Future들의 집합>, <실행이 완료되지 않은 Future들의 집합>) 튜플을 반환한다. [예제 18-5]에서 두 번째 집합은 언제나 공집합이므로 언더바(_)에 할당해서 명백히 무시한다. 그러나 wait()는 일부 Future 객체가 완료되지 않았더라도 반환하게 만드는 timeout과 return_when 키워드 전용 인수를 받는다. 자세한 사항은 asyncio.wait()문서 (http://bit.ly/1JIwZS2) 를 참조하라.

[예제 18-5]에서는 flags.py(예제 17-2)의 get_flag() 함수를 재사용할 수 없었다는 점에 주의하라. get_lfag() 함수는 블로킹 입출력을 수행하는 requests 라이브러리를 사용하기 때문이다. get_flag() 함수는 블로킹 입출력을 수행하는 requests 라이브러리를 사용하기 때문이다. asyncio를 활용하기 위해 네트워크에 접속하는 모든 함수를 yield from으로 호출하는 비동기 버전으로 바꿔서 제어권을 다시 이벤트 루프로 넘겨야 한다. get_flag()에서 yield from을 사용한다는 것은 get_flag()가 코루틴으로 구동되어야 한다는 것을 의미한다.

그렇기 때문에 flags_threadpool.py(예제 17-3)의 download_one() 함수도 재사용할 수 없었다. [예제 18-5]가 yield from으로 get_flag()를 구동하므로 download_one() 자체도 코루틴이다. 매번 요청할 때마다 download_one() 코루틴 객체가 download_many() 안에서 생성되고, 이 코루틴 객체는 asyncio.wait() 코루틴에 의해 래핑된 후, 모두 loop.run_until_complete() 함수에 의해 구동된다.

asyncio에 대해 알야 할 새로운 개념이 많지만, 귀도 반 로섬이 제안한 비결을 사용하면 flags_asyncio.py의 전반적인 논리를 쉽게 이해할 수 있다. 바로 '실눈을 뜨고 보면서 yield from 키워드가 없는 것처럼 생각'하면 된다. 이렇게 하면 처음 구현한 평범한 순차 버전의 코드처럼 읽기 쉬워진다.

예를 들어 다음과 같은 코루틴이 있다고 가정하자.
```
@asyncio.coroutine
def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = yield from aiohttp.request('GET', url)
    image = yield from resp.read()
    return image
```
위 코드는 블로킹되지 않는다는 점을 제외하면 다음 코드와 똑같이 작동한다.
```
def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = aiohttp.request('GET', url)
    image = resp.read()
    return image
```
yield from foo 구문을 사용하면 현재의 코루틴(즉, yield from 코드가 있는 대표 제너레이터)이 중단되지만, 제어권이 이벤트 루프로 넘어가고 이벤트 루프가 다른 코루틴을 구동할 수 있게 되므로, 블로킹되지 않는다. foo가 Future 객체이든 코루틴이든 이 객체가 완료되면, 결과를 중단된 코루틴으로 반환해서 실행을 계속하게 만든다.

16.7절 'yield from 사용하기'의 끝부분에서 yield from의 사용법에 대한 두 가지 사실을 이야기했다. 여기서 다시 요약하면 다음과 같다.
* yield from으로 연결된 전체 코루틴 체인은 궁극적으로 가장 바깥쪽에 있는 대표 제너레이터의 next()나 send()를 명시적 혹은 암묵적(for 루프에 사용하는 경우)으로 호출하는 비코루틴 호출자에 의해 구동된다.
* 이 체인 가장 안쪽에 있는 하위 제너레이터는 단지 yield를 사용하는 단순 제너레이터이거나 반복형 객체이여야 한다.

asyncio API와 함꼐 yield from을 사용할 때도 이 사실은 유효하며, 다음과 같은 특징이 있다.
* 우리가 만든 코루틴 체인은 언제나 가장 바깥쪽 대표 제너레이터를 loop.run_until_complete() 등의 asyncio API에 전달함으로써 구동된다. 즉, asyncio를 사용할 때는 next()나 send() 메서드를 직접 호출해서 코루틴 체인을 구동하는 것이 아니라, asyncio 이벤트 루프가 처리하도록 해야 한다.
* 우리가 만든 코루틴 체인은 언제나 어떤 asyncio 코루틴 함수나 코루틴 메서드([spinner_asyncio.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-1/spinner_asyncio.py)의 yield from asyncio.sleep()), 혹은 상위 수준 프로토콜을 구현하는 라이브러리의 코루틴 ([flags_asyncio.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-2/flags_asyncio.py) get_flag() 코루틴 안의 resp = yield from aiohttp.request('GET', url)))에 yield from을 호출하면서 끝나야 한다. 즉, 가장 안쪽의 하위제너레이터는 우리가 만든 코드가 아니라, 실제로 입출력을 수행하는 라이브러리 함수여야 한다.

요약하자면, asyncio를 사용할 때 우리는 코루틴 체인을 만들며, 가장 바깥쪽 대표 제너레이터는 asyncio 자체에 의해 구동되며, 체인을 통해 궁극적으로 가장 안쪽에 있는 하위 제너레이터는 (aiohttp 등의 서드파티 라이브러리를 경유해서) asyncio 라이브러리가 제공하는 코루틴에 위임한다. 즉, asyncio 이벤트 루프가 코루틴 체인을 구동하고, 코루틴 체인은 결국 저수준 비동기 입출력을 수행하는 라이브러리 함수에서 끝난다.

이제 17장에서 제기한 다음 문제에 답할 준비가 된 것 같다.

**둘 다 단일 스레드로 실행되는데, 어떻게 flags_asyncio.py가 flags.py보다 5배나 빨리 실행될까?**