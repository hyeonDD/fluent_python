cafe = bytes('cafe한', encoding='utf_8') # bytes는 str에 인코딩을 지정해서 만들 수 있다.
print(cafe)
print(cafe[0]) # 각 항목은 range (256)에 들어가는 정수다.
print(cafe[:1]) # bytes는 슬라이싱해도 bytes다. 슬라이스가 한 바이트일 때도 마찬가지다.

cafe_arr = bytearray(cafe)
print(cafe_arr) # bytearray에 대한 리터럴 구문은 없다. bytes 리터럴을 인수로 사용해서 bytearray()를 표현한다.

print(cafe_arr[-1:]) # bytearray는 슬라이싱해도 bytearray다.

