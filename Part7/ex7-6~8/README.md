# 클로저
<!-- 
- [지역 및 전역 변수를 읽는 함수](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-6~8/read_local_global_func.py)
 -->
앞에서 구현한 make_averager()는 그리 효율적이지 않다. 앞에서 우리는 모든 값을 series에 저장하고 average()가 호출될 때마다 sum을 다시 계산했다.
합께와 항목 수를 저장한 후 이 두개의 숫자를 이용해서 평균을 구하면 훨씬 더 효율적으로 구현할 수 있다.

아래 코드는 잘못 구현한 코드다. 어디가 잘못되었을까?

- [잘못된 averager 고위 함수](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-6~8/wrong_averager.py)
위 코드를 실행해보면 아래와 같은 결과가 나온다.

```
Traceback (most recent call last):
  File "d:\code\vscode\github\fluent_python\Part7\ex7-6~8\wrong_averager.py", line 12, in <module>
    make_averager(12)
TypeError: make_averager() takes 0 positional arguments but 1 was given
```
count가 수치형이거나 어떤 가변형일 때 count += 1 문이 실제로는 count = count + 1을 의미하기 때문에 문제가 발생한다. 따라서 averager()본체 안에서 count 변수에 할당하고 있으므로 count를 지역변수로 만든다. total 변수에도 동일한 문제가 발생한다.

[series로 만든 고위 함수](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-5/average.py.py)에서는 series 변수에 할당하지 않기 때문에 이런 문제가 생기지 않았다. 단지 series.append()를 호출한 후 series에 sum()과 len()을 호출했을 뿐이다. 즉, 리스트가 가변형이라는 사실을 이용했을 뿐이다.

그러나 숫자, 문자열, 튜플 등 불변형은 읽을 수만 있고 값은 갱신할 수 없다. count = count+ 1 과같은 문장으로 변수를 다시 바인딩하면 암묵적으로 count라는 지역 변수를 만든다. count가 더 이상 자유 변수가 아니므로 클로저에 저장되지 않는다.

이 문제를 해결하기 위해 파이썬 3에 nonlocal 선언이 소개되었다. 변수를 nonlocal로 선언하면 함수 안에서 변수에 새로운 값을 할당하더라도 그 변수는 자유 변수임을 나타낸다. 새로운 값을 nonlocal 변수에 할당하면 클로저에 저장된 바인딩이 변경된다. 새로운 make_averager()를 올바로 구현한 코드는 아래와 같다.

- [전체 이력을 유지하지 않고 이동 평균 계산하기](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-6~8/correct_averager.py)
    > 파이썬 2 에서 nonlocal을 사용하지 않고 해결하는 방법 
    파이썬 2 에는 nonlocal 기능이 없으므로 다른 방법을 찾아야 한다. 그중 하나는 nonlocal을 제안한 'PEP3104 - 외부 범위의 명칭에 대한 접근문서'(http://python.org/dev/peps/pep-3104)의 세번째 코드에서 설명하고 있다. 이 방법은 본질적으로 내부 함수에서 변경해야 하는 변수(count나 total 등)를 가변객체(dict나 간단한 객체 등)의 항목이나 속성으로 저장하고, 그 객체를 자유변수에 바인딩한다.

파이썬 클로저에 대해 알아보아보았으니, 이제 내포된 함수로 데커레이터를 효율적으로 구현할 수 있을 것이다.

# 간단한 데커레이터 구현하기
아래 예제는 데커레이트된 함수를 호출할 때마다 시간을 측정해서 실행에 소요된 시간, 전달된 인수, 반환값을 출력하는 데커레이터다.

- [함수의 실행 시간을 출력하는 간단한 데커레이터](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-6~8/time_decorate.py)
- [함수의 실행 시간을 출력하는 간단한 데커레이터 사용 예](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-6~8/time_decorate_usage.py)

## 작동 과정
앞에서 설명한 내용을 다시 살펴보자.

```
@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)
```
위 코드는 실제로 다음 코드로 실행된다.

```
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)
factorial = clock(factorial)
```
따라서 앞의 두 예제에서 clock()은 factorial()함수를 func 인수로 받는다. 그 후 clocked()함수를 만들어서 반환하는데, 파이썬 인터프리터가 내부적으로 clocked()를 factorial에 할당했다. 실제로 clockdeco_demo 모듈을 임포트해서 factorial의 __name__속성을 조사해보면 다음과 같은 결과가 나온다.
```
import time_decorate
print(time_decorate.factorial.__name__) # >>> 'clocked'
```
그로므로 factorial은 이제 실제로 clocked()함수를 참조한다. 이제부터 factorial(n)을 호출하면 clocked(n)이 실행된다. 본질적으로 clocked()함수는 다음과 같은 연산을 수행한다.
1. 초기 시각 t0를 기록한다.
2. 원래의 factorial()함수를 호출하고 결과를 저장한다.
3. 흘러간 시간을 계산한다.
4. 수집한 데이터를 포맷하고 출력한다.
5. 2번째 단계에서 저장한 결과를 반환한다.

이 예제 코드는 전형적인 데커레이터의 작동 방식을 보여준다. 데커레이트된 함수를 동일한 인수를 받는 함수로 교체하고, (일반적으로) 데커레이트된 함수가 반환해야 하는 값을 반환하면서, 추가적인 처리를 수행한다.
> **디자인 패턴**에서는 '추가적인 책임을 객체에 동적으로 부여한다'는 설명으로 데커레이터 패턴에 대한 간단한 설명을 시작한다. 함수 데커레이터의 경우에는 이 설명이 적합하다. 그렇지만 구현 수준에서 파이썬 데커레이터는 **디자인 패턴**에서 설명하는 고전적인 데커레이터의 작동 방식과 닮은 점이 거의 없다. 이에 대해서는 이장 마지막에 나오는 '뒷이야기'에서 자세히 설명한다.

위에서 구현한 clock() 데커레이터는 단점이 몇 가지 있다. 키워드 인수를 지원하지 않으며, 데커레이트된 함수의 __name__과__doc__속성을 가린다. 아래 예제는 functools.wraps() 데커레이트를 이용해서 func에서 clocked로 관련된 속성을 복사한다. 게다가 새로운 버전에서는 키워드 인수도 제대로 처리된다.

- [개선된 clock 데커레이터](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-6~8/time_decorate2.py)
functools.wraps()는 표준 라이브러리에서 제공하는 데커레이터 중 하나일 뿐이다. 다음 절에서는 functools가 제공하는 가장 인상적인 데커레이터인 lru_cache()와 singledispatch()를 살펴본다.

# 표준 라이브러리에서 제공하는 데커레이터
파이썬에서 메서드를 데커레이트하기 위해 property(), classmethod(), staticmethod()등 총 3개의 내장 함수를 제공한다. property()에 대해서는 19.2절 '속성을 검증하기 위해 프로퍼티 사용하기'에서 설명하며, 나머지 두 함수는 9.4절 '@classmethod와 @staticmethod'에서 설명한다.

그리고 자주 볼 수 있는 데커레이터 중에는 functools.wraps()가 있다. 이 함수는 제대로 작동하는 데커레이터를 만들기 위한 헬퍼로, [개선된 clock 데커레이터](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-6~8/time_decorate2.py)에서도 사용 했다. 표준 라이브러리가 제공하는 데커레이터들 중 lru_cache()와 파이썬 3.4에 추가된 완전히 새로운 singledispatch()가 가장 흥미롭다. 이 두 데커레이터는 functools 모듈에 정의되어 있으며, 다음 절에서 설명한다.

## functools.lru_cache()를 이용한 메모제이션
functools.lru_cache()는 실제로 쓸모가 많은 데커레이터로서, 메모제이션을구현한다. 메모제이션은 이전에 실행한 값비싼 함수의 결과를 저장함으로써 이전에 사용된 인수에 대해 다시 계산할 필요가 없게 해준다. 이름 앞에 붙은 LRU는 'Least Recently Used'의 약자로서, 오랫동안 사용하지 않은 항목을 버림으로써 캐시가 무한정 커지지 않음을 의미한다.

아래 예제에서 보는것처럼, n번째 피보나치 수열을 생성하기 위해 아주 느리게 실행되는 재귀 함수에서 lru_cache()데커레이터가 진가를 발휘한다.

- [피보나치 수열에서 n번째 숫자를 아주 값비싸게 계산하는 방식](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-6~8/fibonacci.py)
fibonacci(1)이 8번, fibonacci(2)가 5번 호출되는 등 계산 낭비가 엄청나다. 그렇지만 lru_cache()를 사용하기 위해 단 두 줄만 추가하면 성능이 상당히 개선된다. 아래를 보자
```
[0.00000030s] fibonacci(0) -> 0
[0.00000050s] fibonacci(1) -> 1
[0.00000030s] fibonacci(0) -> 0
[0.00000050s] fibonacci(1) -> 1
[0.00029440s] fibonacci(2) -> 1
[0.00069760s] fibonacci(3) -> 2
[0.00168110s] fibonacci(4) -> 3
[0.00000020s] fibonacci(1) -> 1
[0.00000030s] fibonacci(0) -> 0
[0.00000060s] fibonacci(1) -> 1
[0.00024240s] fibonacci(2) -> 1
[0.00051040s] fibonacci(3) -> 2
[0.00000020s] fibonacci(0) -> 0
[0.00000030s] fibonacci(1) -> 1
[0.00015140s] fibonacci(2) -> 1
[0.00000020s] fibonacci(1) -> 1
[0.00000030s] fibonacci(0) -> 0
[0.00000060s] fibonacci(1) -> 1
[0.00014390s] fibonacci(2) -> 1
[0.00027890s] fibonacci(3) -> 2
[0.00056510s] fibonacci(4) -> 3
[0.00120780s] fibonacci(5) -> 5
[0.00308710s] fibonacci(6) -> 8
```
- [피보나치 수열을 캐시를 사용해 더 빠른 구현](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-6~8/fibonacci_cache.py)
```
[0.00000030s] fibonacci(0) -> 0
[0.00000060s] fibonacci(1) -> 1
[0.00058680s] fibonacci(2) -> 1
[0.00000080s] fibonacci(3) -> 2
[0.00105870s] fibonacci(4) -> 3
[0.00000070s] fibonacci(5) -> 5
[0.00142800s] fibonacci(6) -> 8
```
위와 같이 실행 시간이 절반으로 줄었고, 각 n에 대해 함수가 한 번만 호추로딘다.

캐시를 사용한 경우, fibonacci(30)은 피보나치 함수를 31번만 호출해서 0.0005초 만에 실행되었지만,
캐시를 사용하지 않은 경우, fibonacci(30)은 피보나치 함수를 2,692,537번이나 호출해서 17.7초 에 실행되었다.

어리석은 재귀 알고리즘을 쓸 만하게 만드는 것 외에 lru_cache()는 웹에서 정보를 가져와야하는 애플리케이션에서도 진가를 발휘한다.

lru_cache()는 두 개의 선택적 인수를 이용해서 설정할 수 있다는 점에 주의하라. lru_cache()의 전체 시그너처는 다음과 같다.
```
functools.lru_cache(maxsize=128, typed=False)
```
maxsize 인수는 얼마나 많은 호출을 저장할지 결정한다. 캐시가 가득차면 가장 오래된 결과를 버리고 공간을 확보한다. 최적의 성능을 내기 위해 maxsize는 2의 제곱이 되어야 한다. typed인수는 True로 설정되는 경우 인수의 자료형이 다르면 결과를 따로 저장한다. 예를 들어 일반적으로 1과 1.0은 동일하다고 가정하지만 실수형 인수와 정수형 인수를 구분해야 하는 경우가 있을 것이다. 그건 그렇고, lru_cache()가 결과를 저장하기 위해 딕셔너리를 사용하고, 호출할때 사용한 위치 인수와 키워드 인수를 키로 사용하므로, 데커레이트된 함수가 받는 인수는 모두 **해시 가능**해야 한다.

이제 아래에서는 functools.singledispatch() 데커레이터를 살펴보자.

## 단일 디스패치를 이용한 범용 함수
웹 애플리케이션을 디버깅하는 도구를 만들고 있다고 가정하자. 파이썬 객체의 자료형마다 HTML 코드를 생성하고자 한다.

먼저 다음과 같이 기본적인 함수를 정의할 수 있다.
```
import html
    def htmlize(obj):
        content = html.escape(repr(obj))
        return '<pre>{}</pre>'.format(content)
```
이 코드는 모든 파이썬 자료형을 잘 처리한다. 그렇지만 일부 자료형에 대해 다음과 같이 고유한 코드를 생성하도록 이 코드를 확장하려 한다.
* str: 개행 문자를 '<br>\n'으로 대체하고 <pre> 대신 <p> 태그를 사용한다.
* int: 숫자를 10진수와 16진수로 보여준다.
* list: 각 항목을 자료형에 따라 포맷한 HTML 리스트를 출력한다.

우리가 원하는 실행 결과는 아래와 같다.
```
>>> htmlize({1,2,3})
'<pre>{1,2,3}</pre>'
>>> htmlize(abs)
'<pre>&lt;buitl-in function abs&gt;</pre>'
>>> htmlize('Heimlich & Co. \n- a game)
'<p>Heimlich &amp; Co. <br>\n- a game</p>'
>>> htmlize(42)
'<pre>42 (0x2a)</pre>'
>>> print(htmlize('alpha', 66, {3,2,1}))
<ul>
<li><p>aplpha</p></li>
<li><pre>66 (0x42)</pre></li>
<li><pre>{1, 2, 3}</pre></li>
</ul>
```
1. 기본적으로 객체를 표현하고 HTML 이스케이프를 적용해서 <pre></pre>안에 넣는다.
2. str 객체도 HTML 이스케이프를 적용하지만 <p></p>안에 넣고 개행 문자에 <br>을 붙인다.
3. int형 데이터는 <pre></pre>안에 10진수와 16진수로 표현된다.
4. 각 리스트 항목은 해당 자료형에 따라 포맷하고, 전체 시퀀스는 HTML 리스트로 만든다.

파이썬에서는 메서드나 함수의 오버로딩을 지원하지 않으므로, 서로 다르게 처리하고자 하는 자료형별로 서로 다른 시그너처를 가진 htmlize()를 만들 수 없다. 이때 파이썬에서는 일반적으로 htmlize()를 디스패치 함수로 변경하고, 일련의 if/elif/elif 문을 이용해서 htmlize_str(), htmlize_int()등의 특화된 함수를 호출한다. 그러면 이 모듈의 사용자가 코드를 확장하기 쉽지 않으며, 다루기도 어렵다. 시간이 지나면서 htmlize() 디스패치 코드가 커지며, 디스패치 함수와 특화된 함수 간의 결합이 너무 강해진다.

파이썬 3.4에서 새로 소개된 functools.singledispatch() 데커레이터는 각 모듈이 전체 해결책에 기여할 수 있게 해주며, 여러분이 편집할 수 없는 클래스에 대해서도 특화된 함수를 쉽게 제공할 수 있게 해준다. 일반 함수를 @singledispatch로 데커레이트하면, 이 함수는 **범용 함수**가 된다. 즉, 일련의 함수가 첫 번째 인수의 자료형에 따라 서로 다른 방식으로 연산을 수행하게 된다. 아래 예제는 단일 디스패치를 이용해서 구현하는 방법을 보여준다.
>functools.singledispatch()는 파이썬 3.4에 추가되었지만, PyPI에서 내려받을 수 있는 singledispatch 패키지(https://pypi.python.org/pypi/singledispatch)는 파이썬 2.6부터 3.3까지의 하위 버전에 포팅되었다.

- [여러 함수를 범용 함수로 묶는 커스텀 htmlize.register()를 생성하는 singledispatch](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-6~8/singledispatch.py)
1. @singledispatch()는 객체형을 다룰 기반 함수를 표시한다.
2. 각각의 특화된 함수는 @<기반_함수>.register(<객체형>)으로 데커레이트된다.
3. 특화된 함수의 이름은 필요 없으므로 언더바로 함수명을 지정한다.
4. 특별하게 처리할 자료형을 추가할 때마다 새로운 함수를 등록한다. numbers.Integral은 int의 가상 슈퍼클래스다.
5. 동일한 함수로 여러 자료형을 지원하기 위해 register 데커레이터를 여러 개 쌓아올릴 수 있다.

가능하면 int나 list와 같은 구상 클래스보다 numbers.Integral이나 abc.MutableSequence와 같은 추상 베이스 클래스를 처리하도록 특화된 함수를 등록하는 것이 좋다. 추상 베이스 클래스로 등록하면 호환되는 자료형을 폭넓게 지원할 수 있다. 예를 들어 파이썬 확장은 int형의 대안으로 고정된 길이의 비트를 numbers.Integral의 서브클래스로 제공할 수 있다.
> 자료형 검사에 추상 베이스 클래스를 사용하면 기존 클래스 및 앞으로 추가될 그 추상 베이스 클래스의 실질 혹은 가상 서브클래스도 지원할 수 있다. 추상 베이스 클래스의 사용과 가상 서브클래스의 개념에 대해서는 11장에서 다룬다.

singledispatch 매커니즘은 특화된 함수를 시스템 어디에나, 어느 모듈에나 등록할 수 있다는 장점이 있다. 나중에 새로운 사용자 정의 자료형이 추가된 모듈을 추가할 때도 추가된 자료형을 처리하도록 새로운 특화된 함수를 쉽게 추가할 수 있다. 그리고 직접 작성하지 않고 변경할 수 없는 클래스에 대한 특화된 함수도 추가할 수 있다.

singledispatch는 심사숙고 끝에 표준 라이브러리에 추가된 매커니즘으로서, 여기에서 설명한 것보다 더 많은 기능을 제공한다. 자세한 내용은 'PEP 443 - 단일 디스패치 범용 함수'문서(https://www.python.org/dev/peps/pep=0443/)를 참조라하라.
> @singledispatch는 자바 스타일의 메서드 오버로딩을 파이썬에 적용하기 위해 설계된 것이 아니다. 장황하게 if/elif/elif/elif 블록을 가진 단일 함수보다 오버로드된 메서드를 가진 클래스가 더 좋지만, 이 두 방법 모두 단일 코드 유닛(클래스나 함수)에 너무 많은 책임을 부여하는 결함이 있다. @singledispatch는 모듈화된 확장을 지원한다. 각 모듈은 자신이 지원하는 자료형에 대한 특화된 함수를 등록할 수 있다.
데커레이터는 함수이므로 조합할 수도 있다 (예를 들어[여러 함수를 범용 함수로 묶는 커스텀 htmlize.register()를 생성하는 singledispatch](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-6~8/singledispatch.py)에서처럼 이미 데커레이트된 함수에 데커레이터를 적용할 수 있다). 다음 절에서는 조합된 데커레이터가 어떻게 작동하는지 알아보자.






