<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part12/ex12-1~2/UML_class_diagram.png)
 -->
# 내장 자료형의 상속은 까다롭다
파이썬 2.2 이전까지는 list나 dict 등 내장 자료형을 상속할 수 없었다. 2.2 버전 이후부터 내장 자료형을 상속할 수 있엇지만, C 언어로 작성된 내장 클래스의 코드는 사용자가 오버라이드한 코드를 호출하지 않으므로 상당한 주의가 필요하다.

PyPy 문서의 'PyPy와 CPython의차이점'중 '내장 자료형의 서브클래스'절에서는 다음과 같이 문제를 간략히 설명하고 있다.

**공식적으로 CPython은 내장 자료형의 서브클래스에서 오버라이드한 메서드가 언제 호출되는지, 혹은 호출되지 않는지에 대해 명확한 규칙을 정의하지 않는다. 일반적으로 서브클래스에서 오버라이드한 메서드는 같은 객체의 다른 내장 메서드에 의해 결코 호출되지 않는다. 예를 들어 dict의 서브클래스에서 오버라이드한 __getitem__()메서드는 내장된 get()과 같은 메서드에 의해 호출되지 않는다.**
아래 문제를 보면 이 문제를 잘 알 수 있다.
```
class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2) #1


dd = DoppelDict(one=1) #2
dd
# {'one': 1}
dd['two'] = 2 #3
dd
# {'one': 1, 'two': [2, 2]}
dd.update(three=3) #4
dd
# {'one': 1, 'two': [2, 2], 'three': 3}
```
1. DoppelDict.__setitem__()은 저장할 때 값을 복제한다(특별한 이유는 없으며, 단지 눈에 잘 띄게 만들기 위한 것이다). 이는 슈퍼클래스를 호출해서 작동한다.
2. dict 클래스의 __init__() 메서드는 __setitem__()이 오버라이드되었다는 사실을 무시하므로, 'one'의 값을 중복하지 않고 그대로 저장한다.
3. [] 연산자는 오버라이드한 __setitem__()을 호출하므로 예상한대로 'two'가 복제된 [2, 2]에 매핑된다.
4. dict 클래스의 update() 메서드도 오버라이드된 __setitem__() 메서드를 호출하지 않으므로 'three'의 값은 복제되지 않는다.

내장 자료형은 '슈퍼클래스에서 구현된 메서드 안에서 호출하더라도 메서드 검색은 대상 객체(self)의 클래스에서 시작해야 한다'는 객체지향 프로그래밍의 기본 규칙을 어기고 있다. 이런 와중에도 3.4.2절'__missing__() 메서드'에서 설명한 __missing__() 메서드는 예외적인 상황을 처리하는 메서드이므로 문서화된 대로 작동한다.

이 문제는 self.get()이 self.__getitem__()을 호출하는 경우처럼 객체 안에서 호출할 때 뿐만 아니라, 내장 메서드가 호출하는 다른 클래스의 오버라이드된 메서드에서도 발생한다. 아래예제는 PyPy 문서 (http://bit.ly/1JHNmhX) 에서 설명한 내용을 예제 코드로 구현한 것이다.
```
class AnswerDict(dict):
    def __getitem__(self, key): #1
        return 42


ad = AnswerDict(a='foo) #2
ad['a'] #3
#42
d = {}
d.update(ad) #4
d['a] #5
#'foo'
d
#{'a': 'foo'}
```
1. AnswerDict.__getitem__()은 키와 무관하게 42를 반환한다.
2. ad는 ('a', 'foo') 키-값 쌍으로 채운 AnswerDict 객체다.
3. 예상한 대로 ad['a']는 42를 반환한다.
4. d는 평범한 dict 객체며, 여기에서는 ad 객체를 이용해서 갱신한다.
5. dict.update() 메서드는 오버라이드된 AnswerDict.__getitem__() 메서드를 무시한다.
> dict나 list, str 등의 내장 자료형은 사용자가 정의한 오버라이드된 메서드를 무시하므로, 이 클래스들을 직접 상속하면 에러가 발생하기 쉽다. 내장 자료형보다는 쉽게 확장할 수 있도록 설계된 UserDict, UserList, UserString 등을 사용하는 collections 모듈 (http://docs.python.org/3/library/collections.html) 에서 클래스를 상속하는 것이 좋다.
dict 대신 collections.UserDict를 상속하면 위 두 예제에서 발생한 문제가 해결된다. 아래 예제를 보자.
```
import collections

class DoppleDict2(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] *2)


dd = DoppleDict2(one=1)
dd
# {'one': [1, 1]}
dd['two'] = 2
dd
# {'one': [1, 1], 'two': [2, 2]}
dd.update(three=3)
dd
# {'one': [1, 1], 'two': [2, 2], 'three': [3, 3]}
class AnswerDict2(collections.UserDict):
    def __getitem__(self,key):
        return 42


ad = AnswerDict2(a='foo')
ad['a']
# 42
d = {}
d.update(ad)
d['a']
# 42
d
# {'a': 42}
```
내장 자료형을 상속하는 데 필요한 추가 작업량을 실험적으로 알아보기 위해 [예제 308]의 StrKeyDict를 수정했다. StrKeyDict의 원래 버전은 collections.UserDict를 상속하고, __missing__(), __contains__(), __setitem__() 메서드를 구현한다. dict를 직접 상속한 StrkeyDict는 데이터 저장 방식 때문에 약간만 수정한 세 개의 메서드를 구현한다. 그러나 상속한 서브클래스가 오버라이드된 __missing__(), __contains__(), __setitem__() 메서드를 무시하므로, 동일한 테스트들을 통과하기 위해 __init__(), get(), update() 메서드도 구현해야 했다. [예제 3-8]의 UserDict 서브클래스가 16줄의 코드를 필요로 하는 반면, dict를 직접 상속한 서브클래스는 37줄의 코드를 필요로 한다.

정리해보면, 이 절에서 설명한 문제는 C 언어로 구현된 내장 자료형의 메서드에 위임할 때만 발생하므로, 이러한 내장 자료형을 상속한 사용자 정의 클래스에만 영향을 미친다. UserDict나 MutableMapping 등 파이썬으로 구현된 클래스를 상속할 때는 이런 문제가 발생하지 않는다.

상속과 관련해서는 '슈퍼클래스에서 동일한 이름의 속성을 정의할 때 파이썬이 어느 속성을 사용할지 어떻게 결정할까?' 하는 다중 상속에서 발생하는 문제가 있다. 이 문제에 대한 답은 다음 절에서 제시한다.

# 다중 상속과 메서드 결정 순서
다중 상속을 지원하는 언어에서는 별개의 상위클래스가 동일한 이름으로 메서드를 구현할 때 발생하는 이름 충돌 문제를 해결해야 한다. 아래의 예제와 보여주는 것처럼 이런 이름 충돌 문제를 '다이아몬드 문제'라고 한다.

- [diamond.py](https://github.com/hyeonDD/fluent_python/blob/master/Part12/ex12-1~2/diamond.py)
B 클래스와 C 클래스 모두 pong() 메서드를 구현하고 있지만, C.pong() 메서드는 대문자(PONG)로 출력한다는 점이 다르다.

D 객체에서 d.pong()을 호출하면, 실제 어느 pong() 메서드가 호출될까? C++에서는 이런 모호함을 해결하기 위해 프로그래머가 메서드 앞에 클래스명을 명시해야 한다. 아래 예제에서 보는 것처럼 파이썬에서도 클래스명을 직접 명시할 수 있다.

```
from diamond import *
d = D()
d.pong() #1
C.pong(d) #2
```
1. 단순히 d.pong()으로 호출하면 B 클래스의 메서드가 호출된다.
2. 객체를 인수로 전달해서 슈퍼클래스의 메서드를 직접 호출할 수 있다.

파이썬이 상속 그래프를 조회할 때는 특정한 순서를 따르므로, d.pong()과 같은 호출의 모호함이 해결된다. 이 순서를 메서드 결정 순서(MRO)라고 한다. 클래스에 있는 __mro__ 속성은 현재 클래스부터 object 클래스까지 슈퍼클래스들의 MRO를 튜플 형태로 저장한다. D 클래스의 __mro__는 다음과 같다.
```
D.__mro__
```
슈퍼클래스 메서드에 위임할 때는 내장 함수인 super()를 사용하는 것이 좋다. 아래예제의 D 클래스의 pingpong() 메서드에서 보는 것처럼, 파이썬 3에서는 사용하기 더 쉬워졌다. 그러나 MRO를 우회해서 슈퍼클래스 메서드를 직접 호출할 수 있으며, 때로는 이 방법이 더 편리하다. 예를 들어 D.ping() 메서드는 다음과 같이 구현할 수 있다.
```
def ping(self):
    A.ping(self) # super().ping() 대신 호출
    print('post-ping:', self)
```
객체 메서드를 클래스에 직접 호출할 때는 self를 반드시 명시해야 한다. **바인딩되지 않은 메서드**에 접근하는 것이기 때문이다.
그러나 프레임워크 혹은 여러분이 직접 제어할수 없는 클래스 계층구조에 들어 있는 메서드를 호출할 때는 super()를 사용하는 것이 안전하며, 향후 프레임워크가 변경되어도 문제없이 작동한다. 아래예제는 메서드를 호출할 때 super()가 MRO를 따른다는 사실을 보여준다.
```
from diamond import D
d = D()
d.ping() #1
```
1. D클래스의 ping()은 메서드를 두번 호추랗ㄴ다.
2. 첫 번째 호출은 super().ping()으로, super()는 ping()을 A 클래스의 ping()으로 위임한다. 이 메세지는 A.ping()이 출력한 것이다.
3. 두 번째 메시지는 그 다음에 호출한 print('post-ping:', self)가 출력한 것이다.

이제 D 객체에서 pingpong()을 호출할 때 어떤 일이 생기는지 알아보자 (아래 예제)
```
from diamond import D
d = D()
d.pingpong()
```
1. self.ping()이 출력한 것으로서, D 객체의 ping()메서드를 실행한 결과다. 이줄과 다음줄이 출력된다.
2. super().ping()이 출력한 것으로서, D.ping()대신 A.ping()을 호출한다.
3. self.pong()이 출력한 것으로서, __mro__에 따라 B.pong()을 호출한다.
4. super().pong()이 출력한 것으로서, 이것도 __mro__에 따라 B.pong()을 호출한다.
5. C.pong(self)가 출력한 것으로서, __mro__를 무시하고 C.pong()을 호출한다.

MRO는 상속 그래프를 고려할 뿐만 아니라 서브클래스 정의에 나열된 슈퍼클래스들의 순서도 고려한다. 즉, [diamond.py](https://github.com/hyeonDD/fluent_python/blob/master/Part12/ex12-1~2/diamond.py)에서 D 클래스를 class D(C, B)로 선언했다면, B클래스보다 C 클래스를 먼저 찾도록 D 클래스의 __mro__도 변경된다.

클래스 계층구조를 조사할 때 필자는 클래스의 __mro__를 종종 살펴본다. 아래 예제는 우리에게 익숙한 여러 클래스의 __mro__를 조사한 것이다.
```
bool.__mro__ #1
def print_mro(cls): #2 
    print(', '.join(c.__name__ for c in cls.__mro__))

print_mro(bool)
from frenchdeck2 import FrenchDeck2
print_mro(FrenchDeck2) #3
import numbers
print_mro(numbers.Integral) #4
import io #5
print_mro(io.BytesIO)
print_mro(io.TextIOWrapper)
```
1. bool은 int와 object로부터 메서드와 속성을 상속한다.
2. MRO를 좀 더 간결하게 출력하는 print_mro() 함수를 정의한다.
3. FrenchDeck2는 collections.abc 모듈의 여러 ABC를 슈퍼클래스로 가진다.
4. numbers 모듈에서 제공하는 여러 수치형 ABC다.
5. io 모듈에는 BytesIO 및 TextIOWrapper와 같은 구상 클래스와 여러 ABC(...Base가 붙은)가 들어 있다. open()으로 파일을 열 때 모드에 따라 이진 파일의 경우 BytesIO, 텍스트 파일의 경우 TextIOWrapper 객체가 반환된다.
