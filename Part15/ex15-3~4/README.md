<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part15/ex15-3~4/UML_class_diagram.png)
 -->
# contextlib 유틸리티
콘텍스트 관리자 클래스를 직접 만들어보기 전에 파이썬 표준 라이브러리의 29.6절 'contextlib - with 문 콘텍스트를 위한 유틸리티' 문서 (http://bit.ly/1HGqZpJ) 를 살펴보라. 이미 설명한 redirect_stdout 외에도 contextlib 모듈에는 다음과 같이 다양하게 응용할 수 있는 클래스와 함수가 있다.

---

**closing()**
close() 메서드는 제공하지만 __enter__()/__exit__() 프로토콜을 구현하지 않는 객체로부터 콘텍스트 관리자를 생성하는 함수

**suppress**
지정한 예외를 임시로 무시하는 콘텍스트 관리자

**@contextmanager**
클래스를 생성하고 프로토콜을 구현하는 대신, 간단한 제너레이터 함수로부터 콘텍스트 관리자를 생성할 수 있게 해주는 데커레이터

**ConetxtDecorator**
콘텍스트 관리자를 함수 데커레이터로 사용할 수 있게 해주는 기반 클래스

**ExitStack**
여러 콘텍스트 관리자를 입력할 수 있게 해주는 콘텍스트 관리자. with 블록이 끝나면 ExitStack은 누적된 콘텍스트 관리자들의 __exit__() 메서드를 LIFO 순서 (마지막에 들어간 것이 처음 나온다) 로 호출한다. 예를 들어 임의의 파일 리스트에 있는 파일을 한꺼번에 여는 경우처럼, with 블록 안에 들어가기전에 얼마나 많은 콘텍스트 관리자가 필요한지 사전에 알 수 없을 때 이 클래스를 사용하라.

---

이 유틸리티들 중 @contextmanager 데커레이터가 가장 널리 사용되므로, 이 데커레이터에 대해 자세히 살펴볼 필요가 있다. @contextmanager는 반복과 상관없는 yield 문에도 사용할 수 있으므로 흥미롭다. 이 개념을 잘 이해하면 다음 절에서 설명할 코루틴의 기반을 다질 수 있다.

# @contextmanager 사용하기
@contextmanager 데커레이터는 콘텍스트 관리자를 생성할 때 작성하는 틀에 박힌 코드를 줄여준다. __enter__()와 __exit__() 메서드를 가진 클래스 전체를 작성하는 대신 __enter__() 메서드가 반환할 것을 생성하는 yield 문 하나를 가진 제너레이터만 구현하면 된다.

@contextmanager로 데커레이트된 제너레이터에서 yield는 함수 본체를 두 부분으로 나누기 위해 사용된다. yield문 앞에 있는 모든 코드는 with 블록 앞에서 인터프리터가 __enter__()를 호출할 때 실행되고, yield 문 뒤에 있는 코드는 블록의 마지막에서 __exit__()가 호출될 때 실행된다.

예제 코드를 통해 알아보자. 아래 예제는 [예제 15-3]의 LookingGlass 클래스를 제너레이터 함수로 교체한다.

- [mirro_gen.py](https://github.com/hyeonDD/fluent_python/blob/master/Part15/ex15-3~4/mirro_gen.py)
1. @contextmanager 데커레이터를 적용한다.
2. 원래의 sys.stdout.write() 메서드를 보관한다.
3. reverse_write() 함수를 정의한다. original_write()는 클로저를 통해 접근할 수 있다.
4. sys.stdout.write()를 reverse_write()로 교체한다.
5. with문의 as 절에 있는 타깃 변수에 바인딩될 값을 생성한다. with 문의 본체가 실행되는 동안 이 함수는 여기에서 실행을 일시 중단한다.
6. 제어 흐름이 with 블록을 빠져나오면 yield 문 이후의 코드가 실행된다. 여기서는 원래의 sys.stdout.write() 메서드를 복원한다.

아래 에제는 looking_glass() 함수의 사용 예를 보여준다.
```
# looking_glass() 콘텍스트 관리자 함수 사용 예
from mirror_gen import looking_glass
with looking_glass() as what: #1
    print('Alice, Kitty and Snowdrop')
    print(what)


"""
pordwonS dna yttiK ,ecilA
YKCOWREBBAJ
"""
what
# 'JABBERWOCKY'
```
1. [예제15-2]에서 콘텍스트 관리자의 이름만 LookingGlass에서 looking_glass로 바뀌었을 뿐이다.

본질적으로 @contextlib.contextmanager 데커레이터는 데커레이트된 함수를 __enter__()와 __exit__() 메서드를 구현하는 클래스 안에 넣을 뿐이다.

이 클래스의 __enter__() 메서드는 다음과 같은 단계를 실행한다.
1. 제너레이터 함수를 호출해서 제너레이터 객체를 보관한다(여기서는 이 객체를 gen이라고 부르자.)
2. next(gen)을 호출해서 yield 키워드 앞까지 실행한다.
3. next(gen)이 생성한 값을 반환해서, 이 값이 as 절의 타깃 변수에 바인딩되게 한다.

with 블록이 실행을 마칠 때 __exit__() 메서드는 다음과 같은 단계를 실행한다.
1. exc_type에 예외가 전달되었는지 확인한다. 만일 그렇다면 제너레이터 함수 본체 안에 있는 yield 행에서 gen.throw(exception)을 실행해서 예외를 발생시킨 것이다.
2. 그렇지 않다면 next(gen)을 호출해서 제너레이터 함수 본체 앙늬 yield 다음의 코드를 계속 실행한다.

[예제15-5]에는 심각한 문제가 있다. with 블록 안에서 예외가 발생하면 파이썬 인터프리터가이 예외를 잡고, looking_glass() 안에 있는 yield 표현식에서 다시 예외를 발생시킨다. 그러나 그곳에는 예외 처리 코드가 없어서 looking_glass() 함수는 원래의 sys.stdout.write()메서드를 복원하지 않고 중단하므로, 시스템이 불안정한 상태로 남게 된다.

[예제15-7]은 ZeroDivisionError 예외를 특별히 처리해서 클래스 기반의 [예제 15-3]과 기능상 동일하게 작동한다.

- [mirror_gen_exc.py](https://github.com/hyeonDD/fluent_python/blob/master/Part15/ex15-3~4/mirror_gen_exc.py)
1. 에러 메세지에 대한 변수를 생성한다. [예제15-5]에서 변경된 첫 번째 부분이다.
2. 에러 메세지를 설정해서 ZeroDivisionError를 처리한다.
3. 멍키 패칭한 sys.stdout.write()를 원래대로 복원한다.
4. 에러 메세지가 설정되어 있으면 출력한다.

__exit__() 메서드는 예외 처리를 완료했음을 인터프리터에 알려주기 위해 True를 반환한다. True가 반환되면 인터프리터는 예외를 전파하지 않고 억제한다. 한편 __exit__()가 명시적으로 값을 반환하지 않으면 인터프리터가 None을 받으므로 예외를 전파한다. @contextmanager 데커레이터를 사용하면 기본 작동이 반대로 된다. 데커레이터가 제공하는 __exit__() 메서드는 제너레이터에 전달된 예외가 모두 처리되었으므로 억제해야 한다고 생각한다. @contextmanager가 예외를 억제하지 않게 하려면 데커레이트된 함수 안에서 명시적으로 예외를 다시 발생시켜야 한다.
> @contextmanager를 사용할 때는 어쩔 수 없이 yield 문 주변을 try/finally나 with 블록으로 둘러싸야 한다. 콘텍스트 관리자의 사용자가 자신의 with 블록 안에서 어떤 일을 할지 모르기 때문이다.

표준 라이브러리 외에 @contextmanager의 재미있는 실제 사례는 마르틴 피터스의 '파일 덮어쓰기 콘텍스트 관리자' (http://bit.ly/1MM96aR) 에서 볼 수 있다. 아래 예제에서는 이 콘테긋트 관리자를 사용하는 방법을 보여준다.

```
#파일을 덮어쓰기 위한 콘텍스트 관리자
import csv

with inplace(csvfilename, 'r', newline='') as (infh, outfh):
    reader = csv.reader(infh)
    writer = csv.writer(outfh)

    for row in reader:
        row += ['new', 'columns]
        writer.writerow(row)
```
inplace() 함수가 콘텍스트 관리자며, 동일한 파일에 대해 두 개의 핸들(에제에서는 infh과 outfh)을 반환함으로써 파일을 동시에 읽고 쓸 수 있게 해준다. 이 함수는 표준라이브러리에서 제공하는 fileinput.input() 함수 (http://bit.ly/1HGr6Sq) (이 함수도 콘텍스트 관리자를 제공한다)보다 사용하기 쉽다.

마르틴이 만든 inplace()함수의 소스 코드 (http://bit.ly/1MM96aR) 을 분석하고 싶으면 yield 키워드를 찾아라. yield 앞의 모든 코드는 콘텍스트를 설정하고, 백업 파일을 생성하고, 파일을 연 후 __enter__()가 호출되면 반환할 읽기/쓰기용 파일 핸들에 대한 참조를 생성한다. __exit__()가 수행하는 yield 뒤의 코드는 파일을 닫고, 어떤 문제가 생긴 경우에는 백업파일로 복구하는 작업을 수행한다.

@contextmanager 데커레이터와 함께 사용되는 제너레이터 안의 yield 문은 반복과 상관없음을 주의하라. 이 절에서 보여준 예제에서 제너레이터는 코루틴과 비슷하게 동작한다. 코루틴은 어떤 지점까지 실행한 후 호출자가 실행할 수 있도록 멈춘 후, 호출자가 원하면 나머지 작업을 진행한다. 코루틴에 대해서는 다음 장에서 자세히 다룬다.
