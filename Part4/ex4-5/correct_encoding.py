# 인터프립터에서 실행하자.

fp = open('cafe2.txt', 'w', encoding='utf_8')
print(fp)
fp.write('cafe 한')
fp.close()

fp2 = open('cafe2.txt', 'r', encoding='utf_8')
print(fp2)
print(fp2.read())
fp2.close()


