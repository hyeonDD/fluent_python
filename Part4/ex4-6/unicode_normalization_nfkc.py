from unicodedata import normalize, name
half = '½'
print(normalize('NFKC', half))

four_squared = '42'
print(normalize('NFKC', four_squared))

micro = 'µ'
micro_kc = normalize('NFKC',micro)
print(micro,micro_kc)

print(ord(micro),ord(micro_kc))
print(name(micro),name(micro_kc))