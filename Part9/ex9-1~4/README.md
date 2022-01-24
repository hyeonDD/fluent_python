<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part9/ex9-1~4/UML_class_diagram.png)
 -->
# 객체표현

***
repr()
객체를 개발자가 보고자 하는 형태로 표현한 문자열로 반환한다.

str()
객체를 사용자가 보고자 하는 형태로 표현한 문자열로 반환한다.
***
이미 앞에서 설명한 것처럼 repr()과 str() 메서드를 지원하려면 __repr__()과 __str__()특별 메서드를 구현해야 한다.

객체를 표현하는 다른 방법을 지원하는 __bytes__()와 __format__() 두 개의 특별 메서드도 있다. __bytes__()는 __str__()과 비슷하지만 bytes() 메서드에 의해 호출되어 객체를 바이트 시퀀스로 표현한다. __format__()은 내장 함수 format()과 str.format() 메서드 둘다 사용하며, 특별 포맷 코드를 이용해서 객체를 표현하는 문자열을 반환한다. 다음 예제에서는 __bytes__()메서드를, 그 다음 예제에서는 __format__() 메서드를 설명한다.
> 파이썬 2에서 넘어왔다면, 파이썬 3에서는 __repr__(), __str__(),__format__()메서드가 반드시 유니코드 문자열(str 형)을 반환해야 함에 주의하라. __bytes__()만 바이트 시퀀스(bytes 형)를 반환한다.

# 벡터 클래스의 부활
객체 표현을 생성하기 위해 사용하는 여러 메서드의 예를 살펴보기 위해 1장에서 살펴본 것과 비슷한 Vector2d 클래스를 사용한다. 이 절부터 이 클래스를 계속 확장해나간다. 아래 예제는 Vector2d 객체가 수행할 기본적인 동작을 보여준다.

- [Vector2d객체사용법](https://github.com/hyeonDD/fluent_python/blob/master/Part9/ex9-1~4/Vector2d.py)
1. Vector2d 요소들은 게터 메서드를 호출할 필요 없이 직접 속성에 접근할 수 있다.
2. Vector2d를 변수들의 튜플에 언패킹할 수 있다.
3. Vector2d의 repr()은 객체를 생성하는 소스 코드와 같은 형태를 출력한다.
4. eval()을 이용해서 Vector2d의 repr()이 생성자 호출을 제대로 표현했는지 확인한다.
5. Vector2d는 == 연산자를 이용한 비교를 지원한다. 이는 객체를 비교하는 데 유용하다.
6. print()는 str()을 호출하며, str()은 Vector2d 객체의 경우 순서쌍을 생성한다.
7. bytes()는 __bytes__()메서드를 이용해서 이진 표현을 생성한다.
8. abs()는__abs__()메서드를 이용해서 Vector2d 객체의 크기를 반환한다.
9. bool()은 __bool__() 메서드를 사용하며, Vector2d 객체의 크기가 0이면 False, 아니면 True를 반환한다.

아래 예제에서 사용한 Vector2d 클래스는 vector2d_v0.py에 구현되어 있다. 이 코드는 사용하는 == 연산자를 제외한 중위 연산자는 13장에서 구현한다. 현재 Vector2d는 잘 설계된 객체에서 파이썬 개발자가 기대하는 연산을 제공하기 위해 여러 특별 메서드를 구현하고 있다.

- [Vector2d클래스](https://github.com/hyeonDD/fluent_python/blob/master/Part9/ex9-1~4/Vector2d_class.py)
1. typecode는 Vector2d와 bytes 간의 변환에 사용하는 클래스 속성이다.
2. __init__() 안에서 x와 y를 float로 변환하면 부적절한 인수로 Vector2d 객체를 생성하는 경우 조기에 에러를 잡는 데 도움이 된다.
3. __iter__()를 구현하면 Vector2d를 반복할 수 있게 된다. 그렇기 때문에 x, y = my_vector 문장으로 언패킹할 수 있었다. 이 메서드는 제너레이터 표현식을 이용해서 요소를 차례대로 하나씩 생성한다.
4. __repr__()은 {!r}을 각 요소에 repr()을 호출해서 반환된 문자열로 치환해 문자열을 만든다. Vector2d를 반복할 수 있으므로, *self는 format()에 x와 y 속성을 공급한다.
5. 반복형 Vector2d에서 튜플을 만들어 순서쌍으로 출력하는 것은 간단하다.
6. bytes를 생성하기 위해 typecode를 bytes로 변환한다. 그리고 이것을
7. 객체를 반복해서 생성한 배열에서 변환된 bytes와 연결한다.
8. 모든 속성을 비교하기 위해 피연산자로부터 튜플을 생성한다. Vector2d 객체를 피연산자로 사용하면 작동하지만, 문자가 있다 아래 글상자를 참조하라.
9. magnitude()는 x와 y로 만들어진 직삼각형 사변의 길이다.
10. __bool__()은 abs(self)를 사용해서 사변 길이를 계산하고 불리언형으로 변환한다. 따라서 0.0은 False고, 그 외 값은 True다.
> 위 클래스의 __eq__()메서드는 Vector2d 객체를 피연산자로 사용하면 작동한다. 또한 동일한 숫자값을 가진 어떤한 반복형 객체도 Vector2d 객체와 비교하면 True를 반환한다(예를 들면 Vector(3,4) == [3,4]). 이것은 기능일 수도 있고 버그일 수도 있다. 이에 대해서는 연산자 오버로딩을 다루는 13장에서 설명한다.

지금까지 기본적인 메서드를 거의 구현했지만 한 가지가 빠졌다. bytes()로 생성한 이진 표현에서 Vector2d 객체를 다시 만드는 메서드가 없다.

# 대안 생성자
Vector2d를 bytes로 변환하는 메서드가 있으니, 당연히 bytes를 Vector2d로 변환하는 메서드도 있어야 할 것이다. 영감을 얻기 위해 표준 라이브러리를 살펴보면, frombytes()라는 클래스 메서드르 가진 array.array가 우리 상황에 딱 맞는 것 같다. 이 이름과 기능을 이용해서 Vector2d의 클래스 메서드로 추가해보자.
- [Vector2d클래스](https://github.com/hyeonDD/fluent_python/blob/master/Part9/ex9-1~4/Vector2d_class2.py)
1. 클래스 메서드에는 @classmethod 데커레이터가 붙는다.
2. self 매개변수가 없다. 대신 클래스 자신이 cls 매개변수로 전달된다.
3. 첫 번째 바이트에서 typecode를 읽는다.
4. octets 이진 시퀀스로부터 memoryview를 생성하고 typecode를 이용해서 형을 변환한다.
5. cast()가 반환한 memoryview를 언패킹해서 생성자에 필요한 인수로 전달한다.

방금 사용한 @classmethod 데커레이터는 파이썬에 고유한 기능이다. 이에 대해 간단히 알아보자.

# @classmethod와 @staticmethod
파이썬 튜토리얼에서는 @classmethod와 @staticmethod 데커레이터에 대해 설명하지 않는다. 자바 언어로 객체지향 개념을 배운 사람은 이 두 데커레이터가 파이썬에 있는 이유가 궁금할 것이다.

먼저 @classmethod에 살펴보자. 아래예제를 보면 @classmethod 데커레이터는 객체가 아닌 클래스에 연산을 수행하는 메서드를 정의한다는 것을 알 수 있다. @classmethod는 메서드가 호출되는 방식을 변경해서 클래스 자체를 첫 번째 인수로 받게 만들며, 예제에서 본 frombytes()같은 대안 생성자를 구현하기 위해 주로 사용된다. frombytes() 메서드의 마지막 문장에서 cls(*memv)는 객체를 생성하기 위해 cls 인수를 이용해서 실제로 클래스의 생성자를 호출한다. 관습적으로 cls를 클래스 메서드의 첫 번째 매개변수명으로 사용하지만, 파이썬은 특정 매개변수명을 요구하지 않는다.

반대로 @staticmethod 데커레이터는 메서드가 특별한 첫 번째 인수를 받지 않도록 메서드를 변경한다. 본질적으로 정적 메서드는 모듈 대신 클래스 본체 안에 정의된 평범한 함수일 뿐이다. 아래 예제는 @classmethod와 @staticmethod 데커레이터의 동작을 비교해서 보여준다.

- [classmethod, staticmethod 동작 차이](https://github.com/hyeonDD/fluent_python/blob/master/Part9/ex9-1~4/class_static_method.py)
1. klassmeth()는 모든 위치 인수를 보여준다.
2. statmeth()도 마찬가지다.
3. 호출 방법에 무관하게 Demo.klassmeth()는 Demo 클래스를 첫 번째 인수로 받는다.
4. Demo.statmeth()는 단지 평범한 함수처럼 동작할 뿐이다.

> @classmethod 데커레이터는 쓰임새가 많은 게 확실하지만, @staticmethod 데커레이터는 사용해야 하는 이유를 잘 모르겠다. 클래스와 함께 작동하지 않는 함수를 정의하려면, 단지 함수를 모듈에 정의하면 된다. 아마 함수가 클래스를 건드리지는 않지만, 그 클래스와 밀접히 연관되어 있어서 클래스 코드 가까운 곳에 두고 싶을 수는 있을 것이다. 그런 경우에는 클래스의 바로 앞이나 뒤에서 함수를 정의하면 된다.

이제 @classmethod가 어디에 도움이 되는지(그리고 @staticmethod는 그리 도움이 되지 않는다는 것을) 살펴봤으니, 다시 객체 표현 문제로 돌아가서 출력 포맷을 지원하는 방법을 알아보자.