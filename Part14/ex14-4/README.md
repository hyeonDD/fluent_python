<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-4/UML_class_diagram.png)
 -->
# Sentcne 버전 #3: 제너레이터 함수
동일한 기능을 파이썬스럽게 구현하려면 SequenceIterator 클래스 대신 제너레이터 함수를 사용한다. 아래예제를 살펴본 후, 제너레이터 함수에 대해 알아보자.

- [sentence_gen.py](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-4/sentence_gen.py)
1. self.words를 반복한다.
2. 현재 단어(word)를 생성한다.
3. 함수가 끝에 도달하면 값을 자동으로 반환하므로, 이 return 문은 필요 없다. 그리고 제너레이터 함수는 StopIteration도 발생시키지 않는다. 값을 모두 생산한 후 그냥 빠져나간다.
4. 별도의 반복자 클래스가 필요 없다!

여기서는 [에제 14-2]의 테스트를 통과하는 도 다른 버전의 Sentence 클래스를 구현했다. [예제 14-4]의 Sentence 코드에서 __iter__()는 SentenceIterator() 생성자를 호출해서 반복자를 생성하고 반환했다. 위 sentence_gen.py의 반복자는 사실 제네레이터 객체로서, __tier__()메서드를 호출할 때 자동으로 생성된다. 여기서는 __iter__()는 제너레이터 함수이기 때문이다.

다음 절에서는 제너레이터 함수에 대해 자세히 설명한다.

## 제너레이터 함수의 작동 방식
본체 안에 yield 키워드를 가진 함수는 모두 제너레이터 함수다. 제너레이터 함수는 호출되면 제너레이터 객체를 반환한다. 즉, 제너레이터 함수는 제너레이터 팩토리라고 할 수 있다.
> 일반 함수와 제너레이터 함수는 본체 안 어디에선가 yield 키워드를 사용한다는 구문 차이 밖에 없다. 제너레이터 함수는 def 대신 gen과 같은 새로운 키워드를 사용해야 한다고 주장하는 사람도 있었지만, 귀도 반 로섬은 동의하지 않았다. 그는 'PEP 255 - 간단한 제너레이터' 제안서 (https://www.python.org/dev/peps/pep-0255/) 에서 자신의 의견을 피력했다.

제너레이터의 작동을 잘 보여주는 간단한 예는 다음과 같다.
```
def gen_123(): #1
    yield 1 #2
    yield 2
    yield 3

gen_123 # doctest: +ELLIPSIS
# <function gen_123 at 0x...> #3
gen_123() # doctest: +ELLIPSIS
# <generator object gen_123 at 0x...> #4
for i in gen_123(): #5
    print(i)
"""
...
1
2
3
"""
g = gen_123() #6
next(g) #7
# 1
next(g)
# 2
next(g)
# 3
next(g)
"""
Traceback (most recent call alst):
 ...
StopIteration
"""
```
1. yield 키워드를 포함하고 있는 함수는 모두 제너레이터 함수다.
2. 일반적으로 제너레이터 함수 안에는 루프가 있지만, 꼭 그래야 하는 것은 아니다. 여기서 yield 키워드를 세 번 사용했다.
3. 조사해보면 gen_123()이 함수 객체임을 알 수 있다.
4. 그러나 호출하면 gen_123()이 제너레이터 객체를 반환한다.
5. 제너레이터는 yield에 전달된 표현식의 값을 생성하는 반복자다.
6. 자세히 살펴보기 위해 제너레이터 객체를 g에 할당한다.
7. g가 반복자이기도 하므로 next(g)로 호출하면 yield가 생성한 다음 항목을 가져온다.
8. 함수 본체의 실행이 완료되면 제너레이터 객체는 StopIteration을 발생시킨다.

제너레이터 함수는 함수 본체를 포함하는 제너레이터 객체를 생성한다. next()를 제너레이터 객체에 호출하면 함수 본체에 있는 다음 yield로 진행하며, next()는 함수 본체가 중단된 곳에서 생성된 값을 평가한다. 마지막으로, 함수 본체가 반환될 때 이 함수를 포함하고 있는 제너레이터 객체는 Iterator 프로토콜에 따라 StopIteration 예외를 발생시킨다.
> 제너레이터에서 가져온 결과에 대해 이야기할 때는 좀 더 명확히 하는 것이 좋을 것 같다. 제너레이터는 값을 **생성**한다고 이야기했다. 그러나 제너레이터가 값을 '반환'한다고 하면 혼란스럽다. 함수는 값을 반환한다. 제너레이터 함수를 호출하면 제너레이터 객체가 반환된다. 제너레이터 객체는 값을 생성한다. 재너레이터 객체는 일반적인 방식으로 값을 '반환'하지 않는다. 제너레이터 함수 안에 있는 return 문은 제너레이터 객체가 StopIteration 예외를 발생하게 만든다.

아래 예제는 for 루프와 함수 본체 간의 상호작용을 좀 더 명확히 보여준다.
```
# 실행할 때 메세지를 출력하는 제너레이터 함수
def gen_AB(): #1
    print('start')
    yield 'A' #2
    print('continue')
    yield 'B' #3
    print('end.') #4

for c in gen_AB(): #5
    print('-->', c) #6
"""
...
start #7
A #8
continue #9
B #10
end. #11
>>> #12
"""
```
1. 제너레이터 함수는 여느 함수와 동일하게 정의되지만, yield 키워드를 사용한다.
2. 5에 있는 for 루프에서 처음 next()를 암묵적으로 호출하면 'start'를 출력하고, 첫 번째 yield 문에서 멈춰 값 'A'를 생성한다.
3. for 루프에서 두 번째 next()를 암묵적으로 호출하면 'continue'를 출력하고, 두 번째 yield 문에서 멈춰 값 'A'를 생성한다.
4. 세 번째 next()를 호출하면 'end.'를 출력하고 함수 본체의 끝까지 실행되어, 제너레이터 객체가 StopIteration 예외를 발생시킨다.
5. 반복하기 위해 for 루프는 g = iter(gen_AB())와 대등한 문장을 실행해서 제너레이터 객체를 가져오고, 매번 반복할 때마다 next(g)를 호출한다.
6. 루프 안에서는 '-->' 문자열 뒤에 next(g)가 반환한 값을 출력한다. 그러나 이 출력은 제너레이터 함수 안의 print()문 다음에 나온다.
7. 'start'는 제너레이터 함수 본체에 있는 print('start')문에 의해 출력된다.
8. 제너레이터 함수 본체 안에 있는 yield 'A'문은 for 루프가 소비할 값 'A'를 생성하며, 이 값은 c 변수에 할당되어 '--> A'를 출력하게 만든다.
9. 두 번째 next(g)까지 반복이 진행되어 제너레이터 함수 본체는 yield 'A'에서 yield 'B'까지 진행한다. 'continue'는 제너레이터 함수 본체의 두 번째 print()문이 출력한 것이다.
10. yield 'B'는 for 루프가 소비할 값'B'를 생성하고, 이 값은 루프 변수 c에 할당되어 '--> B'를 출력한다.
11. 세 번째 next(g)가 호출되면 함수 본체의 끝까지 실해아게 된다. 'end.'는 제너레이터 함수 본체의 세 번째 print()문이 출력한 것이다.
12. 제너레이터 함수의 끝까지 실행되면 제너레이터 객체는 StopIteration 예외를 발생시킨다. for 루프는 이 예외를 잡은 후 깔끔하게 루프를 종료한다.

이제 [sentence_gen.py](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-4/sentence_gen.py)의 Sentence.__iter__()가 어떻게 작동하는지 명확히 알 수 있을 것이다. __iter__()는 제너레이터 함수로서, 호출되면 반복자 인터페이스를 구현하는 제너레이터 객체를 생성한다. 그러므로 Sentenceiterator 클래스가 더 이상 필요치 않다.

두 번째 Sentence 버전은 첫 번째 버전보다 훨씬 짧지만, 그리 느긋한 것은 아니다. 좀 더 느긋하게 처리하도록 구현할 수 있다. 최근 느긋함은 적어도 프로그래밍 언어와 API에서만큼은 좋은 성질이라고 여긴다. 느긋한 구현은 가능한 한 최후의 순간까지 값 생산을 연기한다. 느긋하게 계산함으로써 메모리를 줄일 수 있을 뿐만 아니라 불필요한 처리도 피할 수 있다.

다음 절에서는 느긋한 Sentence 클래스를 만들어보자.