class MySeq:
    def __getitem__(self, index):
        return index #1

s = MySeq()
print(s[1]) #2
# 1
print(s[1:4]) #3
# slice(1, 4, None)

print(s[1:4:2]) #4
# slice(1, 4, 2)

print(s[1:4:2, 9]) #5 
# (slice(1, 4, 2), 9)

print(s[1:4:2, 7:9]) #6
# (slice(1, 4, 2), slice(7, 9, None))    
