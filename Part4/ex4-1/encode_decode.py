# 꼭 python 인터프리텁에서 실행하자.
s = 'cafe家'
print(len(s)) #'cafe' 문자열은 네 개의 유니코드 문자를 갖고 있다.

b = s.encode('utf8') #UTF-8 인코딩을 이용해서 str을 bytes로 인코딩한다.
print(b) # b'cafe\xe5\xae\xb6' << bytes 리터럴은 접두사 b로 시작한다.

print(len(b)) # bytes 형인 b는 다섯 바이트로 구성된다. e가 UTF-8에서 두 바이트로 인코딩되기 때문이다.
print(b.decode('utf8')) # UTF-8 인코딩을 이용해서 bytes를 str로 디코딩한다.