# 유니코드 텍스트 정렬하기
<!-- 
[예](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-1/encode_decode.py)
 -->
파이썬은 각 시퀀스 안에 들어 있는 항목들을 하나하나 비교함으로써 어떠한 자료형의 시퀀스도 정렬할 수 있다. 문자열의 경우에는 각 단어의 코드 포인트를 비교한다. 불행히도 이런 방식은 비아스키 문자를 사용하는 경우 부적절한 결과가 발생할 수 있다. 브라질에서 재배하는 과일 목록을 정렬해보자.
```
fruits = ['caju', 'atemoia', 'cajá', 'acaí','acerola']
sorted(fruits)
```
정렬 규칙은 현지 언어에 따라 달라진다. 그렇지만 포르투갈어 등 라틴 알파벳을 사용하는 언어에서는 정렬할 때 악센트와 갈고리형 기호가 거의 영향을 미치지 않는다. 따라서'cajá'는 'caja'로 처리해서 'caju보다 먼저 나와야 한다.

정렬된 fruits 리스트는 다음과 같아야한다.

***
['acaí', 'acerola', 'atemoia', 'cajá','caju']
***
파이썬에서 비아스키 텍스트는 locale.strxfrm()함수를 이용해서 변환하는 것이 표준이다.
locale 모듈 문서 (http://bit.ly/1IqyCRf)에 따르면 strxfrm()함수는 문자열을 현지어 비교에 사용할 수 있는 문자열로 변환한다.

locale.strxfrm()함수를 활성화하려면 먼저 애플리케이션에 대해 적절히 현지어를 설정하고, OS가 이 설정을 지원하도록 기도해야 한다. 언어가 pt_BR로 설정된 GUN/리눅스에서 locale.strxfr()함수를 사용한 예는 아래와 같다.

```
import locale
locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')
fruits = ['caju', 'atemoia', 'cajá', 'acaí','acerola']
sorted_fruits = sorted(fruits, key=locale.strxfrm)
sorted_fruits
['acaí', 'acerola', 'atemoia', 'cajá','caju']
```

따라서 정렬할 때는 locale.strxfrm()함수를 키로 사용하기 전에 setlocale(LC_COLLATE, <지역_언어>)를 호출해야 한다.

# 유니코드 대조 알고리즘을 이용한 정렬

장고에 다양한 기여를 하고 있는 제임스 토버도 이 문제를 겪고 유니코드 대조 알고리즘(UCA)을 순수 파이썬으로 구현한 PyUCA(https://pypi.python.org/pypi/pyuca/)를 만들었다.
```
import pyuca
coll = pyuca.Collator()
fruits = ['caju', 'atemoia', 'cajá', 'acaí','acerola']
sorted_fruits = sorted(fruits, key=coll.sort_key)
sorted_fruits
```

사용하기 쉽고 잘 작동한다. 현재는 파이썬 3.x 버전만 지원된다.

PyUCA는 지역 정보를 고려하지 않는다. 정렬 방식을 커스터마이즈하려면 Collator()생성자에 직접 만든 대조 테이블에 대한 경로를 제공하면 된다. 기본적으로는 프로젝트와 함께 제공되는 allkeys.txt(https://github.com/jtauber/pyuca)를 사용한다. 이 키 파일은 유니코드 6.3.0에서 제공하는 기본 유니코드 대조 요소 테이블(http://bit.ly/1IqAk54)의 사본일 뿐이다.

# 유니코드 데이터베이스
유니코드 표준은 수만은 구조화된 텍스트 파일의 형태로 하나의 완전한 데이터베이스를 제공한다.
이 데이터베이스에는 코드 포인트를 문자명으로 매핑하는 테이블뿐만 아니라 각 문자에 대한 메타데이터 및 각 문자의 연관 방법을 담고 있다.
예를 들어 유니코드 데이터베이스는 문자를 출력할 수 있는지, 문자인지, 십진수인지, 혹은 다른 수치형 기호인지 기록한다. str의 isidentifier(), isprintable(), isdecimal(),isnumeric()메서드는 이 데이터베이스를 사용한다. str.casefold()메서드도 유니코드 테이블의 정보를 사용한다.

unicodedata 모듈에는 문자 메타데이터를 반환하는 함수들이 있다. 예를 들어 표준에 정의된 공식 명칭, 결합 문자인지 여부, 사람이 인식하는 기호의 숫자값 등을 반환한다.

- [유니코드 데이터베이스 예](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-7/unicode_database.py)
    1. U+0000 포맷의 코드 포인트
    2. 길이가 6인 str의 중앙에 놓인 문자
    3. r'\d' 정규 표현식과 일치하는 문자의 경우 re_dig 표시
    4. char.isdigit()가 참이면 isdig 표시
    5. char.isnumeric()이 참이면 isnum 표시
    6. 전체 너비는 5칸이며 소수점 2자리까지 포맷한 숫자값
    7. 유니코드 문자명

# 이중 모드 str 및 bytes API

표준 라이브러리에는 str이나 bytes 인수를 모두 받으며, 인수의 자료형에 따라 다르게 작동하는 함수들이 있다. re와 os 모듈이 대표적인 예다.

## 정규 표현식에서의 str과 bytes

bytes로 정규 표현식을 만들면 \d와 \w 같은 패턴은 아스키 문자만 매칭되지만, str로 이 패턴을 만들면 아스키 문자 이외에 유니코드 숫자나 문자도 매칭된다.

- [str과 bytes 정규 표현식 동작 비교](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-7/ramanujan.py)
    1. 앞의 두 정규 표현식은 str형이다.
    2. 마지막의 두 정규표현식은 bytes 형이다.
    3. 타밀 숫자로 1729를 담고 있는 검색할 유니코드 텍스트(논리적으로 닫는 괄호가 나올 때까지 행이 계속된다)
    4. 이 문자열은 컴파일 시 앞 문자열에 연결된다. 파이썬 언어 참조 문서의 2.4.2절 '문자열 리터럴의 연결(http://bit.ly/1lqE2vH)을 참조하라.
    5. bytes 정규 표현식을 검색하려면 bytes 문자열이 필요하다.
    6. str 패턴 r'\d+'는 타밀과 아스키 숫자에 매칭된다.
    7. bytes 패턴 rb '\d+'는 아스키 숫자에만 매칭된다.
    8. str 패턴 r'\w+'는 문자, 위첨자, 타밀, 아스키 숫자에 매칭된다.
    9. bytes 패턴 rb'\w+'는 문자와 숫자에 대한 아스키 바이트에만 매칭된다.

## os 모듈 함수에서 str과 bytes
GNU/리눅스 커널은 유니코드를 모른다. 따라서 실제 OS의 파일명은 어떠한 인코딩 체계에서도 올바르지 않은 바이트 시퀀스로 구성되어 있으며 str로 디코딩할 수 없다.
특히 다양한 운영 체계를 클라이언트로 가지는 파일 서버는 이런 문제가 발생하기 쉽다.
이 문제를 해결하기 위해 파일명이나 경로명을 받는 모든 os 모듈 함수는 str이나 bytes 형의 인수를 받는다. 이런 함수를 str 인수를 받는다. 이런 함수를 str 인수로 호출하면 인수는 sys.getfilesystemencoding()함수에 의해 지정된 코덱을 이용해서 자동으로 변환되고, 운영 체계의 응답은 동일 코덱을 이용해서 디코딩된다. 대부분의 경우 이 방법은 유니코드 샌드위치 모델에 따라 여러분이 원하는 대로 작동한다.

그렇지만 이렇게 처리할 수 없는 파일명을 다루거나 수정해야 할 때는 bytes 인수를 os 함수에 전달해서 bytes 반환값을 가져올 수 있다. 파일명이나 경로명에 얼마나 많은 깨진 문자가 있는지에 상관없이 이 방식을 사용할 수 있다.

***
fsencode(파일명)
'파일명'이 str 형이면 sys.getfilesystemencoding()이 반환한 코덱명을 이용해서 '파일명'을 bytes 형으로 인코딩한다. '파일명'이 bytes 형이면 변환하지 않고 그대로 반환한다.

fsdecode(파일명)
'파일명'이 bytes 형이면 sys.getfilesystemencoding()이 반환한 코덱명을 이용해서 '파일명'을 str 형으로 디코딩한다. '파일명'이 str 형이면 반환하지 않고 그대로 반환한다.
***


