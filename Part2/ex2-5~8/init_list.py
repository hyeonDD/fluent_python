board = [['_'] * 3 for i in range(3)]
print(board)
board[1][2] = 'X'
print(board)

# 동일한 리스트에 대한 세 개의 참조를 가진 리스트
# 잘못 초기화한 예
weird_board = [['_'] * 3] * 3
print(weird_board)
weird_board[1][2] = '0'
print(weird_board)
