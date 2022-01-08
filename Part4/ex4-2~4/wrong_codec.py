octest = b'Montr\xe9al' # 이 바이트들은 latin1으로 인코딩된 'Montreal'이다. '\xe9'는 'é'를 나타내는 바이트다.
print(octest.decode('cp1252')) # cp1252 (Windows 1252)는 latin1의 슈퍼셋(상위집합)이므로 제대로 디코딩된다.
print(octest.decode('iso8859_7')) # ISO-8859-7은 그리스 문자를 위한 코덱이므로 \xe9를 엉뚱하게 해석하지만, 에러는 발생시키지 않는다.
print(octest.decode('koi8_r')) # KOI8-R은 러시아어를 위한 코덱으로, 여기서는 \xe9가 키릴 문자 И로 해석된다.
print(octest.decode('utf_8')) # utf_8 코덱은 octests를 UTF-8로 변환할 수 없음을 알리기 위해 UnicodeDecodeError를 발생시킨다.
print(octest.decode('utf_8', errors='replace')) # replace 에러 처리기를 사용해서 \xe9를 '�'(코드 포인트 U+FFFD)로 치환한다. �는 알 수 없는 문자를 표현하기 위해 사용하는 공식 유니코드 치환 문자 (REPLACEMENT CHARACTER)다.
