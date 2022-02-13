<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-3/UML_class_diagram.png)
 -->
# 프로퍼티 제대로 알아보기

내장된 property()는 비록 데커레이터로 사용되는 경우가 많지만, 사실상 클래스다. 파이썬에서 함수와 클래스는 서로 교환할 수 있는 경우가 많다. 함수와 클래스는 모두 콜러블이고 객체를 생성하기 위한 new 연산자가 없으므로, 생성자를 호출하는 것은 팩토리 함수를 호출하는 것과 차이가 없다. 그리고 장식된 함수를 적절히 대체할 수 있는 콜러블을 생성한다면 둘 다 데커레이터로 사용할 수 있다.

property() 생성자의 전체 시그너처는 다음과 같다.

```
property(fget=None, fset=None, fdel=None, doc=None)
```

모든 인수는 선택적이며, 인수에 함수를 제공하지 않으면 생성된 프로퍼티 객체가 해당 연산을 지원하지 않는다.

property 형은 파이썬 2.2에 추가되었지만, @ 기호를 사용한 데커레이터 구문은 파이썬 2.4에서 등장했다. 따라서 수년간 접근자 함수를 앞의 두 인수로 전달함으로써 프로퍼티를 정의했다.

아래 bulkfood_v2b.py 예제는 데커레이터를 사용하지 않고 프로퍼티를 정의하는 '고전적인' 구문을 보여준다.

- [bulkfood_v2b.py](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-3/bulkfood_v2b.py)
1. 평범한 게터
2. 평범한 세터
3. property 객체를 생성하고 클래스의 공개 속성에 할당한다.

경우에 따라서 고전적인 구문이 데커레이터 구문보다 나을 때도 있다. 잠시 후에 설명할 프로퍼티 팩토리가 그 사례다. 한편 메서드가 많이 있는 클래스 본체 안에서 프로퍼티는 메서드명 앞에 get과 set을 사용하는 관례에 의존하지 않고도 어느 것이 게터고, 어느 것이 세터인지 명확히 보여준다. 클래스 안에 프로퍼티가 존재하면 그 클래스의 객체 안에 있는 속성을 찾는 방식에 영향을 미친다. 처음에는 다소 놀랄 수도 있다. 다음 절에서 자세히 알아보자.

## 객체 속성을 가리는 프로퍼티
프로퍼티는 언제나 클래스 속성이지만, 실제로는 클래스의 객체에 들어 있는 속성에 대한 접근을 관리한다.

9.9절 '클래스 속성 오버라이드'에서 설명한 것처럼, 객체와 클래스가 모두 동일한 이름의 속성을 가지고 있으면, 객체를 통해 속성에 접근할 때 객체 속성이 클래스 속성을 가린다. 아래예제는 이 현상을 잘 보여준다.

```
class Class: #1
    data = 'the class data attr'
    @property
    def prop(self):
        return 'the prop value'


obj = Class()
vars(obj) #2
# {}
obj.data #3
# 'the class data attr'
obj.data = 'bar' #4
vars(obj) #5
# {'data': 'bar'}
obj.data #6
# 'bar'
Class.data #7
# 'the class data attr'
```
1. data 속성과 prop 프로퍼티, 2개의 클래스 속성을 가진 Class를 정의한다.
2. vars()는 인수의 __dict__를 반환하므로, 이 객체에 아무런 속성이 없음을 보여준다.
3. obj.data를 읽으면 Class.data의 값을 가져온다.
4. obj.data에 값을 저장하면 객체 속성이 생성된다.
5. 객체 속성이 만들어졌는지 확인한다.
6. 이제 obj.data를 읽으면 객체 속성의 값을 가져온다. obj 객체에서 값을 읽을 때, 객체 데이터가 클래스 데이터를 가린다.
7. Class.data 속성은 그대로다.

이제 obj 객체의 prop 속성을 덮어써보자. 앞 예제의 콘솔 세션에 이어 아어 아래와 같이 실행한다.

```
Class.prop #1
# <property object at 0x1072b7408>
obj.prop #2
# 'the prop value'
obj.prop = 'foo' #3
"""
Traceback (most recent call last):
 ...
AttributeError: can't set attribute
"""
obj.__dict__['prop'] = 'foo' #4
vars(obj) #5
# {'data': 'bar', 'prop': 'foo'}
obj.prop #6
# 'the prop value'
Class.prop = 'baz' #7
obj.prop #8
# 'foo'
```

1. Class에서 직접 prop을 읽으면 게터 메서드를 통하지 않고 프로퍼티 객체 자체를 가져온다.
2. obj.prop을 읽으면 프로퍼티 게터를 실행한다.
3. 객체의 prop 속성에 값을 할당하면 에러가 발생한다.
4. obj.__dict__에 직접 'prop'을 설정하면 제대로 작동한다.
5. 이제 obj에는 data와 prop, 두 개의 객체 속성이 있는 것을 볼 수 있다.
6. 그러나 obj.prop을 읽으면 여전히 프로퍼티 게터가 실행된다. 프로퍼티는 객체 속성에 의해 가려지지 않는다.
7. Class.prop을 덮어쓰면 프로퍼티 객체가 제거된다.
8. 이제 obj.prop은 객체 속성을 가져온다. Class.prop은 더 이상 프로퍼티가 아니므로 obj.prop을 가리지 않는다.

마지막 예제로 Class에 새로운 프로퍼티를 추가하고, 이 프로퍼티가 객체 속성을 가리는 것을 확인한다. 아래 예제는 위 콘솔화면에 이어 수행한 콘솔 세션이다.

```
# 새로운 클래스 프로퍼티는 기존 객체 속성을 가린다.
obj.data #1
# 'bar'
Class.data #2
# 'the class data attr'
Class.data = property(lambda self: 'the "data" prop value') #3
obj.data #4
# 'the "data" prop value'
del Class.data #5
obj.data #6
# 'bar'
```
1. obj.data는 객체의 data 속성을 가져온다.
2. Class.data는 클래스의 데이터 속성을 가져온다.
3. Class.data를 새로운 프로퍼티로 덮어쓴다.
4. obj.data는 이제 Class.data 프로퍼티에 의해 가려진다.
5. 프로퍼티를 제거한다.
6. 이제 obj.data는 다시 객체의 data 속성을 가져온다.

이 예제에서 설명하고자 하는 요점은 obj.attr 같은 표현식이 obj에서 시작해서 attr을 검색하는 게 아니라는 것이다. 일반적으로 검색은 obj.__class__에서 시작하고, 클래스 안에 attr이라는 이름의 프로퍼티가 없을 때만 파이썬이 obj 객체를 살펴본다. 이 규칙은 프로퍼티뿐만 아니라 모든 종류의 디스크립터(**오버라이딩 디스크립터 포함**)에 적용된다. 디스크립터에 대한 자세한 설명은 20장으로 미루기로 한다. 20장에서 프로퍼티가 사실은 오버라이딩 디스크립터라는 것을 알 수 있다.

이제 다시 프로퍼티로 돌아가자. 모듈, 함수, 클래스, 메서드 등 파이썬 코드의 모든 유닛은 문서화 문자열을 가질 수 있다. 다음 절에서는 문서를 프로퍼티에 연결하는 방법을 설명한다.

## 프로퍼티 문서화

콘솔의 help() 함수나 IDE 같은 도구가 프로퍼티에 대한 문서를 보여주어야 할 때 프로퍼티의 __doc__ 속성에서 정보를 가져온다.

고전적인 호출 구문을 사용하는 경우에는 property()가 doc 인수를 전달된 문자열을 받는다.

```
weight = property(get_weight, set_weight, doc='weight in kilograms')
```

프로퍼티를 데커레이터로 사용하는 경우에는 @property 데커레이터로 장식된 게터 메서드의 문서화 문자열이 프로퍼티 전체의 문서로 사용된다. 아래 그림은 아래 예제의 코드로 생성한 도움말 화면이다.

![help.png](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-3/help.png)

```
# 프로퍼티에 대한 문서화

class Foo:

    @property
    def bar(self):
        '''The bar attribute'''
        return self.__dict__['bar']
    
    @bar.setter
    def bar(self, value):
        self.__dict__['bar'] = value
```

프로퍼티에 대한 핵심사항을 살펴봤으니, 이제 두 개의 거의 동일한 세터/게터를 직접 구현하지 않고도 LineItem의 weight와 prcie속성이 0보다 큰 값만 받을 수 있도록 보호하는 문제로 돌아가자.
