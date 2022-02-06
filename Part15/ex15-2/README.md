<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part15/ex15-2/UML_class_diagram.png)
 -->
# 콘텍스트 관리자와 with 블록
반복자가 for 문을 제어하기 위해 존재하는 것과 마찬가지로, 콘텍스트 관리자 객체는 with 문을 제어하기 위해 존재한다.
with 문은 try/finally 패턴(이 패턴은 예외, return, sys.exit() 호출 등의 이유로 어떤 블록의 실행이 중단되더라도 이후의 일정한 코드를 반드시 실행할 수 있게 보장한다)을 단순화하기 위해 설계되었다. 일반적으로 finally 절 안에 있는 코드는 중요한 리소스를 해제하거나 임시로 변경된 상태를 복원하기 위해 사용된다.

콘텍스트 관리자 프로토콜은 __enter__()와 __exit__() 메서드로 구성된다. with문이 시작될 때 콘텍스트 관리자 객체의 __enter__() 메서드가 호출된다. 이 메서드는 with 블록의 끝에서 finally 절의 역할을 수행한다.

파일 객체를 닫는 작업이 대표적인 예다. 아래 예제는 with를 이용해서 파일을 닫는 예다.
```
with open('mirror.py') as fp: #1
    src = fp.read(60) #2

len(src)
#60
fp #3
<_io.TextIOWrapper name='mirror.py' mode='r' encoding='UTF-8'>
fp.closed, fp.encoding #4
#(True, 'UTF-8')
fp.read(60) #5
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
ValueError: I/O operation on closed file.
```
1. 파일의 __enter__() 메서드가 self를 반환하므로 fp는 열린 파일에 바인딩된다.
2. fp에서 데이터를 읽는다.
3. fp 변수는 여전히 살아 있다.
4. fp 객체의 속성을 읽을 수 있다.
5. 그러나 with 블록이 끝날 때 TextIOWrapper.__exit__() 메서드가 호출되어 파일을 닫으므로, fp를 이용해서 파일 입출력을 할 수 없다.

위 예제의 첫 번째 설명은 중요한 점을 알려준다. 콘텍스트 관리자 객체는 with 문 뒤의 표현식을 평가한 결과지만, as 절에 있는 타깃 변수의 값은 콘텍스트 관리자 객체의 __enter__()호출 결과다.

위 예제에서는 open()함수가 TextIOWrapper 객체를 반환하고, 이 객체의 __enter__()메서드는 self를 반환했을 뿐이다. 그러나 __enter__() 메서드는 콘텍스트 관리자 대신 다른 객체를 반환할 수도 있다.

제어 흐름이 with 문을 빠져나온 후에는 __enter__() 메서드가 반환한 객체가 아니라 콘텍스트 관리자 객체의 __exit__()메서드가 호출된다.

with 문의 as절은 선택적이다. open()의 경우에는 파일에 대한 참조가 필요하지만, 사용자에게 반환할 적절한 객체가 없어서 None을 반환하는 콘텍스트 관리자도 있다.

아래 예제는 아주 간단하지만 콘텍스트 관리자와 __enter__() 메서드가 반환하는 객체의 차이를 잘 보여준다.

```
from mirror import LookingGlass
with LookingGlass() as what: #1
    print('Alice, Kitty and Snowdrop') #2
    print(what)

"""
pardwonS dna yttiK , ecilA #3
YKCOWREBBAJ
"""
what #4
# 'JABBERWOCKY'
print('Back to normal.') #5
# Back to normal.

```
1. LookingGlass 객체가 콘텍스트 관리자다. 파이썬은 콘텍스트 관리자의 __enter__() 메서드를 호출해서 반환된 값은 what에 바인딩한다.
2. 문자열을 출력하고 나서 타깃 변수 what의 값을 출력한다.
3. print()가 문자열을 역순으로 출력한다.
4. 이제 with 블록이 끝났으니, __neter__()가 반환해서 what에 저장한 문자열 'JABBERWOCKY'를 제대로 출력할 수 있다.
5. print()가 정상적으로 출력한다.

LookingGlass 클래스 코드는 아래예제와 같다.

- [mirror.py](https://github.com/hyeonDD/fluent_python/blob/master/Part15/ex15-2/mirror.py)

1. 파이썬은 self 인수만으로 __enter__() 메서드를 호출한다.
2. 나중에 사용하기 위해 객체 속성에 원래 sys.stdout.write() 메서드 객체를 저장한다.
3. sys.stdout.write()를 멍키패칭해서 직접 만든 메서드로 변경한다.
5. 우리가 바꾼 sys.stdout.write() 함수는 text 인수를 거꾸로 뒤집고 나서 원래 sys.stdout.write()함수를 호출한다.
6. 정상적으로 수행이 완료되면 파이썬 None, None, None 인수로 __exit__() 메서드를 호추랗ㄴ다. 예외가 발생한 경우에는 이 세 개의 인수에 예외 데이터(잠시 후에 설명한다)가 전달된다.
7. 파이썬은 임포트된 모듈을 캐시에 저장하므로 그 다음에 모듈을 임포트하면 간단히 처리된다.
8. sys.stdout.write()를 원래 메서드로 변경한다.
9. exception 인수가 None이 아니고 ZeroDivsionError면 메시지를 출력한다.
10. 그러고 나서 True를 반환해서 예외가 처리되었음을 파이썬 인터프리터에 알려준다.
11. __exit__()가 None이나 True 이외의 값을 반환하면 with 블록에서 발생한 예외가 상위 코드로 전달된다.
> 실제 애플리케이션에서 표준 출력을 가로챌 때는 sys.stdout을 다른 파일 객체로 잠시 교체하고 작업을 수행한 후 다시 원래 sys.stdout으로 교체한다. contextlib.redirect_stdout (http://bit.ly/1MM7Sw6) 콘텍스트 관리자는 이 방법을 잘 보여준다. 단지 sys.stdout 대신 사용할 파일 객체를 전달하면 된다.

파이썬 인터프리터는 __enter__() 메서드를 호출할 때 self 이외의 인수는 전달하지 않는다.
__exit__() 메서드를 호출할 때는 다음 세 인수를 전달한다.

---

**exc_type**
ZeroDivisionerror 등이 예외 클래스

**exc_value**
예외 객체. 예외 메시지 등 exception () 생성자에 전달된 인수는 exc_value.args 속성을 이용해서 볼 수 있다.

**traceback**
traceback 객체

---

아래 예제에서는 콘텍스트 관리자가 작동하는 방식을 자세히 볼 수 있다. 여기서는 __enter__()와 __exit__() 메서드를 직접 호출하기 위해 with 무 밖에서 LookingGlass 클래스를 사용한다.

```
# with 블록 없이 LookingGlass 사용하기
from mirror import LookingGlass
manager = LookingGlass() #1
manager
# <mirror.LookingGlass object at 0x2a578ac>
monster = manager.__enter__() #2
monster == 'JABBERWOCKY' #3
# eurT
monster
# 'YKCOWREBBAJ'
manager
# >ca875a2x0 ta tcejbo ssalGgnikooL.rorrim<
manager.__exit__(None, None, None) #4
monster
# 'JABBERWOCKY'
```
1. manager 객체를 생성하고 조사한다.
2. 콘텍스트 관리자의 __enter__() 메서드를 호출하고 결과를 monster에 저장한다.
3. monster에는 'JABBERWOKCY' 문자열이 저장되어 있다. __enter__() 메서드에서 stdout.write()를 reverse_write() 메서드로 멍키 패칭했으므로, 출력 메시지 True가 역순으로 출력되었다.
4. manager.__exit__() 메서드를 호출해서 stdout.write() 메서드를 복원한다.

콘텍스트 관리자는 상당히 독특한 기능으로서, 느리지만 확실히 파이썬 커뮤니티에서 이 기능을 창의적으로 활용하는 방법을 찾아내고 있다. 표준 라이브러리에서 사용되는 예는 다음과 같다.
* sqlite3 모듈의 트랜잭션 관리: 12.6.7.3절 '연결을 콘텍스트 관리자로 사용하기' (http://bit.ly/1MM89PC) 를 보라.
* threading 코드에서 lock, condition, semaphore 보관: 17.1.10절 'with 문 안에서의 락, 컨디션, 세마포어 사용하기' (http://bit.ly/1MM8guy) 를 보라.
* Decimal 객체의 산술 연산 환경 설정: decimal.localcontext 문서 (http://bit.ly/1MM8eTw) 를 보라.
* 객체의 테스트를 위한 임시 패치 적용: unittest.mock.patch() 함수 문서 (http://bit.ly/1MM8imk) 를 보라.

표준 라이브러리에는 contextlib 유틸리도 들어 있다. 다음 절에서 알아본다.