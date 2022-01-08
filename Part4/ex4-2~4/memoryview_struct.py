import struct
fmt = '<3s3sHH' # strcut 포맷을 지정한다. <는 리틀엔디언, 3s3s는 3바이트 시퀀스 두 개, HH는 16비트 정수 두 개를 나타낸다.
# with open('D:\\code\\vscode\\github\\fluent_python\\Part4\\ex4-2\\test.gif','rb') as fp:
with open('test.gif','rb') as fp: # 메모리에 로딩된 파일 내용으로부터 memoryview를 생성한다.
    img = memoryview(fp.read()) 

header = img[:10] # 그러고 나서 먼저 생성한 memoryview를 슬라이싱해서 새로운 memoryview를 만든다. 이때 아무런 바이트도 복사하지 않는다.
print(bytes(header)) # 화면에 출력하기 위해 bytes로 변환한다. 이때 10바이트가 복사된다.

print(struct.unpack(fmt, header)) # memoryview를 (종류, 버전, 너비, 높이) 튜플로 언패킹한다.
del header # memoryview 객체에 연결된 메모리를 해제하기 위해 참조를 삭제한다.
del img
