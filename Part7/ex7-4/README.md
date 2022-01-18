# 변수 범위 규칙
<!-- 
![UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-1~3/UML_class_diagram.png)
 -->
아래 예제에서는 함수 매개변수로 정의된 지역변수 a와 함수 내부에 정의되지 않은 변수 b 등 두 개의 변수를 읽는 함수를 정의하고 테스트한다.

- [지역 및 전역 변수를 읽는 함수](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-4/read_local_global_func.py)

```
3
Traceback (most recent call last):
  File "d:\code\vscode\github\fluent_python\Part7\ex7-4\read_local_global_func.py", line 4, in <module>
    print(f1(3))
  File "d:\code\vscode\github\fluent_python\Part7\ex7-4\read_local_global_func.py", line 3, in f1
    print(b)
NameError: name 'b' is not defined
```
예상한 대로 에러가 발생한다. 그런데 전역 변수 b에 값을 할당하고 f1()을 호출하면 다음과 같이 제대로 작동한다.
```
>>> b = 6
>>> f1(3)
3
6
```

이제 약간 놀라운 예제를 살펴보자.

아래의 f2() 함수를 보자. 처음 두줄은 [지역 및 전역 변수를 읽는 함수](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-4/read_local_global_func.py)의 f1()코드와 동일하다. 그러고 나서 b에 값을 할당한다. 그러나 두 번째 print()문이 변수 b에 값을 할당하기 전에 변수에 접근하므로 에러가 발생한다.

- [지역 및 전역 변수를 읽는 함수2](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-4/read_local_global_func2.py)
```
3
Traceback (most recent call last):
  File "d:\code\vscode\github\fluent_python\Part7\ex7-4\read_local_global_func2.py", line 8, in <module>
    f2(3)
  File "d:\code\vscode\github\fluent_python\Part7\ex7-4\read_local_global_func2.py", line 5, in f2
    print(b)
UnboundLocalError: local variable 'b' referenced before assignment
```
먼저 print(a)문이 실행되면서 3이 출력된다. 그러나 두 번째 문인 print(b)는 실행되지 않는다. 필자가 이 예제를 처음 보았을 때 실행 결과에 놀랐다. 전역 변수 b가 있고 print(b) 다음에 지역 변수 b에 할당하는 문이 나오므로 전역 변수의 값인 6이 출력될 것이라고 생기 때문이다.

그러나 사실은 파이썬이 함수 본체를 컴파일할 때 b가 함수 안에서 할당되므로 b를 지역 변수로 판단한다. 생성된 바이트코드를 보면 이 판단에 의해 지역 환경에서 변수 b를 가져오려 한다는 것을 알 수 있다. 나중에 f2(3)을 호출할 때 f2의 본체는 지역 변수 a의 값을 출력하지만, 지역 변수 b의 값을 가져오려 할 때 b가 바인딩되어 있지 않다는 것을 발견한다.

이 현상은 버그가 아니고 설계 결정사항이다. 파이썬은 변수가 선언되어 있기를 요구하지 않지만, 함수 본체 안에서 할당된 변수는 지역 변수로 판단한다. 이런 방식은 파이썬과 마찬가지로 변수 선언을 요구하지 않지만, var를 이용해서 지역 변수를 선언하지 않ㅇ은 경우 자동으로 전역변수를 사용해버리는 자바스크립트의 방식보다 훨씬 좋다.

함수 안에 할당하는 문장이 있지만 인터프리터가 b를 전역 변수로 다루기 원한다면, 다음과 같이 global 키워드를 이용해서 선언해야 한다.

- [지역 및 전역 변수를 읽는 함수 글로벌 버전](https://github.com/hyeonDD/fluent_python/blob/master/Part7/ex7-4/read_local_global_func_global.py)
    * 글로벌 키워드를 사용한 예제


