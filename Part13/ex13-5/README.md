<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part13/ex13-5/UML_class_diagram.png)
 -->
# 향상된 비교 연산자
파이썬 인터프리터가 ==, !-, >, <, >=, <= 비교 연산자를 다루는 방법은 앞에서 설명한 방법과 비슷하지만(먼저 정방향 메서드를 실행하고, NotImplemented가 반환되면 역순 메서드를 실행한다), 다음과 같은 중요한 차이점이 있다.

![향상된 연산자표](https://github.com/hyeonDD/fluent_python/blob/master/Part13/ex13-5/improved_operator.png)

* 표에 나열한 것처럼 정방향과 역순 연산자에 동일한 세트의 메서드가 사용된다. 예를 들어 == 연산자의 경우에는 정방향과 역순으로 실행하기 위해 인수만 바꿔서 동일한 __eq__() 메서드를 호출하지만, 정방향으로 __gt__() 메서드를 호출하는 경우, 역순으로는 인수를 바꿔서 __lt__()메서드를 호출한다.
* ==와 != 연산자의 경우 역순 메서드가 실패하면, 파이썬은 TypeError를 발생시키는 대신 객체의 ID를 비교한다.

> **파이썬 3에서의 새로운 동작**
모든 비교 연산자의 대안 메서드 호출 과정이 파이썬 2와 달라졌다. __ne__()의 경우, 파이썬 3에서는 단지 __eq__()의 반대값이 반환된다. 순서 비교 연산자의 경우, 예를 들어 정수와 튜플을 비교하면 파이썬 3에서는 'unorderable types: int() < tuple ()>'과 같은 메세지와 함께 TypeError가 발생한다. 파이썬 2에서 이러한 비교는 객체의ID를 이용해서 임의적으로 비교한 이상한 결과가 나왔다. 사실 정수와 튜플을 비교하는 것은 의미가 없으므로, 파이썬 3에서 제대로 개선되었다고 볼 수 있다.

지금까지 설명한 규칙에 따라 [vector_v5.py](https://github.com/hyeonDD/fluent_python/blob/master/Part10/ex10-1~4/vector_v5.py)의 vector_v5.py를 검토하고 Vector.__eq__()메서드의 동작을 다음과 같이 개선해보자.
```
class Vector:
    # 나머지 메서드 생략
    
    def __eq__(self, other):
        return (len(self) == len(ohter) and
                all(a == b for a, b in zip(self, other)))
```
이 메서드는 아래와 같이 실행된다.
```
# Vector를 Vector, Vector2d, 튜플과 비교하기
va = Vector([1.0, 2.0, 3.0])            
vb = Vector(range(1, 4))
va == vb #1
# True
vc = Vector([1, 2])
from vector2d_v3 import Vector2d
v2d = Vector2d(1, 2)
vc == v2d #2
# True
t3 = (1, 2, 3)
va == t3 #3
# True
```
1. 동일한 숫자 요소를 가진 두 Vector 객체를 동일하다고 판단한다.
2. 요소의 값이 같다면, Vector와 Vector2d도 동일하다고 판단한다.
3. Vector가 동일한 갑싀 동일한 숫자 항목을 가진 튜플이나 여타 반복형과도 동일하다고 판단한다.

경우에 따라 위예제의 마지막 결과는 바람직하지 않을 수도 있다. 이에 대한 엄격한 규칙은 없으며, 애플리케이션에 따라 다르다. '파이썬의 선'에서는 다음과 같이 이야기하고 있다.

**모호함에 직면할 때는 추측하려는 유혹을 거부하라**

피연산자를 평가할 때 지나친 자유분방함은 예기치 못한 결과를 낳을 수 있으며, 프로그래머는 예기치 못한 결과를 싫어한다.

파이썬 자체를 보면 [1,2] == (1, 2)는 거짓이다. 그러므로 보수적인 입장을 취하고 어느 정도 자료형을 검사하도록 변경해보자. 두 번째 피연산자가 Vector나 Vector 서브클래스의 객체인지 검사하고, 그렇다면 기존 __eq__() 메서드와 동일하게 처리한다. 그렇지 않은 경우에는 NotImplemented를 반환해서 파이썬 인터프리터가 처리할 수 있게 해준다.(아래 예제)
```
# vector_v8.py: Vector 클래스의 __eq__()메서드 개선
def __eq__(self, other):
    if isinstance(other, Vector): #1
        return (len(self) == len(other) and
                all(a == b for a, b in zip(self, other)))
    else:
        return NotImplemented #2
```
1. other 피연산자가 Vector나 Vector 서브클래스의 객체면 기존과 동일하게 비교한다.
2. 그렇지 않으면 NotImplemented를 반환한다.

위 에서 구현한 Vector.__eq__() 메서드로 Vector를 Vector, Vector2d, 튜플과 비교하기의 테스트를 실행하면 아래 예제와 같은 결과를 볼 수 있다.
```
va = Vector([1.0, 2.0, 3.0])
vb = Vector(range(1, 4))
va == vb #1
# True
vc = Vector([1,2])
from vector2d_v3 import Vector2d
v2d = Vector2d(1, 2)
vc == v2d #2
# True
t3 = (1, 2, 3)
va == t3 #3
# False
```
1. 예상한 대로 전과 동일한 결과가 나온다.
2. 전과 동일한 결과가 나오지만, 왜 그럴까? 잠시 후에 설명한다.
3. 원하는 대로 다른 결과가 나온다. 어떻게 이렇게 되었을까? 뒤에 나오는 설명을 보라.

위 예제의 세 결과 중 첫 번째는 당연하지만, 나머지 두 개는 vector_v8.py:Vector 클래스의 __eq__() 메서드 개선 에서 NotImplemented를 반환하는 __eq__()메서드 때문에 이런 결과가 나온다. Vector와 Vector2d 객체에 일어난 일을 단계별로 설명하면 다음과 같다.
1. vc == v2d를 평가하기 위해 파이썬은 Vector.__eq__(vc, v2d)를 호출한다.
2. Vector.__eq__(vc, v2d)는 v2d가 Vector 객체가 아님을 확인하고 NotImplemented를 반환한다.
3. NotImplemented가 반환되었으므로 파이썬은 Vector2d.__eq__(v2d, vc)를 실행한다.
4. Vector2d.__eq__(v2d, vc)는 피연산자 두 개를 모두 튜플로 변환해서 비교한다. 따라서 결과가 True가 된다.

위 예제에서 Vector와 tuple의 비교는 다음과 같은 단계로 처리된다.
1. va == t3를 평가하기 위해 파이썬 인터프리터가 Vector.__eq__(va, t3)를 호출한다.
2. Vector.__eq__(va, t3)는 t3가 Vector 형이 아닌지 검사하고 NotImplemented를 반환한다.
3. NotImplemented를 받은 파이썬 인터프리터는 tuple.__eq__(t3, va)를 시도한다.
4. tuple.__eq__(t3, va)는 Vector 형에 대해 알지 못하므로 NotImplemented를 반환한다.
5. == 연산자의 경우 특별히 역순 메서드가 NotImplemented를 반환하면, 파이썬 인터프리터는 최후의 수단으로 두 객체의 ID를 비교한다.

!= 연산자는 어떻게 해야 할까? 최후에 호출되는 object 클래스에서 상속한 __ne__() 메서드가 우리 목적에 맞게 처리해주므로, 우리가 직접 구현할 필요는 없다. __eq__() 메서드가 구현되어 있고 NotImplemented를 반환하지 않으면, __ne__()는 __eq__()가 반환한 값의 반댓값을 반환한다.
즉, 위 예제에서 사용한 객체들에 대해 != 연산자는 다음과 같이 일관된 결과를 반환한다.
```
va != vb
# False
vc != v2d
# False
va != (1, 2, 3)
# True
```
obejct 클래스에서 상속한 __ne__()메서드는 원본이 C 언어로 구현되어 있다는 점을 제외하고는 다음 코드와 동일하게 작동한다.

```
def __ne__(self, other):
    eq_result = self == other
    if eq_result is NotImplemented:
        return NotImplemented
    else:
        return not eq_result
```
> **파이썬 3 문서 버그**
이 책을 쓰고 있는 현재 풍부한 비교 메서드 문서 (https://docs.python.org/3/reference/datamodel.html) 에서는 다음과 같이 설명하고 있다.
x == y 가 참이라고 해서 x != y가 거짓인 것은 아니다. 따라서__eq__()를 정의할 때 __ne__()도 연산자가 기대한 대로 동작하도록 정의해야 한다.
이 말은 파이썬 2의 경우에는 맞지만, 파이썬 3에서는 좋은 충고가 되지 않는다. __ne__() 메서드는 object 클래스에서 상속하며, 오버라이드할 필요가 거의 없기 때문이다. 귀도 반 로섬이 작성한 '파이썬 3.0의 새로운기능' 문서의 '연산자와 특별 메서드'절 (http://bit.ly/1C11zP5) 에는 새로운 동작 방식이 문서화되어 있다. 문서의 버그는 issue 4395 (http://bugs.python.org/issue4395) 에 기록되어 있다.

중위 연산자의 오버로딩에 대해 설명했으니, 이제 복합 할당 연산자에 대해 살펴보자.