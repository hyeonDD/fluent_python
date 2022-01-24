v1 = Vector2d(3, 4)
print(v1.x, v1.y) #1

x, y = v1 #2
print(x,y)

print(v1) #3
v1_clone = eval(repr(v1)) #4
v1 == v1_clone #5

print(v1) #6

octets = bytes(v1) #7
print(octets)
print(abs(v1)) #8
print(bool(v1), bool(Vector2d(0, 0))) #9