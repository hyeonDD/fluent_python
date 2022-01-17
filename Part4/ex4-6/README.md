# 제대로 비교하기 위해 유니코드 정규화하기

유니코드에는 결합 문자가 있기 때문에 문자열 비교가 간단하지 않다. 앞 문자에 연결되는 발음 구별 기호는 인쇄할 때 앞 문자와 하나로 결합되어 출력된다.
예를들어 'cafe'라는 단어는 네 개나 다섯 개의 코드 포인트를 이용해서 두 가지 방식으로 표현할 수 있지만 결과는 동일하게 나타난다.

- [유니코드 결합 문자 예제](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-6/unicode_normalization.py)
    - 코드 포인트 U+0301́ 은 COMBINING ACUTE ACCENT(급성 억양 결합하기)다. 'e'다음에 이 문자가 오면 'é'를 만든다.

    - 유니코드 표준에서 'é'와 'e\u0301', 이 두개의 시퀀스를 '규범적으로 동일하다'고 하며, 애플리케이션은 이 두 시퀀스를 동일하게 처리해야 한다. 그렇지만 파이썬은 서로 다른 두 개의 코드 포인트 시퀀스를 보고, 이 둘이 서로 동일하지 않다고 판단한다.

    - 이 문제를 해결하려면 unicodedata.normalize() 함수가 제공하는 유니코드 정규화를 이용해야 한다. 이 함수의 첫 번째 인수는 'NFC', "NFD', 'NFKC', 'NFKD'중 하나여야 하는데, 먼저 NFC와 NFD를 알아보자.

    - 정규화 방식 C(Normalization Form C)(NFC)는 코드 포인트를 조합해서 가장 짧은 동일 문자열을 생성하는 반면, NFD는 조합된 문자를 기본 문자와 별도의 결합 문자로 분리한다. 이 두 방식 모두 문자열을 제대로 비교할 수 있게 해준다. [유니코드 결합 문자 정규화](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-6/unicode_normalization2.py)
    키보드는 일반적으로 결합된 문자를 입력할 수 있으므로, 사용자가 입력하는 텍스트는 기본적으로 NFC 형태다. 그러나 안전을 보장하기 위해 파일에 저장하기 전에 normalize('NFC',user_text) 코드로 문자열을 청소하는 것이 좋다. NFC는 '웹을 위한 문자 모델: 문자열 매칭과 검색'에서 W3C가 추천하는 정규화 형식이기도 하다.[W3C링크](http://www.w3.org/TR/charmod-norm/).

    - NFC에 의해 다른 문자 하나로 정규화되는 문자도 있다. 전기 저항을 나타내는 옴(Ω) 기호는 그리스어 대문자 오메가로 정규화된다. 겉모습은 똑같지만 다르다고 판단되므로 정규화해서 뜻하지 않은 문제를 예방해야 한다. [뜻하지 않은 정규화 예방](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-6/unicode_normalization_attention.py)
    
    - 나머지 두 가지 정규화 방식 NFKC와 NFKD에서 K는 호환성을 나타낸다. 이것은 정규화의 더 강력한 형태로서, 소위 말하는 '호환성 문자'에 영향을 미친다. 하나의 문자에 대해 하나의 '규범적인' 코드를 가지는 게 유니코드의 목표 중 하나였지만, 기존 표준과의 호환성을 위해 두 번 이상 나타나는 문자도 있다. 예를 들어 마이크로 기호 'µ' (U+00B5)는 코드 포인트U+03BC (GREEK SMALL LETTER MU)와 같은 문자지만, latin1과의 상호 변환을 지원하기 위해 유니코드에 추가되었다. 따라서 마이크로 기호를 '호환성 문자'라고 할 수 있다.

    - NFKC와 NFKD 방식에서 각 호환성 문자는 포매팅 손실이 발생하더라도 '선호하는'형태의 하나 이상의 문자로 구성된 '호환성 분할'로 치환된다. 이상적으로 포매팅은 외부 표시의 책임이며, 유니코드의 책임은 아니다. 예를 들어
        1. 절반을 나타내는 '½'(U+00B5)는 문자의 호환성 분할은 세 개 문자의 시퀀스인 '1/2'
        2. 마이크로 기호 'µ'(U+00B5)의 호환성 분할은 소문자 뮤인 'μ' (U+03BC)로 치환된다.
    
    - [NFKC 예제](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-6/unicode_normalization_nfkc.py)
        - '1/2'은 '½'에 대한 적절한 치환이며 마이크로 기호는 실제로는 그리스어 소문자 뮤지만, '4<sup>2</sup>'을 '42'로 변환하는 것은 의미를 변화시킨다. 에플리케이션은 '4<sup>2</sup>'로 저장 할 수 있지만, normalize() 함수는 포맷에 대해 전혀 모른다. 따라서 NFKC나 NFKD는 정보를 왜곡할 수 있지만, 검색 및 색인 생성을 위한 편리한 중간 형태를 생성할 수 있다. '1/2인치'를 검색할 때 '½인치'도 찾아낸다면 사용자들이 좋아할 것이다.
        > NFKC와 NFKD 정규화는 검색이나 색인 생성 등의 특별한 경우에는 조심해서 사용해야 하며, 영구 저장할 때는 사용하면 안된다. 이러한 변환은 데이터가 손실될 수 있기 때문이다.
        
        - 검색 및 색인 생성을 위해 텍스트를 준비할 때는 케이스 폴딩이라는 연산도 유용하게 사용된다.

# 케이스 폴딩    
본질적으로 케이스 폴딩(case folding)은 모든 텍스트를 소문자로 변환하는 연산이며, 약간의 변환을 동반한다. 케이스 폴딩은 파이썬 3.3에 추가된 str.casefold()메서드를 이용해서 수행한다.

latin1 문자만 담고 있는 문자열 s의 경우 s.casefold()와 s.lower()를 실행한 결과가 동일하다. 다만 마이크로 기호'µ'는 그리스어 소문자 뮤(대부분의 폰트에서 동일하게 보인다)로 변환하고, 영어에서 '샤프 에스'라고 부르는 에스체트 'ß'는 'ss'로 변환한다.

- [케이스 폴딩 예제](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-6/case_folding.py)
    - 현재 파이썬 3.4에는 str.casefold()와 str.lower()가 서로 다른 문자를 반환하는 코드 포인트가 116개 있다. 이수치는 유니코드 6.3에서 명명된 110,122개 문자의 0.11%에 해당한다.

    - 유니코드와 관련된 대부분의 문제와 마찬가지로 케이스 폴딩은 수많은 언어학적 특별 케이스를 다루는 복잡한 문제지만, 파이썬 핵심 팀은 대부분의 사용자가 만족할 만한 해결책을 제시하기 위해 노력했다.

# 정규화된 텍스트 매칭을 위한 유틸리티 함수
지금까지 살펴본 것처럼 NFC와 NFD는 안전하며 유니코드 문자열을 적절히 비교할 수 있게 해준다.
NFC는 대부분의 애플리케이션에서 사용할 수 있는 최고의 정규화된 형태며, str.casefold()는 대소문자 구분 없이 문자를 비교할 때 좋은 방법이다.

다양한 언어로 구성된 텍스트를 사용하는 경우, [정규화된 유니코드 문자열 비교](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-6/unicode_normalization_equal.py)
이 코드와 같이 nfc_equal()와 fold_equal()메서드를 추가해두는것이 좋다.

유니코드 표준에 속해 있는 정규화 및 케이스 폴딩 외에, 때로는 'café'를 'cafe'로 변환하는것처럼 더욱 깊이 있게 변환하는 방법도 생각해볼 수 있다. 다음 절에서는 이런 변환을 언제 어떻게 사용하는지 알아본다.

# 극단적인 '정규화':발음 구별 기호 제거하기
구글 검색에서는 많은 기법이 사용되지만, 그중 문맥에 따라 악센트나 갈고리형 기호 등의 발음 구별 기호를 무시하는 방법도 있다. 발음 구별 기호를 제거하는 방법은 단어의 뜻을 변경하기도 하며 검색시 오탐이 발생할 수도 있으므로 적절한 정규화 방식은 아니다. 그렇지만 발음 구별 기호를 무시하거나 정확히 사용하지 못하는 경우가 종종 있으며 철자법 규칙이 시대에 따라 변하기도 하므로, 실제 사용되는 언어에서 악센트 용법은 생겼다가 사라지기도 한다. 그러므로 악센트에 너무 연연할 필요는 없다.

검색하는 경우 외에도 발음 구별 기호를 제거하면, 특히 라틴어의 경우 URL이 읽기 좋아진다.
상파울루시에 대한 위키백과 문서의 URL을 살펴보자.

***
http://en.wikipedia.org/wiki/S%C3%A3o_Paulo
***
%C3%A3 부분은 URL 이스케이프 처리한 부분으로, 물결표가 있는 'a'인 'ã'를 UTF-8로 표현한 것이다. 다음은 철자가 올바르지 않지만 훨씬 더 읽기 좋다.

***
http://en.wikipedia.org/wiki/Sao_Paulo
***

어떤 문자열에서 발음 구별 기호를 모두 제거하려면
- [발음 구별 기호 제거](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-6/delete_shave_marks.py)
    1. 모든 문자를 기본 문자와 결합 표시로 분해한다.
    2. 결합 표시를 모두 걸러낸다.
    3. 문자를 모두 재결합시킨다.
    * 위 예제의 shave_marks()함수는 제대로 작동하지만, 너무 심한듯 하다. 흔히 발음 구별 기호를 제거하는 것은 라틴 텍스트를 순수한 아스키코드로 변환하기 위해서인데, shave_marks()함수는 단지 악센트만 제거해서 아스키 문자로 만들 수 없는 그리스 문자도 변경한다. 따라서 밑의 예제와 같이 모든 기반 문자를 분석해서 기반 문자가 라틴 알파벳인 경우에만 연결된 표시를 제거하는 방법이 더좋다.

- [라틴어만 발음 구별 기호 제거](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-6/delete_shave_marks2.py)
    1. 모든 문자를 기반 문자와 결합 표시 기호로 분리한다.
    2. 기반 문자가 라틴 문자일 때 결합 표시 기호를 건너뛴다.
    3. 아니면 현재 문자를 보관한다.
    4. 새로운 기반 문자를 찾아내고 라틴 문자인지 판단한다.
    5. 문자들을 모두 결합하고 NFC 방식으로 정규화한다.

- [훨씬더 극단적인 방법](https://github.com/hyeonDD/fluent_python/blob/master/Part4/ex4-6/unicode_normalization_change.py)
    위 예제는 원형 따옴표, 전각 대시, 작은 점 등 서양 텍스트에서 널리 사용되는 기호들을 아스키에 해당하는 문자로 바꾸는 훨씬 더 극단적인 방법이다.(asciize() 함수이용)
    1. 문자 대 문자 치환을 위한 매핑 테이블을 만든다.
    2. 문자 대 문자열 치환을 위한 매핑 테이블을 만든다.
    3. 매핑 테이블을 병합한다.
    4. dewinize()함수는 아스키나 latin1 텍스트에 영향을 미치지 않으며, 마이크로소프트가 cp1252안의 latin1에 추가한 문자들만 변경한다.
    5. dewinize()를 호출해서 발음 구별 기호를 제거한다.
    6. 에스체트 'ß'를 'ss'로 치환한다(대소문자를 유지하기 위해 여기서는 casefold()를 사용하지 않는다.)
    7. NFKC 정규화를 적용해서 호환성 코드 포인트로 대체된 문자열을 만든다.
    > 발음 구별 기호를 제거하는 규칙은 언어마다 다르다. 예를 들어 독일어의 경우 'Ü'fmf 'ue'로 대체한다. 위 asciize()함수는 이렇게까지 정교하지 않으므로, 언어에 따라 적절하게 작동하지 않을 수도 있다. 그렇지만 포르투갈어에 대해서는 제법 잘 작동한다.

- 정리하면, 위 예제들에서의 함수들은 표준 정규화를 넘어서 텍스트를 상당히 깊게 변환하므로 텍스트의 원래 의미를 변경할 가능성이 높다. 대상 언어, 사용자, 변환된 텍스트의 사용법에 대해 잘 알고 있는 사람만이 이렇게 깊게 변환해야 할지 여부를 판단할 수 있다.

        

