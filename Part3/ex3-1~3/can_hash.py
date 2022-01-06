tt = (1,2,(30,40))
print(hash(tt))
print(f'1번째 id값 {id(tt)}')

tf = (1,2,frozenset([30, 40]))
print(hash(tf))

tt2 = (1,2,(30,40))
print(hash(tt2))
print(f'2번째 id값 {id(tt2)}')


tl = (1,2,[30,40])
print(hash(tl))

