<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-4/UML_class_diagram.png)
 -->
# asyncio 내려받기 스크립트 개선
17.5절 '진행 상황 출력하고 에러를 처리하며 내려받기'에서 flags2 예제들은 동일한 명령행 인터페이스를 공유했다. 이 절에서 분석할 flags2_asyncio.py도 마찬가지다. 예를 들어 아래 예제 flags2_asyncio.py는 ERROR 서버에서 100개의 동시 요청(-m 100)을 이용해서 100개의 국기 이미지(-al 100)를 내려받는 방법을 보여준다.

```
python3 flag2_asyncio.py -s ERROR -al 100 -m 100
"""
ERROR site: http://localhost:8003/flags
Searching for 100 flags: from AD to LK
100 concurrent connections will be used.
-------------------
73 flags downloaded.
27 errors.
Elapsed time: 0.64s
"""
```
> **동시성 클라이언트를 테스트할 때는 책임성 있는 행동을**</br>스레드 버전과 비동기 버전의 전체적으로 내려받는 시간은 그리 다르지 않지만, asyncio는 요청을 더 빨리 보내므로 서버가 Dos 공격으로 의심할 가능성이 더 높다. 이 동시성 클라이언트를 최대 속도로 테스트해보고 싶다면 내려받은 에제 파일 중 17-futures/contries/README.rst에 설명한 대로 지역 HTTP 서버를 설정하라.

이제 flags2_asyncio.py가 어떻게 구현되어 있는지 살펴보자.

## asyncio.as_completed() 사용하기
[flags_asyncio.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-2/flags_asyncio.py)에서는 코루틴의 리스트를 asyncio.wait()에 전달했다. 그러면 loop.run_until.complete()에 의해 구동되는 await()는 내려받는 작업들이 모두 완료된 후 결과를 반환한다. 다행이도 [예제 17-14]진행 막대를 이용한 스레드 풀 예제에서 사용한 as_completed() 제너레이터 함수에 해당되는 asyncio용 버전이 있다.

asyncio를 이용해서 flags2 예제를 구현하려면 concurrent.futures 버전이 재사용하는 여러 함수를 수정해야 한다. asyncio 프로그램에는 주 스레드가 하나만 있고 주 스레드에서 이벤트 루프를 실행하므로, 주 스레드 안에서 블로킹 함수를 호출하면 안 되기 때문이다. 그래서 모든 네트워크 접속에서 yield from을 사용하기 위해 get_flag() 함수를 수정해야 했다. 이제 get_flag()가 코루틴이 되었으므로, download_one()이 get_flag()를 yield from으로 구동해야 한다. 따라서 download_one() 자체도 코루틴이 된다.[flags_asyncio.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-2/flags_asyncio.py)에서는 download_one()을 asyncio.wait()안에 래핑하고 loop.run_until_complete()에 전달함으로써 결국 download_many()가 download_one()을 구동했다. 이제는 진행 상황을 보여주고 에러를 처리하기 위해 더 세셋히 제어해야 하므로, 대부분의 논리를 download_many()에서 새로 만든 downloader_coro() 코루틴으로 옮기고 download_many()는 단지 이벤트 루프를 생성하고 downloader_coro()를 스케줄링할 뿐이다.

아래 예제는 get_flag()와 download_one()이 정으된 flags2_asyncio.py의 앞부분을 보여준다. downloader_coro()와 download_many()등 나머지 코드는 [예제 18-8]에 있다.

- [flags2_asyncio_front.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-4/flags2_asyncio_front.py)
1. 다른 HTTP와 네트워크 예외를 래핑하고 에러를 보고하기 위해 국가 코드를 보관하는 예외 클래스를 새로 정의한다.
2. get_flag()는 내려받은 이미지 파일의 크기를 바이트 단위로 넘겨주고나, HTTP 응답 상태가 404일 때는 web.HTTPNotFound 예외를, 나머지 HTTP 에러 코드에 대해서는 aiohttp.HttpProcessingError예외를 발생시킨다.
3. semaphore 인수는 asyncio.Semaphore (http://bit.ly/1f6Csp8) 객체로서, 동시 요청 수를 제한하기 위한 동기화 장치다.
4. semaphore를 yield from 표현식의 콘텍스트 관리자로 사용하므로, 시스템 전체가 블로킹되지 않게 한다. 단지 semaphore 카운터가 최대 허용 수에 이르렀을 때만 코루틴이 브로킹된다.
5. 이 with 문장을 빠져나올 때, semaphore 카운터가 감소되고, 이 세마포어 객체를 기다리고 있던 다른 코루틴 객체가 진행되도록 한다.
6. 이미지 파일을 찾을 수 없을 때는 HTTPStatus.not_found를 status로 설정한다.
7. 그 외 나머지 예외는 국가 코드 및 'PEP 3134 - 예외 체이닝과 내장된 역추적' 제안서 (https://www.python.org/dev/peps/pep-3134/) 에 정의된 raise X from Y 구문을 이용해서 연결된 원래 예외를 담은 FetchError로 만들어 전파한다.
8. 이 함수가 실제로 국기 이미지를 디스크에 저장한다.

위예제에서는 get_flag()와 download_one() 함수가 순차 버전과 상당히 많이 달라졌다. 비동기식으로 호출하기 위해 이 함수들이 이제는 yield from을 사용하는 코루틴이 되었기 때문이다.

지금 분석하고 있는 종류의 네트워크 클라이언트는 서버에 너무 많은 동시 요청을 보내지 않도록 적절히 제한하는 매커니즘이 필요하다. 서버에 과부하가 걸리면 전반적인 성능이 떨어지기 때문이다. flags2_threadpool.py (예제 17-14) 에서는 download_many() 함수의 필수 인수인 max_workers를 concur_req로 설정해서 ThreadPoolExecutor 객체를 생성함으로써 스레드 풀에서 concur_req 개수만큼의 스레드만 시작하도록 제한했다. flags2_asyncio.py에서는 asyncio.Semaphore를 이용해서 제한한다. 이 세마포어는 downloader_coro()함수 (예제 18-8)에 의해 생성되어 download_one() 함수 (예제 18-7)의 semaphore 인수로 전달된다. 세마포어는 내부에 카운터를 가지고있는 객체로서 acquire() 코루틴 메서드를 호출할 때마다 감소하고, release() 코루틴 메서드를 호출할 때마다 증가한다. 초깃값은 downloader_coro()에서 다음과 같이 세마포어 객체를 생성할 때 설정된다.
```
semaphore = asyncio.Semaphore(concur_req)
```
카운터가 0보다 클 때는 acquire()를 호출해도 블로킹되지 않지만, 카운터가 0일 때 acquire()를 호출하면 다른 곳에서 release()를 호출해서 카운터를 증가시켜줄 때까지 블로킹된다. 예제 18-7에서는 acquire()나 release()를 직접 호출하지 않고, download_one()에 있는 다음 코드에서 세마포어를 콘텍스트 관리자로 사용한다.
```
with (yield from seaphore):
    image = yield from get_flag(base_url, cc)
```

이 코드는 concur_req보다 작거나 같은 수의 get_flags() 코루틴이 실행되도록 보장한다.

이제 프로그램의 나머지 코드를 아래 예제에서 살펴보자. 이전의 download_many() 함수 안에 있는 대부분의 기능이 downloader_coro() 코루틴으로 옮겨졌다는 점에 주의하라. asyncio.as_completed()에 의해 생성된 Future 객체들의 결과를 yield from을 이용해서 가져와야 하고, 그래서 as_completed()에 의해 생성된 Future 객체들의 결과를 yield from을 이용해서 가져와야 하고, 그래서 as_completed()를 코루틴이 호출해야 하기 때문이다. 그러나 download_many() 자체를 코루틴으로 바꿀 수는 없었다. flags2_common.py 모듈의 제일 마지막 줄에 있는 main() 함수에 download_many() 함수를 전달해야 하는데, main() 함수는 단지 일반 함수를 받을 뿐 코루틴을 받지 않기 때문이다. 따라서 downloader_coro() 코루틴을 만들어서 as_completed() 루프를 실행했으며, 이제 download_many()는 단지 이벤트 루프를 생성하고 downloader_coro()를 loop.run_until_complete()에 전달해서 downloader_coro()를 스케줄링하는 역할만 수행한다.

- [flags2_asyncio.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-4/flags2_asyncio.py)
1. 코루틴은 download_many()와 동일한 인수를 받지만, 일반 함수가 아니라 코루틴 함수이므로 main()에서 바로 호출할 수 없다.
2. 동시에 concur_req 개까지의 코루틴을 실행할 수 있게 해주는 세마포어(asynico.Semaphore)를 생성한다.
3. downlaod_one() 코루틴을 호출하는 코루틴 객체의 리스트를 생성한다.
4. 실행이 완료된 Future 객체를 반환하는 반복자를 가져온다.
5. 반복자를 tqdm() 함수에 래핑해서 진행 상태를 출력한다.
6. 완료된 Future 객체들을 반복한다. 이 루프는 [예제17-14]의 download_many()에 있는 루프와 아주 비슷하다. requests와 aiohttp HTTP 라이브러리의 차이점 때문에 예외 처리에 관련된 부분이 달라졌다.
7. asyncio.Future 객체의 결과를 가져올 때는 객체의 result() 메서드를 호출하는 것보다 yield from을 사용하는 것이 훨씬 더 쉽다.
8. download_one()에서 발생하는 모든 예외는 Fetcherror 객체 안에 래핑되어 있다.
9. FetchError 예외 안에서 에러가 발생한 국가 코드를 가져온다.
10. 원래 예외(__cause__)에서 오류 메시지를 가져오려 시도한다.
11. 원래 예외에서 에러 메시지를 발견할 수 없으면 연결된 예외 클래스명을 에러 메시지로 사용한다.
12. 결과를 합계에 추가한다.
13. 다른 버전의 프로그램과 마찬가지로 카운터를 반환한다.
14. download_many()는 단순히 코루틴 객체를 생성하고 run_until_complete()를 이용해서 이벤트 루프에 전달한다.
15. 모든 작업이 완료되면 이벤트 루프를 종료하고 카운터를 반환한다.

위 예제에서는 [flags_threadpool.py](https://github.com/hyeonDD/fluent_python/blob/master/Part17/ex17-1/flags_threadpool.py)와 달리 Future 객체와 코드 간에 매핑을 사용할 수 없다. asyncio.as_completed()가 반환한 Future 객체가 as_completed()를 호출할 때 전달한 객체와 동일하다고 장담할 수 없기 때문이다. asyncio 패키지는 우리가 제공한 Future 객체를 이와 동일한 결과를 생성하는 다른 객체로 대체하기 때문이다.

에러가 발생한 경우, 딕셔너리에 Future 객체를 키로 사용해서 국가 코드를 가져올 수 없으므로, [flags2_asyncio_front.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-4/flags2_asyncio_front.py)에서 본 것처럼 FetchError 예외를 직접 구현했다. FetchError는 네트워크 예외와 이에 관련된 국가 코드를 래핑하므로 상세 메시지 모드에서 에러와 함께 국가 코드를 리포트할 수 있다. 에러가 없다면 for 루프 제일 위에 있는 yield from future 표현식의 결과로 국가 코드를 가져올 수 있다.

이제 앞에서 봤던 flags2_threadpool.py와 기능상으로 동일한 asyncio 예제에 대한 설명을 마친다. 다음에는 flags2_asyncio.py를 개선하면서 asyncio에 대해 좀 더 파고들어가 보자. [flags2_asyncio_front.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-4/flags2_asyncio_front.py)를 설명하면서 save_flag()가 디스크 입출력을 수행하므로 비동기식으로 실행되어야 한다고 이야기 했을 것이다. 다음 절에서는 구현 방법을 설명한다.

## Executor를 이용해서 이벤트 루프 블로킹 피하기
파이썬 커뮤니티에서는 네트워크 지연이 훨씬 더 크다는 점을 근거로(위험한 가정이다). 지역 파일시스템 접근이 블로킹 연산이라는 점을 간과하는 성향이 있다. 이와 반대로 Node.js 프로그래머들은, 모든 파일시스템 함수가 콜백을 요구하므로, 디스크 입출력 지연 문제에 끊임없이 부딪치고 있다. 디스크 입출력을 블로킹 처리함으로써 수백만 CPU 사이클을 낭비함을 보여주는 

| 장치 | CPU 사이클 수 | 비례'체감'규모 |
| :--- | :--- | :--- |
| L1 캐시 | 3 | 3초 |
| L2 캐시 | 14 | 14초 |
| 램 | 250 | 250초 |
| 디스크 | 41,000,000 | 1.3년 |
| 네트워크 | 240,000,000 | 7.6년 |

를 보면, 디스크 입출력이 애플리케이션의 성능에 상당한 영향을 끼침을 알 수 있다.

[flags2_asyncio_front.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-4/flags2_asyncio_front.py)에서는 flag2_common모듈의 save_flag()가 블로킹 함수다. 스레드 버전 [flags_threadpool.py](https://github.com/hyeonDD/fluent_python/blob/master/Part17/ex17-1/flags_threadpool.py)에서 save_flag()는 download_one() 함수를 실행하는 스레드를 블로킹하지만, 이 스레드는 여러 작업자 스레드 중 하나일 뿐이다. 내부적으로 블로킹하는 입출력 함수들은 GIL을 해제하므로, 다른 스레드가 진행할 수 있다. 그러나 flag2_asyncio.py에서 save_flag()는 asyncio 이벤트 루프와 공유하는 유일한 스레드를 블로킹하므로, 파일을 저장하는 동안 애플리케이션 전체가 멈춘다. 이 문제의 해결책은 이벤트 루프 객체의 run_in_executor() 메서드다.

asyncio 이벤트 루프는 스레드 풀 실행자를 내부에 가지고 있으며 run_in_executor() 메서드에 실행할 콜러블을 전달할 수 있다. 우리 예제에서 이 기능을 사용하기 위해서는 아래 예제에서 보는 것처럼 download_one() 코루틴에서 몇 줄만 수정하면 된다.

- [flags2_asyncio_executor.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-4/flags2_asyncio_executor.py)
1. 이벤트 루프 객체에 대한 참조를 가져온다.
2. run_in_executor()의 첫 번째 인수는 실행자 객체다. 이벤트 루프의 기본 스레드 풀 실행자를 사용할 때는 None으로 지정한다.
3. 나머지 인수는 콜러블 및 콜러블이 받을 위치 인수다.

> 위 예제를 테스트했을 때, 저장할 이미지 파일들이 평균 13KB의 작은 파일들이어서 run_in_executor()를 사용해도 성능이 눈에 띌 정도로 향상되지 않았다. 그러나 저장할 파일의 크기가 10배가 되도록 flags2_common.py의 save_flag() 함수를 수정하면(간단히 fp.write(img)를 fp.write(img*10)으로 변경하면 된다) 향상 정도가 눈에 띌 것이다. 파일의 크기가 평균 130KB 정도 되면 run_in_executor()를 사용하는 효과가 잘 드러난다. 수백만 픽셀의 이미지 파일을 내려받을 때는 속도가 더 많이 향상될 것이다.

완전히 독립적인 요청을 처리할 때보다 비동기식 요청을 조정하고 관리해야 할 때, 콜백 대신 코루틴을 사용하는 장점이 두드러지게 나타난다. 다음 절에서는 이런 형태읨 ㅜㄴ제 및 이에 대한 해결책에 대해 알아본다.
