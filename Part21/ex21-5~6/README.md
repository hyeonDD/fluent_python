<!-- 
- [](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-5~6/aaa)
 -->
# 디스크립터를 커스터마이즈하기 위한 메타클래스

이제 다시 lineItem 예제로 돌아가자. 사용자가 데커레이터나 메타클래스에 신경 쓰지 않고, 단지 아래 예제 bulk_v7.py처럼 라이브러리가 제공하는 클래스를 상속할 수 있게 해주면 좋을 것이다.

- [bulkfood_v7.py](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-5~6/bulkfood_v7.py)
1. LineItem은 model.Entity의 서브클래스다.

위 blukfood_v7.py는 아무런 문제가 없는 것처럼 보인다. 이상한 구문도 전혀 없다. 그러나 이 코드는 model_v7.py에서 메타클르스를 정의하고, model.Entity가 그 메타클래스의 객체여야 제대로 동작한다. 아래 예제에서는 model_v7.py 모듈에서 정의한 Entity 클래스의 소스코드다.

- [model_v7.py](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-5~6/model_v7.py)
1. 슈퍼클래스 (여기서는 type)의 __init__() 메서드를 호출한다.
2. model_v6.py의 @entity 데커레이터와 동일한 논리를 구현한다.
3. 이 클래스는 편의를 위해 제공되었다. 이 모듈을 사용하는 사람은 단지 Entity 클래스를 상속하면 된다. EntityMeta를 신경 쓸 필요 없으며, 심지어 이런 클래스가 있는지 몰라도 된다.

blukfood_v7.py의 클래스는 blukfood_v6.py의 테스트를 통과한다. 지원 모듈인 model_v7.py는 model_v6.py보다 이해하기 어렵지만, 사용자 코드는 더 간단하다. 단지 model_v7.Entity를 상속해서 Validated 필드의 저장소명만 원하는 대로 바꾸면 되기 때문이다.

아래 그림은 우리가 좀 전에 구현한 것을 간단한 그림으로 보여준다. 많은 연산이 수행되지만, 이런 복잡한 과정은 model_v7 모듈 안에 숨어 있다. 사용자 관점에서 보면 LineItem은 단지 Entity의 서브클래스며, blukfood_v7.py와 같이 구현했을 뿐이다. 이는 추상화의 위력을 잘 보여준다.

![entitymeta.png](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-5~6/entitymeta.png)

# 메타클래스 __prepare__() 특별 메서드

몇몇 애플리케이션에서는 클래스의 속성이 정의되는 순서를 알아야 하는 경우가 종종 있다. 예를 들어 사용자 정의 클래스에 의해 구동되어 CSV파일을 읽고 쓰는 라이브러리의 경우 CSV파일에서 열의 순서대로 클래스 안에 필드를 매핑해야 한다.

지금까지 본 것처럼 type() 생성자와 메타클래스의 __new__() 및 __init__()메서드는 이름과 속성의 매핑으로 평가된 클래스 본체를 받는다. 그러나 기본적으로 매핑은 딕셔너리형이므로, 메타클래스나 데커레이터 확인할 수 있을 때는 클래스 본체 안에 등장하는 속성의 순서가 사라져버린다.

이 문제를 해결하려면 파이썬 3에 소개된 __prepare__() 특별 메서드를 사용해야 한다. 이 특별 메서드는 메타클래스에서만 의미가 있으며, 클래스 메서드여야 한다 (즉, @classmethod 데커레이터로 장식해야 한다.). 인터프리터는 메타클래스의 __new__() 메서드를 호출하기 전에 클래스 본체의 속성을 이용해서 채울 매핑을 생성하기 위해 __prepare__() 메서드를 호출한다. 메타클래스를 첫 번째 인수로 전달받는 것 외에, __prepare__()는 생성할 클래스명과 슈퍼클래스가 담겨진 튜플을 받으며, 메타클래스가 새로운 클래스를 만들 때 호출하는 __new__()와 __init__() 메서드의 마지막 인수로 전달할 매핑을 반환해야 한다.

이론적으로는 복잡해보이지만, 실제로 사용되는 __prepare__() 메서드를 볼 때마다 아주 간단하다는 느낌이 들었다. 아래예제를 보자.

- [model_v8.py](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-5~6/model_v8.py)
1. 빈 OrderedDict 객체를 반환한다. 여기에 클래스 속성을 저장할 것이다.
2. 생성하고 있는 클래스 안에 _field_names 속성을 추가한다.
3. 이 코드 자체는 이전 버전과 달라진 것이 없지만, 여기에 있는 attr_dict는 __init__()이 호출되기 전에 __prepare__()에서 생성한 OrderDict 객체다. 따라서 for 루프가 반복되는 순서대로 속성이 추가된다.
4. 발견한 Validated 필드를 모두 _field_names에 추가한다.
5. filed_names() 클래스 메서드는 단순히 추가된 순서대로 필드명을 생성한다.

model_v8.py에서 추가한 간단한 코드 덕분에, 이제 filed_names() 클래스 메서드를 이용해서 모든 Entity 서브클래스의 Validated 필드를 반복할 수 있게 되었다. bulkfood_v8.py는 이 기능을 사용하는 예를 보여준다.

- [bulkfood_v8.py](https://github.com/hyeonDD/fluent_python/blob/master/Part21/ex21-5~6/bulkfood_v8.py)
```
>>> for name in LineItem.field_names():
...     print(name)
...
description
weight
price
```
이제 메타클래스에 대한 설명을 마친다. 실제 메타클래스는 프로그래머들이 다음과 같은 작업을 수행할 수 있도록 프레임워크와 라이브러리에서 사용된다.
* 속성 검증
* 많은 메서드에 데커레이터를 일괄 적용
* 객체 직렬화 및 데이터 변환
* 객체 관계 매핑
* 객체 기반 영속성
* 다른 언어에서 만든 클래스 구조체를 파이썬 클래스로 동적 변환

이제 파이썬 데이터 모델이 모든 클래스에 정의한 메서드를 간략히 살펴보자.