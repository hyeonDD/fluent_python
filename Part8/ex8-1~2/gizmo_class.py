# 인터프립터에서 꼭 실행해 보자
class Gizmo:
    def __init__(self):
        print('Gizmo id: %d' % id(self))

x = Gizmo()
y = Gizmo() * 10
dir()