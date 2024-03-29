<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part12/ex12-1~2/UML_class_diagram.png)
 -->
# 연산자 오버로딩 기본 지식
연산자 오버로딩을 혐오하는 사람도 많다. 이 언어 기능은 남용되거나, 프로그래머를 혼란스럽게 만들거나, 버그를 만들거나, 예상치 못한 성능상의 병목이 될 수도 있다 (지금까지 그래왔다). 그렇지만 잘 사용하면 코드의 가동것ㅇ이 향상되고 만족스러운 API를 구현할 수 있다. 파이썬은 다음과 같은 제한을 두어 융통성, 사용성, 안전성을 적절히 유지한다.
* 내장 자료형에 대한 연산자는 오버로딩할 수 없다.
* 새로운 연산자를 생성할 수 없으며, 기존 연산자를 오버로딩만 할 수 있다.
* is, and, or, not 연산자는 오버로딩할 수 없다(그러나 &, |, ~ 비트 연산자는 가능하다).

10장에서 이미 Vector 클래스에서 __eq__() 메서드가 지원하는 중위 연산자 ==를 구현했다.
이 장에서는 __eq__() 메서드를 개선해서 Vector 이외의 자료형 피연산자도 처리할 수 있게한다. 그러나 향상된 비교 연산자(==, !-, >, <, >=, <=)는 연산자 오버로딩을 하기 위해 특별한 처리가 필요하므로, Vector 클래스에 4개의 산술 연산자부터 구현한자. 먼저 가장 쉬운 단항 연산자 -와 +를 구현하고, 다음으로 중위 연산자 +와*를 구현한다.

# 단항 연산자
파이썬 언어 참조 문서의 6.5절 '단항 산술 및 비트 연산' (http://bit.ly/1JHV4bN) 에 나오는 세 개의 단항 연산자 및 이 연산자와 연관된 특별 메서드는 다음과 같다.

---

**-(__neg__)**
단항 산술 부정. x가 -2면, -x는 2다.

**+(__pos__)**
단항 산술 덧셈. 일반적으로 x와 +x는 동일하지만, 그렇지 않은 경우도 있다. 이 절 끝에 나오는 'x와 +x가 동일하지 않은 경우' 글상자에서 자세히 설명한다.

**~(__invert__)**
정수형의 비트 반전. ~x는 -(x+1)로 정의된다 (~x == -(x+1)). x가 2면, ~x는 -3이다.

---
파이썬 언어 참조 문서의 '데이터 모델'장 (https://docs.python.org/3/reference/datamodel.html#object.__neg__)에서는 내장 함수인 abs()도 단항 연산자로 나열한다.
1.2.1절 '수치형 흉내 내기'에서 설명한 것처럼 abs() 내장 함수는 __abs__() 특별 메서드와 연관되어 있다.

단항 연산자는 구현하기 쉽다. 단지 self 인수 하나를 받는 적절한 특별 메서드를 구현하면 된다. 클래스에 논리적으로 합당한 연산을 수행해야 하지만, 특히 '언제나 새로운 객체를 반환해야 한다'는 연산자의 핵심 규칙을 지켜야 한다. 즐, self를 수정하지 말고 적절한 자료형의 객체를 새로 생성해서 반환해야 한다.

-와+의 경우, 결과는 아마도 self와 같은 클래스의 객체일 것이다. +의 경우 일반적으로 self의 사본을 반환하는 것이 좋다. abs()의 경우 스칼라형 숫자가 결과로 나온다. ~의 경우 정수이외의 피연산자에 적용한다면 어떤 값이 나와야 하는지 확답하기 어려울 것이다. 예를 들어 객체 관계 매핑(ORM)에서 ~를 사용한다면 SQL의 WHERE 구를 부정한 결과를 반환하는 것이 타당할 것이다.

앞에서 약속한 대로 10장에서 구현한 Vector 클래스에 새로운 연산자 여러 개를 구현할 것이다. 아래예제는 10장에서 이미 구현한[vector_v5.py](https://github.com/hyeonDD/fluent_python/blob/master/Part10/ex10-1~4/vector_v5.py)__abs__메서드에 __neg__() 및 __pos__()연산자 메서드를 추가한 코드다.

```
def __abs__(self):
    return math.sqrt(sum(x * x for x in self))

def __neg__(self):
    return Vector(-x for x in self) #1

def __pos__(self):
    return Vector(self) #2
```
1. -v를 계산하기 위해 새로운 Vector 객체를 만들고 self의 모든 요소를 반댓값으로 채운다.
2. +v를 계산하기 위해 새로운 Vector 객체를 만들고 self의 모든 요소로 채운다.

Vector 객체를 반복할 수 있고 Vector.__init__()이 반복형 인수를 받으므로 __neg__()와 __pos__()를 짧고 멋지게 구현할 수 있다.
__invert__() 메서드는 구현하지 않을 것이므로 Vector 객체에 ~v 연산을 실행하면 파이썬은 단항 연산자 ~에 맞지 않는 피연산자라는 것을 의미하는 'bad operand type for unary ~:'Vector'.' 메세지와 함께 TypeError가 발생한다.

다음에 나오는 글상자는 여러분이 언젠가 단항 연산자 +로 내기할 때 도움이 될 내용을 설명한다. 13.3절 '벡터를 더하기 위해 + 오버로딩하기'는 중요한 내용을 담고 있다.

---

**_ x와 +x가 동일하지 않은 경우 _**

누구나 x와 +x가 같을 것이라고 생각한다 (x == +x). 사실 파이썬에서는 거의 항상 똑같다. 그러나 표준 라이브러리 안에서 x와 +x가 다른 (x != +x) 두 가지 사례를 발견했다.

첫 번째 사례는 decimal.Decimal 클래스와 관련되어 있다. 어떤 산술 콘텍스트에서 Decimal 객체 x를 생성하고 나서 다르게 설정된 콘텍스트에서 +x를 평가하면 x와 +x가 달라질 수 있다. 예를 들어 x를 특정 정밀도로 계산하고 나서 정밀도를 변경한 후 +x를 평가하면 달라질 수 있다. 아래예제를 보자.

```
#산술 콘텍스트의 정밀도를 변경하면 x와 +x가 달라질 수 있다.
import decimal
ctx = decimal.getcontext() #1
ctx.prec = 40 #2
one_third = decimal.Decimal('1') / decimal.Decimal('3') #3
one_third #4
one_third == +one_third #5
ctx.prec = 28 #6
one_third == +one_third #7
+one_third #8
```
1. 현재 산술 콘텍스트 전역 설정에 대한 참조를 가져온다.
2. 산술 콘텍스트의 정밀도를 40으로 설정한다.
3. 현재 정밀도를 이용해서 1/3을 계산한다.
4. 결과를 보면 소수점 이하 40자리까지 표현된다.
5. 이때 one_third와 +one_third가 같다.
6. 정밀도를 파이썬 3.4 Decimal 산술의 기본값인 28로 낮춘다.
7. 이제는 one_third와 +one_third가 달라진다.
8. +one_third를 조사해보면 소수점 이하 28자리 숫자까지 표시된다.

정리하면, +one_third 표현식이 나타날 때마다 one_third의 값을 이용해서 Decimal 객체를 새로 만드는데, 이때 현재의 산술 콘텍스트를 사용한다.

x와 +x가 달라지는 두 번째 사례는 collections.Counter 문서 (http://bit.ly/1JHVi2E) 에서 찾아볼 수 있다. Counter 클래스는 두 Counter 객체의 합계를 구하는 중위 연산자 + 등 여러 산술 연산자를 구현한다. 그러나 실제로 카운터는 음스가 될 수 없으므로, Counter의 덧셈은 음수나 0인 카운터를 버린다. 그리고 객체 앞에 붙은 +는 빈 Counter를 더하는 연산이므로 0보다 큰 값만 유지하는 Counter 객체를 새로 생성한다. 아래 예제를 보자.

```
ct = Counter('abracadabra')
ct
ct['r'] = -3
ct['d'] = 0
ct
+ct
```