def tag(name, *content, cls=None, **attrs):
    """하나 이상의 HTML 태그를 생성한다."""
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value)
                            for attr, value
                            in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' %
                            (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)

print(tag('br'))
print(tag('p','hello'))
print(tag('p','hello','world'))
print(tag('p','hello', id=33)) # tag 시그니처에 명시적으로 이름이 지정되지 않은 키워드 인수들은 딕셔너리로 **attrs 인수에 전달된다.
print(tag('p','hello','world',cls='sidebar')) # cls 매개변수만 키워드 인수로 전달된다.
print(tag(content='testing',name="img")) # 첫 번째 위치 인수도 tag가 호출되면 키워드로 전달할 수 있다.
my_tag = {'name':'img', 'title':'Sunset Boulevard',
          'src':'sunset.jpg','cls':'framed'}
print(tag(**my_tag)) # my_tag 딕셔너리 앞에 **를 붙이면 딕셔너리 안의 모든 항목을 별도의 인수로 전달하고, 명명된 매개변수 및 나머지는 **attrs에 전달된다.