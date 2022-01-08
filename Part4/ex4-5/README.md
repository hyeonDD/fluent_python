# 텍스트 파일 다루기

텍스트를 처리하는 최고의 방법은 '유니코드 샌드위치'다. 이 말은 입력할 때(파일을 읽기 위해 여는 때 등) 가능하면 빨리 bytes를 str로 변환해야 한다는 것을 의미한다. 샌드위치에 들어가는 '고기'는 프로그램의 비지니스 논리에 해당하는 부분이며, 여기서는 텍스트를 오로지 str 객체로 다룬다. 즉, 다른 처리를 하는 도중에 인코딩이나 디코딩하면 안된다. 출력 할 때는 가능한 늦게 str을 bytes로 인코딩한다. 대부분의 웹 프레임워크도 이렇게 작동하며, 처리하는 동안 bytes를 다루는 일은 거의 없다.
장고(Django)의 경우 뷰는 유니코드 str만 출력하고, 장고 자체가 응답을 bytes(기본적으로 UTF-8 인코딩을 사용한다)로 인코딩하는 일을 담당한다.

![유니코드샌드위치](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-5/unicodesandwich.png)

파이썬 3는 유니코드 샌드위치 모델을 따르기 쉽게 해준다. 내장된 open()함수는 파일을 텍스트 모드로 일고 쓸 때 필요한 모든 인코딩과 디코딩 작업을 수행해주므로 my_file.read()에서 str 객체를 가져와서 처리하고 my_file.write()에 전달하면 된다.

따라서 텍스트 파일을 사용하는 일은 간단하다. 그렇지만 기본 인코딩에 의존하다보면 뜻하지 않은 봉변을 당할 수 있다.

- [플랫폼 잘못된 인코딩 예제](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-5/wrong_encoding.py)

버그는 인코딩 지정 때문에 발생했다. 파일에 쓸 때는 UTF-8로로 지정했지만, 파일을 읽을 때는 지정하지 않았다. 따라서 파이썬은 시스템 기본 인코딩(cmd 에서 chcp로 확인) 활성 코드 페이지 949(ecu-kr)을 이용해서 파일을 읽게 되고, UnicodeDecodeError를 발생시켰다. 윈도우 에서는 이와 같은 문제가 발생할 확률이 높지만, 기본 인코딩으로 UTF-8을 사용하는 GNU/리눅스나 MAC OS X에서 이 코드를 실행하면 아무런 문제없이 작동하므로 이 코드에 문제가 없다고 생각하기 쉽다. 파일을 쓸 때 encoding 인수를 생략하면 기본 지역 설정에 따른 인코딩 방식을 사용하며, 파일을 읽을 때도 동일한 인코딩 방식을 이용해서 올바로 읽을 수 있다. 하지만 위와 같은 예제는 플랫폼에 따라, 혹은 플랫폼이 동일해도 지역 설정에 따라 다른 바이트를 담은 파일을 생성하게 되어 호환성 문제를 일으킨다.
> 여러 컴퓨터나 여러 상황에서 실행되어야 하는 코드는 결코 기본 인코딩에 의존하면 안 된다. 기본 인코딩 방식은 컴퓨터마다, 혹은 실행할 때마다 달라질 수 있으므로 텍스트 파일을 읽을 때는 언제나 encoding 인수를 명시적으로 지정해야 한다.

- [플랫폼 올바른 인코딩 예제](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-5/correct_encoding.py)
> 인코딩 방식을 알아내기 위해 파일 내용을 분석하는 경우가 아니라면 텍스트 파일을 이진 모드로 열지 않는것이 좋다. 인코딩 방식을 알아낼 때도 직접 하는 것보다 Chardet 모듈을 사용하는 것이 좋다. 일반적으로 래스터 이미지 등 이진 파일을 열 때만 이진 모드를 사용해야 한다.

# 기본 인코딩 설정: 정신 나간 거 아냐?
파이썬에서 입출력할 때 기본 인코딩 방식은 여러 설정에 의해 영향을 받는다.

- [기본 인코딩 예제](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-5/default_encodings.py)
    * locale.getpreferredencoding()이 가장 중요한 설정이다.

    * 텍스트 파일은 기본적으로 locale.getpreferredencoding()을 사용한다.

    * 출력이 콘솔로 나가므로 sys.stdout.isatty()가 True다.

    * 따라서sys.stdout.encoding도 콘솔 인코딩과 동일하다.

***
python default_encodings.py > encodings.log

- 위 명렁어와 같이 리다이렉션을 할시엔 sys.stdout.isatty()는 False가 되고, sys.stdout.encoding은 locale.getpreferredncoding()에 의해 'cp949'로 설정된다.
    * 파일을 열 때 encoding 인수를 생략하면 locale.getpreferredncoding()에 의해 기본 인코딩 방식이 설정된다

    * PYTHONIOENCODING 환경 변수가 설정되어 있다면, 이 변수에 의해 sys의 stdout/stdin/stderr이 설정된다[참고](http://bit.ly/1lqvCUZ). 그렇지 않으면 콘솔의 설정을 가져오거나, 입출력을 파일에서/로 리다이렉션하는 경우 locale.getpreferredncoding()에 의해 정의된다.

    * 이진 데이터와 str 사이를 변환하기 위해 파이썬은 내부적으로 sys.getdefaultencoding()함수를 사용한다. 파이썬 3에서는 덜 사용하지만, 여전히 사용되고 있다. 이 설정을 변경하는 것은 지원되지 않는다.

    * sys.getfilesystemencoding() 함수는 파일 내용이 아니라 파일명을 인코딩 및 디코딩하기 위해 사용된다. 이 함수는 open()이 str 형의 파일명을 인수로 받을 때 사용된다. 파일명이 bytes 인수로 전달되면 인수를 변경하지 않고 그대로 OS의 API로 전달한다. [The Python unicode HOWTO](https://docs.python.org/3/howto/unicode.html)에 따르면 윈도우에서 파이썬은 현재 설정된 인코딩을 언급하기 위해 mbcs라는 명칭을 사용한다. MBCS는 Multi Byte Character Set의 약자로서, UTF-8이 아닌 gb2312나 Shift_JIS와 같은 레거시 가변 길이 인코딩에 사용하던 문자셋이다. 이 주제에 대해서는 스택 오버플로의 [윈도우에서 MBCS와 UTF-8의 차이](http://bit.ly/1lqvRPV)
    > GNU/리눅스 및 OS X에서는 수년간 기본적으로 모든 인코딩이 UTF-8로 설정되었으므로, 모든 입출력 루틴이 유니코드 문자를 다룬다. 윈도우에서는 동일한 시스템 안에 여러 인코딩이 사용될 뿐만 아니라, 아스키 및 인코딩에 따라 달라지는 추가 127개의 문자를 지원하는 'cp850'이나 'cp1252'와 같은 코드페이지가 일반적으로 사용된다. 따라서 윈도우 사용자는 특별한 주의를 기울이지 않으면 인코딩 오류를 접할 가능성이 훨씬 크다.
***

요약하면, 가장 중요한 인코딩 설정은 locale.getpreferredncoding() 함수가 반환하는 설정이다. 이 함수는 텍스트 파일을 열 때 기본적으로 사용되며, 표준 입출력(sys.stdout/stdin/stderr)을 리다이렉션할 때도 사용된다. 그렇지만 파이썬 문서 (http://bit.ly/1IqvYLp)에서 다음과 같이 설명하고 있다.

***
locale.getpreferredncoding(do_setlocale=True)
사용자 환경 설정에 따라 텍스트 데이터에 사용되는 인코딩을 반환한다. 사용자 환경 설정은 시스템마다 다르게 표현되며, 프로그램 코드를 통해 구할 수 없는 시스템도 있으므로, 이 함수가 반환하는 값은 추정치일 뿐이다.
***

따라서 '기본 인코딩에 의존하지 않는'것이 가장 좋다.
    



