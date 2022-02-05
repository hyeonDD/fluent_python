<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-5~7/UML_class_diagram.png)
 -->
# Sentence 버전 #4: 느긋한 구현
Iterator 인터페이스는 느긋하게 처리하도록 설계되어 있다. next(my_iterator)는 한번에 한 항목만 생성한다. 느긋한 계산법의 반대는 조급한 계산법이며, 둘 다 프로그래밍 언어 이론에서 실제로 사용되는 용어다.

우리가 지금까지 구현한 Sentence 버전은 느긋한 버전이 아니엇다. __init__()에서 텍스트안에 있는 단어들의 리스트를 조급하게 생성해서 self.words 속성에 바인딩하기 때문이다. 그러므로 전체 텍스트를 처리해야 하며, 리스트는 거의 텍스트와 맞먹는 양의 메모리를 소비한다(텍스트 안에 비문자가 얼마나 들어 있느냐에 따라 메모리를 더 많이 소비할 수도 있다). 사용자가 처음 몇 단어만 반복한다면, 이런 연산의 대부분은 필요 없을 것이다.

파이썬 3로 프로그래밍할 때 '이것을 느긋하게 처리할 방법은 없을까?'라는 질문에 '그렇다'고 대답할 수 있는 경우가 종종 있다.

re.finditer() 함수는 re.findall()의 느긋한 버전으로, 리스트 대신 필요에 따라 re.MatchObject 객체를 생성하는 제너레이터를 반환한다. 매칭되는 항목이 많으면 re.finditer()가 메모리를 많이 절약해준다. re.finditer()를 사용하는 세 번째 버전의 Sentence 클래스는 느긋하게 처리한다. 필요할 때만 다음 단어를 생성하기 때문이다. 코드는 아래와 같다.

- [sentence_gen2.py](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-5~7/sentence_gen2.py)
1. 단어 리스트를 미리 만들 필요 없다.
2. finditer()는 self.text에서 RE_WORD에 대응되는 단어들의 반복자인 MatchObject 객체를 생성한다.
3. match.group() 메서드는 MatchObject 객체에서 매칭되는 텍스트를 추출한다.

제너레이터 함수도 멋진 방법이지만, 제너레이터 표현식을 사용하면 코드를 훨씬 더 짧게 만들 수 있다.

# Sentence 버전 #5: 제너레이터 표현식

앞 절에서 구현한 Sentence 클래스 [sentence_gen2.py](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-5~7/sentence_gen2.py)에서 사용한 간단한 제너레이터 함수는 제너레이터 표현식으로 바꿀 수 있다.

제너레이터 표현식은 지능형 리스트의 느긋한 버전이라고 생각할 수 있다. 조급하게 리스트를 생성하는 대신, 필요에 따라 항목을 느긋하게 생성하는 제너레이터를 반환하기 때문이다. 즉, 지능형 리스트가 리스트 팩토리라면, 제너레이터 표현식은 제너레이터 팩토리라고 생각할 수 있다.

아래예제는 제너레이터 표현식을 지능형 리스트와 간단히 비교해서 보여준다.
```
# 지능형 리스트와 제너레이터 표현식에 사용된 gen_AB() 제너레이터 함수
def gen_AB(): #1
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end.')
res1 = [x*3 for x in gen_AB()] #2
"""
start
continue
end.
"""
for i in res1: #3
    print('-->', i)
"""
AAA
BBB
"""
res2 = (x*3 for x in gen_AB()) #4
res2 #5
# <generator object <genexpr> at 0x10063c240>
for i in res2: #6
    print('-->', i)
"""
start
--> AAA
continue
BBB
end.
"""
```
1. 이 함수는 예제 14-6의 gen_AB() 함수와 동일하다.
2. 지능형 리스트는 gen_AB()를 호출해서생성된 제너레이터 객체가 생성한 항목(A와 B)을 조급하게 반복한다. 다음 줄에 'start','continue','end.'메세지가 출력되었음에 주의하라.
3. 이 for 루프는 지능형 리스트가 생성한 res1 리스트를 반복한다.
4. 제너레이터 표현식은 res2를 반환한다. gen_AB()를 호출하지만, 이 함수가 반환한 제너레이터를 여기에서 소비하지 않는다.
5. res2는 제너레이터 객체다.
6. for 루프가 res2를 반복해야 gen_AB()의 본체가 비로소 실행된다. for 루프가 반복될 때마다 암묵적으로 next(res2)를 호출해서 gen_AB() 안에서 다음 yield로 진행하게 만든다. gen_AB()가 출력한 메시지가 for 루프 안에서 print()로 출력한 메세지와 어떻게 섞여 있는지 주의해서 보라.

결국 제너레이터 표현식은 제너레이터를 생성하고, 제너레이터 표현식을 사용하면 Sentence 클래스의 코드를 더 짧게 만들 수 있다. 아래 예제를 보자.

- [sentence_genexp.py](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-5~7/sentence_genexp.py)
[sentence_gen2.py](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-5~7/sentence_gen2.py)와 __iter__() 메서드만 다르다. 여기서는 제너레이터 함수가 아니며(yield 문이 없다), 제너레이터를 생성해서 반환하는 제너레이터 표현식을 사용한다. 실행 결과는 sentence_gen2.py와 마찬가지로 __iter__() 메서드의 호출자가 제너레이터 객체를 받는다.

제너레이터 표현식은 편리 구문으로서, 제너레이터 함수로 대체할 수 있지만, 더 편리한 경우도 종종 있다. 다음 절에서는 제너레이터 표현식을 사용하는 방법에 대해 알아보자.

# 제너레이터 표현식: 언제 사용하나?
[예제 10-16]에서 Vector 클래스를 구현할 때 제너레이터 표현식을 여러 번 사용했다. __eq__(), __hash__(), __abs__(), angle(), angles(), format(), __add__(), __mul__() 메서드가 각각 제너레이터 표현식을 사용한다. 이들 메서드에서 지능형 리스트를 사용해도 제대로 작동하겠지만, 그러면 중간의 리스트 값을 저장하기 위해 메모리를 더 많이 사용한다. sentence_genexp.py 에서는 제너레이터 표현식을 함수를 정의하고 호출할 필요 없이 제너레이터를 생성하는 편리 구문이라고 설명했다. 반면 제너레이터 함수는 융통성이 훨씬 더 높다. 여러 문장으로 구성된 복잡한 논리를 구현할 수 있고, 심지어 **코루틴**(16장)으로 사용할 수도 있다.

논리가 간단한 경우에는 제너레이터 표현식으로도 충분하며, Vector 예제에서 본 것처럼 한눈에 보기에도 더 쉽다.

이 두 가지 방식 중에서 어떤 것을 선택할 것인지에 대한 필자의 규칙은 간단하다. 제너레이터 표현식이 여러 줄에 걸쳐 있을 때는 가독성을 위해 제너레이터 함수를 사용한다. 게다가 제너레이터 함수는 이름을 가지고 있으므로 재사용할 수도 있다.
> **구문 팁**</br>
제너레이터 표현식을 함수나 생성자에 단일 인수로 전달할 때는, 함수를 호출하는 괄호 안에서 제너레이터 표현식을 괄호로 에워쌀 필요가 없다. Vector의 __mul__() 메서드에서 Vector() 생성자를 호출할 때 본 것처럼 한 쌍의 괄호만 사용히면 된다(찾아볼 필요 없도록 아래에 가져왔다). 그러나 제너레이터 표현식 다음에 함수 인수가 더 있다면, 구문 에러를 피하기 위해 제너레이터 표현식을 괄호로 에워싸야 한다.
```
def __mul__(self, scalar):
    if isinstance(scalar, numbers.Real):
        return Vector(n * scalar for n in self)
    else:
        return Notimplemented
```
지금까지 본 Sentence 예제는 전통적인 반복자의 역할을 하는 제네레이터의 예를 보여주었다. 즉, 컬렉션에서 항목들을 꺼내오는 것이다. 그러나 제너레이터는 데이터 출처에 무관하게 값을 생성하기 위해 사용할 수도 있다. 다음 절에서 그런 사례를 설명한다.