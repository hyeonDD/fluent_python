# 함수 에너테이션
<!-- 
[예](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-1~3/encode_decode.py)
 -->
파이썬 3는 함수의 매개변수와 반환값에 메타데이터를 추가할 수 있는 구문을 제공한다.
아래 예제는 이전 보았던 clip 함수에 에너테이션을 추가한 버전이다. 단지 첫 번째 줄만 다르다.
- [애너테이션을 추가한 clip](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-9~10/clip_annotation.py)
    1. 함수 선언에 에너테이션을 추가했다.

함수 선언에서 각 매개변수에는 콜론(:) 뒤에 애너테이션 표현식을 추가할 수 있다. 기본값이 있을 때, 애너테이션은 인수명과 등호(=) 사이에 들어간다.
반환값에 애너테이션을 추가하려면 매개변수를 닫는 괄호와 함수 선언의 제일 뒤에 오는 콜론 사이에 -> 기호와 표현식을 추가한다.
표현식은 어떤 자료형도 될 수 있다. str이나 int와 같은 클래스, 혹은 위 예제의 max_len에 대한 애너테이션인 'int >0'과 같은 문자열이 애너테이션에 가장 널리 사용되는 자료형이다.

애너테이션은 전혀 처리하지 않으며, 단지 함수 객체 안의 dict 형 __annotations__ 속성에 저장될 뿐이다.

```
>>>from clip_annotation import clip
>>> clip.__annotations__
{'text': <class 'str'>, 'max_len': 'int >0', 'return': <class 'str'>}
```
'return'키에 대한 항목은 위 예제에서 함수 선언부 중 -> 기호로 표시한 반환값 애너테이션을 담고 있다.

파이썬은 애너테이션을 함수의 __annotations__속성에 저장할 뿐이다. 검사, 단속, 검증 등 아무런 행동도 취하지 않는다.
즉, 애너테이션은 파이썬 인터프리터에 아무런 의미가 없다. 애너테이션은 도구(IDE 등), 프레임워크, 데커레이터가 사용할 수 있는 메타데이터일 뿐이다.
이 책을 쓰고 있는 현재, 이 메타데이터를 사용하는 도구는 표준 라이브러리에 없다. 다만 아래 예제에서 볼 수 있는 것처럼 inspect.signature()만 애너테이션을
추출하는 방법을 알고 있을 뿐이다.

- [함수 시그니처에서 애너테이션 추출하기](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-9~10/clip_parse_annotation.py)
signature() 함수는 Signature 객체를 반환한다. Signature에는 return_annotation과 parameters 속성이 있는데, parameters는 파라미터명을 Parameter 객체에 매핑하는 딕셔너리다.
각 Parameter 객체는 annotation 속성을 가지고 있는데, 이 속성을 이용해서 위 예제처럼 작동한다.

향후에 Bobo와 같은 프레임워크는 요청 처리를 더욱 자동화하기 위해 애너테이션을 지원할 수도 있을 것이다. 예를 들면 다음과 같이 애너테이션을 처리할 수 있다.

***
price:float
쿼리 문자열을 함수가 받는 float 형으로 자동 변환한다.

quantity:'int >0'
애너테이션을 파싱해서 인수를 변환하고 검증한다.
***
함수 애너테이션은 Bobo와 같은 동적 설정보다는 IDE나 linter와 같은 도구에서 정적 자료형 검사를 지원하기 위해 선택적인 자료형 정보를 제공하는 데 큰 영향을 줄 것이다.

# 함수형 프로그래밍을 위한 패키지

귀도 반 로섬은 파이썬이 함수형 프로그래밍 언어를 지향하지 않았다고 공표하고 있지만, operator와 functools 같은 패키지들의 지원 덕분에 파이썬에서도 제법 함수형 코딩 스타일을 사용할 수 있다.

## operator 모듈
함수형 프로그래밍을 할 때 산술 연산자를 함수로 사용하는 것이 편리할 때가 종종 있다. 예를들어 팩토리얼을 계산하기 위해 재귀적으로 함수를 호출하는 대신 숫자 시퀀스를 곱하는 경우를 생각해보자. 합계를 구할 때는 sum()이라는 함수가 있지만, 곱셈에 대해서는 이에 해당하는 함수가 없다. '5.2.1절 map(), filter(), reduce()의 대안'에서 설명한 것처럼 reduce()함수를 사용할 수 있지만, reduce()는 시퀀스의 두 항목을 곱하는 함수를 필요로 한다. 람다를 이용해서 이 문제를 해결하는 방법을 보자.

- [reduce()와 익명 함수로 구현한 팩토리얼](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-9~10/factorial_reduce_lambda.py)
    lambda와 같이 사소한 익명 함수를 작성하는 수고를 덜기 위해 operator 모듈은 수십 개의 연산자에 대응하는 함수를 제공한다.

- [reduce()와 operator를 이용해 구현한 팩토리얼](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-9~10/factorial_reduce_operator.py)
    operator 모듈은 시퀀스에성 항목을 가져오는 람다를 대체하는 itemgetter()함수와 객체의 속성을 읽는 람다를 대체하는 attregetter()함수를 제공한다.

