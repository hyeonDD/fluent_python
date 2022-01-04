# 가변 시퀀스는 새로운 항목을 추가만 해주기에 타깃은 변하지 않음.

l = [1,2,3]
print(id(l))
l *= 2
print(l)
print(id(l))

# 불변 시퀀스는 새로운 항목을 추가하는 대신 항목이 추가된 시퀀스 전체를 새로 만들어 타깃 변수에 저장하므로 비효율적
t = (1,2,3)
print(id(t))
t *= 2
print(id(t))
