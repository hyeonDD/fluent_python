# 일반적인 딕셔너리 (dict)

* dict 의 사용처 및 특성
    - 표준 라이브리에서 제공하는 매핑형은 모두 dict을 이용해서 구현하며, 키가 **해시 가능** 해야 한다는 제한을 갖고있다.
    > **해시 가능하다라** 는 말의 의미는 수명 주기동안 결코 변하지 않는 해시값을 갖고 있고(__hash__()메서드가 필요하다) 다른 객체와 비교할 수 있으면(__eq__() 메서드가 필요하다), 객체를 해시 가능하다고 한다. 동일하다고 판단되는 객체는 반드시 해시값이 동일해야 한다.
    원자적 불변형(str, byte, 수치형)은 모두 해시 가능하다. frozenset은 언제나 해시 가능하다. 모든 요소가 해시 가능하도록 정의되어 있기 때문이다. 튜플은 들어 있는 항목들이 모두 해시가능해야 해시 가능하다.

    [해쉬가능한 자료형](https://github.com/hyeonDD/fluent_python/blob/master/Part3/ex3-1~3/can_hash.py "소스코드")

    - 위 소스를 참고하면 frozenset은 언제나 해시가능하며, 일반적으로 쓰인 list 자료형은 해쉬가 불가능하다.
    > 파이썬 용어집(http://bit.ly/1K4qjwE)에서는 '파이썬이 제공하는 불변 내장 객체는 모두 해시 가능하다'고 설명하지만, 이설명은 정확하지 않다. 튜플은 불변형이긴 하지만, 해시 불가능한 객체를 참조할 수 있기 때문이다.

    - 객체가 자신의 내부 상태를 평가해서 __eq__() 메서드를 직접 구현하는 경우에는 해시값 계산에 사용되는 속성이 모두 불변형일 때만 해시 가능하다.

    - 딕셔너리의 다양한 구현은 파이썬 라이브러리 참조문서 사이트의 [여러 dict 선언방법](https://github.com/hyeonDD/fluent_python/blob/master/Part3/ex3-1~3/init_dict.py "소스코드")

    - 딕셔너리의 update(m, [**kargs]) 메서드가 첫 번째 인수 m을 다루는 방식은 덕 타이핑(duck typing)의 대표적인 사례다. 먼저 m이 keys() 메서드를 갖고 있는지 확인한 후, 만약 메서드를 갖고 있다면 매핑이라고 간주한다. keys()메서드가 없으면, update()메서드는 m의 항목들이 (키,값) 쌍으로 되어 있다고 간주하고 m을 반복한다. 대부분의 파이썬 매핑은 update() 메서드와 같은 논리를 내부적으로 구현한다. 따라서 매핑은 다른 매핑으로 초기화하거나, (키, 값) 쌍을 생성할 수 있는 반복형 객체로 초기화할 수 있다.
        - setdefault() 메서드는 신비롭다. 이 메서드가 늘 필요한 것은 아니지만, 이 메서드가 필요할 때는 똑같은 키를 여러 번 조회하지 않게 해줌으로써 속도를 엄청나게 향상시킨다.

        - **존재하지 않는 키를 setdefault()로 처리하기**
            - 조기실패(fail-fast) 철학에 따라, 존재하지 않는 키 k로 d[k]를 접근하면 dict는 오류를 발생시킨다. KeyError를 처리하는 것보다 기본값을 사용하는 것이 더 편리한경우네는 d[k] 대신 d.get(k,default)를 사용한다. [setdefault 예시](https://github.com/hyeonDD/fluent_python/blob/master/Part3/ex3-1~3/not_exist_dict_key.py "소스코드")

    

* 지능형 딕셔너리(dictcomp)
    - 모든 반복형 객체에서 키-값 쌍을 생성함으로써 딕셔너리 객체를 만들 수 있다.

    [지능형 딕셔너리 예제](https://github.com/hyeonDD/fluent_python/blob/master/Part3/ex3-1~3/smart_dict.py "소스코드")