# 인터프립터에서 실행하자.
city = 'Seoul ã'

print(city.encode('utf_8'))
print(city.encode('utf_16'))
print(city.encode('iso8859_1'))
print(city.encode('cp437')) # cp437은 물결표가 있는 ã를 인코딩할 수 없다. 기본 에러 처리기인 'strict'는 UnicodeEncodeError를 발생함
print(city.encode('cp437', errors='ignore')) # error='ignore' 처리기는 인코딩할 수 없는 문자를 말없이 건너뛴다. 일반적으로 상당히 좋지 않은 방법이다.
print(city.encode('cp437', errors='replace')) # error='replace' 처리기는 인코딩할 수 없는 문자를 물음표?로 치환한다. 데이터가 손실되지만, 어떤문제가 있음을 사용자가 확인할 수 있게 해준다.
print(city.encode('cp437', errors='xmlcharrefreplace')) # 'xmlcharrefreplace 처리기는 인코딩할 수 없는 문자를 XML 개체로 치환한다.
