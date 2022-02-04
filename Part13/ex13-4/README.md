<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part13/ex13-4/UML_class_diagram.png)
 -->
# 벡터를 스칼라와 곱하기 위해 * 오버로딩하기
Vector([1, 2, 3]) * x가 뜻하는 것은 무엇일까? x가 숫자면 이 문장은 스칼라곱으로서, 벡터의 각 항목에 x를 곱해서 새로운 Vector 객체를 생성하는 것을 뜻한다.
```
v1 = Vector([1, 2, 3])
v1 * 10
# Vector([10.0, 20.0, 30.0])
11 * v1
# Vector([11.0, 22.0, 33.0])
```
Vector 피연산자를 이용해서 곱하는 또 다른 방법은 두 벡터의 내적을 구하는 스칼라곱이다.
현재 NumPy 및 이와 유사한 라이브러리에서는 * 연산자를 사용하는 경우, 벡터의 각 항목에 값을 곱하며, 벡터의 스칼라곱을 구하기 위해서는 numpy.dot()함수를 사용한다.

다시 벡터와 스칼라곱으로 돌아가자. 먼저 작동하는 가장 간단한 __mul__()과 __rmul__() 메서드를 구현하자.
```
# Vector 클래스 내부
def __mul__(self, scalar):
    return Vector(n * scalar for n in self)

def __rmul__(self, scalar):
    return self * scalar
```
이 메서드들은 호화되는 피연산자를 사용하는 한 제대로 작동한다. scalar 인수는 float 형을 곱했을 때 float 형 결과가 나오는 숫자여야 한다(Vector 클래스가 내부적으로 float의 배열을 사용하고 있기 때문이다). 따라서 complex 숫자는 사용할 수 없지만, int, bool (bool은 int의 서브클래스다), 심지어 fractions.Fraction 객체도 사용할 수 있다.

전장의 vector_v6.py:vector_v5.py에 + 연산자 메서드 추가에서 했던 것처럼 덕 타이핑 기법을 사용해서 __mul__() 안에서 TypeError를 잡을 수도 있지만, 여기서는 **구스 타이핑** 기법을 이용한 명시적인 방법을 사용하는 것이 타당하다.
scalar의 자료형을 검사하기 위해 isinstance() 함수를 사용하지만, 어떤 구체적인 자료형으로 하드코딩하는 대신 numbers.Real ABC로 검사한다. numbers.Real은 이 메서드에 필요한 자료형을 모두 포함할 뿐만 아니라 향후에 numbers.Real ABC의 실제 서브클래스나 **가상 서브클래스**로 선언된 수치형 자료도 모두 포함한다. 아래에제는 추상 자료형에 대해 명시적으로 검사하는 기법인 구스 타이핑을 사용한 예를 보여준다. 전체 코드는 내려받은 예제 코드 중 vector_v7.py를 참조하라.
> 11.6절 '표준 라이브러리의 ABC'에서 설명한 것처럼 decimal.Decimal은 numbers.Real의 가상 서브클래스로 등록되어 있지 않으므로, 여기에서 구현한 Vector 클래스는 decimal.Decimal을 처리하지 못한다.

- [vector_v7.py](https://github.com/hyeonDD/fluent_python/blob/master/Part13/ex13-4/vector_v7.py)
1. 자료형을 검사하기 위해 numbers 모듈을 임포트한다.
2. scalar가 numbers.Real 서브클래스의 객체면 항목 값들로 구성된 Vector 객체를 새로 생성한다.
3. 그렇지 않으면 NotImplemented를 반환해서 파이썬 인터프리터가 스칼라 피연산자에 __rmul__() 메서드를 시도해볼 수 있게 해준다.
4. 이 예제에서는 self * scalar 연산을 수행해서 __mul__() 메서드에 위임함으로써 __rmul__()이 정상 작동한다.

위 vector_v7에서 구현한 클래스를 이용하면 일반적인 수치형뿐만 아니라 보기 드문 수치형의 스칼라 값으로도 Vector 객체를 곱할 수 있다.
```
v1 = Vector([1.0, 2.0, 3.0])
14 * v1
# Vector([14.0, 28.0, 42.0])
v1 * True
# Vector([1.0, 2.0, 3.0])
from fractions import Fraction
v1 * Fraction(1, 3)
# Vector([0.3333333333, 0.6666666666666, 1.0])
```

+와 * 연산자를 구현하면서 중위 연산자를 구현하는 일반적인 형태를 볼 수 있따. +와 * 연산자에 대한 설명은 아래표에 나열된 모든 연산자에 적용할 수 있다. 인플레이스 연산자는 13.6절 '복합 할당 연산자'에서 자세히 설명한다.

| 연산자 | 정방향  | 역순 | 인플레이스 | 설명 |
| :--- | :--- | :--- | :--- | :--- |
| + | __add__() | __radd__() | __iadd__() | 덧셈이나 연결 |
| - | __sub__() | __rsub__() | __isub__() | 뺄셈 |
| * | __mul__() | __rmul__() | __imulv__() | 곱셈이나 반복 |
| / | __truediv__() | __rtruediv__() | __itruediv__() | 참 나눗셈 |
| // | __floordiv__() | __rfloordiv__() | __ifloordiv__() | 플로어 나눗셈 |
| % | __mod__() | __rmod__() | __imod__() | 모듈로(나머지) 연산 |
| divmod() | __divmod__() | __rdivmod__() | __idivmod__() | 플로어 나눗셈의 몫과 나머지를 튜플로 반환한다. |
| **, pow() | __pow__() | __rpow__() | __ipow__() | 누승. |
| @ | __matmul__() | __rmatmul__() | __imatmul__() | 행렬 곱셈(파이썬 3.5에 추가됨) |
| & | __and__() | __rand__() | __iand__() | 비트단위 곱(bitwise and) |
| | | __or__() | __rorv__() | __ior__() | 비트단위 합(bitwise or) |
| ^ | __xor__() | __rxor__() | __ixor__() | 비트단위 베타합(bitwise xor) |
| << | __lshift__() | __rlshift__() | __ilshift__() | 비트단위 왼쪽 쉬프트 |
| >> | __rshift__() | __rrshift__() | __irshift__() | 비트단위 오른쪽 쉬프트 |

향상된 비교 연산자는 중위 연산자의 다른 범주에 속하며, 적용되는 규칙이 약간 다르다. 향상된 비교 연산자는 13.5절 '향상된 비교 연산자'에서 자세히 다룬다.

다음 글상자는 파이썬 3.5에 소개된 @ 연산자에 대한 설명이다.

---

**_파이썬 3.5에 추가된 @ 중위 연산자 _**

파이썬 3.4에는 내적을 위한 중위 연산자가 없다. 그러나 이 책을 쓰고 있는 현재 파이썬 3.5 프리알파 버전에서는 이미 'PEP 465 - 행렬 곱셈을 위한 전용 중위 연산자' 제안서 (https://www.python.org/dev/peps/pep-0465/) 를 구현해서 @기호로 행렬 곱셈을 지원하고 있다. 즉, a @ b는 a행렬과 b 행렬의 내적을 나타낸다. @ 연산자는 '행렬 곱셈'을 나타내는 __matmul__(), __rmatmul__(), __imatmul__() 특별 메서드에 의해 지원된다. 현재 이 메서드는 표준 라이브러리 어디에서도 사용되고 있지 않지만, 파이썬 3.5 인터프리터가 @ 연산자를 인식하므로 NumPy 등의 개발자가 조만간 사용자 정의형에 이 연산자를 지원할 것이다. 파이썬 파서도 변경되어 @ 중위 연산자를 처리한다 (파이썬 3.4에서는 a @ b로 작성하면 에러가 발생한다).

호기심에 필자는 파이썬 3.5 소스 코드를 컴파일한 후, Vector의 내적을 구하기 위해 @ 연산자를 구현하고 테스트해봤다.
수행한 테스트는 다음과 같다.

```
va = Vector([1, 2, 3])
vz = Vector([5, 6, 7])
va @ vz == 38.0 # 1*5 +2*6 +3*7
# True
[10, 20, 30] @ vz
# 380.0
va @ 3
"""
Tracebak (most recent call last):
 ...
TypeError: unsupported perand type(s) for @: 'Vector' and 'int'
"""
```

@ 연산자와 관련된 특별 메서드 코드는 다음과 같다.

```
class Vector:
    # 나머지 코드는 생략한다.

    def __matmul__(self, other):
        try:
            return sum(a * b for a, b in zip(self, other))
        except TypeError:
            return Notimplemented
    
    def __rmatmul__(self, other):
        return self @ other
```

전체 소스 코드는 내려받은 예제 중 vector_py3_5.py 파일 안에 들어 있다. [vector_py3_5.py](https://github.com/hyeonDD/fluent_python/blob/master/Part13/ex13-4/vector_py3_5.py)

이 예제는 반드시 파이썬 3.5에서 실행해야 한다. 그렇지 않으면 SyntaxError 가 발생한다!

---

