<!-- 
- [](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-4/aaa)
 -->
# 메타클래스 기본 지식

메타클래스는 일종의 클래스 팩토리다. 다만 [factories.py](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-1~2/factories.py)의 record_factory()와 같은 함수대신 클래스로 만들어진다는 점이 다르다. 아래 그림은 공장과 장치 표기법을 이용해서 메타클래스를 설명한다. 공장이 또 다른 공장을 만든다.

![class_creater.png](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-4/class_creater.png)

파이썬 객체 모델을 생각해보자. 클래스도 객체이므로, 각 클래스는 다른 어떤 클래스의 객체여야 한다. 기본적으로 파이썬 클래스는 type의 객체다. 즉, type은 대부분의 내장된 클래스와 사용자 정의 클래스에 대한 메타클래스다.
```
>>> 'spam'.__class__
<class 'str'>
>>> str.__class__
<class 'type'>
>>> from bulkfood_v6 import LineItem
>>> LineItem.__class__
<class 'type'>
>>> type.__class__
<class 'type'>
```
무한 회귀를 방지하기 위해, 마지막 행에서 보는 것처럼 type은 자기 자신의 객체로 정의도어 있다.

여기서는 str이나 LineItem이 type을 상속한다는 것이 아니라, str과 LineItem 클래스가 모두 type의 객체라는 점을 강조하려는 것이다. 이들 클래스는 object의 서브클래스다. 아래 그림을 보면 이런 이상한 현실을 접하는 데 도움이 될것이다.

![diagram.png](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-4/diagram.png)

왼쪽 그림은 str, type, LineItem이 object의 서브클래스임을 강조하고, 오른쪽 그림은 str, object, LineItem이 클래스이기 때문에 type의 객체임을 강조한다.
> object와 type 클래스는 독특한 관계를 맺고 있다. object는 type의 객체며, type은 object의 서브클래스다. 이 관계는 '마술'과도 같아서 파이썬으로는 표현할 수 없다. 두 클래스 모두 다른 클래스를 정의하기 전에 존재해야 하기 때문이다. 사실 type 클래스가 type 자신의 객체라는 사실도 신비롭다.

표준 라이브러리에는 type 외에도 ABCMeta, Enum 등이 메타클래스도 있다. 다음 예제는 collections.Iterable의 클래스가 abc.ABCMeta임을 보여준다. Iteralbe은 추상 클래스지만, ABCMeta는 아니다. 즉, Iterable은 ABCMeta 클래스의 객체다.
```
>>> import collections
>>> collections.Iterable.__class__
<class 'abc.ABCMeta'>
>>> import abc
>>> abc.ABCMeta.__class__
<class 'type'>
>>> abc.ABCMeta.__mro__
(<class 'abc,ABCMeta'>, <class 'type'>, <class 'object'>)
```

궁극적으로 ABCMeta의 클래스도 type이다. 모든 클래스는 직간접적으로 type의 객체지만, 메타클래스만 type의 서브클래스다. 메타클래스를 이해하려면 이점에 주의해야 한다. ABCMeta 등의 메타클래스는 type으로부터 클래스 생성 능력을 상속한다. 아래그림은 이러한 중요한 관계를 잘 보여준다.

![diagram2.png](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-4/diagram2.png)

정리하자면, 모든 클래스는 type의 객체지만, 메타클래스는 type의 서브클래스이기도 하므로, 클래스 팩토리로서 행동한다. 특히 메타클래스는 __init__() 메서드를 구현함으로써 자신의 객체를 커스터마이즈할 수 있다. 메타클래스의 __init__() 메서드는 클래스 데커레이터가 하는 모든 일을 할 수 있지만, 다음 연습문제에서 알 수 있는 것처럼 더욱 강력한 영향력을 발휘한다.

## 메타클래스 평가 시점 연습문제
다음 예제는 21.3.1절 '코드 평가 시점 연습문제'를 변형한 것으로서, evalsupport.py는 [evalsupport.py](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-3/evalsupport.py)과 동일하지만, 핵심 스크립트인 evaltime_meta.py는 아래와 같다.


- [evaltime_meta.py](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-4/evaltime_meta.py)

여기서도 마찬가지로 종이와 연필을 들고 다음 두 시나리오에서 <[N]> 표신의 숫자를 평가 순서대로 적어보라.

---

**시나리오 #3**
파이썬 콘솔에서 evaltime_meta.py 모듈을 임포트한다.

**시나리오 #4**
명령행에서 evaltime_meta.py 모듈을 실행한다.

---

### 시나리오 #3에 대한 해결책
아래 에제는 파이썬 콘솔에서 evaltime_meta.py를 임포트한 결과다.
```
>>> import evaltime_meta
<[100]> evalsupport module start
<[400]> MetaAleph body
<[700]> evalsupport module end  
<[1]> evaltime_meta module start
<[2]> ClassThree body
<[200]> deco_alpha
<[4]> ClassFour body
<[6]> ClassFive body
<[500]> MetaAleph.__init__ #1
<[9]> ClassSix body
<[500]> MetaAleph.__init__ #2
<[15]> evaltime_meta module end 
```
1. 시나리오 #1과 두드러진 차이점은 방금 생성된 ClassFive를 초기화하기 위해 MetaAleph.__init__() 메서드가 호출된다는 점이다.
2. MetaAleph.__init__()은 ClassFive의 서브클래스인 ClassSix도 초기화한다.

파이썬 인터프리터는 ClassFive의 본체를 평가한다. 그러고 나서 실제 클래스 본체를 만들기 위해 type()을 호출하는 대신 MetaAleph()를 호출한다. 아래 eavlsupport.py에서 MetaAleph의 정의를 보면 __init__() 메서드가 다음과 같이 인수 네 개를 받는 것을 알 수 있따.

---

**self**
초기화하고 있는 클래스 객체다(예를 들면 ClassFive).

**name, bases, dic**
클래스를 생성하기 위해 type에 전달되는 인수와 동일한 인수다.

---

```
class MetaAleph(type):
    print('<[400]> MetaAleph body')

    def __init__(cls, name, bases, dic):
        print('<[500]> MetaAleph.__init__')

        def inner_2(self):
            print('<[600]> MetaAleph.__init__:inner_2')

        cls.method_z = inner_2
```
> 메타클래스를 구현할 때는 관례적으로 self대신 cls를 사용한다. 예를 들어 메타클래스의 __init__() 메서드에서 첫 번째 인수에 cls라는 이름을 사용해서 현재 생성하고 있는 것이 클래스임을 명시한다.

__init__() 본체에서는 inner_2() 함수를 정의하고, 이 함수를 cls.method_z에 바인딩한다. MetaAleph.__init__() 시그너처에서 cls 인수는 현재 생성하고 있는 것(ClassFive)이 클래스임을 알려준다. 한편 inner_2()의 시그너처에 있는 self라는 이름은 우리가 궁극적으로 생성할 객체(예를 들면 ClassFive의 객체)를 가리킨다.

### 시나리오 #4에 대한 해결책
아래는 evaltime_meta.py 명령행에서 evaltime_meta.py를 실행한 결과를 보여준다.

```
$ python evaltime_meta.py
<[100]> evalsupport module start
<[400]> MetaAleph body
<[700]> evalsupport module end
<[1]> evaltime_meta module start
<[2]> ClassThree body
<[200]> deco_alpha
<[4]> ClassFour body
<[6]> ClassFive body
<[500]> MetaAleph.__init__
<[9]> ClassSix body
<[500]> MetaAleph.__init__
<[11]> ClassThree tests ..............................
<[300]> deco_alpha:inner_1 #1
<[12]> ClassFour tests .............................. 
<[5]> ClassFour.method_y #2
<[13]> ClassFive tests .............................. 
<[7]> ClassFive.__init__
<[600]> MetaAleph.__init__:inner_2 #3
<[14]> ClassSix tests ..............................  
<[7]> ClassFive.__init__
<[600]> MetaAleph.__init__:inner_2 #4
<[15]> evaltime_meta module end
```
1. 데커레이터가 ClassThree에 적용되면, method_y()가 inner_1() 메서드로 대체된다.
2. 그러나 ClassFour가 ClassThree를 상속하더라도, 데커레이터가 ClassFour에는 영향을 미치지 않는다.
3. MetaAleph의 __init__() 메서드는 ClassFive.method_z()를 자신의 inner_2() 메서드로 대체한다.
4. __init__() 메서드가 ClassFive의 서브클래스 ClassSix에도 적용되어, method_z()를 inner_2() 메서드로 대체한다.

ClassSix가 MetaAleph를 직접 참조하지는 않지만, MetaAleph의 영향을 받는다. ClassFive를 상속하므로 ClassSix도 MetaAleph의 객체가 되어 MetaAleph.__init__()에 의해 초기화되기 때문이다.
> 메타클래스에서 __new__() 메서드를 구현함으로써 클래스를 더 많이 커스터마이즈할 수 있지만, __init__()만 구현해도 충분한 경우가 많다.

지금까지 이론으로 배운 모든 것을 통합해서 자동 저장소 속성명을 가진 디스크립터에 최상의 해결책을 제공하는 메타클래스를 만들어보자.