def taxi_process(ident, trips, start_time=0): #1
    """각 단계 변화마다 이벤트를 생성하며 시뮬레이터 제어권을 넘긴다."""
    time = yield Event(start_time, ident, 'leave garage') #2
    for i in range(trips): #3
        time = yield Event(time, ident, 'pick up passenger') #4
        time = yield Event(time, ident, 'drop off passenger') #5
        yield Event(time, ident, 'going home') #6
        # 택시 프로세스의 끝 #7