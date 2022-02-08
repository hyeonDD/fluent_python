<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-1/UML_class_diagram.png)
 -->
# Future를 이용한 동시성

이 장에서는 파이썬 3.2에 소개되었지만, 파이썬 2.5 이후 버전에서 PyPi의 futures 패키지 (https://pypi.python.org/pypi/futures/) 를 통해 사용할 수 있는 concureent.futures 라이브러리를 중점적으로 알아본다. 이 라이브러리는 앞의 인용문에서 미셸 시미오나토가 설명한 패턴을 구현해주므로 사용하기 쉽다.

그리고 비동기 작업의 실행을 나타내는 객체인 Future의 개념에 대해 소개한다. 이 강력한 개념은 concurrent.futures뿐만 아니라 asyncio 패키지의 기반이 된다. ayncio는 18장에서 설명한다.

일단 재미있는 에제로 시작해보자.