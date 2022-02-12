<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-1/UML_class_diagram.png)
 -->
# 동적 속성을 이용한 데이터 랭글링

다음에 나올 몇 가지 에제에서는 OSCON 2014 콘퍼런스에서 오라일리가 공개한 JSON 데이터 피드를 사용하기 위해 동적 속성을 이용한다. 아래예제는 이 데이터 피드에서 레코드 네개를 가져왔다.

- [osconfeed.json](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-1/osconfeed.json)
위예제는 JSON 피드의 895개 레코드 중 4개를 보여준다. 여기에서 보는 것처럼 전체 데이터셋이 "Schedule"이라는 키를 가진 하나의 JSON 객체며, 이 값은 "conferences", "events", "speakers", "venues"등 4개의 키로 매핑되어 있으며, 이 네 개의 키는 각각 레코드 리스트와 짝지어져 있다. 위 JSON에서는 각 리스트에 레코드가 하나만 있지만, 전체 데이터셋에는 이 리스트에 수십 혹은 수백 개읠 ㅔ코드가 들어 있다. 다만 "conferences"에는 레코드가 하나만 들어 있다. 이 네 개의 리스트에 들어 있는 모든 항목은 "serial" 필드를 가지고 있는데, 이 필드는 리스트 안에서 고유한 식별자로 사용된다.

OSCON 피드를 처리하는 첫 번째 스크립트에서는, 지역에 사본이 있는지 검사하여 없는 경우에만 피드를 내려받음으로써 불필요한 네트워크 트래픽을 발생시키지 않는다. OSCON 2014는 이미 예전에 진행된 콘퍼런스라서 더 이상 갱신된 내용이 없으므로, 이렇게 하는 것이 타당하다.

아래 예제에서는 메타프로그래밍을 볼 수 없다. 거의 모든 표현식이 결국은 json.load(fp)형태가 되지만, 데이터셋을 둘러보기에는 이 정도면 충분하다. osconfeed.load() 함수는 뒤에 나오는 여러 예제에서 사용한다.

- [osconfeed.py](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-1/osconfeed.py)
1. 새로 내려받아야 하는 경우에는 경고 메시지를 출력한다.
2. 두 개의 콘텍스트 관리자(파이썬 2.7과 3.1 이후 허용됨)를 이용해서 원격 파일을 읽고 저장하는 with 문
3. json.load() 함수는 JSON 파일을 파싱하고 네이티브 파이썬 객체로 반환한다. 이 피드에는 dict,list,str,int 형의 데이터가 있다.

위 osconfeed.py를 이용해서 데이터에 들어 있는 어떠한 필드도 조사할 수 있다. 아래 예제를 보자.
```
# osconfeed.py: 예제19-2에 대한 doctest
feed = load()  # <1>
sorted(feed['Schedule'].keys())  # <2>
# ['conferences', 'events', 'speakers', 'venues']
for key, value in sorted(feed['Schedule'].items()):
    print('{:3} {}'.format(len(value), key))  # <3>


"""
    1 conferences
484 events
357 speakers
    53 venues
"""
feed['Schedule']['speakers'][-1]['name']  # <4>
# 'Carina C. Zona'
feed['Schedule']['speakers'][-1]['serial']  # <5>
# 141590
feed['Schedule']['events'][40]['name']
# 'There *Will* Be Bugs'
feed['Schedule']['events'][40]['speakers']  # <6>
# [3471, 5199]
```
1. feed는 내포된 dict 및 문자열과 정수값이 들어 있는 리스트를 가진 딕셔너리 객체다.
2. 'Schedule' 안에 있는 네 개의 레코드 컬렉션을 나열한다.
3. 각 컬렉션 안에 있는 레코드 수를 출력한다.
4. 내포된 딕셔너리와 리스트를 조사해서 마지막 발표자의 이름을 가져온다.
5. 마지막 발표자의 일련번호를 가져온다.
6. 각 이벤트에는 0개 이상의 발표자 일련번호가 들어 있는 'speakers' 리스트가 있다.

## 동적 속성을 이용해서 JSON과 유사한 데이터 둘러보기
위 소스코드는 아주 간단하지만, feed['Schedule']['events'][40]['name']과 같은 구문은 번거롭다. 자바스크립트에서는 feed.Schedule.events[40].name과 같은 구문으로 동일한 값을 가져올 수 있다. 파이썬에서는 이와 비슷하게 작동하는 사용자 정의 dict 클래스를 쉽게 구현할 수 있으며, 구현된 클래스는 웹에서도 많이 볼 수 있다. 필자는 FronzenJSON을 직접 구현했는데, 읽기 연산만 지원하므로 다른 코드보다 간단하다. 지금은 데이터 조회만 하므로 이 정도면 충분하다. 그러나 이 코드는 재귀적으로 호출되므로 내포된 매핑과 리스트를 자동으로 처리한다.

아래 예제는 FrozenJSON의 사용 예를 보여주며, 소스 코드는 [예제 19-5]에 있다.

```
# 예제 19-5 의 FrozenJSON은 name 등의 속성을 읽거나 kyes()와 items()등의 메서드를 호출할 수 있게 해준다.
from osconfeed import load
raw_feed = load()
feed = FronzenJSON(raw_feed) #1
len(feed.Schedule.speakers) #2
# 357
sorted(feed.Schedule.keys()) #3
# ['conferences', 'events', 'speakers', 'venues']
for key, value in sorted(feed.Schedule.items()): #4
    print('{:3} {}'.format(len(value), key))

"""
  1 conferences
484 events
357 speakers
 53 venues
"""
feed.Schedule.speakers[-1].name #5
# 'Carina C. Zona'
talk = feed.Schedule.events[40]
type(talk) #6
# <class 'explore0.FrozenJSON'>
talk.name
# "There *Will* Be Bugs'
talk.speakers #7
# [3471, 5199]
talk.flavor #8
"""
Traceback (most recent call last):
 ...
KeyError: 'flavor'
"""
```
1. 내포된 딕셔너리와 리스트로 구성된 raw_feed로부터 FrozenJSON 객체를 생성한다.
2. FrozenJSON을 사용하면 점 표기법을 이용해서 내포된 딕셔너리를 순회할 수 있다. 여기서는 발표자 list의 길이를 보여준다.
3. key() 등 내포된 딕셔너리의 메서드에도 접근해서 레코드 컬렉션명을 가져올 수 있다.
4. imtes()를 이용해서 컬렉션명 및 그 안에 들어 있는 내용을 가져와서 각 항목의 길이를 출력할 수 있다.
5. feed.Schedule.speakers와 같은 list는 그대로 list로 남지만, 내부 항목 중 매핑형은 FrozenJSON으로 변환된다.
6. events 리스트에서 40번 항목은 JSON 객체였지만, 이제는 FrozenJSON 객체가 되었다.
7. 이벤트 레코드에는 발표자의 일련번호가 들어 있는 speakers 리스트가 있다.
8. 없는 속성을 읽으려 시도하면 일반적으로 발생하는 AttributeError 대신 KeyError 예외가 발생한다.

FronzenJSON 클래스의 핵심은 __getattr__() 메서드다. 이 메서드는 10.5절 'Vector 버전#3: 동적 속성 접근'에서 v.x, v.y, v.z와 같이 문자를 이용해서 벡터 요소를 가져오기 위해 이미 사용해봤다. __getattr__() 특별 메서드는 속성을 가져오기 위한 일반적인 과정이 실패할때(즉, 지명한 속성을 객체, 클래스, 슈퍼클래스에서 찾을 수 없을 때)만 인터프리터에서 호출한다는 점에 유의하라

위 소스코드의 마지막 행은 구현에 관련된 작은 문제를 보여준다. 이상적으로는 없는 속성을 읽을 때 AttributeError 예외가 발생해야 한다. 사실 예외 처리를 구현했었지만, 예외를 처리하느라 __getattr__() 코드가 두 배로 커지면서 보여주고자 하는 핵심 논리가 잘 드러나지 않았기 때문에, 여기서는 예외 처리 코드를 제거했다.

아래 예제 explore0.py에서 보여주는 것처럼 FrozenJSON 클래스에는 __init__(), __getattr__() 메서드와 __data 객체 속성만 있으므로, 다른 이름으로 속성을 접근할 때는 __getattr__() 메서드가 호출된다. __getattr__()은 먼저 self.__data 딕셔너리에 그 이름의 속성(키가 아니다!)이 있는지 살펴본다. 이때 FrozenJSON 객체는 self.__data.items() 등에 위임해서 items() 등의 딕셔너리 메서드를 처리할 수 있게 해준다. self.__data에 해당 이름의 속성이 없으면, __getattr__()은 해당 이름을 키로 사용하여 self.__data에 해당 이름을 키로 사용하여 self.__data에서 항목을 가져와서 FrozenJSON.build()에 전달한다. 각각의 내포된 데이터 구조체를 build() 클래스 메서드를 이용해서 내포된 FrozenJSON 객체로 변환하면서 JSON 데이터에 내포된 구조체를 순회할 수 있다.

- [explore0.py](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-1/explore0.py)
1. mapping 인수로부터 딕셔너리를 생성한다. 이렇게 함으로써 딕셔너리 메서드를 사용할 수 있고, 원본을 변경하지 않는다.
2. name 속성이 없을 때만 __getattr__() 메서드가 호출된다.
3. __data에 들어 있는 객체가 name 속성을 가지고 있으면 그 속성을 반환한다. 이 방식은 keys() 메서드가 처리하는 방식과 동일하다.
4. 그렇지 않으면 self.__data에 name을 키로 사용해서 항목을 가져오고, 가져온 항목에 FrozenJSON.build()를 호출한 결과를 반환한다.
5. 대안 생성자로서, 일반적으로 @classmethod 데커레이터가 사용된다.
6. obj가 매핑형이면, 이 객체로부터 FrozenJSON 객체를 생성한다.
7. 그렇지 않고 obj가 MutableSequence 형이면, 이는 리스트이므로 obj 안에 있는 모든 항목에 build()메서드를 적용해서 생성된 객체들의 리스트를 반환한다.
8. obj가 매핑도 아니고 리스트도 아니면, 항목을 그대로 반환한다.

원래 피드를 보관하거나 변환하지 않음에 주의하라. 피드를 순회하면서 내포된 데이터 구조체들이 계속해서 FrozenJSON으로 변환된다. 그러나 이 정도 크기의 데이터셋에서 데이터를 순회만 하는 코드에서는 이 변환 작업이 큰 문제가 되지 않는다.

임의의 데이터 원천에서 동적 속성명을 생성하거나 흉내 내는 프로그램에서는 원래 데이터에 들어 있는 키를 속성명으로 사용할 수 없는 경우를 처리해야 한다. 다음 절에서는 이 문제를 다룬다.

## 잘못된 속성명 문제
FrozenJSON 클래스는 한계가 있다. 파이썬 키워드가 속성명으로 사용된 경우를 처리하지 못한다. 예를 들어 다음과 같은 객체를 만드는 경우를 생각해보자.
```
grad = FrozenJSON({'name': 'Jim Bo', 'class': 1982})
```
class는 파이썬에 예약된 키워드이므로 grad.class 속성을 읽을 수 없다.
```
grad.class
"""
File "<stdin>", line 1
    grad.class
             ^
SyntaxError: invalid syntax
"""
```
그렇지만 다음 방법으로 읽을 수 있다.
```
getattr(grad, 'class')
#1982
```

그러나 FrozenJSON은 데이터에 편리하게 접근하기 위해 만든 것이므로 FrozenJSON.__init__()에 전달된 매핑 안의 키가 파이썬 키워드인지 검사하고, 파이썬 키워드인 경우에는 뒤에 _를 붙여 속성을 다음과 같은 방법으로 읽을 수 있게 만드는 것이 좋다.
```
grad.class_
# 1982
```

아래 예제는 위 explore0.py의 한 줄짜리 __init__() 메서드를 변경해서 키워드와 같은 속성명에 언더바를 붙인다.

- [explore1.py](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-1/explore1.py)
1. keyword.iskeyword() 함수가 바로 우리에게 필요한 함수다. 이 함수를 사용하려면 keyword 모듈을 임포트해야 하는데, 이 코드에는 나타나 있지 않다.

다음 실행 예에서 보는 것처럼 JSON에서 사용된 키가 올바른 파이썬 식별자가 아닐 때도 비슷한 문제가 발생한다.
```
x = FrozenJSON({'2be':'or not'})
x.2be
"""
File "<stdin>", line 1
 x.2be
  ^
SyntaxError: invalid syntax
```

파이썬 3의 str 클래스에서는 s가 정당한 파이썬 식별자인지 판단하는 s.isidentifier() 메서드를 제공하므로, 이렇게 문제를 야기하는 키를 쉽게 탐지할 수 있다. 그렇지만 정당한 식별자가 아닌 문자열을 정당한 속성명으로 바꾸는 것은 간단하지 않다. 예외를 발생시키는 방법이나 부적절한 키를 attr_0, attr_1 등의 일반적인 이름으로 바꾸는 두 가지 방법을 생각해볼 수 있지만, 여기서는 코드를 단순하게 만들기 위해 문제에 대해서는 신경 쓰지 않는다.

동적 속성명에 대해 생각해보았으니, 이제 FrozenJSON의 또 다른 중요한 특징인 접근하는속성값에 따라 다양한 유형의 객체를 FrozenJSON 객체 혹은 FrozenJSON 객체의 리스트로 변환해서 반환하기 위해 __getattr__() 메서드가 사용하는 build() 클래스 메서드의 논리에 대해 알아보자.

클래스 메서드 대신, 다음 절에서 설명하는 것처럼 __new__() 특별 메서드를 이용해서 동일한 논리를 구현할 수 있다.

## __new__()를 이용한 융통성 있는 객체 생성
흔히 __init__() 메서드를 생성자 메서드라고도 부르지만, 생성자라는 말은 다른 언어에서 빌려온 용어일 뿐이다. 실제로 객체를 생성하는 특별 메서드는 __new__()다. 이 메서드는 클래스 메서드로서 (그러나 특별 대우를 받으므로 @classmethod 데커레이터를 사용하지 않는다) 반드시 객체를 반환한다. 그러고 나서 그 객체가 __init__() 메서드의 첫 번째 인수 self로 전달된다. __init__()은 호출될 때 객체를 받으며 아무 것도 반환할 수 없으므로, 실제로 __init__()은 '초기화 메서드'일 뿐이다. 실제 생성자인 __new__() 메서드는 object 클래스에서 상속받은 메서드로도 충분하므로 직접 구현할 일은 거의 없다.

방금 설명한 __new__()에서 __init__()으로의 경로는 가장 일반적인 경로지만, 이 경로만 있는 것은 아니다. __new__() 메서드는 다른 클래스의 객체도 반환할 수 있는데, 이 경우에는 파이썬 인터프리터가 __init__()을 호출하지 않는다.

즉, 파이썬에서 객체를 생성하는 과정은 다음 의사코드로 요약할 수 있다.
```
# 객체를 생성하는 의사코드
def object_maker(the_class, some_arg):
    new_object = the_class.__new__(some_arg)

    if isinstance(new_obejct, the_class):
        the_class.__init__(new_object, some_arg)
    return new_object
# 다음 두 문장은 거의 동일하다.
x = Foo('bar')
x = object_maker(Foo, 'bar')
```

아래 explore2.py는 이전에 build() 클래스에서 처리하던 논리를 __new__() 메서드로 옮긴 새로운 버전의 FrozenJSON 클래스를 보여준다.

- [explore2.py](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-1/explore2.py)
1. 클래스 메서드로서 __new__()가 첫 번째로 받는 인수는 클래스 자신이다. 그리고 나머지 인수는 __init__()이 받는 인수와 동일하다. __init__()이 받는 첫 번째 인수는 self다.
2. 기본적으로 슈퍼클래스의 __new__() 메서드에 위임한다. 이 경우 FrozenJSON을 유일한 인수로 전달해서 object 클래스의 __new__() 메서드를 호출한다.
3. __new__() 메서드의 나머지 코드는 기존 build() 메서드와 완전히 동일하다.
4. 여기서 기존 코드는 FrozenJSON.build() 메서드를 호출했지만, 이제는 단지 FrozenJSON() 생성자를 호출한다.

__new__() 메서드는 일반적으로 해당 클래스의 객체를 생성하므로 클래스를 첫 번째 인수로 받는다. 따라서 FrozenJSON.__New__() 안에서 super().__new__(cls)는 object.__new__(FrozenJSON) 을 호출하는 셈이 되어 object 클래스가 실제로는 FrozenJSON 객체를 생성한다. 즉, 실제로는 파이썬 인터프리터 내부에서 C 언어로 구현된 object.__new__()가 객체를 생성하지만, 생성된 객체의 __class__ 속성은 FrozenJSON을 가리키게 된다.

OSCON JSON 피드를 구조화한 방식에는 명백한 단점이 있다. 'There *Will* Be Bugs'라는 제목이 붙은 인덱스 40번에 있는 이벤트는 3471과 5199, 두 명의 발표자가 있지만, 이 발표자들을 찾아내기 쉽지 않다. 이 숫자들은 일련번호지만, Schedule.speakers 리스트가 일련번호로 인덱싱되어 있지 않기 때문이다. 모든 event 레코드에 존재하는 venue 필드 역시 일련번호로 인덱싱되어 있지 않기 때문이다. 모든 event 레코드에 존재하는 venue 필드 역시 일련번호를 가지고 있지만, 해당 venue 레코드를 찾으려면 Schedule.venues 리스트를 순차적으로 검색해야 한다. 다음으로 할 일은 데이터를 다시 구조화해서 연결된 레코드의 판도을 자동화하는 것이다.

## shelve를 이용해서 OSCON 피드 구조 변경하기

파이썬 객체 직렬화 포맷이자 객체를 이 포맷으로/으로부터 변환하는 모듈의 이름이 pickle인 것을 알고 있으면, 표준 shelve 모듈의 우스꽝스러운 이름이 이해가 될 것이다. 오이절임은 선반에 보관하므로 shelve가 pickle을 조관하는 게 쉽게 이해될 것이다.

shelve.open() 고위 함수는 shelve.Shelf 객체를 반환한다. shelve.Shelf는 dbm 모듈을 이용해서 키-값 객체를 보관하는 단순한 객체로서, 다음과 같은 특징이 있다.
* shelve.Shelf는 abc.MutableMapping 클래스를 상속하므로, 매핑형이 제공하는 핵심 메서드들을 제공한다.
* sh elve.Shelf는 sync(), close() 등의 입출력을 관리하는 메서드도 제공한다. shelve.Shelf는 콘텍스트 관리자이기도 하다.
* 새로운 값이 키에 할당될 때마다 키와 값이 저장된다.
* 키는 반드시 문자열이어야 한다.
* 값은 반드시 pickle 모듈이 처리할 수 있는 객체여야 한다.

자세한 내용과 주의할 점은 각각 shelve 모듈 (https://docs.python.org/3/library/shelve.html) , dbm 모듈 (https://docs.python.org/3/library/dbm.html) 에 대한 문서를 참조하라. 지금 우리에게 중요한 점은 OSCON 스케줄 데이터를 재구성할 수 있는 간단하고 효율적인 방법을 shelve가 제공한다는 것이다. 우리는 JSON파일에서 레코드를 모두 읽어 shelve.Shelf에 저장할 것이다. 각 키는 'event.33950'이나 'speaker.3471'처럼 레코드 유형과 일련번호를 만들며, 값을 이제 설명할 새로 만든 Record 클래스 객체가 된다.

아래 예제는 shelve를 사용하는 schedule1.py 스크립트의 doctest를 보여준다. 대화식으로 테스트해보려면 python -i schedule1.py 명령을 실행해서 모듈을 로딩하면 콘솔 프롬프트를 볼 수 있다. load_db() 함수가 중책을 맡고 있다. 이 함수는 [osconfeed.py](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-1/osconfeed.py)의 osconffeed.load()를 호출해서 JSON 데이터를 읽고 각 레코드를 Shelf 객체 안에 있는 Record 객체로 저장해서 db로 전달한다. 이 작업을 수행한 후에는 speaker = db['speaker.3471']과 같이 간단하게 발표자 레코드를 가져올 수 있다.

```
# 예제 19-9의 schedule1.py가 제공하는 기능 시험
import shelve
db = shelve.open(DB_NAME) #1
if CONFERENCE not in db: #2
    load_db(db) #3

speaker = db['speaker.3471'] #4
type(speaker) #5
# <class 'schedule1.Record'>
speaker.name, speaker.twitter #6
# ('Anna Martelli Ravenscroft', 'annaraven')
# db.close()
```
1. shelve.open()은 기존 데이터베이스 파일을 열거나 새로 만든다.
2. 데이터베이스에 데이터가 들어 있는지 간단히 확인하려면, 알려진 키로 검색한다. 이 데이터베이스의 경우 단 하나 있는 conference 레코드의 키인 'conference.115'로 확인할 수 있다.
3. 데이터베이스가 비어 있으면 load_db(db)를 호출해서 데이터베이스를 로딩한다.
4. speaker 레코드를 가져온다.
5. 아래schedule1.py에서 정의한 Record 클래스의 객체를 반환한다.
6. 각각의 Record 객체는 하위 JSON 레코드의 필드를 반영한 속성을 구현한다.
7. shelve.Shelf를 사용한 후에는 반드시 닫아야 한다. 가능하면 with 블록을 이용해서 닫는 연산이 보장되도록 하는 것이 좋다.

schedule1.py 코드는 아래와 같다.

- [schedule1.py](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-1/schedule1.py)
1. osconfeed.py 모듈을 로드한다.
2. 키워드 인수로부터 생성된 속성으로 객체를 생성할 때 간편히 사용하는 방법이다(잠시 후에 자세히 설명한다).
3. 이 함수는 디스크에 사본이 없는 경우 웹에서 JSON 피드를 가져올 수도 있다.
4. 'conferences', 'events'등 컬렉션을 반복한다.
5. 컬렉션명에서 마지막의 's'를 제거해서 record_type으로 설정한다(예를 들어 'events'는 'event'가된다).
6. record_type과 'serial' 필드로부터 key를 생성한다.
7. 'serial' 필드를 새로 생성한 key로 설정한다.
8. Record 객체를 생성하고, 해당 key로 데이터베이스에 저장한다.

Record.__init__() 메서드는 널리 사용되는 파이썬 꼼수를 보여준다. 9.8절 '__slots__ 클래스 속성으로 공간 절약하기'에서 설명한 것처럼 __slots__ 속성이 클래스에 선언되어 있지 않은 한, 객체의 __dict__에 속성들이 들어 있다. 따라서 객체의 __dict__를 직접 매핑형으로 설정하면, 그 객체의 속성묶음을 빠르게 정의할 수 있다.
> 19.1.2절 '잘못된 속성명 문제'에서 자세히 설명했던 내용을 다시 반복하지는 않겠지만, 애플리케이션 상황에 따라 Record 클래스는 속성명으로 사용할 수 없는 키를 처리해야 한다.

예제 schedule1.py에서 정의한 Record 클래스는 아주 간단하므로, 왜 이전에는 복잡한 FrozenJSON 클래스 대신 이렇게 간단한 방법을 사용하지 않았을까 하는 의문이 들지도 모른다. 여기에는 두가지 이유가 있다. 첫째, FrozenJSON은 내포된 매핑과 리스트를 재귀적으로 변환하면서 작동한다. 우리가 변환한 데이터셋에서는 매핑이나 리스트 안에 매핑이 내포되어 들어가지 않으므로 Record는 이런 기능이 필요 없다. 레코드에너느 문자열, 정수, 문자열의 리스트, 정수의 리스트만 들어 있다. 둘째, FrozenJSON은 keys()와 같은 호출하기 위해 사용했던 __data 딕셔너리 속성에 접근할 수 있게 해주지만, 지금은 그런 기능이 필요하지 않다.
> 파이썬 표준 라이브러리는 우리가 구현한 Record와 비슷한 클래스를 최소 두 개 이상 제공한다. 이 클래스들은 생성자에 전달된 키워드 인수로부터 일련의 속성을 무작위로 가질 수 있으며, multiprocessing.Namespace 클래스 (문서는 http://bit.ly/1cPLZzd , 소스 코드는 http://bit.ly/1cPM2uJ )와 argparse.Namespace 클래스 (문서는 http://bit.ly/1cPM1qG, 소스 코드는 http://bit.ly/1cPM4Ti )등이 있다. __dict__를 갱신하는 __init__() 개념의 본질을 보여주기 위해 여기서는 Record 클래스를 직접 구현했다.

지금까지 스케줄 데이터셋의 구조를 변경하는 작업을 완료했으니, 이제 event 레코드에서 참조하는 venue와 speaker 레코드를 자동으로 가져오도록 Record 클래스를 확장해보자. 이 방법은 models.Foreignkey 필드에 접근할 때 장고 ORM이 수행하는 것과 비슷하다. 다만 키 대신 연결된 모델 객체를 가져오는 점이 다르다. 다음 절에서는 프로퍼티를 이용해서 연결된 객체를 가져온다.

## 프로퍼티를 이용해서 연결된 레코드 읽기

shelf에서 가져온 event 레코드의 venue나 speakers 속성을 읽을 때 일련번호 대신 온전한 레코드 객체를 반환하는 것이 이번 버전의 목표다. 아래 schedule2.py은 일부 사용 예를 보여준다.

```
    >>> DbRecord.set_db(db)  # <1>
    >>> event = DbRecord.fetch('event.33950')  # <2>
    >>> event  # <3>
    <Event 'There *Will* Be Bugs'>
    >>> event.venue  # <4>
    <DbRecord serial='venue.1449'>
    >>> event.venue.name  # <5>
    'Portland 251'
    >>> for spkr in event.speakers:  # <6>
    ...     print('{0.serial}: {0.name}'.format(spkr))
    ...
    speaker.3471: Anna Martelli Ravenscroft
    speaker.5199: Alex Martelli
```
1. DbRecord는 Record를 상속해서 데이터베이스를 지원한다. 사용하려면 DbRecord에 데이터베이스에 대한 참조를 전달해야 한다.
2. DbRecord.fetch() 클래스 메서드는 어떠한 종류의 레코드도 가져온다.
3. event는 DbRecord 클래스를 상속한 Event 클래스 객체다.
4. event.venue에 접근하면 Dbrecord 객체가 반환한다.
5. 이제 eventvenue의 이름을 알아내는 것은 아주 쉽다. 이렇게 자동으로 참조소환하는 것이 이예제의 목표다.
6. 그리고 event.speakers 리스트를 반복해서, 각 발표자를 나타내는 DbRecord 객체들도 가져올 수 있다.

아래 그림은 이 절에서 공부할 클래스들을 간략히 보여준다.

![record_uml.png](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-1/record_uml.png)

---

**Record 클래스**</br>
__init__() 메서드는 예제19-9의 schedule1.py와 동일하다. 쉽게 비교할 수 있도록 __eq__()메서드를 추가했다.

**DbRecord 클래스**</br>
Record의 서브클래스. __db 클래스 속성, 속성을 설정하고 가져오는 set_db()와 get_db() 정적 메서드, 데이터베이스에서 레코드를 가져오는 fetch() 클래스 메서드, 디버깅과 테스트를 지원하기 위한 __repr__() 객체 메서드가 추가되었다.

**Event 클래스**</br>
DbRecord의 서브클래스. 연곂된 레코드를 가져오기 위한 venue와 speakers 프로퍼티, 특별 메서드 __repr__()이 추가되었다.

---

DbRecord.__db 클래스 속성은 열려진 shelve.Shelf 데이터베이스에 대한 참조를 보고나하므로, 그것에 의존하는 DbRecord.fetch() 메서드와 Event.venue 및 Event.speakers 프로퍼티에 의해 사용될 수 있다. 실수로 값이 변경되지 않도록, 전통적인 게터와 세터 메서드를 가진 비공개 클래스 속성으로 __db를 구현했다. 프로퍼티는 객체 속성을 관리하기 위해 만들어진 클래스 속성이라는 점을 염두에 두었기에 _-db를 관리하는 프로퍼티는 사용하지 않았다.

이 절에서 설명하는 내용은 내려받은 코드 중 schedule2.py 모듈에 들어 있다. 이 모듈의 소스코드는 100줄이 넘으므로, 부분별로 나눠서 설명한다.

schedule2.py의 첫 번째 부분은 아래소스코드와 같다.

```
import warnings
import inspect  # <1>

import osconfeed

DB_NAME = 'data/schedule2_db'  # <2>
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):  # <3>
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented
```
1. load_db() 함수 (예제 19-14)에서 inspect모듈을 사용한다.
2. 다른 클래스의 객체를 저장하므로 [예제 schedule1.py]에서 사용한 'schedule_db'가 아니라 'schedule2_db'데이터베이스 파일을 생성해서 사용한다.
3. __eq__() 메서드는 비교하는 데 유용하게 사용된다.

> 파이썬 2에서는 '새로운 스타일'의 클래스만 프로퍼티를 지원한다. 파이썬 2에서 새로운 스타일의 클래스를 정의하려면 object 클래스를 직간접적으로 상속해야 한다. 예제schedule2.py의 Record는 프로퍼티를 사용할 계층 구조에서의 베이스 클래스이므로, 파이썬 2에서는 다음과 같이 클래스를 정의해야 한다.</br> class Record(object):</br>    # 기타...

다음으로 schedule2.py에서 사용자 정의 예외 클래스와 DbRecord 클래스를 정의한다 (아래 예제)

```
# schedule2.py의 MissingDatabaseError와 DbRecord 클래스
class MissingDatabaseError(RuntimeError):
    """Raised when a database is required but was not set."""  # <1>


class DbRecord(Record):  # <2>

    __db = None  # <3>

    @staticmethod  # <4>
    def set_db(db):
        DbRecord.__db = db  # <5>

    @staticmethod  # <6>
    def get_db():
        return DbRecord.__db

    @classmethod  # <7>
    def fetch(cls, ident):
        db = cls.get_db()
        try:
            return db[ident]  # <8>
        except TypeError:
            if db is None:  # <9>
                msg = "database not set; call '{}.set_db(my_db)'"
                raise MissingDatabaseError(msg.format(cls.__name__))
            else:  # <10>
                raise

    def __repr__(self):
        if hasattr(self, 'serial'):  # <11>
            cls_name = self.__class__.__name__
            return '<{} serial={!r}>'.format(cls_name, self.serial)
        else:
            return super().__repr__()  # <12>
```
1. 일반적으로 사용자 정의 예외는 표시 클래스로서, 본체가 없다. 문서화 문자열을 이용해서 예외의 사용법을 설명하는 것이 단순히 pass 문으로 표시하는 것보다 낫다.
2. DbRecord는 Record를 상속한다.
3. __db 클래스 속성은 열린 shelve.Shelf 데이터베이스에 대한 참조를 보관한다.
4. set_db()는 정적 메서드로서, 호출 방법에 무관하게 언제나 동일한 결과가 나옴을 명시한다.
5. 이 메서드를 Event.set_db(my_db)로 호출하더라도, DbRecord 클래스에 __db 속성이 설정된다.
6. get_db()도 정적 메서드로서, 호출 방법에 무관하게 언제나 DbRecord.__db가 참조하는 객체를 반환한다.
7. fetch()는 클래스 메서드로서, 호출 방법에 무관하게 언제나 DbRecord.__db가 참조하는 객체를 반환한다.
8. 데이터베이스에서 ident 키를 가진 레코드를 가져온다.
9. TypeError가 발생하고 db가 None이면, 사용자 정의 예외를 발생시켜 데이터베이스를 반드시 설정해야함을 알려준다.
10. 나머지 예외는 여기에서 처리할 수 없으므로, 다시 발생시킨다.
11. 레코드에 'serial' 속성이 있으면 문자열 표현 안에 사용한다.
12. 'serial' 속성이 없으면 슈퍼클래스의 __repr__() 메서드를 사용한다.

이제 이 예제의 중심인 Event 클래스를 살펴보자

```
# schedule2.py의 event 클래스
class Event(DbRecord):  # <1>

    @property
    def venue(self):
        key = 'venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key)  # <2>

    @property
    def speakers(self):
        if not hasattr(self, '_speaker_objs'):  # <3>
            spkr_serials = self.__dict__['speakers']  # <4>
            fetch = self.__class__.fetch  # <5>
            self._speaker_objs = [fetch('speaker.{}'.format(key))
                                  for key in spkr_serials]  # <6>
        return self._speaker_objs  # <7>

    def __repr__(self):
        if hasattr(self, 'name'):  # <8>
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)
        else:
            return super().__repr__()  # <9>
```
1. Event는 DbRecord 클래스를 상속한다.
2. venue 프로퍼티는 venue_serial 속성으로부터 key를 생성하고, DbRecord에서 상속한 fetch()클래스 메서드에 전달한다(DbRecord는 잠시 후에 설명한다).
3. speakers 프로퍼티는 레코드에 _speaker_objs 속성이 있는지 검사한다.
4. 속성이 없으면 무한 재귀호출을 방지하기 위해 __dict__객체에서 'speakers' 속성을 바로 가져온다. 이 속성명도 speakers이기 때문이다.
5. fetch() 클래스 메서드에 대한 참조를 가져온다(이렇게 하는 이유도 잠시 후에 설명한다).
6. fetch()를 이용해서 speaker 레코드들의 리스트로 self._speaker_objs를 설정한다.
7. 이 리스트를 반환한다.
8. 레코드에 'name' 속성이 있으면, 이 속성을 이용해서 문자열로 표현한다.
9. 그렇지 않으면 슈퍼클래스의 __repr__() 메서드를 호출한다.

위 Event 클래스에서의 venue 프로퍼티의 마지막 행에서 self._class__.fetch(key)를 반환한다. 이것을 간단히 self.fetch(key)로 쓰지 않는 이유는 무엇일까? OSCON 피드 데이터셋의 경우에는 'fetch'라는 키를 가진 이벤트 레코드가 없으므로, 간단히 self.fetch(key)로 쓸 수 있다. 그렇지만 'fetch'라는 키를 가진 이벤트 레코드가 하나라도 있으면 그 Event 객체에서 메서드를 사용하지 않는다. 이것은 미묘한 버그로서, 테스트 단계에서 운 좋게 통과한 후 실제 사용시 'fetch' 필드를 가진 venue나 speaker 레코드에 연결된 Event 객체를 가져올 때 문제가 발생할 수 있다.
> 데이터를 가져와서 객체 속석명을 생성할 때는, 클래스 속성이나 메서드를 가려서 버그가 발생하거나 기존 객체 속성을 실수로 덮어써서 데이터를 잃어버릴 위험이 언제나 있다. 애초에 파이썬 딕셔너리와 자바스크립트 객체가 다르다고 하는 이유는 아마도 이런 주의 사항 때문일 것이다.

Record 클래스가 매핑과 비슷하게 작동된다면 __getattr__() 대신 __getitem__()을 구현해서 속성을 가리거나 덮어쓸 버그 위험을 피할 수 있다. 사용자 정의 매핑이 Record를 구현하는 파이썬스러운 방법일 수도 있지만, 그 방법을 택했다면 동적 속성 프로그래밍 기법의 위험성을 생각해볼 기회가 없었을 것이다.

이 예제의 마지막 부분은 수정된 load_db() 함수다.
```
# schedule2.py의 load_db함수
def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        record_type = collection[:-1]  # <1>
        cls_name = record_type.capitalize()  # <2>
        cls = globals().get(cls_name, DbRecord)  # <3>
        if inspect.isclass(cls) and issubclass(cls, DbRecord):  # <4>
            factory = cls  # <5>
        else:
            factory = DbRecord  # <6>
        for record in rec_list:  # <7>
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = factory(**record)  # <8>
```
1. 여기까지는 schedule1.py에 이쓴ㄴ load_db와 동일 하다.
2. 클래스명으로 사용하기 위해 record_type의 첫 글자를 대문자로 만든다(예를 들어 'event'는 'Event'가 된다).
3. 모듈의 전역 범위에서 그 클래스명의 객체를 가져온다. 그런 이름의 객체가 없다면 DbRecord를 가져온다.
4. 가져온 객체가 클래스고, 그 클래스가 DbRecord의 서브클래스인지 검사한다.
5. 그렇다면 factory를 그 클래스에 바인딩한다. 그러면 factory는 record_type에 따라 DbRecord의 서브클래스가 될 수도 있다.
6. 그렇지 않으면 factory를 DbRecord에 바인딩한다.
7. 이 for 루프는 이전과 동일하게 keyf를 생성하고 그 이름으로 레코드를 저장한다.
8. 다만 데이터베이스에 저장할 객체는 factory로 생성되며, factory는 record_type에 따라 DbRecord이거나 DbRecord의 서브클래스다.

사용자 정의 클래스가 있는 record_type만 Event 지만, Speaker나 Veneue라는 클래스를 구현했다면, load_db()는 레코드를 만들어서 저장할 때 DbRecord 클래스 대신 구현된 클래스를 자동으로 사용하므로 주의해야 한다.

지금까지 __getattr__(), hasattr(), getattr(), @property, __dict__등의 기본적인 도구를 이용해서 동적 속성을 구현하는 다양한 기법을 보여주는 예제들을 살펴보았다.

프로퍼티는 공개 속성을 클라이언트 코드에 영향을 끼치지 않으면서 게터와 세터로 관리하는 속성으로 변경함으로써 비지니스 논리를 적용하기 위해 종종 사용된다. 다음 절에서 자세히 알아보자.

<!-- - [schedule2.py](https://github.com/hyeonDD/fluent_python/blob/master/Part19/ex19-1/schedule2.py) -->
