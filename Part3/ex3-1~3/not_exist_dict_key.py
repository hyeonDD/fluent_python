import sys
import re

WORD_RE = re.compile(r'\w+')
index = {}

with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp,1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            print(word)
            column_no = match.start()+1
            location = (line_no,column_no)
            index.setdefault(word, []).append(location) # 키가 있으면 index[word] 를 반환 없다면 index[word] = default로 설정하고 이값을 를 반환해줌
            # index.setdefault(word, []).append(location) 와 같은 코드.. 비효율적이다
            """ occurrences = index.get(word,[]) # word라는 키를 가진 index[word] 를 반환 없다면 default나 None을 반환한다.
            occurrences.append(location)
            index[word] = occurrences """


# 알파벳 순으로출력
for word in sorted(index, key=str.upper): #일급 함수를 사용하는 하나의 예
    print(word, index[word])


