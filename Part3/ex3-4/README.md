# 융통성 있게 키를 조회하는 매핑 
검색할 때 키가 존재하지 않으면 어떤 특별한 값을 반환하는 매핑이 있으면 편리한 때가 종종 있다.
이런 딕셔너리를 만드는 방법은 크게 두 가지다.

1. 하나는 평범한 dict 대신 defaultdict를 사용하는 방법이고
2. 다른 하나는 dict 등의 매핑형을 상속해서 __missing__() 메서드를 추가하는 방법이다.

* defaultdict: 존재하지 않는 키에 대한 또 다른 처리
    
    - defaultdict 객체를 생성할 때 존재하지 않는 키 인수로 __getitem__() 메서드를 호출할 때마다 기본값을 생성하기 위해 사용되는 콜러블을 제공하는 것이다.
    예를들어 dd = defaultdict(list) 코드로 기본 defaultdict 객체를 생성한 후, dd에 존재하지 않는 키인 'new-key'로 dd['new-key'] 표현식을 실행하면 다음과 같이 처리된다.
        1. 리스트를 새로 생성하기 위해 list()를 호출한다.
        2. 'new-key'를 키로 사용해서 새로운 리스트를 dd에 삽입한다.
        3. 리스트에 대한 참조를 반환한다.
        [defaultdict 예제소스](https://github.com/hyeonDD/fluent_python/blob/master/Part3/ex3-4/index_default.py "소스코드")

    - __missing__(메서드) 매핑형은 이름으로도 쉽게 추측할 수 있게 __missing__() 메서드를 이용해서 존재하지 않는 키를 처리한다.
    이 특수 메서드는 기본 클래스인 dict에는 정의도어 있지 않지만, dict는 이 메서드를 알고 있다.
    따라서 dict 클래스를 상속하고 __missing__()메서드를 정의하면, dict.__getitem__() 표준 메서드가 키를 발견할 수 없을때 KeyError를 발생시키지 않고 __missing__()메서드를 호출한다.
    > __missing__()메서드는 d[k]연산자를 사용하는 경우 등 __getitem__()메서드를 사용할 때만 호출된다. in 연산자를 구현하는 get()이나 __contains__()메서드 등 키를 검색하는 다른메서드에는 __missing__() 메서드가 영향을 미치지 않는다. 그렇기 때문에 3.4.1절 마지막 부분의'CAUTION' 글상자에서 설명한 것처럼 __getitem__() 메서드를 사용할때만 defaultdict의 default_factory가 작동한다.

    > 파이썬 3에서는 아주 큰 매핑의 경우에도 k in my_dict.keys() 형태의검색이 효율적이다. dict.keys()는 집합과 비슷한 뷰를 반환하는데, 집합에 포함되었는지 여부를 검사하는것은 딕셔너리만큼 빠르기 때문이다. 자세한 설명은 파이썬 문서의 '딕셔너리 뷰 객체'절(http://bit.ly/lVm7E4q)를 참조하라. 파이썬 2에서 dict.keys()는 리스트를 반환하므로, 여기에서 설명하는 코드가 작동은 하지만, k in my_list 연산이 리스트를 검색해야 하므로 딕셔너리가 커지면 효율이 떨어진다.

    