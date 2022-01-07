# UserDict

* UserDict 상속하기
    - UserDict는 dict를 상속하지 않고 내부에 실제 항목을 담고 있는 data라고 하는 dict 객체를 갖고 있다. 이렇게 구현함으로써 __setitem__() 등의 특수 메서드를 구현할 때 발생하는 원치않는 재귀적 호출을 피할 수 있으며, __contains__() 메서드를 간단히 구현할 수 있다. [UserDict 예제소스](https://github.com/hyeonDD/fluent_python/blob/master/Part3/ex3-6/userdict.py
    
    -  UserDict 클래스가 MutableMapping을 상속하므로 StrKeyDict는 결국 UserDict, MutableMapping, 또는 Mapping을 상속하게 되어 매핑의 모든 기능을 가지게 된다. Mapping은 추상 베이스 클래스(ABC)임에도 불구하고 유용한 구상(구체적인)메서드를 다수 제공한다.
        -**MutableMapping.update()**
        이 강력한 메서드는 직접 호출할 수도 있지만, 다른 매핑이나 (키, 값) 쌍의 반복형 및 키워드 인수에서 객체를 로딩하기 위해 __init__()에 의해 사용될 수도 있다. 이메서드는 항목을 추가하기위해 'self[키] = 값'구문을 사용하므로 결국 서브클래스에서 구현한 __setitem__()메서드를 호출하게 된다.
        -**Mapping.get()**
        StrKeyDict0(에제 3-7)[UserDict 예제소스](https://github.com/hyeonDD/fluent_python/blob/master/Part3/ex3-6/strkeydict0.py에서는 __getitem__()과 일치하는 결과를 가져오기 위해 get() 메서드를 직접 구현해야 했지만, 위 UserDict예제소스와 같이 StrKeyDict0.get()과 완전히 동일하게 구현된 Mapping.get()을 상속받는다. 파이썬 코드[참고](http://bit.ly/1FEOPPB)
