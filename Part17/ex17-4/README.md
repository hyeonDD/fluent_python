<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part17/ex17-4/UML_class_diagram.png)
 -->
# Executor.map() 실험
[flags_threadpool_ac.py](https://github.com/hyeonDD/fluent_python/blob/master/Part17/ex17-2~3/flags_threadpool_ac.py)에서 본 것처럼 Executor.map() 메서드를 이용하면 여러 콜러블을 아주 간단히 동시에 실행할 수 있다. 아래예제에 있는 스크립트는 Executor.map()이 작동하는 과정을 자세히 보여준다. 이 스크립트를 실행한 결과는 그뒤의 코드와 같다.

- [demo_executor_map.py](https://github.com/hyeonDD/fluent_python/blob/master/Part17/ex17-4/demo_executor_map.py)
1. 이 함수는 자신이 받은 인수 앞에 [HH:MM:SS] 포맷의 타임스탬프를 찍어서 출력한다.
2. loiter() 함수는 단지 시작할 때 메시지를 출력하고, 인수로 받은 n초 동안 잠자고, 마지막 메시지를 출력한다. 메시지 앞에 n개의 탭을 붙여 메시지를 들여 쓴다.
3. 결과를 가져오는 방법을 보여주기 위해 loiter()는 n * 10을 반환한다.
4. 스레드 세 개를 가진 ThreadPoolExecutor 객체를 생성한다.
5. executor에 5개의 작업을 요청한다. 작업자 스레드가 3개밖에 없으므로, 일단은 loiter(0).loiter(1).loiter(2) 작업만 먼저 실행된다. map()메서드는 논블로킹 메서드다.
6. executor.map()이 반환한 값을 바로 출력한다. 아래예제에서 보는 것처럼 제너레이터가 반환된다.
7. for 루프 안에서 enumerate()를 호출하면 암묵적으로 next(results)를 호출하는데, next(results)는 먼저 내부적으로 첫 번째 호출한 loiter(0)을 나타내는 Future 객체 _f의 result()메서드를 호출한다. _f.result()메서드는 _f가 완료될 때까지 블로킹되므로, 다음번 결과가 나올 때까지 이 루프는 블로킹된다.

demo_executor_map.py를 실행해서 하나씩 나오는 결과를 직접 확인기 바란다. ThreadPoolExecutor에 대한 max_workers 인수도 변경해보고 executor.map()에 사용할 인수를 생성하는 range()함수도 변경해보면서 달라지는 결과를 확인해보라. rnage()함수 대신 직접 원하는 숫자를 골라서 리스트를 만들어도 좋다.

위 예제를 실행한 결과는 아래코드와 같다.

```
python3 demo_executor_map.py
"""
[21:48:17] Script starting. #1
[21:48:17] [21:48:17]loiter(0): doing nothing for 0s... #2
[21:48:17] loiter(0): done.
[21:48:17][21:48:17] [21:48:17] results:        loiter(1): doing nothing for 1s... #3
<generator object Executor.map.<locals>.result_iterator at 0x0000023AD84E9120> #4

                        loiter(3): doing nothing for 3s... #5
                                    loiter(2): doing nothing for 2s...

[21:48:17] Waiting for individual results:
[21:48:17] result 0: 0 #6
[21:48:18]      loiter(1): done. #7
[21:48:18][21:48:18] result 1: 10 #8
                                loiter(4): doing nothing for 4s...
[21:48:19]              loiter(2): done. #9
[21:48:19] result 2: 20
[21:48:20]                      loiter(3): done.
[21:48:20] result 3: 30
[21:48:22]                              loiter(4): done. #10
[21:48:22] result 4: 40
"""
```
1. 코드 실행시각을 알려준다.
2. 첫 번째 스레드가 loiter(0)을 실행하면, 이 함수는 0초간 자고 두 번째 스레드가 시작되기 전에 반환할수도 있지만 경우에 따라 달라질 수도 있다.
3. loiter(1)과 loiter(2)는 바로 실행된다. 스레드 풀에 작업자 스레드가 세 개 있으므로, 함수 세 개를 동시에 실행할 수 있기 때문이다.
4. executor.map() 메서드가 반환한 값이 제너레이터임을 알 수 있다. 작업 수와 max_workers 설정에 상관없이 여기까지는 전혀 블로킹되지 않고 실행된다.
5. loiter(0)이 완료되었으므로, 첫 번째 작업자 스레드가 이제 네 번째 스레드인 loiter(3)을 실행할 수 있다.
6. 여기서는 loiter()를 호출할 때 전달한 인수에 따라 실행이 블로킹될 수 있다. results 제너레이터의 __next__()메서드는 첫 번째 Futuer 객체가 완료될 때까지 대기해야 한다. 여기서는 이 루프를 시작하기 전에 loiter(0)이 완료되었으므로 블록되지 않는다. 여기까지는 모두 처음시작한 시간과 같다.
7. loiter(1)은 1초 후인 +1초에 완료된다. 이 스레드는 이제 loiter(4)를 호출하게 된다.
8. loiter(1)의 결과인 10이 출력된다. for 루프는 loiter(2)의 결과를 기다리면서 블로킹될 것이다.
9. 이러한 형태가 반복된다. 이제 loiter(2)가 완료되어 결과를 출력한다. loiter(3)도 마찬가지다.
10. loiter(4)가 완료되기까지 2초 걸린다. 이 함수는 +1초에 시작되어 4초간 자고 있었기 때문이다.

Executor.map()은 사용하기 쉽지만, 호출한 순서 그대로 결과를 반환하는 특징이 있다. 이러한 특징은 상황에 따라 도움이 되기도 하고 아닐 수도 있다. 첫 번째 호출이 결과를 생성할 때까지 10초 걸리고 나머지 호출은 1초씩 걸린다면, map()이 반환한 제너레이터가 첫 번째 결과를 가져오기까지 10초 걸린다. 그 후 다른 함수는 이미 실행을 완료했을 테니 나머지 결과는 바로 가져올 수 있다. 더 진행하기 전에 모든 결과가 필요한 경우라면 이 특징은 문제가 되지 않지만, submit()한 순서와 상관없이 완료되는 대로 결과를 가져오는 게 더 좋은 경우도 있다. 완료되는 대로 결과를 가져오려면 flags_threadpool_ac.py에서 본 것처럼 Executor.submit() 메서드와 futures.as_completed() 함수를 함께 사용해야 한다. 이 기법은 17.5.2절 'futures.as_completed() 사용하기'에서 설명한다.
> submit()이 다양한 콜러블과 인수를 제출할 수 있는 반면 executor.map()은 여러 인수에 동일한 콜러블을 실행하도록 설계되어 있으므로, executor.submit()/futures.as_completed() 조합이 executor.map()보다 융통성이 높다. 게다가 일부는 ThreadPoolExecutor 객체에서, 다른 일부는 ProcessPoolExecutor 객체에서 가져오는 등 여러 실행자에서 가져온 Future 객체의 집합을 futures.as_completed()에 전달할 수 있다.

다음 절에서는 executor.map()를 사용하는 대신 futures.as_completed()를 반복하게 만드는 요구사항에 따라 국기를 내려받는 예제를 수정해본다.

