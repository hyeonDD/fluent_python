<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-7/UML_class_diagram.png)
 -->
# yield from 사용하기
우선 yield from이 완전히 새로운 언어 구성체라는 점을 명심해야 한다. yield보다 훨씬 더 많은 일을 하므로 비슷한 키워드를 재사용한 것은 오해의 소지가 있다. 다른 언어에서는 이와 비슷한 구성체를 await라고 하는데, 핵심을 잘 전달하므로 더 좋은 키워드라고 생각한다. 제너레이터 gen()이 yield from subgen()을 호출하고, subgen()이 이어받아 값을 생성하고 gen()의 호출자에 반환한다. 실질적으로 subgen()이 직접 호출자를 이끈다. 그러는 동안 gen()은 subgen()이 종료될 때까지 실행을 중단한다.

14장에서 yield from을 for 루프 안의 yield에 대한 단축문으로 사용할 수 있다고 설명했다.
예를 들어 다음 코드가 있다고 하자.
```
def gen():
    for c in 'AB':
        yield c
    for i in range(1, 3):
        yield i

list(gen())
# ['A', 'B', 1, 2]
```

위 코드는 다음과 같이 바꿀 수 있다.
```
def gen():
    yield from 'AB'
    yield from range(1, 3)

list(gen())
# ['A', 'B', 1, 2]
```
14.10절 '파이썬 3.3의 새로운 구문: yield from'에서 yield from을 처음 언급했을 때, 아래예제의 코드를 이용해서 사용법을 보여주었다.
```
# yield from으로 반복형 객체를 연결하기
def chain(*iterables):
    for it in iterables:
        yield from it
    
s = 'ABC'
t = tuple(range(3))
list(chain(s, t))
# ['A', 'B', 'C', 0, 1, 2]
```
약간 복잡하지만 더 유용한 yield from의 에는 데이비드 비즐리, 브라이언 K. 존스의 'Python Cookbook, 3E(O'Reilly) 4.14절 '중첩 시퀀스를 단일 시퀀스로 변환하기'에서 볼 수 있다 (에제 코드는 http://bit.ly/1MMe1sc 에 있다.)

yield from x 표현식이 x 객체에 대해 첫 번째로 하는 일은 iter(x)를 호출해서 x의 반복자를 가져오는 것이다. 이는 모든 반복형이 x에 사용될 수 있다는 의미다.

그러나 값을 생성하는 내포된 for 루프를 대체하는 게 yield from이 하는 일의 전부라면 yield from 구성자가 파이썬에 추가되지 않았을 것이다. yield from의 진정한 가치는 단순한 반복형을 이용해서는 설명할 수 없고, 중첩된 제너레이터를 복잡하게 사용하는 예제가 필요하다. 그렇기 때문에 yield from을 제안한 PEP 380의 제목이 '하위 제너레이터에 위임하기 위한 구문'이다.

yield from의 주요한 특징은 가장 바깥쪽 호출자와 가장 안쪽에 있는 하위 제너레이터 사이에 양방향 채널을 열어준다는 것이다. 따라서 이 둘이 값을 직접 주고받으며, 중간에 있는 코루틴이 판에 박힌 듯한 예외 처리 코드를 구현할 필요 없이 예외를 직접 던질 수 있다. 이전에는 불가능 했던 이 새로운 방식 덕분에 코루틴 위임을 할 수 있게 되었다.

yield from을 사용하려면 코드를 상당히 많이 준비해야 한다. 필요한 작동 부위를 설명하기 위해 PEP 380은 다음과 같이 주요 용어들을 상당히 구체적으로 정의하고 있다.

---

**대표 제너레이터**
yield from <반복형> 표현식을 담고 있는 제너레이터 함수

**하위 제너레이터**
yield from 표현식 중 <반복자>에서 가져오는 제너레이터. PEP 380의 제목 '하위 제너레이터에 위임하기 위한 구문'에서 말하는 하위 제너레이터가 바로 이것이다.

**호출자**
PEP 380은 대표 제너레이터를 호출하는 코드를 '호출자'라고 표현한다. 문맥에 따라서 필자는 대표 제너레이터와 구분하기 위해 '호출자' 대신 '클라이언트'라는 용어를 사용하기도 한다. 하위 제너레이터 입장에서 보면 대표 제너레이터도 호출자기 때문이다.

---

> PEP 380에서는 하위 제너레이터를 '반복자'라고 부르기도 한다. 그러나 대표 제너레이터도 일종의 반복자이므로 이런 용어는 혼란스럽다. 따라서 필자는 PEP의 제목에 따라 '하위 제너레이터'라고 부르는 것을 선호한다. 그러나 yield from이 __next__(), send(), close(), throw()를 구현하는 제너레이터를 처리하도록 만들어졌지만, __next__()만 구현한 간단한 반복형도 하위 제너레이터가 될 수 있으며, yield from도 이 반복형을 처리할 수 있다.

아래 예제는 yield from이 작동하는 환경을 제공하며, 아래 그림은 이 에제에서 주요 부분을 설명한다.

대표 제너레이터가 yield from에서 중단하고 있는 동안, 호출자는 하위 제너레이터에 데이터를 직접 전송하고, 하위 제너레이터는 다시 데이터를 생성해서 호출자에 전달한다. 하위 제너레이터가 실행을 완료하고 인터프리터가 반환된 값을 첨부한 StopIteration을 발생시키면 대표 제너레이터가 실행을 재개한다.

![yield-channel](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-7/yield-channel.png)

coroaverager3.py 스크립트는 가상의 중1 남학생과 여학생의 몸무게와 키를 담은 딕셔너리를 일근ㄴ다. 예를 들어 'boys;m' 키는 남학생 9명의 키에 매핑되고(미터 단위), 'girls;kg'키는 여학생 10명의 몸무게에 매핑된다(킬로그램 단위). 이 스크립트는 지금까지 보아온 averager() 코루틴 각각에 데이터를 제공하고, 다음과 같이 출력한다.
```
python3 coroaverager3.py
"""
 9 boys  averaging 40.42kg
 9 boys  averaging 1.39m
10 girls averaging 42.04kg
10 girls averaging 1.43m
```
아래 예제는 이 문제에 대한 가장 간단한 해결책은 아니지만, yield from을 사용하는 방법을 잘 보여준다. 이 에제는 '파이썬 3.3의 새로워진 기능' (http://bit.ly/1HGrnVq) 에 나온 예제에서 영감을 얻었다.

- [coroaverager3.py](https://github.com/hyeonDD/fluent_python/blob/master/Part16/ex16-7/coroaverager3.py)
1. coroaverager2.py의 averager() 코루틴과 동일하다. 여기서는 하위 제너레이터다.
2. main()안의 클라이언트가 전송하는 각각의 값이 여기에 있는 term 변수에 바인딩된다.
3. 종료 조건이다. 이 조건이 없으면 이 코루틴을 호출하는 yield from은 영원히 중단된다.
4. 반환된 Result는 grouper()의 yield from 표현식의 값이 된다.
5. grouper()는 대표 제너레이터다.
6. 이 루프는 반복할 때마다 하나의 averager()객체를 생성한다. 각 averager() 객체는 하나의 코루틴으로 작동한다.
7. grouper()가 값을 받을 때마다, 이 값은 yield from에 의해 averager() 객체로 전달된다. grouper()는 클라이언트가 전송한 값들을 averager() 객체가 소진할 때까지 여기에서 중단된다. averager() 객체가 실행을 완료하고 반환한 값은 results[key]에 바인딩된다. 그러고 나서 while 루프가 avaerager() 객체를 하나 더 만들고 계속해서 값을 소비하게 한다.
8. main()이 클라이언트 코드(PEP 380에서는 '호출자'라고 한다)다. 이 함수가 코드 전체를 실행한다.
9. group은 결과를 저장할 results 딕셔너리와 특정 key로 grouper()를 호출해서 반환된 제너레이터 객체다. 이 객체는 코루틴으로 작동한다.
10. 코루틴을 기동시킨다.
11. 값을 하나씩 grouper()에 전달한다. 이 값은 averager()의 term = yield 문장의 yield 값이 된다. grouper()는 이 값을 볼 수 없다.
12. None을 grouper()에 전달하면 현재 averager()객체가 종료하고 grouper()가 실행을 재개하게 만든다. 그러면 grouper()는 또 다른 averager() 객체를 생성해서 다음 값들을 받는다.

위 예제에서 12번 설명이 가리키는 행의 '이 부분이 중요하다!'는 주석은 group.send(None)의 중요함을 강조한다. None을 전송해야 현재의 averager()객체가 종료되고 다음번 객체를 생성하게 된다. 이 코드를 제거하면 스크립트는 아무것도 출력하지 않는다. 이대 main() 함수의 거의 마지막 부근에 있는 print(results) 행의 주석을 해제하고 실행해보면 results 딕셔너리가 비어 있음을 알 수 있다.
> 왜 results에 아무런 값도 수집되지 않았는지 그 원인을 직접 알아내면 yield from의 작동 방식을 이해하는 데 큰 도움이 될 것이다. 원인은 잠시 후에 설명한다.
여기서는 위 예제의 전반적인 작동 과정을 알아보고, main()에서 중요하다고 표시한 group.send(None)을 제거하면 어떤 일이 생기는지 설명한다.
* 바깥쪽 for 루프를 반복할 때마다 group이라는 이름의 grouper() 객체를 새로 생성한다. group이 대표 제너레이터다.
* next(group)을 호출해서 grouper() 대표 제너레이터를 기동시킨다. 그러면 while True 루프로 들어가서 하위 제너레이터 averager()를 호출한 후 yield from에서 대기한다.
* 내부 for 루프에서 group.send(value)를 호출해서 하위 제너레이터 averager()에 직접 데이터를 전달한다. 이때 grouper()의 현재 group 객체는 여전히 yield from에서 멈추게 된다.
* 내부 for 루프가 끝났을 때 grouper() 객체는 여전히 yield from에 멈춰있으므로, grouper() 본체안의 results[key]에 대한 할당은 아직 실행되지 않는다.
* 바깥쪽 for 루프에서 마지막으로 group.send(None)을 호출하지 않으면, 하위 제너레이터인 averager()의 실행이 종료되지 않으므로, 대표 제너레이터인 group이 다시 활성화되지 않고, 결국 results[key]에 아무런 값도 할당되지 않는다.
* 바깥쪽 for 루프의 꼭대기로 올라가서 다시 반복하면, 새로운 grouper() 객체가 생성되어 group 변수에 바인딩된다. 기존 grouper() 객체는 더 이상 참조되지 않으므로 가비지 컬렉트된다(이때 아직 실행이 종료되지 않은 averager() 하위 제너레이터 객체도 가비지 컬렉트된다.)
> 이 실험에서 챙겨야 할 핵심 내용을 정리해보자. 하위 제너레이터가 실행을 종료하지 않으면 대표 제너레이터는 영원히 yield from에 멈춰 있게 된다. 그렇다고 해서 전체 프로그램의 진행이 중단되지는 않는다. yield와 마찬가지로 yield from이 제어권을 클라이언트(즉, 대표 제너레이터의 호출자)에 넘겨주기 때문이다. 실행이 계속되더라도 일부 작업은 끝나지 않은 상태로 남아 있게 된다.

위 예제는 대표 제너레이터와 하위 제너레이터가 하나씩만 있는 가장 간단한 형태의 yield from 예를 보여준다. 대표 제너레이터가 일종의 파이프 역할을 하므로, 대표 제너레이터가 하위 제너레이터를 호출하기 위해 yield from을 사용하고, 그 하위 제너레이터는 대표 제너레이터가 되어 또 다른 하위 제너레이터를 호출하기 위해 yield from을 사용하는 과정을 반복해서 아주 긴 파이프라인도 만들 수 있다. 이 파이프라인은 결국 yield를 사용하는 간단한 제너레이터에서 끝나야 한다. 그러나 yield from으로 반복형 객체를 연결하기 의 예제처럼 어떤 반복형 객체에서 끝날 수도 있다. 모든 yield from 체인은 가장 바깥쪽 대표 제너레이터에 next()와 send()를 호출하는 클라리이언트에 의해 주도된다. 이 메서드들은 for 루프를 통해 암묵적으로 호출할 수도 있다.

이제 PEP 380에서 공식적으로 설명하고 있는 yield from 구성체에 대해 자세히 알아보자.