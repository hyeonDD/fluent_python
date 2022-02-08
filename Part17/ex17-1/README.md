<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part17/ex17-1/UML_class_diagram.png)
 -->
# 예제: 세 가지 스타일의 웹 내려받기

긴 지연 시간 동안 CPU 클록을 낭비하지 않기 위해 네트워크 입출력을 효율적으로 처리하려면 동시성을 이용해야 한다. 네트워크에서 응답이 오는 동안 다른일을 처리하는 것이 좋다.

동시성을 활용하는 방법을 코드로 보여주기 위해 여기서는 웹에서 20개 국가의 국기 이미지를 내려받는 간단한 프로그램을 3개 작성한다. 첫 번째 flags.py는 순차적으로 실행되므로 이전 이미지를 내려받아 디스크에 저장한 후 다음번 이미지를 내려받는다. 나머지 프로그램 두개는 동시에 내려받는다. 즉, 모든 이비지를 동시에 요청한 후 도착하는 대로 파일에 저장한다. flags_threadpool.py 스크립트는 concurrent.futures 패키지를 사용하는 반면, flags_asyncio.py 스크립트는 asyncio를 사용한다.

아래예제는 스크립트 세 개를 세 번 실행한 결과를 보여준다. 그리고 국기가 저장되는 동안 볼 수 있도록 73초 분량의 비디오를 유튜브 (https://www.youtube.com/watch?v=A9e9Cy1UkME) 에 올렸다. 프로그램이 CDN 서비스를 받고 있는 flupy.org에서 국기 이미지를 내려받으므로, 처음 실행할 때는 약간 느릴 수 있다. 아래 예제는 프로그램을 여러 번 실행해서 CDN 캐시에 이미지가 올라간 후에 얻은 결과다.

```
python3 flags.py
"""
BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN #1
20 flags downloaded in 7.26s #2
"""
python3 flags.py
"""
BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN #1
20 flags downloaded in 7.20s
"""
python3 flags.py
"""
BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN #1
20 flags downloaded in 7.09s
"""
python3 flags_threadpool.py
"""
DE BD CN JP ID EG NG BR RU CD IR MX US PH FR PK VN IN ET TR
20 flags downloaded in 1.37s #3
"""
python3 flags_threadpool.py
"""
EG BR FR IN BD JP DE RU PK PH CD MX ID US NG TR CN VN ET IR
20 flags downloaded in 1.60s #3
"""
python3 flags_threadpool.py
"""
BD DE EG CN ID RU IN VN ET MX FR CCD NG US JP TR PK BR IR PH
20 flags downloaded in 1.22s #3
"""
python3 flags_asyncio.py #4
"""
BD BR IN ID TR DE CN US IR PK PH FR RU NG VN ET MX EG JP CD
20 flags downloaded in 1.36s
"""
python3 flags_asyncio.py
"""
RU CN BR IN FR BD TR EG VN IR PH CD ET ID NG DE JP PK MX US
20 flags downloaded in 1.27s
"""
python3 flags_asyncio.py
"""
RU IN ID DE BR VN PK MX US IR ET EG NG BD FR CN JP PH CD TR #5
20 flags downloaded in 1.42s
"""
```
1. 실행하면 국기를 내려받은 순서대로 국가 코드와 실행된 시간을 출력한다.
2. flags.py가 20개의 이미지를 내려받는 데 평균 7.18초 걸렸다.
3. flags_threadpool.py의 평균 소요 시간은 1.40초다.
4. flag_asyncio.py의 평균 소요 시간은 1.35초다..
5. 국가 코드의 순서에 주의하라. 동시성을 지원하는 스크립트를 실행하면 매번 내려받는 순서가 달라진다.

여기서 동시성 스크립트 간의 성능 차이는 중요하지 않지만, 둘 다 순차적인 스크립트보다 5배 빠르다. 이런 간단한 작업에서도 차이가 난다. 만약 수백 개의 이미지를 내려받았다면, 동시성 스크립트는 순차적 스크립트보다 20배 이상 빨랐을 것이다.
> 공개된 웹 서버에 동시에 수많은 HTTP 요청을 보내 테스트하는 경우, 뜻하지 않게 일종의 서비스 거부 공격(DoS)을 하는 셈이 된다. 위 예제의 경우 단지 20개의 요청만 보내도록 하드코딩되어 있으므로 문제가 없지만, 상당한 부하를 주는 HTTP 클라이언트를 테스트하는 경우에는 서버를 직접 만드는 것이 좋다. 이 책의 예제 코드 중 17-futures/countries/README.rst (https://bit.ly/1JIsg2L) 는 별도의 지역 서버에 Nginx를 설정하는 방법을 설명한다.

위 예제에서 테스트한 스크립트 중 flags.py와 flags_threadpool.py의 소스 코드를 들여다보자. 세 번째 스크립트 flags_asyncio.py는 asyncio를 사용하므로 18장에서 설명한다. 여기에서 이 세 개의 스크립트를 테스트한 이유는, 스레드를 사용하든 asyncio를 사용하든 입출력 위주의 작업을 순차적으로 처리하는 것보다는 아주 빠르다는 것을 보여주기 위해서였다. 물론 동시성 코드도 제대로 구현해야 성능 향상 효과를 볼 수 있다.

이제 코드를 살펴보자.

flags.py에 그리 새로운 것은 없다. 단지 다른 스크립트와 비교를 하기 위한 기준선이며, 필자는 동시성 버전을 구현할 때 중복을 피하기 위해 이 코드를 하나의 라이브러리로 사용했다. 이제 concurrent.futures를 이용해서 다시 구현해보자.

## 순차 내려받기 스크립트
아래 flags.py 예제는 그리 흥미롭지는 않지만, 이 코드 대부분을 동시성 스크립트를 구현하는 데 다시 사용하므로, 주의해서 봐둘 필요가 있다.
> 아래 flags.py에서는 에러를 전혀 처리하지 않음을 명확히 해둔다. 나중에 예외도 처리하겠지만, 여기서는 동시성 스크립트와 비교하기 쉽도록 기본적인 코드 구조에만 집중하고자 한다.

- [flags.py](https://github.com/hyeonDD/fluent_python/blob/master/Part17/ex17-1/flags.py)
1. request 라이브러리를 임포트한다. 표준 라이브러리에 속해 있지 않으므로 관례에 따라 os, time, sys 표준 라이브러리 모듈을 먼저 임포트하고 나서 한 줄 띈 후에 임포트한다.
2. 인구가 많은 순서대로 나열한 20개 국가의 ISO 3166 국가 코드를 담은 리스트
3. 국기 이미지를 갖고 있는 웹사이트
4. 이미지를 저장할 지역 디렉터리
5. 단지 img(바이트 시퀀스)를 DEST_DIR 안의 filename으로 저장한다.
6. 국가 코드를 인수로 받아서 URL을 만들고 이미지를 내려받는다. 응답으로 내려받은 이진 시퀀스를 반환한다.
7. 문자열을 출력하고 sys.stdout.flush()를 호출해서 진행 상황을 한 줄에 출력한다. 일반적으로 파이썬은 개행 문자를 받기 전까지 문자열을 출력하지 않으므로 sys.stdout.flush()를 호출해서 stdout 버퍼에 남아 있는 내용을 모두 화면에 출력하게 만들어야 한다.
8. download_many()는 동시성 버전과 다른 핵심 부분이다.
9. 국가 코드를 알파벳순으로 반복해서, 출력할 때 순서대로 나오도록 만든다. 내려받은 나라 수를 반환한다.
10. main() 함수는 download_many()를 실행하는 데 걸린 시간을 기록하고 출력한다.
11. main()은 내려받을 때 사용할 함수를 인수로 받아야 한다. main()은 내려받기에 사용할 함수들을 인수로 받는 일종의 라이브러리 함수로서, 동시성 버전에서는 download_many()의 동시성 버전을 호출하면 된다.
> 캐네스 레이츠가 만든 requests 라이브러리는 PyPI (https://pypi.python.org/pypi/requests) 에서 내려받을 수 있으며, 파이썬 3 표준 라이브러리에서 제공하는 urllib.request 모듈보다 강력하고 사용하기 쉽다. 사실 requests 라이브러리는 더 파이썬스러운 API다. 파이썬 2의 urllib2가 파이썬 3에서는 이름이 바뀐 반면, requests는 파이썬 2.6이후 버전과 호환되므로, 파이썬 버전에 무관하게 더욱 편리하게 사용할 수 있다.

flags.py에 그리 새로운 것은 없다. 단지 다른 스크립트와 비교를 하기 위한 기준선이며, 필자는 동시성 버전을 구현할 때 중복을 피하기 위해 이 코드를 하나의 라이브러리로 사용했다. 이제 concurrent.futures를 이용해서 다시 구현해보자.

## concurrent.futures로 내려받기
concurrent.futures 패키지의 가장 큰 특징은 ThreadPoolExecutor와 ProcessPoolExecutor 클래스인데, 이 클래스들은 콜러블 객체를 서로 다른 스레드나 프로세스에서 실행할 수 있게 해주는 인터페이스를 구현한다. 이 클래스들은 작업자 스레드나 작업자 프로세스르를 관리하는 풀과 실행할 작업을 담은 큐를 가지고 있다. 그러나 아주 고수준의 인터페이스를 구현하고 있어서 국기를 내려받는 간단한 프로그램을 구현할 때는 내부의 작동 과정을 알 필요가 없다.

아래 에제는 ThreadPoolExecutor.map() 메서드를 이용해서 동시에 내려받는 작업을 아주 간단히 구현한다.

- [flags_threadpool.py](https://github.com/hyeonDD/fluent_python/blob/master/Part17/ex17-1/flags_threadpool.py)
1. 위 flags.py 모듈의 함수들을 재사용한다.
2. ThreadPoolExecutor에서 사용할 최대 스레드 수
3. 하나의 이미지를 내려받을 함수, 각 스레드에서 이 함수를 실행한다.
4. 작업자 스레드의 수를 설정한다. 허용할 최대 작업자 스레드의 수 (MAX_WORKERS)와 실체 처리할 항목의 수 중 더 작은 수를 사용해서 불필요한 스레드를 생성하지 않게 한다.
5. 작업자 스레드의 수를 전달해서 ThreadPoolExecutor 객체를 생성한다. executor.__exit__() 메서드는 excutor.shutdown(wait=True) 메서드를 호출하는데, 이 메서드는 모든 스레드가 완료될 때까지 블록된다.
6. map() 메서드는 여러 스레드에 의해 download_one() 함수가 동시에 호출된다는 것을 제외하면 내장된 map()함수와 비슷하게 작동한다. map() 메서드는 각 함수가 반환한 값을 가져올 수 있도록 박복할 수 있는 제너레이터를 반환한다.
7. 가져온 결과의 수를 반환한다. 스레드에서 호출한 함수 중 하나라도 예외를 발생시키면, 암묵적으로 호출된 next()에서 반복자의 해당 반환값을 가져올 때와 마찬가지로 여기에서 예외가 발생한다.
8. flags모듈에서 가져온 main() 함수를 호출해서 개선된 버전의 download_many()함수를 전달한다.

flags_threadpool.py의 download_one() 함수는 flags.py의 download_many()함수의 for 루프 본체와 본질적으로 동일하다. 순차적으로 실행되는 for 루프 본체를 동시에 호출할 함수로 바꾼 것이다.

라이브러리 이름이 concurrency.futures인데, flags_threadpool.py에서는 Future를 볼 수 없다. Future가 어디에 있는지 궁금할 텐데, 이에 대해서는 다음 절에서 설명한다.

## Future는 어디에 있나?
Future는 concurrent, futures와 asyncio의 내부에 있는 핵심 컴포넌트인데, 이 라이브러리의 사용자에게 드러나지 않는 경우가 종종 있다. flags_threadpool.py는 암묵적으로 Future를 사용하지만, 이 코드에서는 Future를 직접 건드리지 않는다. 이 절에서는 전반적인 Future의 특징에 대해 설명하고, Future를 이용한 예제 코드를 구현해본다.

파이썬 3.4 표준 라이브러리에서 Future라는 이름을 가진 클래스는 concurrent, futures.Future와 asyncio.Future다. 이 두 Future 클래스의 객체는 완료되었을 수도 있고 아닐 수도 있는 지연된 계산을 표현하기 위해 사용된다. Future 클래스는 Twisted의 Deferred 클래스, Tornado의 Future 클래스, 자바스크립트 라이브러리의 Promise 객체와 비슷하다. Future는 대기 중인 작업을 큐에 넣고, 완료 상태를 조사하고, 결과(혹은 예외)를 가져올 수 있도록 캡슐화한다.

일반적으로 Future에 대해 알아야 할 중요한 점은 여러분이나 나 같은 사람이 직접 객체를 생성하면 안 된다는 것이다. Future 객체는 concurrent.futures나 asyncio 같은 동시성 프레임워크에서만 베타적으로 생성해야 한다. 이유는 간단하다. Future는 앞으로 일어날 일을 나타내고, Future의 실행을 스케줄링하는 프레임워크마니 어떤 일이 일어날지 확실히 알 수 있기 때문이다. 따라서 concurrent.futures.Future 객체는 concurrent.futures.Executor의 서브클래스로 실행을 스케줄링한 후에만 생성된다. 예를 들어 Executor.submit() 메서드는 콜러블을 받아서, 이 콜러블의 실행을 스케줄링하고, Future 객체를 반환한다.

클라이언트 코드는 Future 객체의 상태를 직접 변경하면 안 된다. Future 객체가 나타내는 연산이 완료되었을 때, 동시성 프레임워크가 Future 객체의 상태를 변경하기 때문이다. 우리는 이 객체의 상태가 언제 바뀔지 제어할 수 없다.

두 프레임워크의 Future 클래스에는 논블로킹이며 이 객체에 연결된 콜러블의 실행이 완료되었는지 여부를 불리언형으로 반환하는 done() 메서드가 있다. 일반적으로 클라이언트 코드는 Future가 완료되었는지 직접 물어보지 않고, 통지해달라고 요청한다. 그렇기 때문에 이 두Future 클래스에 add_done_callback() 메서드가 있다. 이 메서드에 하나의 인수를 받는 콜러블을 전달하면, Future 객체의 작업이 완료되었을 때 이 콜러블이 호출되면서 Future 객체를 인수로 받는다.

그리고 이 두 프레임워크의 Future 클래스는 result() 메서드도 가지고 있는데, 완료된 경우 둘 다 콜러블의 결과를 반환하거나, 콜러블이 실행될 때 발생한 예외를 다시 발생시킨다. 그러나 Future 객체의 실행이 완료되지 않았을 때는 이 두 프레임워크의 f.result()는 결과가 나올 때까지 호출자의 스레드를 블로킹한다. 선택적으로 timeout 인수를 전달할 수 있으며, 지정한 시간까지 Future 객체의 작업이 완료되지 않으면, TimeoutError 예외가 발생한다. 그러나 18.1.1절 'asyncio.Future: 논블로킹 설계'에서 설명하는 것처럼 asyncio.Future.result()는 시간초과를 지원하지 않으며 yield from을 사용해서 Future 객체의 상태를 가져오는 방법을 선호한다. concurrency.futures.Future는 yield from을 사용할 수 없다.

두 라이브러리에는 Future 객체를 반환하는 함수가 많이 있다. 나머지 함수들은 사용자에게 보이지 않도록 자기 내부에서 Future 객체를 사용한다. flags_threadpool.py에서 본 Executor.map()메서드는 내부에서 Future 객체를 사용하는 예다. Executor.map()이 반환하는 반복형 객체는 __next__() 메서드가 호출될 때마다 각 Future 객체의 result() 메서드를 호출하므로, Future 객체 자체가 아니라 Future 객체의 결과를 가져올 수 있게 해준다.

Future 객체를 실제로 보기 위해 concurrent.futures.as_completed() 함수 (https://bit.ly/1JIsEOW) 를 사용하도록 flags_threadpool.py를 수정해보자. as_completed() 함수는 Future 객체를 담은 반복형을 인수로 받아, 완료된 Future 객체를 생성하는 반복자를 반환한다.

futures.as_completed()를 사용하려면 download_many()만 변경하면 된다. 상위 수준의 excutor.map() 메서드는 Future 객체를 생성하고 스케줄링하는 루프와 Future 객체의 결과를 가져오는 루프로 분할된다. 코드를 수정하면서 print() 문을 추가해서 완료 전후의 Future 객체를 출력한다. 수정한 download_many() 함수는 아래와 같다. 5줄이었던 download_many()함수가 17줄이 되었지만, 이제는 십니에 싸인 Future 객체를 볼 수 있다. 나머지 함수는 flags_threadpool.py와 동일하다.

- [flags_threadpool_ac.py](https://github.com/hyeonDD/fluent_python/blob/master/Part17/ex17-1/flags_threadpool_ac.py)
1. 이 에제에서는 인구가 많은 다섯 나라만 사용한다.
2. 대기 중인 Future 객체를 출력해서 살펴보기 위해 max_workers를 3으로 하드코딩한다.
3. 결과의 순서가 뒤바뀐다는 것을 확인하기 위해 국가 코드를 알파벳순으로 반복한다.
4. executor.submit()은 콜러블이 실행되도록 스케줄링하고 이 작업을 나타내는 Future 객체를 반환한다.
5. 나중에 as_completed()로 가져올 수 있도록 Future 객체를 모두 저장한다.
6. 국가 코드와 해당 Future 객체를 메시지로 출력한다.
7. as_completed()는 Future가 완료될 때 해당 Future 객체를 생성한다.
8. 이 Future 객체의 결과를 가져온다.
9. Future 객체와 이 객체의 결과를 출력한다.

여기서는 as_completed()가 반환한 완료된 Future 객체를 사용하므로 futre.result()가 결코 블로킹되지 않는다. flags_threadpool_ac.py를 한 번 실행하면 아래와 같은 결과가 나온다.

```
# flags_threadpool_ac.py의 출력
python3 flags_threadpool_ac.py
# Scheduled for BR: <Future at 0x1f7f1976b20 state=running> #1
# Scheduled for CN: <Future at 0x1f7f1d90a30 state=running>
# Scheduled for ID: <Future at 0x1f7f1da24f0 state=running>
# Scheduled for IN: <Future at 0x1f7f1da2dc0 state=pending> #2
# Scheduled for US: <Future at 0x1f7f1dac820 state=pending>
...
# 5 flags downloaded in 0.70s
```
1. Future 객체가 알파벳순으로 스케줄링되었다. Future 객체의 repr() 메서드가 상태를 보여주는데, 처음 세 개만 실행 중이다. 작업자 스레드의 수를 최대 3으로 설정했기 때문이다.
2. 마지막 두 개의 Future 객체는 대기 중으로서, 작업자 스레드를 기다리고 있다.
3. 제일 앞의 두 글자 'CN'은 작업자 스레드에 있는 download_one()이 출력한 메시지다. 그 뒤부터 이 줄의 끝까지 모두 download_many()가 출력한 것이다.
4. 주 스레드의 download_many()에서 첫 스레드 BR의 결과를 출력하기 전에 BR과 ID 스레드가 국가 코드를 먼저 출력한다.
> flags_threadpool_ac.py를 여러 번 실행하면 결과 순서가 달라지는 것을 볼 수 있다. max_workers를 5로 설정하면 결과 순서가 더욱 다양하게 달라지며, 1로 설정하면 코드가 순차적으로 실행되므로 언제나 submit()을 호출한 순서와 동일한 결과가 나온다.

ThreadPoolExecutor.map()을 사용하는 flags_threadpool.py과 futures.as_completed()를 사용하는 flags_threadpool_ac.py를 통해 concurrent.futures를 사용하는 두 가지 버전의 내려받기 스크립트를 보았다. flags_asyncio.py 코드가 궁금하다면 [예제 18-5]를 살짝 들여다봐도 좋다.

엄격히 말하자면, 지금까지 테스트한 동시성 스크립트는 어느 것도 병렬로 내려받을 수 없다. concurrent.futures는 전역 인터프리터 락(GIL)에 의해 제한되며, flags_asyncio.py는 단일 스레드로 실행된다.

그렇다면 우리가 방금 수행한 간략한 성능 측정에 대해 다음과 같은 질문이 떠오를 것이다.
* 파이썬 스레드가 한 번에 한 스레드만 실행할 수 있게 해주는 GIL에 의해 제한된다면, 어떻게 flags_threadpool.py가 flags.py보다 5배나 빨리 실행될 수 있을까?
* 둘 다 단일 스레드인데, 어떻게 flags_asyncio.py가 flags.py보다 5배나 빨리 실행될 수 있을까?

두 번 째 질문에 대해서는 18.3절 '블로킹 호출을 에둘러 실행하기'에서 답변한다.

다음 절에서는 입출력 위주의 처리에서는 GIL이 미치는 악영향이 거의 없는 이유를 설명한다.