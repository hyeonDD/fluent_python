# 특별메서드 __getitem__() 와 __len__ 만으로도 강력한 기능 구현 가능

* __len__()
    - Object 의 갯수를 바로 반환 가능.

* __getitem__()
    - __getitem__() 특별메서드 구성을 통해 위 예제에서는 이터러블한 list 객체인 self._cards를 넘겼기에 반복문,슬라이싱 등을 지원가능하게 해줌.

> 파이선 2에서는 FrenchDeck(object)와 같이 명시적으로 작성해야 하지만, 파이썬 3 에서는 기본적으로 object를 상속받음.