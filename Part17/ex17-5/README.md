<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part17/ex17-5/UML_class_diagram.png)
 -->
# 진행 상황 출력하고 에러를 처리하며 내려받기
앞에서 얘기한 것처럼 17.1절 '예제: 세 가지 스타일의 웹 내려받기'에서 구현한 스크립트들은 읽기 쉽게 만들기 위해, 그리고 순차, 스레드, 비동기 방식의 구조를 비교하기 쉽게 만들기 위해 아무런 에러도 처리하지 않는다.

다양한 에러 조건의 처리를 테스트하기 위해 다음과 같은 flags2 예제들을 만들었다.

---

**flags2_common.py**
이 모듈은 명령행 인수를 처리하고, 시간을 측정하고, 결과를 출력하는 main() 함수를 포함해서 모든 flags2 스크립트가 공통으로 사용할 함수와 설정을 담고 있다. 이 코드는 테스트를 지원하기 위한 코드이며, 이 장에서 설명하는 내용과 직접적인 연관성이 없으므로, 소스 코드는 [예제 A-10]에 나열한다.

**flags2_sequential.py**
에러를 적절히 처리하며 진행 막대를 보여주는 순차 HTTP 클라이언트다. 여기에서 구현하는 download_one()함수는 flags2_threadpool.py에서도 사용된다.

**flags2_threadpool.py**
futures.ThreadPoolExecutor에 기반해서 에러 처리와 진행 막대 통합을 보여주는 동시성 HTTP 클라이언트

**flags2_asyncio.py**
스레드 예제와 기능상으로 동일하지만, asyncio와 aiohttp를 이용해서 구현한다. 이 스크립트는 18.4절 'asyncio 내려받기 스크립트 개선'에서 설명한다.
> **동시성 클라이언트를 테스트할 때는 주의하라**</br>
동시성 HTTP 클라이언트를 공개 HTTP 서버에서 테스트하면 짧은 시간 동안 아주 많은 요청을 생성하게 되는데, 이것이 바로 서비스 거부(Dos)공격이 된다. 우리는 고성능 클라이언트를 만들고 싶을뿐 누구도 공격하려는 것은 아니다. 공개 서버에 테스트할 때는 클라이언트의 요청을 신중히 억제해야 하며, 테스트하기 위한 지역 HTTP 서버를 별도로 준비하는 것이 좋다. 웹 서버를 설정하는 방법에 대해서는 이 책의 예제 코드 중 17-futures/contries/README.rst 파일을 참조하라.

flags2 예제의 가장 두드러진 특징은 TQDM 패키지 (https://github.com/noamraph/tqdm) 를 이용해서 텍스트 기반의 진행 막대를 애니메이트한다는 점이다. 진행 막대를 보여주고 세 가지 flags2 버전의 속도를 비교하기 위해 유튜브에 108초짜리 동영상 (https://www.youtube.com/watch?v=M8Z65tAl5l4) 를 올렸다. 676개의 URL을 통해 194개의 국기 이미지를 내려받으려면 5분이 넘게 걸리므로, 순차 내려받기 스크립트는 32초에 중단했다. 그러고 나서 스레드 버전과 비동기 버전을 세 번씩 실행했는데, 한 번 실행하는 데 6초가 채 걸리지 않았다 (즉, 순차 버전보다 60배 이상 빠르다). 아래그림은 flags2_threadpool.py를 실행하는 도중의 모습 (왼쪽 위)과 실행이 완료된 후 (오른쪽 아래)의 모습이다. (그림 생략)

TQDM은 사용하기 아주 쉬우며, 프로젝트의 README.md 페이지 (https://github.com/noamraph/tqdm/blob/master/README.md) 를 보면 간단한 예제를 애니메이션. GIF 파일을 이용해서 보여준다. TQDM 패키지를 설치한 후 다음 코드를 입력하면 주석이 있는 위치에서 진행 막대가 애니메이트되는 것을 볼 수 있다.
```
import time
from tqdm import tqdm
for i in tqdm(range(1000)):
    time.sleep(.01)
# -> 진행 막대가 여기에 나타난다)
```
깔끔한 효과 외에도 tqdm() 함수는 개념적으로 흥미롭다. 모든 형태의 반복형을 인수로 받아 항목들을 처리하면서 진행 막대를 보여주며, 완료되기까지 남은 시간을 추정해서 보여준다. 남은 시간을 추정하기 위해 tqdm()은 len()을 지원하는 반복형을 받거나, 예상 항목 수를 두 번째 인수로 받는다. TQDM과 flags2 예제를 통합하려면 각 Future 객체가 완료되면서 tqdm()이 출력할 수 있게 futures.as_completed()와 asyncio.as_completed()함수를 사용해야 하므로 동시성 스크립트가 작동하는 방식을 들여다보는 좋은 기회가 된다.

flags2 예제는 명령행 인터페이스도 제공한다. 스크립트 세 개가 동일한 옵션을 받으며, 어느 스크립트든 -h 옵션을 이용해서 스크립트를 호출하면 도움말을 볼 수 있다 (예제 17-8)

인수는 모두 선택적이다. 중요한 인수 몇 개를 설명하면 다음과 같다.

여기서 -s/--server 옵션이 특히 중요하다. 이 옵션에는 테스트에 사용할 HTTP 서버와 기반 URL을 지정한다. 다음 네 개의 문자열 중 하나를 전달해서 어디에서 국기 이미지를 가져올지 결정한다 (문자열은 소문자로 입력해도 상관없다).

---

**LCOAL**
기본값이며, http://localhost:8001/flags 를 사용한다. 지역 HTTP 서버가 8001 포트에서 응답하도록 설정해야 한다. 필자는 테스트에 Nginx를 사용했다. 이 장의 예제 코드 중 README.rst 파일 (http://bit.ly/1JIsg2L) 은 서버를 설치하고 구성하는 방법을 설명한다.

**REMOTE**
http://flupy.org/data/flags 를 사용한다. 이것은 필자가 소유한 공개 웹 서버로서 공유 서버에 호스팅되어 있다. 이 서버에 너무 많은 요청을 동시에 보내지 않았으면 한다. flupy.org 도메인은 Cloudflare CDN (http://www.cloudlare.com/) 에서 제공되는 무료 계정에 의해 처리되므로 처음 내려받을 때는 약간 느리지만, 파일이 CDN 캐시에 올라가면 빨라진다.

**DELAY**
http://localhost:8002/flags 를 사용한다. HTTP 응답을 지연시키는 프락시는 8002번 포트에서 처리해야 한다. 응답을 지연시키기 위해 Nginx 앞에 모질라 Vaurien을 사용했다. 앞에서 언급한 README.rst 파일에서 Vaurien 프락시 실행 방법을 참조하라.

**ERROR**
http://localhost:8003/flags 를 사용한다. HTTP 에러를 발생시키고 응답을 지연시키는 프락시는 8003 포트에서 처리해야ㅑ 한다. 이를 위해 Vaurien 설정을 변경해서 적용했다.

---

> LOCAL 옵션은 자신의 컴퓨터 8001 포트에서 HTTP 서버를 설정하고 실행해야 작동한다. DELAY와 ERROR 옵션은 8002번과 8003번 포트에 바인딩된 프락시 서버가 필요하다. 이 옵션을 사용하기 위해 Nginx와 모질라 Vaurien을 설정하는 방법은 내려받은 파일의 17-futures/countries/README.rst 를 참조하라.

기본적으로 각각의 flags2 스크립트는 LOCAL 서버 (http://localhost:8001/flags) 에서 인구가 많은 20개 나라의 국기를 가져온다. 기본 동시 연결 수는 스크립트마다 다르다. 아래 예제는 모두 기본값을 사용해서 실행한 예다.

```
# 모두 기본값으로 flags2_sequential.py 실행하기. 순차적으로 내려받으므로 동시 연결 수가 1이다.
python3 flags2_sequntial.py
"""
LOCAL site: http://localhost:8001/flags
Searching for 20 flags: from BD to VN
1 concurrent connection will be used.
----------------
20 flags downloaded.
Elapsed time: 0.10s
"""
```

내려받는 국기는 다양한 방법으로 선택할 수 있다. 아래에제는 국가 코드가 A, B, C로 시작하는 모든 나라의 국기 이미지를 DELAY 서버에서 가져오는 방법을 보여준다.

```
python3 flags2_threadpool.py -s DELAY a b c
"""
DELAY site: http://localhost:8002/flags
Searching for 78 flags: from AA to CZ
30 concurrent connections will be used.
---------
43 flags downloaded.
35 not found.
Elapsed time: 1.72s
"""
```

국가 코드를 선택하는 방법과 무관하게 가져올 국기 이미지의 수를 -l/--limit 옵션으로 제한할 수 있다. 아래예제는 -l 100 옵션을 -a 옵션과 함께 사용해서 ERROR 서버에서 정확히 국기 100개를 요청하는 방법을 알려준다.

```
python3 flags2_asyncio.py -s ERROR -al 100 -m 100
"""
ERROR site: http://localhost:8003/flags
Searching for 100 flags: from AD to LK
100 concurrent connections will be used.
---------
73 flags downloaded.
27 erros.
Elapsed time: 0.64s
"""
```

지금까지 flags2 예제를 실행하는 방법에 대해 알아보았다. 이제 이 스크립트들이 어떻게 구현되어 있는지 알아보자.

## flags2 예제에서의 에러 처리

이 세 스크립트에서는 모두 파일을 실제로 내려받는 download_one() 함수가 404 에러 (Not Found)를 처리한다. 그 외 다른 에러는 위로 전달되어 download_many()함수가 처리한다.

여기서도 순차 코드부터 분석한다. 이해하기 더 쉬우며, 이 코드 대부분이 스레드 버전에서 다시 쓰이기 때문이다. 아래에제는 flags2_sequential.py와 flags2_threadpool.py 스크립트에서 실제로 내려받는 작업을 수행하는 함수를 보여준다.

- [flags2_sequential.py](https://github.com/hyeonDD/fluent_python/blob/master/Part17/ex17-5/flags2_sequential.py)
1. get_flag()는 에러를 처리하지 않고, 대신 200 이외의 HTTP 코드에 대해 requests.Response.raise_for_status()를 이용해서 예외를 발생시킨다.
2. download_one()은 requests.exceptions.HTTPError를 잡아서 HTTP 404 코드만 처리한다.
3. status를 HTTPStatus.not_found로 설정한다. HTTPStatus는 flags2_common 모듈(예제 A-10)에서 임포트한 열거형이다.
4. 그외 HTTPError 예외를 다시 발생시켜서 호출자로 전달한다.
5. 명령행에서 -v/--verbose 옵션을 설정한 경우, 국가 코드와 상태 메시지가 출력된다. 이렇게 해서 진행상황을 상세한 모드로 볼 수 있다.
6. download_one()에서 반환한 Result namedtuple은 status 필드에 HTTPStatus.not_found나 HTTPStatus.ok 값을 가진다.

아래 예제는 순차 스크립트의 download_many()함수를 보여준다. 이 코드는 간단하지만 나중에 설명할 동시 버전과 비교하기 위해 공부해둘 필요가 있다. 진행 상황을 보여주고, 에러를 처리하고, 내려받은 항목의 합계를 구하는 방법을 신중히 살펴보라.

- [flags2_sequential.py](https://github.com/hyeonDD/fluent_python/blob/master/Part17/ex17-5/flags2_sequential.py)
1. 이 Couner 객체는 HTTPStatus.ok, HTTPStatus.not_found, 또는 HTTPStatus.error의 합계를 각각 구한다.
2. cc_iter는 인수로 받은 국가 코드 리스트를 알파벳순으로 정렬해서 보관한다.
3. 상세 메시지 모드로 작동하지 않는 경우, cc_iter를 tqdm()함수에 전달하고, tqdm()은 움직이는 진행막대를 보여주면서 cc_iter에 들어 있는 항목을 생성하는 반복자를 반환한다.
4. 이 for 루프는 cc_iter를 반복한다.
5. 그리고 연속해서 download_one()을 호출해서 국기 이미지를 내려받는다.
6. get_flag()에 의해 발생되어 download_one()에 의해 처리되지 않은 HTTP 관련 예외는 여기에서 처리한다.
7. 다른 네트워크 관련 예외는 여기에서 처리한다. flags2_common.main()이 try/except를 이용하지 않고 download_many()를 호출했으므로, 그 외 에외가 발생하면 스크립트가 중단된다.
8. 아무런 예외도 download_one()을 빠져나오지 않았다면, download_one()이 반환한 HTTPStatus namedtuple에서 status 값을 가져온다.
9. 에러가 발생했다면 status에 에러를 저장한다.
10. HTTPStatus 열거형 값을 키로 사용해서 카운터 값을 증가시킨다.
11. 상세 메시지 모드에서 실행되는 경우, 에러가 있다면 현재 국가 코드에 대한 에러 메시지를 출력한다.
12. coutner를 main()함수로 반환해서 최종 보고에 숫자를 출력할 수 있게 한다.

이제 이 코드를 리팩토링해서 스레드 버전으로 만든 flags2_threadpool.py를 살펴보자.

## futures.as_completed() 사용하기
각각의 요청마다 TQDM 진행 막대를 표시하고 에러 처리를 하기 위해 flags2_threadpool.py 스크립트는 우리가 이미 살펴본 futures.as_completed() 함수와 함께 futures.ThreadPoolExecutor 클래스를 사용한다. 아래 소크도는 flags2_threadpool.py의 전체 소스 코드다. download_many() 함수만 직접 구현하며, 나머지 함수는 flags2_common과 flags2_sequential 모듈에서 가져와서 사용한다.

- [최종 flags2_threadpool.py](https://github.com/hyeonDD/fluent_python/blob/master/Part17/ex17-5/flags2_threadpool.py)
1. 진행 막대 표시 라이브러리를 임포트한다.
2. flags2_common 모듈에서 함수 한 개와 열거형 한 개를 임포트한다.
3. flags2_sequential 모듈에서 가져온 download_one() 함수를 재사용한다.
4. -m/--ax_req 명령행 옵션을 지정하지 않으면 이 숫자가 최대 동시 요청 수가 되며, 스레드 풀의 크기로 사용된다. 내려받는 국기의 숫자가 더 적으면, 실제 숫자가 더 적어질 수 있다.
5. MAX_CONCUR_REQ는 내려받을 국기의 숫자나 명령행 옵션 -m/--max_req에 상관없이 동시 요청 수를 제한한다. 일종의 안전장치다.
6. main()이 찾아낸 MAX_CONCUR_REQ, cc_list 길이, -m/--ax_req 인수값 중 가장 작은 값인 concur_req 값으로 max_workers를 설정해서 executor 객체를 생성한다. 이렇게 하면 필요 이상의 스레드를 만들지 않는다.
7. 이 딕셔너리는 각각의 국가 코드에 Future 객체(하나의 내려받기 작업을 나타낸다)를 매핑하며, 오류 보고에 사용된다.
8. 국가 코드를 알파벳순으로 반복한다. 결과가 나오는 순서는 무엇보다도 HTTP 응답 시간에 의해 결정되지만, concur_req로 지정한 스레드 풀의 크기가 len(cc_list)의 항목 수보다 훨씬 작은 경우에는 군데군데 알파벳순으로 나오는 것을 볼 수 있을 것이다.
9. executor.submit()을 호출할 때마다 하나의 콜러블의 실행을 스케줄링하며 Future 객체를 반환한다. 첫 번째 인수는 콜러블이며, 나머지 인수는 이 콜러블에 전달된다.
10. 국가 코드와 Future 객체를 딕셔너리에 저장한다.
11. futures.as_completed()는 완료된 순서대로 Future 객체를 생성하는 반복자를 반환한다.
12. 상세 메시지 모드가 아닌 경우 as_completed()의 결과를 tqdm() 함수에 전달해서 진행 막대를 출력한다. done_iter에 len()메서드가 없으므로, tqdm()에 total 인수로 에상 항목 수를 알려줘야 tqdm()이 예상 시간을 계산할 수 있다.
13. 완료되는 순서대로 Future 객체를 반복한다.
14. Future 객체의 result() 메서드를 호출하면 콜러블이 반환한 값이나 콜러블을 실행하는 동안 잡은 예외가 발생한다. result() 메서드는 Future가 완료될 때까지 블로킹될 수 있지만, as_completed()가 완료된 Future 객체만 반환하므로 여기에서는 result() 메서드가 블로킹되지 않는다.
15. 발생할 수 있는 예외를 처리한다. 이 함수의 나머지 부분은 밑의16번 부분을 제외하고 순차 버전의 download_many()함수와 동일하다.
16. 에러 메시지에 대한 정보를 제공하기 위해 현재의 Future 객체를 키로 사용해서 to_do_map에서 국가 코드를 가져온다. 순차 버전에서는 국가 코드를 반복하므로 루프의 현재 국가 코드를 사용하면 되기 때문에 이 과정이 필요 없지만, 여기에서는 Future 객체를 반복하므로 국가 코드를 검색해야 한다.

위 예제는 Future 객체를 Future가 완료되었을 때 필요한 다른 데이터와 매핑하는 딕셔너리를 만든다. 이 방법은 futures.as_completed()에 관련된 관용구로서 유용하게 사용된다. 여기에서는 do_do_map 딕셔너리가 Future 객체를 해당 국가 코드에 매핑한다. 이렇게 하면 Future가 임의의 순서대로 완료되더라도 Future 객체의 결과를 가져와서 처리하기 쉬워진다.

파이썬 스레드는 입출력 위주의 애플리케이션에 잘 맞으며, 경우에 따라 concurrent.futures패키지를 이용하면 아주 간단히 처리할 수 있다. 이것으로 concurrent.futures에 대한 설명을 마친다. 이제 ThreadPoolExecutor나 ProcessPoolExecutor가 절절히 처리할 수 없는 경우에 사용할 수 있는 다른 방법을 알아보자.

## 스레드 및 멀티프로세스의 대안
파이썬은 0.9.8버전 (1993년)부터 스레드를 지원했다. concurrent.futures는 단지 스레드를 사용하기 위해 나중에 추가된 방법일 뿐이다. 파이썬 3에서는 원래의 thread 모듈의 사용중단을 안내했으며 더 높은 수준의 threading 모듈 (https://docs.python.org/3/library/threading.html) 의 사용을 권장하고 있다. futures.ThreadPoolExecutor로 처리하기 어려운 작업을 수행해야 하는 경우 Thread, Lock, Semaphore 등 threading 모듈의 기본 컴포넌트를 이용해서 처리할 수 있다. 스레드 간에 데이터를 전송할 때는 queue 모듈 (https://docs.python.org/3/library/queue.html) 에서 제공하는 스레드 안전한 큐를 사용할 수 있다. 이 컴포넌트들은 futures.ThreadPoolexecutor에 캡슐화되어 있다.

계산 위주의 작업을 수행하는 경우에는 여러 프로세서를 실행해서 GIL을 피해나가야 한다. futures.ProcessPoolExecutor를 사용하면 간단히 처리할 수 있지만, 애플리케이션의 구조가 이 클래스에 잘 맞지 않는 경우에는, threading API와 비슷하지만 작업을 여러 프로세스에 할당하는 multiprocessing 패키지 (https://docs.python.org/3/library/multiprocessing.html) 를 사용해야 한다. 간단한 프로그램이라면 약간만 수정해도 threading 대신 multiprocessing을 사용할 수 있다. 협업하는 프로세스들은 데이터 공유라는 가장 큰 문제를 해결해야 하는데, multiprocessing 패키지에는 이 문제를 쉽게 해결해주는 장치도 있다.
