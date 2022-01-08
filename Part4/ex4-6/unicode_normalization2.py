from unicodedata import normalize
s1 = 'café'
s2 = 'cafe\u0301'

print(len(s1),len(s2))
print(len(normalize('NFC', s1)), len(normalize('NFC', s2))) # 코드 포인트를 조합해서 가장 짧은 동일 문자열을 생성 이 예제에선 4

print(len(normalize('NFD', s1)), len(normalize('NFD', s2))) # 조합된 문자를 기본 문자와 별도의 결합 문자로 분리한다, 이 예제에선 5

print(normalize('NFC',s1) == normalize('NFC',s2))
print(normalize('NFD',s1) == normalize('NFD',s2))
