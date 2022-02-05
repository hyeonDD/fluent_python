<!-- 
- [UML클래스전략패턴](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-9/UML_class_diagram.png)
 -->
# 표준 라이브러리의 제너레이터 함수
텍스트를 한 줄씩 반복할 수 있게 해주는 텍스트 파일 객체에서부터 디렉터리 안에 있는 파일들의 이름을 생성해서 for 루프 안에서 재귀적인 파일 검색을 쉽게 구현할 수 있게 해주는 os.walk()함수 (http://bit.ly/1HGqqwh) 에 이르기까지 표준 라이브러리는 많은 제너레이터를 제공한다.

os.walk() 제너레이터 함수가 멋지기는 하지만, 이 절에서는 반복형 객체를 인수로 받아 선택, 계산, 혹은 재정렬된 항목을 생성하는 제너레이터를 반환하는 범용 함수를 위주로 살펴본다. 잠시 후에 나오는 표에서는 내장된 혹은 itertools나 functools 모듈에서 제공하는 제너레이터 함수 20개를 간략히 설명한다. 편의를 위해 함수가 정의된 위치와 상관없이 상위 수준에서 제공하는 기능별로 그룹 지었다.
> 이절에서 설명하는 함수를 모두 알고 있을 수도 있지만, 일부 함수는 잘 사용되지 안흔ㄴ다. 따라서 이미 제공되고 있는 함수를 다시 한 번 쭉 둘러보는 정도로 읽어보는 것도 나쁘지 않다.

첫 번째 표에는 필터링 제너레이터 함수들을 모았다. 이 함수들은 입력된 반복형을 그대로 사용해서 생성된 항목들의 일부를 생성한다. 14.8.1절 'itertools를 이용한 등차수열'에서 itertools.takewhile()을 사용했었다. takewhile()과 마찬가지로 아래 표와 나열된 대부분의 함수는 조건식을 받는다. 조건식은 인수 하나를 받는 불리언형 함수로서 입력된 반복형 항목마다 적용해서 출력할 항목을 결졍한다.

![gen_filter사진](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-9/gen_filter.png)

아래 에제는 표에 나열된 함수들의 사용 예를 보여준다.
```
# 필터링 제너레이터 함수 예
def vowel(c):
    return c.lower() in 'aeiou'

list(filter(vowel, 'Aardvark'))
# ['A', 'a', 'a']
import itertools
list(itertools.filterfalse(vowel, 'Aardvark'))
# ['r', 'd', 'v', 'r', 'k']
list(itertools.dropwhile(vowel, 'Aardvark'))
# ['r', 'd', 'v', 'a', 'r', 'k']
list(itertools.takewhile(vowel, 'Aradvar'))
# ['A']
list(itertools.compress('Aardvark', (1,0,1,1,0,1)))
# ['A', 'r', 'd', 'a']
list(itertools.islice('Aardvark', 4))
# ['A', 'a', 'r', 'd']
list(itertools.islice('Aardvark', 4, 7))
# ['v', 'a', 'r']
list(itertools.islice('Aardvark', 1, 7, 2))
# ['a', 'd', 'a']
```

다음 그룹은 매핑 제네레이터로서, 입력된 반복형(MAP()과 STARMAP()의 경우에는 하나 이상의 반복형)에 들어 잇는 각 항목에 연산을 수행한 결과를 생성한다. 아래 표의 제너레이터 들은 입력된 반복형 안의 항목 하나마다 값 하나를 생성한다. 두 개이상의 반복형을 입력받는 경우에는 반복형 중 하나라도 소진되면 바로 출력을 중단한다.

![gen_mapping사진](https://github.com/hyeonDD/fluent_python/blob/master/Part14/ex14-9/gen_mapping.png)

아래 에제는 itertools.accumulate()의 사용 예를 보여준다.
```
sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
import itertools
list(itertools.accumulate(sample)) #1
# [5, 9, 11, 19, 26, 32, 35, 35, 44, 45] 
list(itertools.accumulate(sample, min)) #2
# [5, 4, 2, 2, 2, 2, 2, 0, 0, 0]
list(itertools.accumulate(sample, max)) #3
# [5, 5, 5, 8, 8, 8, 8, 8, 9, 9]
import operator
list(itertools.accumulate(sample, operator.mul)) #4
# [5, 20, 40, 320, 2240, 13440, 40320, 0, 0, 0]
list(itertools.accumulate(range(1, 11), operator.mul))
# [1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
```
1. 합계를 구한다.
2. 최솟값을 구한다.
3. 최댓값을 구한다.
4. 곱셈을 수행한다.
5. 1!에서 10! 까지 팩토리얼을 구한다.

위 표의 나머지 함수의 사용 예즌 아래의 소스코드와 같다.

```
# 매핑 제너레이터 함수 예
list(enumerate('albatorz', 1)) #1
# [(1, 'a'), (2, 'l'), (3, 'b'), (4, 'a'), (5, 't'), (6, 'o'), (7, 'r'), (8, 'z')]
import operator
list(map(operator.mul, range(11), range(11))) #2
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
list(map(operator.mul, range(11), [2, 4, 8])) #3
# [0, 4, 16]
list(map(lambda a, b: (a, b), range(11), [2, 4, 8])) #4
# [(0, 2), (1, 4), (2, 8)]
import itertools
list(itertools.starmap(operator.mul, enumerate('albatroz', 1))) #5
# ['a', 'll', 'bbb', 'aaaa', 'ttttt', 'rrrrrr', 'ooooooo', 'zzzzzzzz']
sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
list(itertools.starmap(lambda a, b: b/a,
    enumerate(itertools.accumulate(sample), 1))) #6
# [5.0, 4.5, 3.6666666666666665, 4.75, 5.2, 5.333333333333333, 5.0, 4.375, 4.888888888888889, 4.5]
```
다음 그룹은 병합 제너레이터다. 여기에 속한 함수는 여러 반복형을 입력받아서 항목을 생성한다.
chain()과 chain.from_iterable() 제너레이터는 입력받은 반복형을 순차적으로 소비하는 반면, product(), zip(), zip_longest() 제너레이터는 입력받은 반복형을 병렬로 소비한다.

... ~ 이후 14.9 메서드들은 생략 ...