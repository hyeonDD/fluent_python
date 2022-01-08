from unicodedata import normalize

def nfc_equal(str1,str2):
    return normalize('NFC', str1) == normalize('NFC', str2)

def fold_equal(str1,str2):
    return (normalize('NFC', str1).casefold() ==
            normalize('NFC', str2).casefold())

"""
정규화된 유니코드 문자열을 비교하기 위한 유틸리티 함수

대소문자를 구분하고, NFC를 사용하는 경우 :

s1 = 'café'
s2 = 'cafe\u0301'
print(s1 == s2)
print(nfc_equal(s1, s2))

# 케이스 폴딩과 함께 NFC를 사용하는 경우:
print('\n\n')
s3 = 'Straße'
s4 = 'strasse'
print(s3 == s4)
print(nfc_equal(s3,s4))
print(fold_equal(s3,s4))
print(fold_equal(s1,s2))
print(fold_equal('A','a'))

"""