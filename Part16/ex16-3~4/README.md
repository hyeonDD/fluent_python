<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-3/UML_class_diagram.png)
 -->
# 예제: 이동 평균을 계산하는 코루틴

약간 더 복잡한 코루틴 예제를 살펴보자. 7장에서 클로저를 설명하면서, 이동 평균을 계산하는 객체를 만들어보았다. [예제 7-8]에서는 간단한 클래스를 구현했고, [예제 7-14]에서는 클로저를 생성해서 total과 count 변수를 보존하는 고급 함수를 구현했다. 아래 예제는 코루틴을 이용해서 이동 평균을 구하는 방법을 보여준다.

- [coroaverager0.py](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-3/coroaverager0.py)
1. 무한 루프이므로 이 코루틴은 호출자가 값을 보내주는 한 계속해서 값을 받고 결과를 생성한다. 이 코루틴은 호출자가 close() 메서드를 호출하거나, 이 객체에 대한 참조가 모두 사라져서 가비지 컬렉트되어야 종료된다.
2. 이 yield 문은 코루틴을 중단하고, 지금까지의 평균을 생성하기 위해 사용된다. 나중에 호출자가 이 코루틴에 값을 보내면 루프를 다시 실행한다.

코루틴을 사용하면 total과 count를 지역 변수로 사용할 수 있다는 장점이 있다. 객체 속성이나 별도의 클로저 없이 평균을 구하는 데 필요한 값들을 유지할 수 있다. 아래 예제는 averager() 코루틴을 활용하는 방법을 보여주는 doctest다.

- [coroaverager0.py](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-3/coroaverager0.py)
1. 코루틴 객체를 생성한다.
2. next()를 호출해서 코루틴을 기동시킨다.
3. 이제 본격적인 작업이 시작된다. send()를 호출할 때마다 현재 이동 평균이 생성된다.

위 예제의 doctest에서 next(coro_avg)를 호출하면 코루틴이 yield 문까지 실행되어 average의 초싯값이 None을 반환한다. 이 값은 콘솔에 나타나지 않는다. 이때 코루틴은 호출자가 값을 보내기를 기다리며 이 yield 문에서 중단한다. coro_avg.send(10)은 코루틴에 값을 보내 코루틴을 활성화시키고, 이 값을 term에 할당하고, total, count, averager를 계산하고, while 루프를 다시 돌아 averager를 생성하고, 또 다시 들어오기를 기다린다.

이 코드를 유심히 살펴봤다면, 본체 안에 무한 루프를 가진 averager 객체(여기서는 coro_avg)를 어떻게 종료시킬 수 있을지 궁금할 것이다. 이에 대해서는 16.5절 '코루틴 종료와 예외 처리'에서 설명한다.

코루틴의 종료에 대해 설명하기 전에, 코루틴을 기동하는 방법에 대해 알아보자. 코루틴은 사용하기 전에 기동해야 하지만, 이런 사소한 작업은 까먹기 쉽다. 이런 문제를 해결하기 위해 특별한 데커레이터를 코루틴에 적용할 수 있다. 그 데커레이터 중 하나를 다음 절에서 설명한다.

# 코루틴을 기동하기 위한 데커레이터
코루틴은 기동되기 전에는 할 수 있는 일이 많지 않다. my_coro.send(x)를 처음 호출하기 전에 반드시 next(my_coro)를 호출해야 한다. 코루틴을 편리하게 사용할 수 있도로 ㄱ기동하는 데커레이터가 종종 사용된다. 대표적으로 아래 예제의 @coroutine 데커레이터가 널리 사용된다.
- [coroutil.py](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-3/coroutil.py)
1. 데커레이트된 제너레이터 함수는 primer() 함수로 치환되며, 실행하면 기동된 제너레이터를 반환한다.
2. 데커레이트된 함수를 호출해서 제너레이터 객체를 가져온다.
3. 제너레이터를 기동한다.
4. 제너레이터를 반환한다.

- [coroaverager1.py](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-3/coroaverager1.py)
1. averager()를 호출해서 @coroutine 데커레이터의 primer() 함수 안에서 기동된 제너레이터 객체를 생성한다.
2. getgeneratorstate()함수가 'GEN_SUSPENDED'를 반환하므로, 코루틴이 값을 받을 준비가 되어 있다.
3. coro_avg 객체에 바로 값을 전송할 수 있다. 이것이 바로 데커레이터를 사용하는 이유다.
4. @coroutine 데커레이터를 임포트한다.
5. @corutine 데커레이터를 averager()함수에 적용한다.
6. 함수 본체는 coroaverager0.py 과 똑같다.

코루틴과 함께 사용하도록 설계된 특별 데커레이터를 제공하는 프레임워크가 많이 있지만, 이 프레임워크들이 모두 코루틴을 기동시키는 것은 아니다. 코루틴을 이벤트 루프에 연결하는 등 다른 서비스를 제공하는 프레임워크도 있다. 그중 Tornado 비동기 네트워킹 라이브러리에서 제공하는 @tornado.gen 데커레이터 (http://bit.ly/1MMcGBF) 가 있다.

16.7절 'yield from 사용하기'에서 설명하겠지만, yield from 구문은 자동으로 자신을 실행한 코루틴을 기동시키므로, coroutil.py에서 설명한 @coroutine 데커레이터와 함께 사용할 수 없다. 파이썬 3.4 표준 라이브러리에서 제공하는 @asyncio.coroutine 데커레이터는 yield from과 함께 사용할 수 있게 설계되었으므로 코루틴을 기동시키지 않는다. 이 데커레이터는 18장에서 설명한다.

이제 코루틴의 핵심 기능에 대해 자세히 살펴보자. 다음 절에서는 코루틴을 종료시키는 메서드와 코루틴에 예외를 던지는 메서드를 설명한다.