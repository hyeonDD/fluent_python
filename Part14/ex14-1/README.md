<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-1/UML_class_diagram.png)
 -->
# Sentence 버전 #1: 단어 시퀀스
먼저 Sentence라는 클래스를 구현하면서 반복형을 알아보자. 이 클래스의 생성자는 텍스트로 구성된 문자열을 받은 후 단어별로 반복할 수 있다. 첫 번째 버전은 시퀀스 프로토콜을 구현하며 반복할 것이다. 앞에서도 설명한 것처럼 모든 시퀀스는 반복할 수 있기 때문이다. 그러나 여기서는 왜 그렇게 되는지 알아볼 것이다.

- [sentence.py](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-1/sentence.py)
1. re.findall()은 정규 표현식에 매칭되는 중복되지 않는 문자열의 리스트를 반환한다.
2. self.words가 findall()의 결과를 담고 있으므로, 주어진 인덱스에 해당하는 단어를 반환한다.
3. 완전히 시퀀스 프로토콜에 따르려면 __len__() 메서드도 구현해야 하지만, 반복형 객체에 이 메서드가 필요한 것은 아니다.
4. reprlib.repr()은 유틸리티 함수로서, 매우 큰 데이터 구조체를 표현하는 문자열을 축약해서 생성한다.

기본적으로 reprlib.repr()은 생성할 문자열을 30자로 제한한다. 아래예제 콘솔 세션에서 Sentence를 사용하는 방법을 살펴보자.

```
s = Sentence('"the time has com," the Walrus said,') #1
s
# Sentence('"the time has com," the Walrus said,') #2
for word in s: #3
    print(word)
"""
The
time
has
come
the
Walrus
said
"""

list(s) #4
# ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']
```
1. 문자열을 이용해서 Sentence 객체를 생성한다.
2. __repr__()이 ...를 이용해서 출력한 메세지는 실제로는 reprlib.repr()이 생성한 것임에 주의하라.
3. Sentence 객체는 반복할 수 있다. 이유는 잠시 후에 설명한다.
4. 반복할 수 있으므로 Sentence 객체는 리스트 혹은 다른 반복형을 생성하기 위한 입력으로 사용할 수 있다.

이제부터 위예제의 테스트를 통고화나는 버전의 Sentence 클래스를 구현한다. 그러나 [sentence.py](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-1/sentence.py)의 구현은 시퀀스로서 다음과 같이 인덱스를 이용해서 단어를 가져올 수 있으므로, 나머지 버전과는 다르다.
```
s[0]
# 'The'
s[5]
# 'Walrus'
s[-1]
# 'said'
```
파이썬 프로그래머라면 시퀀스는 반복할 수 있다는 것을 누구나 알고 있다. 이제 그 이유를 알아보자.

## Sequence가 반복 가능한 이유: iter()함수
파이썬 인터프리터가 x 객체를 반복해야 할 때는 언제나 iter(x)를 자동으로 호출한다.
iter() 내장 함수는 다음 과정을 수행한다.
1. 객체가 __iter__() 메서드를 구현하는지 확인하고, 이 메서드를 호출해서 반복자를 가져온다.
2. __iter__() 메서드가 구현되어 있지 않지만 __getitem__()이 구현되어 있다면, 파이썬은 인덱스 0에서 시작해서 항목을 순서대로 가져오는 반복자를 생성한다.
3. 이 과정이 모두 실패하면 파이썬은 'TypeError: 'C' object is not iterable'이라는 메세지와 함께 TypeError가 발생한다. 여기서 C는 대상 객체의 클래스다.

그렇기 때문에 모든 파이썬 시퀀스는 반복할 수 있다. 시퀀스가 __getitem__()을 구현하고 있기 때문이다. 사실 표준 시퀀스는 __iter__() 메서드도 구현하고 있으므로 여러분이 정의한 시퀀스도 이 메서드를 구현해야 한다. __getitem__()을 특별히 다루는 이유는 하위 버전과의 호환성을 유지하기 위해서며, 이런 특별한 대우는 언젠가는 사라질 것이다(이 책을 쓰고 있는 현재 아직까지는 사용 중단 안내되지 않았다).

11.2절 '파이썬은 시퀀스를 찾아낸다'에서 설명한 것처럼 __iter__() 특별 메서드를 구현하는 객체뿐만 아니라 0에서 시작하는 정수형 키를 받는 __getitem__() 메서드를 구현하는 객체도 반복형으로 간주하는 것은 덕 타이핑의 극단적이 형태다.

구스 타이핑 기법을 사용하면 반복형에 대한 정의가 단순해질 수 있지만, 융통성이 떨어져서 __iter__() 특별 메서드를 구현하는 객체만 반복형이라고 간주한다. abc.iterable 클래스가 __subclasshook__() 메서드를 구현하고 있으므로 11.10절 '오리처럼 행동할 수 있는 거위'에서 설명한 것처럼 상속이나 등록은 필요 없다. 다음 예를 보자.
```
class Foo:
    def __iter__(self):
        pass


from collections import abc
issubclass(Foo, abc.Iterable)
# True
f = Foo()
isinstance(f, abc.Iterable)
# True
```
그러나 우리가 처음 구현한 Sentence 클래스는 반복형으로 사용하고는 있지만 issubclass(Sentence, abc.Iterable) 테스트를 통과하지 못한다.
> 파이썬 3.4까지는 x 객체가 반복형인지 확인하는 가장 정확한 방법은 iter(x)를 호출하고 만일에 발생할 수 있는 TypeError를 처리하는 것이다. 이 방법이 isistance(x, abc.Iterable)을 사용하는 방법보다 더 정확하다. iter(x)는 __getitem__() 메서드도 확인하는 반면, Iterable ABC는 확인하지 않기 때문이다.

객체를 반복하기 전에 그 객체가 반복형인지 명시적으로 검사하는 것은 필요하지 ㅇ낳다. 반복할 수 없는 객체를 반복하려고 시도하면 파이썬이 'TypeError: 'C' object is not iterable'이라는 명료한 메세지를 담은 에외를 발생시키기 때문이다. 예외를 발생시키는 것보다 깔끔하게 처리할 수 있다면 try/except 블록으로 처리하는 것이 좋다. 나중에 반복하기 위해 객체에 저장 해두는 경우에는 미리 명시적으로 검사하는 것도 좋다. 에러는 가능한 한 빨리 잡는 것이 좋기 때문이다.

다음 절에서는 반복형과 반복자의 관계를 명시하는 방법을 알아본다.