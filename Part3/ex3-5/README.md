# 그 외 매핑형

1. COLLECTIONS.OrderedDict
    - 키를 삽입한 순서대로 유지함으로써 항목을 반복하는 순서를 예측할 수 있다. OrderedDict의 popitem() 메서드는 기본적으로 최근에 삽입한 항목을 꺼내지만, my_odict.popitem(last=True)형태로 호출하면 처음 삽입한 항목을 꺼낸다.

2. collections.ChainMap
    - 매핑들의 목록을 담고 있으며 한꺼번에 모두 검색할 수 있다. 각 매핑을 차례대로 검색하고, 그중 하나에서라도 키가 검색되면 성공한다. 이 클래스는 내포된 범위를 지원하는 언어에서 각 범위를 하나의 매핑으로 표현함으로써 인터프리터를 구현하는 데 유용하게 사용할 수 있다. 파이썬 문서의 collections 절에서 'ChainMap 객체' 부분(http://bit.ly/1Vm7I4c:) 을 보면 ChainMap을 사용하는 여러 예제를 볼 수 있는데, 그중 다음 코드는 파이썬에서 변수를 조회하는 기본 규칙을 표현하고 있다.
    ```
    import builtins
    pylookup = ChainMap(locals(), globals(), vars(builtins))
    ```

3. collections.Counter
    - 모든 키에 정수형 카운터를 갖고 있는 매핑. 기존 키를 갱신하면 카운터가 늘어난다. 이 카운터는 해시 가능한 객체(키)나 한 항목이 여러 번 들어갈 수 있는 다중 집합에서 객체의 수를 세기 위해 사용할 수 있다. Counter 클래스는 합계를 구하기 위한 +와 - 연산자를 구현하며, n개의 가장 널리 사용된 항목과 그들의 카운터로 구성된 튜플의 리스트를 반환하는 most_common([n])등의 메서드를 제공한다. 자세한 설명은 문서(http://bity.ly/1JHVi2E)를 참조하라. 다음 코드는 Counter를 이용해서 단어 안에서 각 글자의 횟수를 계산하는 예를 보여준다.
    ```
    ct = collections.Counter('abracadabra)
    print(ct)
    ct.update('aaaaazzz)
    print(ct)
    print(ct.most_common(2))
    ```

4. collections.UserDict
    - 표준 dict처럼 작동하는 매핑을 순수 파이썬으로 구현한 클래스.