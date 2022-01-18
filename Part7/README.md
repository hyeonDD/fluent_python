# 함수 데커레이터와 클로저
함수 데커레이터는 소스 코드에 있는 함수를 '표시'해서 함수의 작동을 개선할 수 있게 해준다. 강력한 기능이지만, 데커레이터를 자유자재로 사용하려면 먼저 클로저를 알아야 한다.

파이썬 3.0에 추가된 nonlocal은 최근에 추가된 예약 키워드 중 하나다. 클래스 중심의 엄격한 객체지향 방식을 고수한다면 이 기능을 사용하지 않고도 파이썬 프로그래머로서의 살멩 아무런 지장을 받지 않을 수 있다. 그러나 자기만의 데커레이터를 구현하고자 한다면 클로저를 속속들이 이해해야 하며, 그로거 나면 nonlocal이 필요해진다.

데커레이터에서 사용하는 것 외에도, 클로저는 콜백을 이용한 효율적인 비동기 프로그래밍과 필요에 따라 함수형 스타일로 코딩하는 데에도 필수적이다.

이 장의 궁극적인 목표는 아주 단순한 등록 데커레이터에서부터 복잡한 매개변수화된 데커레이터에 이르기까지 함수 데커레이터가 정확히 어떻게 작동하는지 설명하는 것이다. 그렇지만 목표에 도달하기 전에 다음과 같은 내용을 먼저 살표봐야 한다.
* 파이썬이 데커레이터 구문을 평가하는 방식
* 변수가 지역 변수인지 파이썬이 판단하는 방식
* 클로저의 존재 이유와 작동 방식
* nonlocal로 해결할 수 있는 문제
이런 기반을 갖추고 나면 다음과 같이 데커레이터 주제를 심도 있게 다룰 수 있다.
* 잘 작동하는 데커레이터 구현하기
* 표준 라이브러리에서 제공하는 재미있는 데커레이터들
* 매개변수화된 데커레이터 구현하기
먼저 데커레이터에 대한 아주 기초적인 내용부터 살펴보고, 위에서 나열한 주제들을 살펴보자.