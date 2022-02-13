<!-- 
- [](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-5~6/UML_class_diagram.png)
 -->
# 속성 제거 처리하기

del 문을 이요해서 객체 속성을 제거할 수 있음을 잘 알것이다.
```
del my_object.an_attribute
```

실제로 속성을 제거하는 연산은 파이썬에서 항상 수행하는 연산은 아니면, 프로퍼티로 처리해야 하는 경우는 더더욱 드물다. 그러나 프로퍼티로 속성을 제거하는 연산이 지원되며, 필자는 이 기능을 보여줄 우스꽝스러운 예제를 생각해낼 수 있다.

프로퍼티 정의에서 @my_property.deleter로 장식된 데커레이터는 이 프로퍼티에 의해 관리되는 속성을 제거하는 책임을 지고 있다. 아래 예제는 프로퍼티 제거자를 구현하는 방법을 보여주는 우스꽝스러운 예제다.

- [blackknight.py](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-5~6/blackknight.py)

blackknight.py에 있는 doctest는 아래 예제와 같다.
```
    >>> knight = BlackKnight()
    >>> knight.member
    next member is:
    'an arm'
    >>> del knight.member
    BLACK KNIGHT (loses an arm)
    -- 'Tis but a scratch.
    >>> del knight.member
    BLACK KNIGHT (loses another arm)
    -- It's just a flesh wound.
    >>> del knight.member
    BLACK KNIGHT (loses a leg)
    -- I'm invincible!
    >>> del knight.member
    BLACK KNIGHT (loses another leg)
    -- All right, we'll call it a draw.
```
데커레이터 대신 고전적인 호출 구문을 사용할 때는 fdel 인수를 사용해서 제거자 함수를 설정한다. 예를 들어 BlackKnight 클래스이 본체에서는 다음과 같이 member 프로퍼티를 구현할 수 있다.
```
member = property(member_getter, fdel=member_deleter)
```
프로퍼티를 사용하지 않을 때는 19.6.3절 '속성을 처리하는 특별 메서드'에서 설명한 __delattr__() 저수준 특별 메서드를 구현해서 속성을 제거할 수 있다. __delattr__() 특별 메서드를 이용해서 이 우스꽝스러운 클래스를 구현하는 것은 꾸물거리는 독자들을 위한 연습 문제로 남겨둔다.

프로퍼티는 강력한 기능이지만, 더 간단하거나 저수준의 다른 방법이 좋을 때도 있다. 이 장의 마지막 절에서는 동적 속성 프로그래밍을 위해 파이썬이 제공하는 핵심 API 몇 가지를 살펴본다.

# 속성을 처리하는 핵심 속성 및 함수

이 장 내내, 그리고 이 책의 앞에 나온 여러 장에서 동적 속성을 처리하기 위해 파이썬이 제공하는 몇 가지 내장 함수와 특별 메서드를 사용했다. 이 절에서는 이 속성과 메서드를 한데 모아 간략히 정리해본다. 공식 문서에서는 이들 속성과 메서드에 대한 문서가 여기저기 흩어져 있기 때문이다.

## 속성 처리에 영향을 주는 특별 속성

앞으로 설명할 함수와 특별 메서드의 작동은 다음과 같은 세 가지 특별 속성에 의존한다.

---

**__class__**
객체의 클래스에 대한 참조(즉, obj.__class__는 type(obj)와 동일하다). 파이썬은 __getattr__()과 같은 특별 메서드를 객체 자ㅔ가 아니라 객체의 클래스에만 검색한다.

**__dict__**
객체나 클레스의 쓰기가능 속성을 저장하는 매핑. __dict__를 가진 객체는 임의의 새로운 속성을 언제든지 설정할 수 있다. 클래스에 __slots__ 속성이 있으면, 이 클래스의 객체에는 __dict__가 없을 수도 있다. 다음의 __slots__ 설명을 참조하라.

**__slots__**
자신의 객체가 가질 수 있는 속성을 제한하려는 클래스에 정의하는 속성. __slots__는 허용된 속성명을 담은 일종의 튜플이다. __dict__가 __slots__에 들어 있지 않으면, 이 클래스의 객체는 자체적인 __dict__를 가질 수 없고, 여기에 나열된 속성만 만들 수 있다.

---

## 속성을 처리하는 내장 함수
다음 다섯 개의 내장 함수는 읽기, 쓰기, 내부 조사를 할 수 있다.

---

**dir([object])**
대부분의 객체 속성을 나열한다. 공식 문서 (http://bit.ly/1HGvLDV) 에 따르면 dir()은 대화형 세션에서 사용하기 위한 것으로 전체 속성의 리스트를 제공하지 않지만 '흥미로운' 속성명들을 나열한다. 객체에 __dict__가 잇든 없든 dir()은 객체 내부를 조사할 수 있다. __dict__ 자체는 dir()이 나열하지 않지만, __dict__에 들어 있는 키들은 나열한다. __mro__(), __bases__(), __name__() 등의 특별 메서드도 dir()이 나열하지 않는다. dir()의 object는 선택적 인수로서, 이 인수를 지정하지 않으면 현재 범위에 있는 이름들을 나열한다.

**getattr(object, name[, default])**
obejct에서 name 문자열로 식별된 속성을 가져온다. 객체의 클래스나 슈퍼클래스에서 속성을 가져올 수 있다. 이러한 속성이 존재하지 않으면 getattr()은 AttributeError를 발생시키거나 default 값을 반환한다.

**hasattr(object, name)**
해당 이름이 속성이 object에 있거나 상속 등의 메커니즘으로 가져올 수 있으면 True를 반환한다. 공식 문서 (https://python.org/3/library/functions.html#hasattr) 에 따르면 이 메서드는 getattr(object, name)을 호출하고 AttributeError 예외가 발생하는지 아닌지 확인해서 구현했다.

**seattr(object, name, value)**
object가 허용하면 name 속성에 value를 할당한다. 이 메서드에 의해 새로운 속성이 생성되거나 기존 속성의 값이 변경된다.

**vars([obejct])**
object의 __dict__를 반환한다. dir() 메서드와 달리 __slots__는 있고 __dict__는 없는 클래스의 객체는 처리할 수 없다. 인수를 전달하지 않으면 vars()는 현재 범위의 __dict__를 가져오므로 locals()와 동일하게 작동한다.

---

## 속성을 처리하는 특별 메서드

다음의 특별 메서드를 사용자 정의 클래스에서 구현하면, 속성을 가져오고, 설정하고, 삭제하고, 나열한다. 점 표기법이나 getattr(), hasattr().setattr() 내장 함수를 이용해서 속성에 접근하면, 실제로 여기에 나열된 특별 메서드를 호출한다. __dict__에 직접 속성을 쓰거나 읽으면 특별메서드를 호출하지 않는데, 이는 특별 메서드를 우회하기 위해 일반적으로 사용하는 방법이다.

파이썬 공식 문서의 3.3.9절 '특별 메서드 조회' (http://bit.ly/1cPO3qP) 에서는 다음과 같이 주의를 준다.

**사용자 정의 클래스의 경우 객체의 __dict__가 아니라 객체의 클래스에 정의되어야 암묵적으로 호출하는 특별 메서드가 제대로 작동한다.**

즉, 실제 행동의 대상이 객체인 경우에도 특별 메서드를 클래스 자체에서 가져온다고 생각할 수 있다. 그렇기 때문에 특별 메서드는 동일한 이름의 속성이 객체에 있더라도 가려지지 않는다.

다음 예제에는 Class라는 이름의 클래스, Class의 객체 obj, obj의 속성 attr이 있다고 가정하자.

여기에 나열된 특별 메서드들은 19.6.2절 '속성을 처리하는 내장 함수'에서 설명한 내장 함수를 사용하든 점 표기법을 사용하든, 속성에 접근하면 호출된다. 예를 들어 obj.attr과 getattr(obj, 'attr', 42)는 모두 Class.__getattribute__(obj, 'attr')을 호추랗ㄴ다.

---

**__delattr__(self, name)**
del 문을 이용해서 속성을 제거하려 할 때 호출된다. 즉, del obj.attr은 Class.__delattr__(obj, 'attr')을 호출한다.

**__dir__(self)**
속성을 나열하기 위해 객체에 dir()을 호출할 때 호출된다. 즉, dir(obj)는 Class.__dir__(obj)를 호출한다.

**__getatt__(self, name)**
obj, Class, Class의 슈퍼클래스를 검색해서 명명된 속성을 가져오려고 시도하다 실패할 때 호출된다. 예를 들어 obj, Class, Class의 슈퍼클래스에서 no_such_attr이라는 속성을 찾을 수 없을 때 obj.no_such_attr, getattr(obj, 'no_such_attr'), hasattr(obj, 'no_such_attr')은 Class.__getattr__(obj, 'no_such_attr')을 호출한다.

**__getattribute__(self, name)**
특별 속성이나 메서드가 아닌 속성을 가져올 때 언제나 호출된다. 점 표기법 및 getattr()과 hasaatr() 내장 함수가 이 메서드를 호출한다. __getattr__()은 __getattribute__()가 AttributeError를 발생시킨 후에만 호출된다. obj의 속성을 가져올 때 무한히 재귀적으로 호출되는 것을 방지하기 위해 __getatrribute__()는 super().__getattribute__(obj, name)을 이용해야 한다.

**__setattr__(self, name, value)**
지명된 속성에 값을 설정할 때 언제나 호출된다. 점 표기법과 setattr() 내장 함수가 이 메서드를 호출한다. 즉, obj.attr = 42와 setattr(obj, 'attr', 42)는 모두 Class.__setattr__(obj, 'attr', 42)를 호출한다.

---
> 실제로 __getattribute__()와 __setattr__() 특별 메서드는 무조건 호출되며 거의 모든 속성 접근에 영향을 미치므로, 존재하지 않는 속성만 처리하는 __getattr__()보다 제대로 구현하기 어렵다. 이런 특별메서드를 정의하는 것보다 프로퍼티나 디스크립터를 이용하는 것이 에러를 중리는 데 도움이 된다.

이것으로 프로퍼티, 특별 메서드, 그 외 동적 속성 구현 기법에 대한 설명을 마친다.