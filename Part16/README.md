<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-1/UML_class_diagram.png)
 -->
# 코루틴

영어 사전에서 'yield' 단어를 찾아보면 '생산한다'와 '양보한다'는 두 가지 뜻을 볼 수 있다. 파이썬 제너레이터에서 yield 키워드를 사용할 때, 이 두가지 의미가 모두 적용된다. 예를 들어 yield item 문장은 next()의 호출자가 받을 값을 생성하고, 양보하고, 호출자가 진행하고 또 다른 값을 소비할 준비가 되어 다음번 next()를 호출할 때까지 제너레이터 실행을 중단한다. 호출자가 제너레이터에서 값을 꺼내오는 것이다.

구문 측면에서 보면 코루틴은 제너레이터와 똑같이 본체 안에 yield 키워드를 가진 함수일 뿐이다. 그러나 코루틴에서는 datum = yield처럼 일반적으로 yield 문이 표현식의 오른쪽에 나오거나, 값을 생성하지 않는 경우도 있다. yield 키워드 뒤에 표현식이 없으면 제너레이터는 None을 생성한다. 호출자가 next() 대신 값을 전송하는 send()를 호출하면 코루틴이 호출자로부터 데이터를 받을 수 있다. 일반적으로 호출자가 코루틴에 값을 밀어 넣는다.

심지어 yield 키워드를 통해 아무런 데이터도 주고받지 않을 수 있다. 데이터의 흐름에 무관하게 yield는 실행을 제어하는 장치로서 멀티태스킹에서의 협업을 구현하기 위해 사용할 수 있다. 즉, 각 코루틴이 중앙의 스케줄러에 제어를 양보해서 다른 코루틴이 실행되게 할 수 있다.

제어 흐름의 관점에서 yield를 보는 것에 익숙해지면, 코루틴을 이해할 수 있는 마음의 준비가 된 것이다.
파이썬 코루틴은 이 책에서 지금까지 보아온 초라한 제너레이터 함수를 계속해서 개선해온 산물이다. 파이썬 코루틴의 진화를 따라가다 보면 단계별로 기능이 많아지면서 더 복잡해지는 특징을 이해하는 데 도움이 된다.

제너레이터를 어떻게 코루틴으로 만들 수 있는지 간략히 설명한 후 이 장의 핵심으로 넘어갈것이다. 그러고 나서 다음과 같은 내용을 설명한다.
* 코루틴으로 작동하는 제너레이터의 동작과 상태
* 데커레이터를 이용해서 코루틴을 자동으로 기동하기
* 제너레이터 객체의 close()와 throw()메서드를 통해 호출자가 코루틴을 제어하는 방법
* 종료할 때 코루틴이 값을 반환하는 방법
* 새로운 yield from 구문의 사용법과 의미
* 사용 예: 시뮬레이션의 동시 활동을 관리하기 위한 코루틴

# 요약
귀도 반 로섬은 제너레이터를 이용해서 코드를 작성하는 세 가지 스타일이 있다고 했다.

**'풀' 스타일(반복자), '푸시' 스타일(이동 평균 예제), '작업'이 있다(데이비드 비즐리의 코루틴 튜토리얼을 읽어보셨나요?...)**

14장에서는 반복자를 집중적으로 다루었고, 이 장에서는 '푸시' 스타일에서 사용하는 코루틴과 간단한 '작업'스타일(시뮬레이션 예제에서의 택시 프로레스)을 설명했다. 18장에서는 이들을 병렬 프로그래밍에서의 비동기 작업으로 사용한다.

이동 평균 예제는 일반적인 코루틴 사용법(받은 항목을 처리하는 누산기로 사용)을 잘 보여준다. 코루틴을 자동으로 기동해주는 데커레이터를 이용하면 코루틴을 편리하게 사용할 수 있다. 그러나 기동해주는 데커레이터와 호환되지 않는 코루틴도 있다는 점을 명심하라. 특히 yield from subgenerator()는 하위 제너레이터가 기동되지 않았다고 가정하고 자동으로 기동해주므로 주의해야 한다.

누산기 코루틴은 send() 메서드가 호출될 때마다 중간 결과를 생성할 수 있지만, 값을 반환할수 있을 때 더 유용해진다. 코루틴이 값을 반환하는 기능은 PEP 380을 구현한 파이썬 3.3에 추가되었다. 제너레이터 안에서 return the_result 문을 실행하면 StopIteration(the_result) 예외가 발생되어 호출자가 예외 객체의 value 속성에서 the_result를 가져오는 방법을 예를 들어 알아보았다. 코루틴 결과를 가져오기 위해 다소 성가신 방법이긴 하지만 PEP380에 소개된 yield from 구문이 자동으로 처리해준다.

간단한 반복형을 이용해서 yield from에 대해 설명하기 시작하고 난 후, yield from을 제대로 사용할 때의 세 가지 구성 요소(대표 제너레이터, 하위 제너레이터, 클라이언트)를 사용한 에제를 다루었다. 대표 제너레이터는 자신의 본체 안에서 yield from을 사용하고, 하위 제너레이터는 yield from으로 활성화되며, 클라이언트 코드가 대표 제너레이터의 yield from으로 설정된 통로를 통해 하위 제너레이터에 값을 전송함으로써 전반적인 운영을 주도한다. 그리고 PEP 380에서 영어 및 파이썬과 비슷한 의사코드로 설명한 yield from의 내부 작동 과정을 자세히 살펴보았다.

그리고 마지막으로 이산 이벤트 시뮬레이션 예제를 통해 동시성을 지원하기 위해 스레드와 콜백을 대신해서 제너레이터를 사용하는 방법을 보여주었다. 간단하기는 하지만, 택시 시뮬레이션을 통해 Tornado나 asyncio 같은 이벤트 주도 프레임워크가 단일 스레드에서 핵심 루프를 사용해서 코루틴을 병렬로 실행할 수 있는지 감을 잡을 수 있었다. 코루틴을 사용하는 이벤트주도 프로그래밍 환경에서는 코루틴이 반복적으로 핵심 루프에 제어권을 넘겨주어 핵심 루프가 다른 코루틴을 활성화하고 실행할 수 있게 해줌으로써 작업을 동시에 실행한다. 이런 방식의 협업 멀티태스킹 환경에서는 코루틴이 중앙 스케줄러에 자발적으로 제어권을 넘겨준다. 이와 반대로, 스레드는 선점형 멀티태스킹을 구현한다. 선점형 멀티태스킹은 스케줄러가 언제든 스레드를 중단하고 다른 스레드를 실행할 수 있다.

그리고 이 장에서는 코루틴에 대해 'send()를 호출하거나 yield from을 이용해서 데이터를 보내는 클라이언트에 의해 실행되는 제너레이터'라고 두루뭉술한 정의를 채택했다. 'PEP 342 - 향상된 제너레이터를 통한 코루틴' (https://www.python.org/dev/peps/pep-0342/) 과 대부분의 파이썬 책은 코루틴을 이렇게 정의한다. 18장에서 설명할 asyncio 라이브러리는 코루틴을 기반으로 만들어졌지만, 코루틴을 더욱 엄격히 정의한다. asyncio 코루틴은 일반적으로 @asyncio.coroutine 데커레이터가 붙으며, send()로 직접 호출되지 않고 언제나 yield from으로 호출된다. 물론 asyncio 코루틴도 내부적으로는 next()와 send()에 의해 실행되지만, 클라이언트는 반드시 yield from만 사용해야 한다.