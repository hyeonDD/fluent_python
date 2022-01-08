import unicodedata
import string

def shave_marks(txt):
    """발음 구별 기호를 모두 제거한다."""
    norm_txt = unicodedata.normalize('NFD',txt)
    shaved = ''.join(c for c in norm_txt
                     if not unicodedata.combining(c))
    return unicodedata.normalize('NFC',shaved)
"""
발음기호 제거 (너무 심하게 제거한다.)
order = '“Herr Voß: • ½ cup of Œtker™ caffè latte • bowl of açaí.”'
print(shave_marks(order))
greek = 'Ζέφυρος, Zéfiro'
print(shave_marks(greek))
"""