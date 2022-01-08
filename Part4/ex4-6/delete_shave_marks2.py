import unicodedata
import string

def shave_marks(txt):
    """라틴 기반 문자에서 발음 구별 기호를 모두 제거한다."""
    norm_txt = unicodedata.normalize('NFD',txt)
    latin_base = False
    keepers = []
    for c in norm_txt:
        if unicodedata.combining(c) and latin_base:
            continue # 라틴 기반 문자의 발음 구별 기호를 무시한다.
        keepers.append(c)
        # 결합 문자가 아니면, 이 문자를 새로운 기반 문자로 간주한다.
        if not unicodedata.combining(c):
            latin_base = c in string.ascii_letters
    shaved = ''.join(keepers)
    return unicodedata.normalize('NFC',shaved)
order = '“Herr Voß: • ½ cup of Œtker™ caffè latte • bowl of açaí.”'
print(shave_marks(order))
greek = 'Ζέφυρος, Zéfiro'
print(shave_marks(greek))

"""
발음기호 제거 (너무 심하게 제거한다.)
order = '“Herr Voß: • ½ cup of Œtker™ caffè latte • bowl of açaí.”'
print(shave_marks(order))
greek = 'Ζέφυρος, Zéfiro'
print(shave_marks(greek))
"""



"""
Radical folding and text sanitizing.

Handling a string with `cp1252` symbols:

order = '“Herr Voß: • ½ cup of Œtker™ caffè latte • bowl of açaí.”'
print(shave_marks(order))    
print(shave_marks_latin(order))    
print(dewinize(order))

    '"Herr Voß: - ½ cup of OEtker(TM) caffè latte - bowl of açaí."'
    >>> asciize(order)
    '"Herr Voss: - 1⁄2 cup of OEtker(TM) caffe latte - bowl of acai."'

Handling a string with Greek and Latin accented characters:

greek = 'Ζέφυρος, Zéfiro'
print(shave_marks(greek))    
print(shave_marks_latin(greek))
print(dewinize(greek))
print( asciize(greek))    
"""