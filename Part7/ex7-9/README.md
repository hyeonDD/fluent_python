# 누적된 데커레이터
<!-- 
- [지역 및 전역 변수를 읽는 함수](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-9/read_local_global_func.py)
 -->
앞에서는 누적된 데커레이터가 사용된 것을 보았다. @clock이 적용된 fibonacci()에 다시 @lru_cache가 적용되었다. 또, @htmlize.register 데커레이터가 두번 적용되었다.

하나의 함수 f()에 두 데커레이터 @d1과 @d2를 차례대로 적용하면, 결과는 f = d1(d2(f))와 동일하다.
```
@d1
@d2
def f():
    print('f)
```
위 코드는 다음 코드와 동일하다.
```
def f():
    print('f')
f = d1(d2(f))
```
이 장에서는 누적된 데커레이터 외에 인수를 받는 데커레이터도 이용했다. 예를 들어 @lru_cache()및 @singledispatch에 의해 생성된 htmlize.register(<객체형>)데커레이터가 인수를 받는다. 다음 절에서는 매개변수를 받는 데커레이터를 만드는 방법을 살펴본다.

# 매개변수화된 데커레이터
소스 코드에서 데커레이터를 파싱할 때 파이썬은 데커레이트된 함수를 가져와서 데커레이터 함수의 첫 번째 인수로 넘겨준다. 그러면 어떻게 다른 인수를 받는 데커레이터를 만들 수 있을까? 인수를 받아 데커레이터를 반환하는 데커레이터 팩토리를 만들고 나서, 데커레이트될 함수에 데커레이터 팩토리를 적용하면 된다. 설명이 복잡한가? 아마 그럴 것이다. 아래에 나온 지금까지 우리가 본 가장 간단한 데커레이터인 register()를 예를 들어 알아보자.

- [register 축약버전](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-9/register_old.py)

## 매개변수화된 등록 데커레이터
register()가 등록하는 함수를 활성화 혹은 비활성화하기 쉽게 만들기 위해, 선택적인 인수 active를 받도록 만들어보자. active가 False면 데커레이트된 함수를 등록 해제한다. 아래 예제를 보면 어떻게 하는지 알 수 있을 것이다. 새로 만든 register()함수는 개념적으로는 데커레이터가 아니라 데커레이터 팩토리다. 호출되면 대상 함수에 적용할 실제 데커레이터를 반환하기 때문이다.

- [매개변수를 받기 위해 함수로 호출되어야 하는 새로운 register()데커레이터](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-9/register_new.py)
1. 함수의 추가와 제거를 빠르게 하기 위해 registry를 집합형으로 정의한다.
2. register()는 선택적 키워드 인수를 받는다.
3. decorate() 내부 함수가 실제 데커레이터다. 함수를 인수로 받는 방법에 주의하라.
4. 클로저에서 읽어온 active 인수가 True일 때만 func()를 등록한다.
5. active가 True가 아니고 func가 registry에 들어 있으면 제거한다.
6. decorate()는 데커레이터이므로 함수를 반환해야 한다.
7. register()는 데커레이터 팩토리이므로 decorate()를 반환해야한다.
8. @register 팩토리는 원하는 매개변수와 함께 함수로 호출해야 한다.
9. 인수를 전달하지 않더라도 register는 여전히 함수로 호출해야 하므로 @register() 형태로 호출한다. 그러면 실제 데커레이터인 decorate()를 반환한다.

핵심은 register()가 decorate()를 반환하고, 데커레이트될 함수에 decoreate()가 적용된다는 것이다.
