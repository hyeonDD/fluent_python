# 함수를 객체처럼 다루기
<!-- 
[예](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-1~3/encode_decode.py)
 -->

- [함수를 생성하서 테스트하고, 함수의 __doc__을 읽어서 자료형 확인하기](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-1~3/check_type.py)
    1. 지금 콘솔 세션에 있으므로, 함수를 '런타임'에 만들고 있는 것이다.
    2. __doc__은 함수 객체의 여러 속성 중 하나다.
    3. factorial은 function 클래스의 객체다.

__doc__ 속성은 객체의 도움말 텍스트를 생성하기 위해 사용된다. 파이썬 대화형 콘솔에서 help(factorial) 명령은

***
Help on function factorial in module __main__:

factorial(n)
    returns n!
***
와 같은 화면을 출력한다. 설명문은 함수 객체의 __doc__속성에서 가져온다.

- [함수를 다른 이름으로 사용하고 함수의 인수로 전달하기](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-1~3/arg_function.py)
    - 함수 객체의 '일급' 본질을 보여준다. 함수를 fact 변수에 할당하고, 이 변수명을 통해 함수를 호출한다.
    - factorial을 map()의 인수로 전달할 수도 있다. map()함수는 두 번째 인수의 연속된 요소(반복 가능한 객체)에 첫 번째 인수(함수)를 적용한 결과를 가지는 반복 가능형 객체를 반환한다.
    - 일급 함수가 있으면 함수형 스타일로 프로그래밍할 수 잇다. 함수형 프로그래밍의 특징 중 하나는 고위 함수이다.

# 고위 함수
함수를 인수로 받거나, 함수를 결과로 반환하는 함수를 **고위 함수**라고 한다.
대표적으로 [함수를 다른 이름으로 사용하고 함수의 인수로 전달하기](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-1~3/arg_function.py)의 map()함수가 있다. 2.7절 'list.sort()와 sorted()내장 함수'에서 설명한 sorted() 내장 함수도 일급 함수의 예다. sorted() 함수는 선택적인 key 인수로 함수를 전달받아 정렬할 각 항목에 적용한다.

- [단어 리스트를 길이에 따라 정렬하기](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-1~3/sorted_len.py)
    - 길이에 따라 단어 리스트를 정렬하려면 위 예제처럼 len 함수를 key 인수로 전달하면 된다.
    - 인수를 하나 받는 함수는 모두 key 인수로 사용할 수 있다. 예를 들어 운문 사전을 만들 때 단어 철자를 거꾸로 해서 정렬하면 도움이 된다.

- [단어 리스트를 철자 역순으로 정렬하기](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-1~3/revers_word.py)
    - 리스트 안의 단어들은 전혀 바뀌지 않고 오로지 거꾸로 된 철자가 정렬 기준으로 사용되었을 뿐이다. 따라서 berry로 끝나는 단어들이 함께 나온다.

함수형 프로그래밍 세계에서는 map(), filter(), reduce(), apply() 등의 고위함수가 널리 알려져 있다.
apply()함수는 파이썬 2.3에서 사용 중단 안내되었으며, 더 이상 필요하지 않기 때문에 파이썬 3에서 제거되었다.
일련의 동적인 인수에 함수를 호출해야 할 때는 apply(fn, args, kwars) 대신 fn(*args, **keywords) 형태로 작성하면 된다.

map(), filter(), reduce() 고위 함수는 여전히 존재하지만, 다음 절에서 설명하듯이 대부분의 경우 더 나은 방법이 있다.

## map(), filter(), reduce()의 대안
이름이 다른 경우도 있지만, 함수형 언어는 모두 map(), filter(), reduce() 고위 함수를 제공한다.
map()과 filter() 함수는 여전히 파이썬 3에 내장되어 있지만, 지능형 리스트와 제너레이터 표현식이 소개된 후에는 이 함수들의 중요성이 떨어졌다.
지능형 리스트가 제너레이터 표현식이 map()과 filter()의 조합이 처리하는 작업을 표현할 수 있을 뿐만 아니라 가독성도 더 좋기 때문이다.

- [팩토리얼 목록을 map()/filter()로 생성하는 방법과 지능형 리스트로 생성하는 방법](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-1~3/factorial_list.py)
    1. 0!에서 5!까지 팩토리얼 리스트를 만든다.
    2. 동일한 연산을 수행하지만 지능형 리스트를 사용한다.
    3. map()과 filter()를 사용해서 5!까지 홀수에 대한 팩토리얼 리스트를 만든다.
    4. map()과 filter()를 대체하고 lambda 없이 지능형 리스트로 동일한 작업을 수행한다.

파이썬 3에서 map()과 filter()는 제너레이터(일종의 반복 가능 객체)를 반환하므로, 제너레이터 표현식이 이 함수들을 직접 대체한다(파이썬 2에서는 이 함수들이 리스트를 반환하므로 listcomp가 가장 근접한 대안이었다.)

파이썬 2에 내장되었던 reduce()함수는 파이썬 3에서는 functools 모듈로 떨어져 나왔다. reduc()는 주로 합계를 구하기 위해 사용되는데, 2003년에 배포된 파이썬 2.3부터 내장 함수로 제공되는 sum()을 사용하는 것이 낫다. sum()이 가독성과 성능 면에서 훨씬 낫다.

- [reduce()와 sum()을 이용해서 99까지 정수 더하기](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-1~3/reduce_sum.py)
    1. 파이썬 3.0부터 reduce()는 더 이상 내장 함수로 제공되지 않는다.
    2. add()를 임포트함으로써 숫자 두 개를 더하는 함수를 생성할 필요 없다.
    3. 정수를 99까지 더한다.
    4. sum()으로 동일 작업을 수행한다. 함수를 임포트하거나 추가할 필요 없다.

sum()과 reduce()는 연속된 항목에 어떤 연산을 적용해서, 이전 결과를 누적시키면서 일련의 값을 하나의 값으로 리덕션한다는 공통점이 있다.
그 외 내장된 리덕션 함수는 all과 any다.

***
all(iterable)
모든 iterable이 참된 값이면 True를 반환한다. all([])은 True를 반환한다.

any(iterable)
iterable 중 하나라도 참된 값이면 True를 반환한다. any([])는 False를 반환한다.
***
reduce()함수는 10.6절 'Vector 버전 #4: 해싱 및 더 빠른 =='에서 자세히 설명한다. 그곳에서는 reduce()함수를 사용하기 적절하도록 예제를 계속해서 개선한다.
리덕션 함수는 반복 가능 객체에 대해 집중적으로 살펴보는 14.11절 '반복형을 리듀스하는 함수'에서 요약 설명한다.

고위 함수를 사용할 때 작은 일회용 함수를 생성하는 것이 편리할 때도 있다. 그렇기 때문에 익명 함수가 유용하게 사용된다. 익명 함수 에 대해 알아보자.

# 익명 함수

lambda 키워드는 파이썬 표현식 내에 익명 함수를 생성한다.

그렇지만 파이썬의 단순한 구문이 람다 함수의 본체가 순수한 표현식으로만 구성되도록 제한한다. 즉, 람다 본체에서는 할당문이나 while, try 등의 파이썬 문장을 사용할 수 없다.

익명 함수는 인수 목록 안에서 아주 유용하게 사용된다. 예를들어 밑에 예제는 철자 역순으로 정렬하는 [reverse()](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-1~3/revers_word.py) 함수 대신 람다를 사용하도록 수정한 코드다.

- [lambda를 이용한 reverse](https://github.com/hyeonDD/fluent_python/blob/master/Part5/ex5-1~3/reverse_to_lambda.py)
    - 고위 함수의 인수로 사용하는 방법 외에 익명 함수는 파이썬에서 거의 사용되지 않는다. 구문 제한 때문에 복잡한 람다는 가독성이 떨어지고 사용하기 까다롭다.

***

- 런드의 람다 리팩토링 비법 
    람다 때문에 코드를 이해하기 어렵다면 다음과 같이 프레드릭 런드가 제안하는 리팩토링 절차를 따라해 보라.
    1. 람다가 하는 일이 무엇인지 설명하는 주석을 작성한다.
    2. 잠시 주석을 주의 깊게 파악하고, 주석의 본질을 전달하는 이름을 생각해낸다.
    3. 그 이름을 이용해서 람다를 def 문으로 변경한다.
    4. 주석을 제거한다.

이 단계들은 'Functional Programming HOWTO'[링크](http://docs.python.org/3/howto/functional.html)에서 가져왔다.

***

람다 구분은 단지 편리 구문일 뿐이다. def 문과 마찬가지로 람다 표현식도 하나의 함수 객체를 만들다. 즉, 파이썬에서 제공하는 여러 콜러블 객체일 뿐이다.