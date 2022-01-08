# 문자 문제

- '문자열'이라는 개념은 아주 간단하다. 문자열은 문자의 열이다. 그런데 문제는 '문자'의 정의에 있다.
    - 현재 '문자'를 가장 잘 정의한 것은 유니코드 문자다. 이에 따라 파이썬 3 str에서 가져오는 항목도 유니코드 문자다. 파이썬 2의 unicode 객체에서 가져오는 항목은 유니코드지만, 파이썬 2 str에서 가져오는 저수준 바이트는 유니코드가 아니다.

- 유니코드 표준은 문자의 단위 원소와 특정 바이트 표현을 명확히 구분한다.
    * 문자의 단위 원소(코드포인트)는 10진수 0에서 1,114,111까지의 숫자며, 유니코드 표준에서는 'U+' 접두사를 붙여 4자리에서 6자리 사이의 16진수로 표현한다. 예를 들어 A라는 문자는 코드 포인트 U+0041에, 유로화 기호는 U+20AC에, 음악에서 사용하는 높은음자리표 기호는 U+1D11E에 할당되어 있다. 유니코드 6.3에서 가용한 코드 포인트의 약 10%정도가 문자에 할당되어 있으며, 파이썬 3.4에서도 유니코드 6.3 표준을 사용한다.

    * 문자를 표현하는 실제 바이트는 사용하는 **인코딩**에 따라 달라진다. 인코딩은 코드 포인트를 바이트 시퀀스로 변환하는 알고리즘이다. 문자 A(U+0041)에 대한 코드 포인트는 UTF-8 인코딩에서는 1바이트\x41로, UTF-16LE 인코딩에서는 2바이트 \x41\x00으로 인코딩된다. 그리고 유로화 기호(U+20AC)는 UTF-8에서는 3바이트 \xe2\x82\xac로, UTF-16LE에서는 2바이트 \xac\x20으로 인코딩된다.

- 코드 포인트를 바이트로 변환하는 것을 인코딩, 바이트를 코드 포인트로 변환하는 것을 디코딩이라고한다.[인코딩 디코딩 예](https://github.com/hyeonDD/fluent_python/blob/master/Part3/ex4-1/encode&decode.py)
    > decode()와 encode()를 헷갈리지 않고 구분하려면, bytes 시퀀스는 알아보기 어려운 기계 메모리 덤프로, 유니코드 str은 '사람'이 읽을 수 있는 텍스트로 '디코딩(해독)'하고, str을 저장하거나 전송하기 위해 bytes로 '인코딩(암호화)'한다는 말이 이해될것이다.

- 파이썬 3의 str은 파이썬 2의 unicode 형의 이름을 변경한 것과 상당히 비슷하지만, 파이썬 3의 bytes는 단지 이전의 str 클래스의 이름을 변경한 것이 아니며, 이와 밀접하게 연관되어 있는 bytearray 형도 있다. 따라서 인코딩과 디코딩 문제로 넘어가기 전에 이진 시퀀스형을 살펴볼 필요가 있다.