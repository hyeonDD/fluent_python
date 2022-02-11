<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-6/UML_class_diagram.png)
 -->
# asyncio 서버 작성

에코 서버는 TCP 서버의 고전적인 예제로 많이 사용된다. 여기서는 먼저 TCP로 구현한 뒤 HTTP로 구현하여 유니코드 문자를 찾아내는 약간 더 재미있는 서버를 만들어본다. 이 서버들은 4.8절 '유니코드 데이터베이스'에서 설명한 unicodedata 모듈을 이용해서 클라이언트가 유니코드 공식 명칭으로 유니코드 문자를 검색할 수 있게 해준다. 아래 그림은 공식 명칭에 'chess black'과 'sun'이 들어 있는 유니코드 문자를 찾아주는 TCP 문자 검색 서버에 텔넷으로 연결한 세션을 보여준다.

![텔넷세션 사진](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-6/telnet_session.png)

이제 이 서버를 구현해보자.

## asyncio TCP 서버

여기서 살펴볼 예제들의 논리 대부분은 charfinder.py 모듈에 들어 있는데, 이 모듈은 동시성을 전혀 사용하지 않는다. charfinder.py는 명령행에서 문자를 검색하기 위해 사용할 수도 있지만, asyncio 서버에 콘텐츠를 제공하기 위해 설계되었다. charfinder.py 소스 코드는 내려받은 에제의 18-asyncio/charfinder/ 폴더에 있다.

charfinder 모듈은 파이썬에 기본 제공되는 유니코드 데이터베이스의 문자명에 나타나는 단어들을 인덱싱하고, 역인덱스를 생성해서 딕셔너리에 저장한다. 예를 들어 'SUN'키에 대한 역인덱스 항목은 자신의 문자명에 'SUN"단어가 들어 있는 유니코듀 집합에 매핑된다. 역인덱스 항목의 지역의 charfinder_index.pickle 파일에 저장된다. 여러 단어로 검색하는 경우 charfinder는 각 단어에 대한 인덱스에서 가져온 집합들의 교집합을 구한다.

여기서는 위 그림에서 본 것처럼 쿼리에 응답하는 tcp_charfinder.py 스크립트를 중점적으로 살펴본다. 이 코드에 대해서는 설명할 내용이 많으므로 코드를 2번 나누어서 설명한다.

- [tcp_charfinder.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-6/tcp_charfinder.py)
1. UnicodeNameIndex 클래스는 문자명 인덱스를 생성하고 쿼리 메서드를 제공한다.
2. UnicodeNameIndex 객체를 생성할 때 기존 charfinder_index.pickle이 있으면 사용하지만, 그렇지 않으면 인덱스를 빌드하므로 시작하는 데 몇 초 정도의 시간이 걸릴 수 있다.
3. asyncio_startserver()에 전달할 코루틴이다. asyncio.StreamReader와 asyncio.StreamWriter 객체를 인수로 받는다.
4. 클라이언트에서 제어 문자를 받을 때까지 이 루프는 계속 세션을 처리한다.
5. StreamWritier.write() 메서드는 코루틴이 아니라 일반 함수며, '?>'문자열 프롬포트를 전송한다.
6. StreamWriter.drain() 메서드는 출력 버퍼를 플러시한다. 이 메서드는 코루틴이므로 yield from으로 호출해야 한다.
7. StreamWriter.readline() 메서드는 코루틴이며, bytes형을 반환한다.
8. 텔넷 클라이언트가 제어 문자를 보내면 UnicodeDecodeError 예외가 발생한다. 간편함을 위해 제어 문자를 받으면 널 문자가 보내진 것처럼 처리한다.
9. 소켓이 연결된 원격 주소를 반환한다.
10. 클라이언트가 보낸 쿼리를 서버 콘솔에 출력한다.
11. 제어 문자나 널 문자를 받으면 루프를 종료한다.
12. U+0039\t9\tDIGIT NINE과 같은 형태로 유니코드 포인트, 실제 문자, 문자명을 문자열로 생성하는 제너레이터를 반환한다. 여기서는 간단히 처리하기 위해 리스트를 반환한다.
13. 각 행을 bytes 형으로 변환하고 기본 인코딩 방식인 UTF-8로 인코딩한 데이터에 CR(캐리지 리턴)과 LF(라인 피드) 문자를 추가해서 전송한다. 여기서는 제너레이터 표현식을 인수로 사용했다.
14. 627 matches for 'digit'와 같은 형태로 상태 메시지를 보낸다.
15. 출력 버퍼를 플러시한다.
16. 응답 메시지를 서버 콘솔에 출력한다.
17. 세션 종료 메시지를 서버 콘솔에 출력한다.
18. SteramWriter를 닫는다.

handle_queries() 코루틴은 대화형 세션을 시작하고 클라이언트에서 오는 여러 쿼리를 처리하므로 함수명이 복수형으로 되어 있다.

위 예제의 모든 입출력은 bytes 형을 읽거나 쓴다는 점에 주의하자. 네트워크에서 받은 문자열은 디코딩해야 하며, 보내기 전에 인코딩해야 한다. 파이썬 3에서는 UTF-8을 기본 인코딩 방식으로 사용하므로, 예제에서는 별도의 인코딩 방식을 지정하지 않았다.

한 가지 주의할 점은 입출력 메서드들 중 일부는 코루틴이므로 yield from으로 구동해야 하며, 그 외 일반 함수들은 호출해야 한다는 것이다. 예를 들어 버퍼에 쓰는 작업을 수행하므로 일반적으로 블로킹되지 않는다고 간주되는 StreamWriter.write()는 일반 함수로 구현되어 있다. 한편 버퍼를 플러시해서 실제로 입출력 작업을 수행하는 StreamWritier.drain() 메서드는 Streamreader.readline()과 동일하게 코루틴으로 구현되어 있다. 이 책을 쓰고 있는 현재 asyncio API 문서는 코루틴을 쉽게 구분할 수 있도록 레이블을 붙이는 개선 작업이 진행되고 있다.

아래 예제는 위 예제와 이어지며, 이 모듈의 main()함수를 보여준다.
```
def main(address='127.0.0.1', port=2323):  # <1>
    port = int(port)
    loop = asyncio.get_event_loop()
    server_coro = asyncio.start_server(handle_queries, address, port,
                                loop=loop) # <2>
    server = loop.run_until_complete(server_coro) # <3>

    host = server.sockets[0].getsockname()  # <4>
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))  # <5>
    try:
        loop.run_forever()  # <6>
    except KeyboardInterrupt:  # CTRL+C pressed
        pass

    print('Server shutting down.')
    server.close()  # <7>
    loop.run_until_complete(server.wait_closed())  # <8>
    loop.close()  # <9>

if __name__ == '__main__':
    main(*sys.argv[1:])  # <10>
```
1. main() 함수는 아무런 인수 없이 호출할 수 있다.
2. 완료된 후 asyncio.start_server()가 반환한 코루틴 객체는 TCP 소켓 서버인 asyncio.Server 객체를 반환한다.
3. 서버를 가져오기 위해 server_coro를 구동한다.
4. 서버의 첫 번째 소켓의 주소와 포트를 가져온다.
5. 그리고 서버 콘솔에 출력한다. 이는 서버 콘솔에 이 스크립트가 처음으로 출력하는 메시지다.
6. 이벤트 루프를 실행한다. main()함수는 서버 콘솔에서 CTRL-C를 눌러 종료될 때까지 여기에서 블로킹된다.
7. 서버를 닫느다.
8. server.wait_closed()는 Future 객체를 반환한다. 이 객체가 작업을 완료할 때까지 기다리기 위해 loop.run_until_complete()를 실행한다.
9. 이벤트 루프를 종료한다.
10. 선택적 명령행 인수를 간단히 처리한다. sys.argv[1:] 항목들을 각기 main() 함수의 인수로 전달한다.

run_until_complete()는 코루틴 (start_server()의 반환값) 이나 Future 객체(server.wait_closed()의 반환값)를 모두 받을 수 있음에 주의하라. run_until_complete()는 코루틴을 인수로 받으면, 이 코루틴을 Task 객체 안에 래핑한다.

아래 소스코드에 나열된 서버 콘솔에서 생성된 메시지를 자세히 살펴보면 tcp_charfinder.py의 제어 흐름을 이해하는 데 도움이 될것이다.

```
python3 tcp_charfinder.py
"""
Serving on ('127.0.0.1', 2323). Hit CRL-C to stop. #1
Received from ('127.0.0.1', 62910): 'chess black' #2
Sent 6 results
Received from ('127.0.0.1', 62910): 'sun' #3
Sent 10 results
Received from ('127.0.0.1', 62910): '\x00' #4
Close the client socket #5
"""
```
1. main()이 출력한 메시지다.
2. handle_queries() 안에 있는 while 루프의 첫 번째 반복이다.
3. while 루프의 두 번째 반복이다.
4. 사용자가 CTRL-C를 눌렀다. 서버는 제어 문자를 받고 나서 세션을 닫는다.
5. 클라이언트 소켓은 닫혔지만 서버는 계속 실행되므로 다른 클라이언트를 처리할 수 있다.

main() 함수는 거의 즉시'Serving on...'메시지를 출력하고 loop.run_forever()에서 블로킹된다. 이때 제어 흐름은 이벤트 루프 안으로 들어가 있으면서 이따금씩 handle_queries() 코루틴으로 빠져나오는데, handle_queries()가 데이터를 보내거나 받기 위해 네트워크 연산을 기다려야 할 때는 제어권이 다시 이벤트 루프로 넘어간다. 이벤트 루프가 살아 있는 동안, 새로운 클라이언트가 서버에 접속할 때마다 handle_queries() 코루틴 객체가 새로 생성된다. 이렇게 해서 여러 클라이언트가 이 단순한 서버에 의해 동시에 처리될 수 있다. 이 과정은 서버에서 CTRL-C를 누르거나 프로세스를 강제 종료시킬 때까지 계속된다.

tcp_charfinder.py 코드는 바로 사용할 수 있는 서버를 제공하는 고수준 asyncio Stream API (https://docs.python.org/3/library/asyncio-stream.html) 를 사용하므로, 일반 함수나 코루틴 형태로 처리 함수만 구현하면 된다. 그리고 Twisted 프레임워크가 제공하는 전송 및 프로토콜 추상화에서 영감을 얻은 하위 수준의 전송과 프로토콜 API (https://docs.python.org/3/library/asyncio-stream.html) 도 있다. 저수준 API를 이용해서 구현한 TCP 에코 서버 등에 대한 자세한 정보는 asyncio의 '전송과 프로토콜' 문서 (http://bit.ly/1f6D9i6) 를 참조하라.

다음 절에서는 HTTP로 구현한 문자 검색 서버를 설명한다.

## aiohttp 웹 서버

asyncio 국기 예제에서 사용했던 aiohttp 라이브러리는 서버 측 HTTP도 지원하므로 http_charfinder.py 스크립트를 구현하기 위해 aiohttp 라이브러리를 사용했다. 아래 그림에서는 'cat face'로 검색한 결과를 출력하는 간단한 웹 인터페이스를 보여준다.
> 어떤 브라우저는 다른 브라우저보다 유니코드를 더 잘 보여준다. 아래그림의 화면은 OS X에서 파이어폭스를 실행한 화면으로, 사파리 브라우저를 사용했을 때 동일한 결과가 나왔다. 그러나 동일 컴퓨터에서 크롬 브라우저와 오페라 브라우저를 사용했을 때 'cat face'이모지 문자가 제대로 출력되지 않았다. 그 외'chess'등의 문자는 정상적으로 보였으므로, OS X용 크롬과 오페라의 폰트 문제인 것으로 생각된다.

![http_charfinder사용사진](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-6/http_charfinder.png)

먼저 이벤트 루프와 HTTP 서버를 생성하고 종료하는 http_charfinder.py의 후반부 코드를 분석해보자 아래 소스코드.
```
@asyncio.coroutine
def init(loop, address, port):  # <1>
    app = web.Application(loop=loop)  # <2>
    app.router.add_route('GET', '/', home)  # <3>
    handler = app.make_handler()  # <4>
    server = yield from loop.create_server(handler,
                                           address, port)  # <5>
    return server.sockets[0].getsockname()  # <6>

def main(address="127.0.0.1", port=8888):
    port = int(port)
    loop = asyncio.get_event_loop()
    host = loop.run_until_complete(init(loop, address, port))  # <7>
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))
    try:
        loop.run_forever()  # <8>
    except KeyboardInterrupt:  # CTRL+C pressed
        pass
    print('Server shutting down.')
    loop.close()  # <9>
```
1. init() 코루틴은 이벤트 루프가 구동할 서버를 생성한다.
2. aiohttp.web.Application 클래스는 웹 애플리케이션을 나타낸다.
3. 그리고 URL 패턴을 처리 함수에 매핑한다. 여기서는 GET / 요청을 home() 함수 (뒤의 예제 18-18)에서 처리하도록 설정한다.
4. app.make_handler() 메서드는 app 객체에 설정된 라우트에 따라 HTTP 요청을 처리할 aiohttp.web.RequestHandler 객체를 반환한다.
5. create_server()는 handler를 프로토콜 처리기로 사용하고 address와 port에 바인딩해서 서버를 실행한다.
6. 첫번 째 서버 소켓의 주소와 포트를 반환한다.
7. init()을 실행해서 서버를 기동하고 주소와 포트를 가져온다.
8. 이벤트 루프를 실행한다. 이벤트 루프가 제어권을 가진 동안 main() 함수는 여기에서 블로킹된다.
9. 이벤트 루프를 닫는다.

asyncio API에 익숙해졌으므로 위 소스코드와 [tcp_charfinder.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-6/tcp_charfinder.py)에서 서버를 기동하는 방법을 비교해보면 흥미로울 것이다.

[tcp_charfinder.py](https://github.com/hyeonDD/fluent_python/blob/master/Part18/ex18-6/tcp_charfinder.py) TCP 예제에서는 main() 함수 안에서 다음과 같이 코드 두 줄을 실행해서 서버를 생성하고 스케줄링했다.
```
server_coro = asyncio.start_server(handle_queries, address, port,
                                   loop=loop)
server = loop.run_until_complete(server_coro)
```

HTTP 예제에서는 init() 함수에서 다음과 같이 서버를 생성했다.
```
server = yield from loop.create_server(handler,
                                        address, port)
```

그러나 init() 자체도 코루틴이므로, main() 함수에서는 다음과 같이 init()을 구동한다.
```
host = loop.run_until_complete(init(loop, address, port))
```

그러나 asyncio.start_server()와 loop.create_server() 코루틴은 둘 다 asyncio.Server객체를 반환한다. 서버를 실행하고 서버에 대한 참조를 반환하려면 둘 다 끝까지 구동되어야 한다. TCP 예제의 경우 loop.run_until_complete(server_coro)를 호출해서 코루틴이 끝까지 실행되도록 만든다(server_coro는 asyncio.start_server()가 반환한 값이다).
HTTP 예제의 경우, create_server()가 init() 코루틴 안에 있는 yield from으로 구동되며, init()은 main() 함수 안에서 loop.run_until_complete(init(...))을 호출할 때 구동된다.

아래 예제는 우리가 설정한 HTTP 서버의 루트(/) URL을 처리하도록 설정된 home() 함수를 보여준다.
```
# http_charfinder.py: home() 함수
def home(request):  # <1>
    query = request.GET.get('query', '').strip()  # <2>
    print('Query: {!r}'.format(query))  # <3>
    if query:  # <4>
        descriptions = list(index.find_descriptions(query))
        res = '\n'.join(ROW_TPL.format(**vars(descr))
                        for descr in descriptions)
        msg = index.status(query, len(descriptions))
    else:
        descriptions = []
        res = ''
        msg = 'Enter words describing characters.'

    html = template.format(query=query, result=res,  # <5>
                           message=msg)
    print('Sending {} results'.format(len(descriptions)))  # <6>
    return web.Response(content_type=CONTENT_TYPE, text=html) # <7>
```
1. 라우트 처리기는 aiohttp.web.Request 객체를 받는다.
2. 쿼리 문자열에서 앞뒤 공백을 제거한다.
3. 쿼리를 서버 콘솔에 출력한다.
4. 쿼리가 있으면, 인덱스에 대한 쿼리 결과로 생성된 HTML 테이블 행에 res를, 상태 메시지에 msg를 바인딩한다.
5. HTML 페이지를 생성한다.
6. 응답을 서버 콘솔에 출력한다.
7. Response 응답을 생성해서 반환한다.

home()은 코루틴이 아니며, 그 안에 yield from 표현식을 가지고 있지 않다면 코루틴이 될 필요도 없다. aiohttp의 add_route() 메서드 문서 (http://bit.ly/1HGu5dz) 에 따르면 처리기가 일반 함수면 메서드 내부에서 코루틴으로 변환된다.

위 소스코드에 있는 home()함수의 단순함에는 단점도 있다. 이 함수가 코루틴이 아니고 일반 함수라는 사실은 커다란 문제를 야기할 수 있다. 즉, 높은 동시성을 이루기 위해 웹 애플리케이션을 개발하는 방법에 대해 다시 생각해볼 필요성이 생긴 것이다. 이제 이 문제에 대해 생각해보자.

## 동시성을 향상시키는 똑똑한 클라이언트

위 예제의 home함수는 장고나 플라스크의 뷰 함수와 아주 비슷해 보인다. 이 코드에서 비동기성은 전혀 보이지 않는다. 요청을 받고, 데이터베이스에서 데이터를 가져오고, 응답을 만들고, 완전한 HTML 페이지를 그린다. 이 예제에서 '데이터베이스'는 메모리에 저장된 UnicodeNameIndex 객체다. 그러나 디스크에 있는 데이터베이스에 대한 접근은 비동기식으로 실행해야 한다. 그렇지 않으면 데이터베이스 결과가 나올 때까지 이벤트 루프가 블로킹된다. 예를 들어 aiopg 패키지 (https://aiopg.readthedocs.org/en/stable/) 는 asyncio와 호환되는 비동기식 PostgreSQL 드라이버를 제공한다. 이 드라이버는 yield from으로 쿼리를 보내고 결과를 가져올 수 있게 해주므로, 뷰 함수는 제대로 된 코루틴으로 작동할 수 있다.

블로킹 함수를 피하는 것 외에도, 높은 동시성을 가진 시스템은 커다란 작업을 작은 작업 여러개로 분활해서 응답성을 유지해야 한다. http_charfinder.py 서버를 보면 이 문제를 쉽게 이해할 수 있다. 유니코드 문자명을 'cjk'로 검색하면 중국어, 일본어, 한국어에서 사용하는 상형문자 75,821개가 나온다. 이때 home() 함수는 75,821행의 테이블을 가진 5.3MB 크기의 HTML 문서를 생성한다.

지역 http_charfinder.py 서버에서 curl 명령행 HTTP 클라이언트를 사용하는 경우, 필자 컴퓨터에서는 'cjk'쿼리에 대한 응답을 가져오는 데 2초 정도 걸린다. 실제 이렇게 큰 테이블을 렌더링해야 하는 브라우저의 경우 시간이 훨씬 더 많이 걸린다. 물론 대부분의 쿼리에 대한 응답은이보다 훨씬 작다. 'braile'로 쿼리하면 256개의 행이 있는 19KB 페이지가 나오며, 필자 컴퓨터에서 0.017초 걸렸다. 그러나 서버에서 'cjk'쿼리를 처리하는 데 2초 걸린다면, 나머지 클라이언트는 모두 최소 2초 이상 기다려야 하며, 이는 받아들 일 수 없는 시간이다.

응답 지연 문제를 처리하기 위해 응답을 페이지로 구분할 수 있다. 예를 들어 최대 200행으로 제한하고, 사용자가 클릭하거나 페이지를 스크롤해야 데이터를 더 가져오는 방식을 사용할 수 있다. 내려받은 예제에서 charfinder.py 모듈을 보면 UnicodeNameIndex.find_descriptions()메서드가 선택적으로 start와 stop 인수를 받는 것을 볼 수 있다. 이 인수들은 페이지 구분을 지원하기 위한 오프셋 값이다. 따라서 처음 200개의 결과를 가져오고 나서, 사용자가 원하면 AJAX나 웹소켓을 이용해서 다음 페이지를 보낼 수 있다.

결과를 부분적으로 보내는 데 피룡한 대부분의 코드는 브라우저 측에서 구현된다. 그렇기 때문에 구글 및 대부분의 대형 인터넷 서비스는 상당 부분을 클라이언트 측에 의존한다. 영리한 비동기식 클라이언트는 서버 자원을 더 잘 활용한다.

영리한 클라이언트는 구식 장고 애플리케이션에도 도움이 되지만, 제대로 구현하려면 HTTP요청과 응답의 처리에서부터 데이터 접근에 이르기까지 모든 부분에서 비동기식 프로그래밍을 체계적으로 지원하는 프레임워크가 필요하다. 이것은 웹소켓을 이용한 게임과 미디어 스트리밍 등 실시간 서비스를 구현할 때도 마찬가지다.

점진적 내려받기를 지원하도록 http_charfinder.py를 개선하는 것은 독자 여러분의 숙제로 남겨놓는다. 트위터처럼 '무한 스크롤'을 구현하면 보너스 점수를 더 준다. 이 숙제를 내면서 asyncio를 이용한 동시성 프로그래밍에 대한 설명을 마친다.