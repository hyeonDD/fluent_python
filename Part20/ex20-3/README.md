<!-- 
- [](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-3/UML_class_diagram.png)
 -->
# 메서드는 디스크립터

모든 사용자 정의 함수는 __get__() 메서드를 가지고 있어서, 클래스에 연결된 함수는 디스크립터로 작동하기 때문에, 클래스 안의 함수는 클래스에 바인딩된 메서드가 된다. 아래예제에서는 [descriptorkinds.py](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-2/descriptorkinds.py)에서 만든 Managed 클래스의 spam() 메서드를 읽는 예를 보여준다.

```
    >>> obj.spam  # doctest: +ELLIPSIS
    <bound method Managed.spam of <descriptorkinds.Managed object at 0x...>>
    >>> Managed.spam  # doctest: +ELLIPSIS
    <function Managed.spam at 0x...>   
    >>> obj.spam = 7
    >>> obj.spam
    7
```
1. obj.spam을 읽으면 바인딘된 메서드 객체가 나온다.
2. 그러나 Managed.spam을 읽으면 함수가 나온다.
3. obj.spam에 값을 할당하면 클래스 속성을 가리므로 obj 객체에서는 spam() 메서드에 접근할 수 없게된다.

함수가 __set__() 메서드를 구현하지 않으므로, 위 예제에서의 마지막 행에서 보는 것처럼 함수는 논오버라이딩 디스크립터다.

위 예제에서 obj.spam과 Managed.spam이 서로 다른 객체를 반환하는 것을 눈여겨보기 바란다.디스크립터가 그러하듯이 관리 대상 클래스를 통해 접근할 때 함수의 __get__() 메서드는 자기 자신을 반환한다. 그러나 객체를 통해 함수에 접근할 때는 함수의 __get__() 함수가 바인딩된 메서드 객체를 반환한다. 메서드는 5.10.2절 'functools.partial()로 인수 고정하기'에서 본 functools.partial() 함수처럼 관리 대상 객체(obj)를 함수의 첫 번째 인수(self)에 바인딩하는 콜러블 객체다.

이 메커니즘을 자세히 알아보기 위해 아래예제를 살펴보자.
- [method_is_descriptor.py](https://github.com/hyeonDD/fluent_python/blob/master/Part20/ex20-3/method_is_descriptor.py)

이제 실험을 통해 Text.reverse() 메서드를 조사해보자.(아래예제)
```
    >>> word = Text('forward')
    >>> word  # <1>
    Text('forward')
    >>> word.reverse()  # <2>
    Text('drawrof')
    >>> Text.reverse(Text('backward'))  # <3>
    Text('drawkcab')
    >>> type(Text.reverse), type(word.reverse)  # <4>
    (<class 'function'>, <class 'method'>)
    >>> list(map(Text.reverse, ['repaid', (10, 20, 30), Text('stressed')]))  # <5>
    ['diaper', (30, 20, 10), Text('desserts')]
    >>> Text.reverse.__get__(word)  # <6>
    <bound method Text.reverse of Text('forward')>
    >>> Text.reverse.__get__(None, Text)  # <7>
    <function Text.reverse at 0x101244e18>
    >>> word.reverse  # <8>
    <bound method Text.reverse of Text('forward')>
    >>> word.reverse.__self__  # <9>
    Text('forward')
    >>> word.reverse.__func__ is Text.reverse  # <10>
    True
```
1. Text 객체의 표현은 동일한 객체를 생성하기 위해 호출하는 Text() 생성자 호출과 동일하게 보인다.
2. reverse() 메서드는 텍스트의 순서를 거꾸로 한 문자열을 반환한다.
3. 클래스에 호출한 메서드는 함수로 작동한다.
4. 각각의 자료형이 function과 method다.
5. Text.reverse()는 Text 이외의 객체에 대해서도 하나의 함수로 작동한다.
6. 모든 함수는 논오버라이딩 디스크립터다. 객체를 전달해서 함수의 __get__() 메서드를 호출하면 그 객체에 바인딩된 메서드가 반환된다.
7. istance 인수로 None을 전달해서 함수의 __get__(word)를 호출하면 함수 자신이 반환된다.
8. word.reverse 표현식은 실제로는 Text.reverse.__get__(word)를 호출하므로 바인딩된 메서드를 반환한다.
9. 바인딩된 메서드 객체는 __self__ 속성에 호출된 객체에 대한 참조를 담고 있다.
10. 바인딩된 메서드의 __func__ 속성은 관리 대상 클레스에 연결된 원래 함수를 참조한다.

바인딩된 메서드 객체는 호출을 실제로 처리하는 __call__() 메서드도 가지고 있다. __call__()은 메서드의 __self__ 속성을 첫 번째 인수로 전달해서 __func__ 속성이 참조하는 원래 함수를 호출한다. 전형적인 self 인자는 이런 방식으로 바인딩된다.

함수가 바인딩된 메서드로 변환되는 과정은 파이썬 언어의 밑바닥에 디스크립터가 사용되는 방식을 잘 보여준다.

디스크립터와 메서드가 어떻게 작동하는지 자세히 살펴보았으니, 이제 메서드 사용과 관련하여 도움이 되는 조언을 살펴보자.