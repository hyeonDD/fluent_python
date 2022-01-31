<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-5/UML_class_diagram.png)
 -->
# ABC 상속하기
알렉스 마르텔리의 충고에 따라, 직접 ABC를 만드는 작업을 시도해보기 전에 collections.MutableSequence라는 ABC를 활용해보자. 아래 예제에서는 FrenchDeck2를 collections.MutableSequence의 서브클래스로 선언한다.

- [frenchdeck2.py](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-5/frenchdeck2.py)
1. 카드를 섞기 위해서는 __setitem__() 메서드만 있으면 된다.
2. 그러나 MutableSequence 클래스를 상속했으므로, 이 클래스의 추상 메서드인 __delitem__()도 구현해야 한다.
3. 그리고 MutableSequence의 세 번째 추상 메서드인 insert()도 구현해야 한다.

파이썬은 모듈을 로딩하거나 컴파일할 때가 아니라, 실행 도중 실제로 FrenchDeck2  객체를 생성할 때 추상 메서드의 구현 여부를 확인한다. 이때 추상 메서드 중 하나라도 구현되어 있지 않으면 '추상 메서드 __delitem__(), insert()를 가진 추상 클래스 FrenchDeck2의 객체를 생성할 수 없습니다'라는 메시지와 함께 TypeError 예외가 발생한다. 그렇기 때문에 우리가 구현한 FrenchDeck2 예제에서 사용하지도 않는 __delitem__()과 insert() 메서드를 구현해야 했다. MutableSequence ABC가 요구하는 사항이기 때문이다.

아래 그림을 보면 Sequence와 MutableSequnce ABC의 메서드 전부가 추상 메서드는 아님을 알 수 있다.

![collections_abc사진]](https://github.com/hyeonDD/fluent_python/blob/master/Part11/ex11-5/collections_abc_mutablesequence.jpg)

FrenchDeck2는 Sequence로부터 __contains__(), __iter__(), __reversed__(), index(), count()와 같은 바로 사용할 수 있는 메서드를 상속한다. MutableSequence 클래스로부터는 append(), reverse(), extend(), pop(), remove(), __iadd__() 메서드를 상속한다.

collections.abc ABC의 구상 메서드는 클래스의 공개 인터페이스만 이용해서 구현하므로, 클래스 내부 구조를 몰라도 제대로 작동한다.
> 구상 서브클래스를 구현하는 여러분은 ABC로부터 상속한 메서드를 효융리 더 뛰어난 메서드로 오버라이드 할 수 있다. 예를 들어 __contains__()는 시퀀스 전체를 조사하지만, 구상 클래스가 항목들을 정렬된 상태로 유지하고 있다면 bisect()함수(2.8절 '정렬된 시퀀스를 bisect로 관리하기' 참조)를 이용해서 이진 검색함으로써 __contains__()의 속도도 향상시킬 수 있다.

ABC를 잘 활용하려면 어떤 것들이 제공되는지 알아야 한다. 다음 절에서는 collections에서 제공하는 ABC를 살펴본다.