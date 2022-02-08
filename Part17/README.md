<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-1/UML_class_diagram.png)
 -->
# Future를 이용한 동시성

이 장에서는 파이썬 3.2에 소개되었지만, 파이썬 2.5 이후 버전에서 PyPi의 futures 패키지 (https://pypi.python.org/pypi/futures/) 를 통해 사용할 수 있는 concureent.futures 라이브러리를 중점적으로 알아본다. 이 라이브러리는 앞의 인용문에서 미셸 시미오나토가 설명한 패턴을 구현해주므로 사용하기 쉽다.

그리고 비동기 작업의 실행을 나타내는 객체인 Future의 개념에 대해 소개한다. 이 강력한 개념은 concurrent.futures뿐만 아니라 asyncio 패키지의 기반이 된다. ayncio는 18장에서 설명한다.

일단 재미있는 에제로 시작해보자.

# 요약
이 장 앞에서는 두 개의 동시 HTTP 클라이언트와 순차 HTTP 클라이언트를 비교해서 순차 버전보다 동시 버전이 훨씬 빠르다는 것을 보여주었다.

concurrent.futures에 기반한 예제 코드를 살펴본 후, concurrent.futures와 asyncio에서 제공하는 Future 객체에 대해 자세히 알아보았다. 여기서는 concurrent.futures.Future 클래스와 asyncio.Future 클래스의 공통점을 갖오했는데, 18장에서는 이 둘의 차이점을 자세히 알아본다. 그리고 Executor.submit() 메서드로 Future 객체를 생성하고 concurrent.futures.as_completed()로 실행이 완료된 Future 객체를 반복하는 방법을 설명했다.

다음으로 GIL이라는 제한에도 불구하고 파이썬 스레드는 입출력 위주의 애플리케이션에서 유용하게 사용할 수 있음을 보여주었다. C 언어로 작성된 모든 표준 라이브러리는 GIL을 해제하므로, 스레드가 입출력을 기다리는 동안 파이썬 스케줄러는 다른 스레드로 전환할 수 있다. 그러고 나서 concurrent.futures.ProcessPoolexecutor 클래스를 이용해서 다중 프로세스를 구현하면 GIL을 우회해서 여러 CPU 코어를 사용하므로, 암호화 알고리즘을 실행할 때 4개의 작업자를 사용해서 두 배나 빨리 처리할 수 있음을 보여주었다.

그 다음 절에서는 단지 상태와 타임스탬프를 출력하며 몇 초 동안 아무런 작업을 수행하지 않는 여러 스레드를 실행하는 기본적인 예제 코드를 이요해서 concurrent.futures.Threadp=PoolExecutor 클래스가 작동하는 방식을 자세히 들여다보았다.

그리고 다시 국기 이미지를 내려받는 예제 코드로 돌아가서, 진행 막대와 에러 처리 기능을 보강하면서 futures.as_completed() 제너레이터 함수가 제공하는 공통적인 패턴을 살펴보았다. 이는 Future 객체와 Future 객체에 관련된 정보를 딕셔너리에 저장하고, 실행이 완료되어 as_completed() 반복자를 통해 반환되는 Future 객체에 대한 정보를 이 딕셔너리에서 가져오는 패턴이다.

마지막으로 하위 수준이지만 전통적으로 파이썬에서 스레드와 프로세스를 활용하기 위해 사용했던 threading과 multiprocessing 모듈을 이용해서 상위 수준의 API에 잘 맞지 않는 동시성 작업도 처리할 수 있음을 간략히 설명했다.