<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part13/ex13-5/UML_class_diagram.png)
 -->
# 복합 할당 연산자
우리가 구현한 Vector 클래스는 이미 +=과 *= 복합 할당 연산자를 지원하고 있다. 아래예제에서 이를 확인해보자.
```
v1 = Vector([1, 2, 3])
v1_alias = v1 #1
id(v1) #2
# 4302860128
v1 += Vector([4, 5, 6]) #3
v1 #4
# Vector([5.0, 7.0, 9.0])
id(v1) #5
4302859904
v1_alias #6
Vector([1.0, 2.0, 3.0])
v1 *= 11 #7
v1 #8
# Vector([55.0, 77.0, 99.0])
id(v1)
# 4302858336
```
1. 별명을 생성해서 Vector([1, 2, 3]) 객체를 나중에 다시 조사할 수 있게 한다.
2. 원래 Vector 객체의 ID는 v1에 바인딩되었다.
3. 덧셈 할당자를 실행한다.
4. 예상한 대로 실행된다.
5. 그러나 Vector 객체가 새로 생성되었다.
6. v1_alias를 조사해서 원래 Vector 객체가 변경되지 않았음을 확인한다.
7. 곱셈 할당자를 실행한다.
8. 예상한 결과가 나오지만, Vector 객체가 새로 생성되었다.

클래스가 

[향상된 연산자표](https://github.com/hyeonDD/fluent_python/blob/master/Part13/ex13-5/improved_operator.png)

에 나열된 인플레이스 연산자를 구현하지 않으면, 복합 할당 연산자는 단지편의 구문으로서, a += b를 정확히 a = a + b와 동일하게 평가한다. 가변형의 경우 이렇게 동작하는 것이 타당하며, __ad__() 메서드가 구현되어 있으면 아무런 코드를 추가하지 않고도 += 연산자가 작동한다.

그러나 __iadd__() 등의 인플레이스 연산자 메서드를 정의한 경우, a += b를 계산하기 위해 정의된 메서드가 호출된다. 이름에서도 알 수 있듯이 이런 연산자는 새로운 객체를 생성하지 않고 왼쪽에 나온 피연산자를 직접 변경한다.
> 인플레이스 연산자처럼 피연산자를 변경하는 특별 메서드는 우리가 구현한 Vector 클래스 같은 불변 자료형에서는 구현하면 안 된다. 당연한 것 같지만, 다시 한번 얘기할 필요는 있다.
객체의 내용을 변경하는 연산자를 보여주기 위해 11장의 BingoCage 클래스를 확장해서 __add__()와 __iadd__()를 구현해보자.

새로운 서브클래스를 Addablebingocage라고 하자. 아래 예제는 우리가 원하는 + 연산자의 동작 방식이다.
```
vowels = 'AEIOU'
globe = AddableBingoCage(vowels) #1
globe.inspect()
# ('A', 'E', 'I', 'O', 'U')
globe.pick() in vowels #2
# True
len(globe.inspect()) #3
# 4
globe2 = AddableBingoCage('XYZ') #4
globe3 = globe + globe2
len(globe3.inspect()) #5
# 7
void = globe + [10, 20] #6
Traceback (most recent call last):
 ...
TypeError: unsupported operand type(s) for +: 'AddableBingoCage' and 'list'
```
1. 항목 다섯 개 (각기 모음에 해당한다)를 가진 globe 객체를 생성한다.
2. 항목 하나를 꺼내서 모음 문자(vowels)인지 확인한다.
3. globe의 항목이 네 개로 줄었는지 확인한다.
4. 항목 세 개를 가진 두 번째 객체를 생성한다.
5. 앞의 객체 두 개를 더해서 세 번째 객체를 생성한다. 이 객체는 일곱 개의 항목을 가지고 있다.
6. AddableBingoCage를 list에 더하려고 시도하면 TypeError가 발생하면서 실패한다. 이 에러 메세지는 __add__() 메서드가 NotImplemented를 반환한 후 파이썬 인터프리터가 생성한다.

AddableBingoCage는 가변형이므로 아래예제에서는 우리가 __iadd__()를 직접 구현했을 때 어떻게 작동하는지 보여준다.
```
globe_orig = globe #1
len(globe.inspect()) #2
# 4
globe += globe2 #3
len(globe.inspect())
# 7
globe += ['M', 'N'] #4
len(globe.inspect())
# 9
globe is globe_orig #5
# True
globe +=1 #6
Traceback (most recent call last):
 ...
TypeError: right operand in += must be 'AddableBingoCage' or an iterable
```
1. 별명을 생성해서 나중에 객체의 정체성을 확인할 수 있게 한다.
2. globe는 네 개의 항목을 가지고 있다.
3. AddableBingoCage 객체는 동일한 클래스의 다른 객체에서 항목을 받을 수 있다.
4. += 연산자의 오른쪽 피연산자에는 어떠한 반복형이라도 올 수 있다.
5. 이 예제 내내 globe는 globe_orig 객체를 참조하고 있다.
6. 비반복형을 AddableBingoCage에 추가하면 적절한 에러 메시지와 함께 실패한다.

두 번째 피연산자의 측면에서 보면 += 연산자가 + 연산자보다 자유롭다. + 연산자의 경우 서로다른 자료형을 받으면 결과가 어떤 자료형이 되어야 하는지 혼란스러울 수 있으므로, 양쪽 피연산자가 동일한 자료형(여기서는 AddableBingoCage)이기를 원한다. += 연산자의 경우에는 이러한 혼란이 없다. 왼쪽 객체의 내용이 갱신되므로, 연산 결과 자료형이 명확하다.
> 필자는 내장된 list형이 작동하는 방식을 관찰하면서 +와 += 연산자의 상충되는 동작 방식을 확인했다. my_list + x 연산을 수행할 때는 x가 list일 때만 my_list에 연결할 수 있지만, my_list += x 연산을 구행할 때는 x가 어떠한 반복형이더라도 my_list에 연결할 수 있다. 이러한 작동 방식은 모든 반복형을 인수로 받는 list.extend() 메서드의 작동 방식과도 일치한다.

AddableBingoCage의 올바른 작동 방식에 대해 명확히 정리했으므로, 아래예제에 구현된 클래스를 살펴보자.
```
import itertools #1

from tombola import Tombola
from bingo import Bingocage

class AddableBingoCage(BingoCage): #2

    def __add__(self, other):
        if isinstance(other, Tombola): #3
            return AddableBingoCage(self.inspect() + other.inspect()) #4
        else:
            return NotImplemented
    
    def __iadd__(self, other):
        if isinstance(other, Tombola):
            other_iterable = other.inspect()
        else:
            try:
                other_iterable = iter(other) #5
            except TypeError: #6
                self_cls = type(self).__name__
                msg = "right operand in += must be {!r} or an iterable"
                raise TypeError(msg.format(self_cls))
        self.load(other_iterable) #7
        return self #8
```
1. 'PEP 8 - 파이썬 코드 스타일 가이드 문서 (https://www.python.org/dev/peps/pep-0008/#imports) 에서는 여러분이 구현한 모듈보다 표준 라이브러리를 먼저 임포트하라고 권고한다.
2. AddableBingoCage는 BingoCage 클래스를 확장한다.
3. __add__() 메서드는 두 번째 피연산자가 Tombola 객체일 때만 작동한다.
4. other 객체에서 항목을 가져온다.
5. Tombola 객체가 아닐 때는 other의 반복자를 가져온다.
6. 실패하면 메시지와 함께 예외를 발생시킨다. 가능하면 에러 메시지에 사용자가 문제를 해결할 방법을 명확히 알려주는 것이 좋다.
7. 여기까지 왔다면 other_iterable을 self에 로딩할 수 있다.
8. 이 부분이 정말 중요하다. 할당 연산 특별 메서드는 반드시 self를 반환해야 한다.

위 예제의 __add__()와 __iadd__() 메서드에서 결과를 생성하는 return 문을 비교해서 인플레이스 연산자의 특징을 다음과 같이 정리할 수 있다.

---

**__add__()**
AddableBingoCage()를 호출해서 생성된 새로운 객체를 반환한다.

**__iadd__()**
객체 자신을 변경한 후 self를 반환한다.

---

위 예제를 마치기 전에 예제를 한 번 더 살펴보자. 구조적으로 AddableBingoCage에는 __radd__()가 구현되어 있지 않다. 필요가 없기 때문이다. 정방향 메서드 __add__()는 오른쪽에도 동일한 자료형의 객체가 와야 작동하므로, AddableBingoCage인 a와 AddableBingoCage가 아닌 b를 이용해서 파이썬이 a + b를 계산하면 NotImplemented를 반환하므로, b 객체의 클래스가 이 연산을 처리할 수 있다. 그러나 표현식이 b + a고, b가 Addable bingoCage가 아니며, 그 결과 NotImplemented를 반환하면 파이썬이 TypeError를 발생시키고 포기하는 것이 낫다. b객체는 처리할 수 없기 때문이다.
> 일반적으로 __mul__()과 같은 정방향 중위 연산자는 self와 동일한 자료형만 처리할 수 있도록 설계되었다. __rmul__()과 같이 대응하는 역순 메서드를 구현할 수 있지만, 역순 메서드는 피연산자의 자료형이 다를 때만 호출되도록 설계되어 있다.

이것으로 파이썬에서의 연산자 오버로딩에 대한 설명을 마친다.