<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part10/ex10-1~4/UML_class_diagram.png)
 -->
# Vector 버전 #3: 동적 속성 접근

Vector2d에서 Vector로 진화하면서 v.x, v.y처럼 벡터 요소를 이름으로 접근하는 능력을 상실했다. 이제는 아주 많은 요소를 가진 벡터를 다루고 있다. 그렇지만 앞에 있는 요소 몇 개는 v[0], v[1], v[2] 대신 x, y, z로 접근할 수 있으면 편리할 것이다.

벡터의 처음 네 요소를 읽는 또 다른 구문은 다음과 같다.
```
v = Vector(range(10))
v.x
# 0.0
v.y, v.z, v.t
# (1.0, 2.0, 3.0)
```
Vector2d에서 @property 데커레이터를 이용해서 x와 y에 읽기 전용 접근을 제공했다 (9.7절). Vector에 네 개의 프로퍼티를 작성할 수도 있지만, 그 과정은 지루하다. __getattr__() 특별 메서드를 이용하면 더욱 깔끔하게 구현할 수 있다.

속성을 찾지 못하면 인터프리터는 __getattr__() 메서드를 호출한다. 간단히 말해, my_obj.x표현식이 주어지면, 파이썬은 my_obj 객체에 x 속성이 있는지 검사한다. 속성이 없으면 이 객체의 클래스(my_obj.__class__)에서 더 검색한다. 그러고 나서 상속 그래프를 따라 계속 올라간다. 그래도 x 속성을 찾지 못하면 self와 속성명을 문자열(에를 들면 'x')로 전달해서 my_obj의 클래스에 정의된 __getattr__() 메서드를 호출한다.

아래의 예제는 우리가 구현한 __getattr__() 메서드를 보여준다. 본질적으로 이 메서드는 찾고 있는 속성이 x, y, z, t 문자 중 하나인지 검사하고, 이중 하나인 경우에는 해당 벡터 요소를 반환한다.

```
# vector_v3.py의 일부
shortcut_names = 'xyzt'

def __getattr__(self, name):
    cls = type(self) #1
    if len()name) == 1: #2
        pos = cls.shortcut_names.find(name) #3
        if 0 <= pos < len(self._components): #4
            return self._components[pos]
    msg = '{.__name__!r} object has no attribute {!r}' #5
    raise AttributeError(msg.format(cls, name))
```
1. 나중에 사용하기 위해 Vector 클래스를 가져온다.
2. name이 한글자면 shortcut_names 중 하나일 수 있다.
3. 한 글자 name의 위치를 찾는다. str.find()는 'yz'의 위치도 찾을 수 있으므로, 위에서 name의 길이가 1인지 확인한 것이다.
4. position이 범위 안에 있으면 배열 항목을 반환한다.
5. 두 개의 검사 과정에 실패하면 표준 메세지와 함께 AttributeError가 발생한다.

__getattr__() 메서드를 구현하는 것이 어렵지는 않지만, 여기서는 이 정도면 충분하다. 이제 아래의 예제와 같이 엉뚱하게 사용하는 경우를 생각해보자.

```
v = Vector(range(5))
v
# Vector([0.0, 1.0, 2.0, 3.0, 4.0])
v.x #1
# 0.0
v.x = 10 #2
v.x #3
# 10
v
#Vector([0.0, 1.0, 2.0, 3.0, 4.0]) #4
```
1. v.x를 이용해서 v[0]에 접근한다.
2. v.x에 새로운 값을 할당한다. 이 연산에서 오류가 발생했어야 한다.
3. v.x 값을 읽으면 새로운 값인 10이 나온다.
4. 그러나 벡터 요소는 변경되지 않았다.

무슨 일이 벌어진 걸까? 특히 두 번째 v.x는 왜 벡터 요소 배열에 들어 있지 않은 10을 반환할까? 바로 답이 나오지 않는다면 위의 __getattr__() 메서드에 대한 설명을 차근차근 읽어보자. 약간 이해하기 힘들지만, 이 책 뒷부분에 나오는 내용을 이해하는 중요한 기반이 된다.

위 소스코드에서의 불일치 문제는 __getattr__() 메서드가 작동하는 방식 때문에 발생한다. 파이썬은 해당 이름의 속성을 찾지 못할 때 최후 수단으로 __getattr__() 메서드를 호출한다. 그러나 v.x = 10 문장으로 x 속성에 값을 할당할 때 v 객체에 x 속성이 추가되므로, 더이상 v.x값을 가져오기 위해 __getattr__()을 호출하지 안흔ㄴ다. 인터프리터는 단지 v.x에 바인딩된 값 10을 반환한다. 한편 우리가 구현한 __getattr__()은 shortcut_names에 나열된 '가상 속성'의 값을 가져오기 위해 self._components 이외의 다른 속성에는 주의를 기울이지 않는다. 

이와 같은 불일치 문제를 해결하려면 Vector 클래스에서 속성값을 설정하는 부분의 논리를 수정해야 한다.

9장의 마지막 Vector2d 예제에서 x나 y 객체의 속성에 값을 할당할 때 AttributeError가 발생했었다. Vector에서도 이런 문제를 피하기 위해 소문자 하나로 된 속석명에 값을 할당할 때 동일한 에외를 발생시키려 한다. 그렇게 하려면 아래 예제와 같이 __setattr__() 메서드를 구현해야 한다.

```
vector_v3.py의 일부: Vector 클래스에 추가된 __setattr__() 메서드

def __setattr__(self, name, value):
    cls = type(self)
    if len(name) == 1: #1
        if name in cls.shortcut_names: #2
            error = 'readonly attribute {attr_name!r}'
        elif name.islower(): #3
            error = "can't set attributes 'a' to 'z' in {cls_name!r}"
        else:
            error = '' #4
        if error: #5
            msg = error.format(cls_name=cls.__name__, attr_name=name)
            raise AttributeError(msg)
    super().__setattr__(name, value) #6
```
1. 단일 문자 속석명에 대해 특별한 처리를 한다.
2. name이 x, y, z, t중 하나면 구체적인 에러 메세지를 설정한다.
3. name이 그 외 소문자면 단일 문자 속석명에 대한 일반적인 메세지를 설명한다.
4. 그렇지 않으면 error를 빈 문자열로 설정한다.
5. error 안에 어떠한 문자가 들어 있으면 AttributeError를 발생시킨다.
6. 에러가 발생할지 않을 때는 표준 동작을 위해 슈퍼클래스의 __setattr__() 메서드를 호출한다.

> super()함수는 슈퍼클래스의 메서드에 동적으로 접근할 수 있는 방법을 제공하며, 파이썬과  같이 다중 삭속을 지원하는 동적 언어에서 필수적인 기능이다. 위 예제에서 보는것처럼 super()는 서브클래스가 처리할 작업의 일부를 슈퍼클래스로 위임하기 위해 사용된다. super() 함수에 대해서는 12.2절 '다중 상속과 메서드 결정 순서'에서 자세히 설명한다.

AttributeError와 함께 출력할 에러 메세지를 선택하는 동안 내장된 complex 형의 동작을 조사했다. complex 형이 불변형이며 real과 imag, 두 개의 데터 속성을 가지고 있기 때문이다. complex 형의 두 속성 중 하나를 변경할 때 '속성을 설정할 수 없습니다'라는 메세지와 함께 AttributeError가 발생했다. 한편 9.6절 '해시 가능한 Vector2d'에서 구현한 것과 같이 프로퍼티로 보호한 읽기 전용 속성을 설정할 때는 '읽기 전용 속성'이라는 에러 메세지가 나왔다. 이 두 메세지에서 영감을 얻어 __setattr__()에 사용할 에러 메세지를 정했지만, 금지된 속성을 더욱 명확히 보여준다.
여기서 주의할 점은, 모든 속성의 설정을 막는 것이 아니라 지원되는 읽기 전용 속성 x, y, z, t와의 혼동을 피하기 위해 단일 소문자로 되어 있는 속성의 설정만 막고 있다는 것이다.

> 클래스 수준에서 __slots__를 정의하면 새로운 객체 속성을 생성할 수 없다는 것을 알고 있으므로, 우리가 구현한 __setattr__() 대신 __slots__ 속성을 사용하고 싶을 것이다. 그러니 9.8.1절 __slots__를 사용할 때 주의할 점'에서 설명한 것처럼, 단지 객체 속성의 생성을 막기 위해 __slots__를 사용하는 것은 권장하지 않는다. __slots__는 정말로 문제가 있을 때만 메모리를 절약하기 위해 사용해야한다.

Vector 요소에 저장하는 기능을 지원하지는 않지만, 이 예제는 중요한 비결을 가르쳐준다. 객체 동작의 불일치를 피하려면 __getattr__()을 구현할 때 ++setattr__()도 함께 구현해야 한다는 것이다.

벡터 요소의 변경을 허용하고 싶은 경우, __setitem__() 메서드를 구현하면 v[0] = 1.1의 형태로, __setattr__() 메서드를 구현하면 v.x = 1.1로 작성할 수 있다. 그러나 다음 절에서 Vector를 해시 가능하게 만들려고 하므로, 일단 Vector는 불변형으로 유지한다.


