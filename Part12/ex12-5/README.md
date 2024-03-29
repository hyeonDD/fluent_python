<!-- 
[UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part12/ex12-1~2/UML_class_diagram.png)
 -->
# 최신 사례: 장고 제너릭 뷰의 믹스인

---

이 절의 설명을 이해하기 위해 Django를 알고 있을 필요는 없다. 다중 상속의 실제 사례로서 프레임워크의 일부분만 살펴보며, 다른 언어나 프레임워크를 이용해서 서버 측 웹을 개발해본 경험이 있는 독자를 위해 필요한 배경도 모두 설명한다.

---
장고의 뷰는 콜러블 객체로서 HTTP 요청을 나타내는 객체를 인수로 받아서 HTTP 응답을 나타내는 객체를 반환한다. 이때 반환될 수 있는 다양한 HTTP 응답이 흥미롭다. HTTP 응답은 본체가 없는 리다이렉션처럼 아주 간단할 수 있고, HTML 템플릿으로 렌더링해서 구입 버튼과 자세한 정보 페이지에 대한 링크를 나열하는 온라인 스토어 카탈로그 페이지처럼 복잡할 수도 있다.

원래 장고는 일반적인 용도를 구현하는 제너릭 뷰라고 하는 일련의 함수를 제공했다. 인터넷 검색 엔진의 겸색 결과에서는 자세한 정보 페이지에 대한 링크를 여러 페이지에 걸쳐 나열하는데, 장고의 리스트 뷰와 상세 뷰는 각 항목에 대한 페이지를 생성한다.

그렇지만 원래의 제너릭 뷰는 함수였으므로 확장할 수 없었다. 제너릭 뷰와 비슷하지만 완전히 똑같지 않은 무언가를 만드는 경우 처음부터 시작해야 한다.

장고 1.3에서는 기반 클래스, 믹스인, 바로 사용할 수 있는 구상 클래스로 구성된 일련의 범용뷰 클래스와 함께 클래스 기반의 뷰를 소개했다. 아래 그림에서 보는 것처럼 기반 클래스와 믹스인은 django.views.generic 패키지의 base 모듈에 들어 있다. 다이어그램의 꼭대기에는 서로 다른 책임을 지고 있는 View 클래스와 TemplateResponseMixin 클래스가 있다.

![django클래스사진]](https://github.com/hyeonDD/fluent_python/blob/master/Part12/ex12-5/django.png)

> 이 클래스들을 연구하는 데 'Classy Class-Based Views' 웹사이트 (http://ccbv.co.uk/) 가 상당히 유용하다. 이 사이트에서는 각 클래스를 쉽게 둘러볼 수 있으며, 각 클래스별 모든 메서드 (상속된 메서드, 오버라이드한 메서드, 추가한 메서드 등)를 볼 수 있으며, 다이어그램을 보고, 문서를 살펴보고, 깃허브의 해당 소스코드를 바로 볼 수 있다 (http://bit.ly/1JHSoe8) .

View는 모든 뷰의 기반 클래스로서(ABC), 다양한 HTTP 동사를 처리하는 구상 서브클래스가 구현한 get(), head(), post()등의 처리 메서드를 호출하는 dispatch() 메서드와 같은 핵심 기능을 제공한다. RedirectView 클래스는 View 클래스만 상속하며, get(), head(), post() 등의 메서드를 구현한다.

View의 구상 서브클래스는 처리 메서드를 구현해야 하는데, 왜 이 메서드가 View 인터페이스에 정의되어 있지 않을까? 이는 서브클래스가 자신이 지원하려는 처리기만 구현할 수 있도록 하기 위해서다. TemplateView는 내용을 화면에 출력하기 위해 사용하므로, Get() 메서드만 구현한다. HTTP POST 요청을 TemplateView에 보내면 상속된 View.dispatch() 메서드는 post() 처리기가 없다는 것을 확인하고 'HTTP 405 Method Not Allowed' 응답을 생성한다.

TemplateResponseMixin은 템플릿을 사용해야 하는 뷰에만 관련된 기능을 제공한다. 예를 드어 RedirectView는 내용 본체가 없어서 템플릿이 필요 없으므로 TemplateResponseMixin을 상속하지 않는다. TemplateResponseMixin은 TemplateView 및 django.views.generic 패키지의 다른 모듈에 정의된 ListView, DetailView등의 템플릿을 렌더링하는 뷰에 필요한 행동을 제공한다. django.views.genereic.list 모듈 및 base 모듈의 일부를 아래 그림에 나타냈다.

아래 그림에서 장고 사용자에게 가장 중요한 클래스느 ListView 클래스로서 자기 자신만의 코드는 전혀 없는 집합 클래스다 (클래스 본체에는 문서화 문자열만 있다). 생성된 ListView 객체에는 object_list라는 속성이 있는데, 템플릿은 페이지의 내용을 보여주기 위해 이 속성을 반복한다. 일반적으로 여러 객체를 반환하는 데이터베이스 쿼리 결과가 object_list에 저장된다. 이렇게 반복할 수 있는 객체를 생성하는 것과 관련된 기능은 모두 MultipleObjectMixin이 제공한다. 이 믹스인은 결과 중 일부를 한 페이지에 출력하고 다른 페이지에 대한 링크를 걸기 위해 복잡한 페지화 논리도 제공한다.

![django클래스사진]](https://github.com/hyeonDD/fluent_python/blob/master/Part12/ex12-5/django_list.png)

템플릿을 렌더링하지 않지만 JSON 형식으로 객체의 리스트를 생성하는 뷰가 필요하다고 가정해보자. 이런 용도에 BaseListView 클래스가 제공된다. 이 클래스는 템플릿 구성의 부담 없이 View와 MultipleOjbectMixin을 쉽게 통합할 수 있는 확장 지점을 제공한다.

다중 상속의 예를 보여주기에는 장고의 클래스 기반 뷰 API가 Tkinter보다 좋다. 특히 장고의 믹스인은 용도가 분명하고 클래스명이 Mixin으로 끝나므로 쉽게 알아볼 수 있다.

클래스 기반 뷰는 장고 사용자들이 두루 사용하는 것은 아니었다. 일종의 블랙박스로서 일부 기능만 사용하며, 새로운 무언가가 필요할 때 기반 뷰와 믹스인을 재사용하지 않고 모든 기능을 하나의 뷰에 몰아넣어 구현하려는 사용자들도 많다.

클래스 기반 뷰를 활용하고 애플리케이션의 특정 용도에 맞게 확장하는 방법을 배우려면 어느정도 시간이 걸리지만, 배워둘 가치는 있다고 생각한다. 획일적으로 반복되는 코드를 상당히 줄일 수 있고, 해결책을 재사용하기 쉽게 만들어주며, 심지어 템플릿 및 템플릿 콘텍스트에 전달되는 변수에 대한 표준적인 명칭을 정의함으로써 팀 내 의사소통도 원활히 할 수 있다. 클래스 기반 뷰는 장고 뷰'온 레이즈'라고 할 수 있다.

이것으로 다중 상속과 믹스인 클래스에 대한 설명은 마친다.
