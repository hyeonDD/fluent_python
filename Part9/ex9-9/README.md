<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part9/ex9-1/UML_class_diagram.png)
 -->
# 클래스 속성 오버라이드
클래스 속성을 객체 속성의 기본값으로 사용하는 것은 파이썬의 독특한 특징이다. Vector2d클래스에는 typecode라는 클래스 속성이 있다. 이 속성 __bytes__() 메서드에서 두 번 사용되는데, 우리는 단지 self.typecode로 그 값을 읽었다. Vector2d 객체가 그들 자신의 typecode 속성을 가지고 생성된 것이 아니므로, self.typecode는 기본적으로 Vector2d.typecode 클래스 속성을 가져온다.

그러나 존재하지 않는 객체 속성에 값을 저장하면, 새로운 객체 속성(예를 들면 typecode 객체 속성)을 생성하고 동일한 이름의 클래스 속성은 변경하지 않는다. 그 후부터는 객체가 self.typecode를 읽을 때 객체 자체의 typecode를 가져오므로, 동일한 이름의 클래스 속성을 가리게 된다. 그러면 각 객체가 서로 다른 typecode를 갖도록 커스터마이즈할 수 있게 된다.

Vector2d.typecode의 기본값이 'd'이므로 객체를 익스포트할 때 Vector2d의 각 요소가 8바이트 배밀도 실수로 표현된다. Vector2d 객체를 익스포트 하기 전에 typecode를 'f'로 설정하면, 각 요소는 4바이트 단밀도 실수로 익스포트된다.

변경의도를 명백히 보여주고 영구적으로 효과가 지속되는 파이썬에서 즐겨 사용하는 방법이 있다. 클래스 속성은 공개되어 있고 모든 서브클래스가 상속하므로, 클래스 데이터 속성을 커스터마이즈할 때는 클래스를 상속하는 것이 일반적인 방식이다. 장고 클래스 기반 뷰가 이 기법을 많이 사용한다. 아래 소스를 보자.
```
from vector2d_v3 import Vector2d
class ShortVector2d(Vector2d): #1
    typecode = 'f'

sv = ShortVector2d(1/11, 1/27) #2
sv
# ShortVector2d(0.090909090909090991, 0.03703703703703703703703735)
len(bytes(sv))
# 9
```
1. ShortVector2d를 Vector2d의 서브클래스로 만들어서 단지 typecode 클래스 속성만 덮어쓴다.
2. 사용 예를 보여주기 위해 ShorteVector2d 객체 sv를 생성한다.
3. sv의 repr()을 조사한다.
4. 익스포트된 bytes를 확인한다. 이전과 달리 17바이트가 아니라 9바이트다.

이 예제를 보면 Vector2d.__repr__()에서 class_name을 하드코딩하지 않고, 다음과 같이 type(slef).__name__에서 읽어오는 이유를 알 수 있다.
```
# Vector2d 클래스 내부
def __repr__(self):
    class_name = type(self).__name__
    return '{}({!r}, {!r})'.format(class_name, *self)
```
class_name을 하드코딩했다면 단지 class_name을 변경하기 위해 ShortVector2d와 같은 Vector2d 서브클래스의 __repr__() 메서드도 변경해야 했을 것이다. 객체의 type에서 이름을 읽어오도록 만듦으로써 이 클래스를 상속하더라도 __repr__()를 안전하게 사용할 수 있다.

이제 파이썬 세계와 잘 어울리는 데이터 모델을 활용하는 간단한 클래스의 구현을 마친다. 이 클래스는 다양한 객체 표현을 제공하고, 객체 고유의 포맷 코드를 구현하고, 읽기 전용 속성을 노출시키며, 집합이나 매핑에 하용할 수 있도록 hash()를 지원한다.