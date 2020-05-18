
import unicodedata

def codepoints(s):
    hs = 0
    for c in s:
        c = ord(c)
        if 0xdc00 <= c <= 0xdfff and hs:
            yield ((hs&0x3ff)<<10 | (c&0x3ff)) + 0x10000
            hs = 0
        elif 0xd800 <= c <= 0xdbff:
            hs = c
        else:
            yield c
    if hs:
        yield hs


def expandUniCombiningClass(abbr):
    d = {
    '0': 'Spacing, split, enclosing, reordrant, and Tibetan subjoined',
    '1': 'Overlays and interior',
    '7': 'Nuktas',
    '8': 'Hiragana/Katakana voicing marks',
    '9': 'Viramas',
    '10': 'Start of fixed position classes',
    '199': 'End of fixed position classes',
    '200': 'Below left attached',
    '202': 'Below attached',
    '204': 'Below right attached',
    '208': 'Left attached (reordrant around single base character)',
    '210': 'Right attached',
    '212': 'Above left attached',
    '214': 'Above attached',
    '216': 'Above right attached',
    '218': 'Below left',
    '220': 'Below',
    '222': 'Below right',
    '224': 'Left (reordrant around single base character)',
    '226': 'Right',
    '228': 'Above left',
    '230': 'Above',
    '232': 'Above right',
    '233': 'Double below',
    '234': 'Double above',
    '240': 'Below (iota subscript)',
    }
    return d.get(str(abbr), "")


def expandUniDirectionClass(abbr):
    d = {
    'L': 'Left-to-Right',
    'LRE': 'Left-to-Right Embedding',
    'LRO': 'Left-to-Right Override',
    'R': 'Right-to-Left',
    'AL': 'Right-to-Left Arabic',
    'RLE': 'Right-to-Left Embedding',
    'RLO': 'Right-to-Left Override',
    'PDF': 'Pop Directional Format',
    'EN': 'European Number',
    'ES': 'European Number Separator',
    'ET': 'European Number Terminator',
    'AN': 'Arabic Number',
    'CS': 'Common Separator',
    'NSM': 'Non-Spacing Mark',
    'BN': 'Boundary Neutral',
    'B': 'Paragraph Separator',
    'S': 'Segment Separator',
    'WS': 'Whitespace',
    'ON': 'Other Neutrals',
    'FSI': 'First Strong Isolate',
    'PDF': 'Pop Directional Format',
    'PDI': 'Pop Directional Isolate',
    }
    return d.get(abbr, "")


def expandUniCategories(abbr):
    d = {
    'Lu': 'Letter, Uppercase',
    'Ll': 'Letter, Lowercase',
    'Lt': 'Letter, Titlecase',
    'Lm': 'Letter, Modifier',
    'Lo': 'Letter, Other',
    'Mn': 'Mark, Nonspacing',
    'Mc': 'Mark, Spacing Combining',
    'Me': 'Mark, Enclosing',
    'Nd': 'Number, Decimal Digit',
    'Nl': 'Number, Letter',
    'No': 'Number, Other',
    'Pc': 'Punctuation, Connector',
    'Pd': 'Punctuation, Dash',
    'Ps': 'Punctuation, Open',
    'Pe': 'Punctuation, Close',
    'Pi': 'Punctuation, Initial quote (may behave like Ps or Pe depending on usage)',
    'Pf': 'Punctuation, Final quote (may behave like Ps or Pe depending on usage)',
    'Po': 'Punctuation, Other',
    'Sm': 'Symbol, Math',
    'Sc': 'Symbol, Currency',
    'Sk': 'Symbol, Modifier',
    'So': 'Symbol, Other',
    'Zs': 'Separator, Space',
    'Zl': 'Separator, Line',
    'Zp': 'Separator, Paragraph',
    'Cc': 'Other, Control',
    'Cf': 'Other, Format',
    'Cs': 'Other, Surrogate',
    'Co': 'Other, Private Use',
    'Cn': 'Other, Not Assigned (no characters in the file have this property)',
    }
    return d.get(abbr, "")


def expandUniDecompositionClass(abbr):
    d = {
    '<font>': 'A font variant (e.g. a blackletter form).',
    '<noBreak>': 'A no-break version of a space or hyphen.',
    '<initial>': 'An initial presentation form (Arabic).',
    '<medial>': 'A medial presentation form (Arabic).',
    '<final>': 'A final presentation form (Arabic).',
    '<isolated>': 'An isolated presentation form (Arabic).',
    '<circle>': 'An encircled form.',
    '<super>': 'A superscript form.',
    '<sub>': 'A subscript form.',
    '<vertical>': 'A vertical layout presentation form.',
    '<wide>': 'A wide (or zenkaku) compatibility character.',
    '<narrow>': 'A narrow (or hankaku) compatibility character.',
    '<font color=#555555>': 'A small variant form (CNS compatibility).',
    '<square>': 'A CJK squared font variant.',
    '<fraction>': 'A vulgar fraction form.',
    '<compat>': 'Otherwise unspecified compatibility character.',
    }
    return d.get(abbr, "")


def wunichr(dec):
    """Returns the Unicode glyph for a given decimal representation even if Python is not compile in UCS-4"""
    return ("\\U%08X" % dec).decode("unicode-escape")


def wuniord(s):
    if s:
        if u"\udc00" <= s[-1] <= u"\udfff" and len(s) >= 2 and u"\ud800" <= s[-2] <= u"\udbff":
            return (((ord(s[-2])&0x3ff)<<10 | (ord(s[-1])&0x3ff)) + 0x10000)
        return (ord(s[-1]))
    return (-1)


def getNameForRange(dec):
    hexcode = " : U+%04X" % dec
    if 0x3400 <= dec <= 0x4DBF:
        return "CJK UNIFIED IDEOGRAPH" + "-%04X" % dec
    elif 0x4E00 <= dec <= 0x9FFF:
        return "CJK UNIFIED IDEOGRAPH" + "-%04X" % dec
    elif 0xAC00 <= dec <= 0xD7AF: # Hangul
        return unicodedata.name(unichr(dec), hexcode)
    elif 0xD800 <= dec <= 0xDB7F:
        return "Non Private Use High Surrogate" + hexcode
    elif 0xDB80 <= dec <= 0xDBFF:
        return "Private Use High Surrogate" + hexcode
    elif 0xDC00 <= dec <= 0xDFFF:
        return "Low Surrogate" + hexcode
    elif 0xE000 <= dec <= 0xF8FF:
        return "Private Use" + hexcode
    elif 0x20000 <= dec <= 0x2A6DF:
        return "CJK UNIFIED IDEOGRAPH" + "-%04X" % dec
    elif 0x2A700 <= dec <= 0x2B81F:
        return "CJK UNIFIED IDEOGRAPH" + "-%04X" % dec
    elif 0x2B820 <= dec <= 0x2CEAF:
        return "CJK UNIFIED IDEOGRAPH" + "-%04X" % dec
    elif 0x2F800 <= dec <= 0x2FA1F:
        return "CJK COMPATIBILITY IDEOGRAPH" + "-%04X" % dec
    elif 0xF0000 <= dec <= 0xFFFFF:
        return "Supplementary Private Use Area-A" + hexcode
    elif 0x100000 <= dec <= 0x10FFFF:
        return "Supplementary Private Use Area-B" + hexcode
    else:
        return "not defined"


def getBlockName(s):
    if 0x0000 <= s <= 0x007F:
        return "Basic Latin"
    elif 0x0080 <= s <= 0x00FF:
        return "Latin-1 Supplement"
    elif 0x0100 <= s <= 0x017F:
        return "Latin Extended-A"
    elif 0x0180 <= s <= 0x024F:
        return "Latin Extended-B"
    elif 0x0250 <= s <= 0x02AF:
        return "IPA Extensions"
    elif 0x02B0 <= s <= 0x02FF:
        return "Spacing Modifier Letters"
    elif 0x0300 <= s <= 0x036F:
        return "Combining Diacritical Marks"
    elif 0x0370 <= s <= 0x03FF:
        return "Greek and Coptic"
    elif 0x0400 <= s <= 0x04FF:
        return "Cyrillic"
    elif 0x0500 <= s <= 0x052F:
        return "Cyrillic Supplement"
    elif 0x0530 <= s <= 0x058F:
        return "Armenian"
    elif 0x0590 <= s <= 0x05FF:
        return "Hebrew"
    elif 0x0600 <= s <= 0x06FF:
        return "Arabic"
    elif 0x0700 <= s <= 0x074F:
        return "Syriac"
    elif 0x0750 <= s <= 0x077F:
        return "Arabic Supplement"
    elif 0x0780 <= s <= 0x07BF:
        return "Thaana"
    elif 0x07C0 <= s <= 0x07FF:
        return "NKo"
    elif 0x0800 <= s <= 0x083F:
        return "Samaritan"
    elif 0x0840 <= s <= 0x085F:
        return "Mandaic"
    elif 0x0860 <= s <= 0x086F:
        return "Syriac Supplement"
    elif 0x08A0 <= s <= 0x08FF:
        return "Arabic Extended-A"
    elif 0x0900 <= s <= 0x097F:
        return "Devanagari"
    elif 0x0980 <= s <= 0x09FF:
        return "Bengali"
    elif 0x0A00 <= s <= 0x0A7F:
        return "Gurmukhi"
    elif 0x0A80 <= s <= 0x0AFF:
        return "Gujarati"
    elif 0x0B00 <= s <= 0x0B7F:
        return "Oriya"
    elif 0x0B80 <= s <= 0x0BFF:
        return "Tamil"
    elif 0x0C00 <= s <= 0x0C7F:
        return "Telugu"
    elif 0x0C80 <= s <= 0x0CFF:
        return "Kannada"
    elif 0x0D00 <= s <= 0x0D7F:
        return "Malayalam"
    elif 0x0D80 <= s <= 0x0DFF:
        return "Sinhala"
    elif 0x0E00 <= s <= 0x0E7F:
        return "Thai"
    elif 0x0E80 <= s <= 0x0EFF:
        return "Lao"
    elif 0x0F00 <= s <= 0x0FFF:
        return "Tibetan"
    elif 0x1000 <= s <= 0x109F:
        return "Myanmar"
    elif 0x10A0 <= s <= 0x10FF:
        return "Georgian"
    elif 0x1100 <= s <= 0x11FF:
        return "Hangul Jamo"
    elif 0x1200 <= s <= 0x137F:
        return "Ethiopic"
    elif 0x1380 <= s <= 0x139F:
        return "Ethiopic Supplement"
    elif 0x13A0 <= s <= 0x13FF:
        return "Cherokee"
    elif 0x1400 <= s <= 0x167F:
        return "Unified Canadian Aboriginal Syllabics"
    elif 0x1680 <= s <= 0x169F:
        return "Ogham"
    elif 0x16A0 <= s <= 0x16FF:
        return "Runic"
    elif 0x1700 <= s <= 0x171F:
        return "Tagalog"
    elif 0x1720 <= s <= 0x173F:
        return "Hanunoo"
    elif 0x1740 <= s <= 0x175F:
        return "Buhid"
    elif 0x1760 <= s <= 0x177F:
        return "Tagbanwa"
    elif 0x1780 <= s <= 0x17FF:
        return "Khmer"
    elif 0x1800 <= s <= 0x18AF:
        return "Mongolian"
    elif 0x18B0 <= s <= 0x18FF:
        return "Unified Canadian Aboriginal Syllabics Extended"
    elif 0x1900 <= s <= 0x194F:
        return "Limbu"
    elif 0x1950 <= s <= 0x197F:
        return "Tai Le"
    elif 0x1980 <= s <= 0x19DF:
        return "New Tai Lue"
    elif 0x19E0 <= s <= 0x19FF:
        return "Khmer Symbols"
    elif 0x1A00 <= s <= 0x1A1F:
        return "Buginese"
    elif 0x1A20 <= s <= 0x1AAF:
        return "Tai Tham"
    elif 0x1AB0 <= s <= 0x1AFF:
        return "Combining Diacritical Marks Extended"
    elif 0x1B00 <= s <= 0x1B7F:
        return "Balinese"
    elif 0x1B80 <= s <= 0x1BBF:
        return "Sundanese"
    elif 0x1BC0 <= s <= 0x1BFF:
        return "Batak"
    elif 0x1C00 <= s <= 0x1C4F:
        return "Lepcha"
    elif 0x1C50 <= s <= 0x1C7F:
        return "Ol Chiki"
    elif 0x1C80 <= s <= 0x1C8F:
        return "Cyrillic Extended-C"
    elif 0x1C90 <= s <= 0x1CBF:
        return "Georgian Extended"
    elif 0x1CC0 <= s <= 0x1CCF:
        return "Sundanese Supplement"
    elif 0x1CD0 <= s <= 0x1CFF:
        return "Vedic Extensions"
    elif 0x1D00 <= s <= 0x1D7F:
        return "Phonetic Extensions"
    elif 0x1D80 <= s <= 0x1DBF:
        return "Phonetic Extensions Supplement"
    elif 0x1DC0 <= s <= 0x1DFF:
        return "Combining Diacritical Marks Supplement"
    elif 0x1E00 <= s <= 0x1EFF:
        return "Latin Extended Additional"
    elif 0x1F00 <= s <= 0x1FFF:
        return "Greek Extended"
    elif 0x2000 <= s <= 0x206F:
        return "General Punctuation"
    elif 0x2070 <= s <= 0x209F:
        return "Superscripts and Subscripts"
    elif 0x20A0 <= s <= 0x20CF:
        return "Currency Symbols"
    elif 0x20D0 <= s <= 0x20FF:
        return "Combining Diacritical Marks for Symbols"
    elif 0x2100 <= s <= 0x214F:
        return "Letterlike Symbols"
    elif 0x2150 <= s <= 0x218F:
        return "Number Forms"
    elif 0x2190 <= s <= 0x21FF:
        return "Arrows"
    elif 0x2200 <= s <= 0x22FF:
        return "Mathematical Operators"
    elif 0x2300 <= s <= 0x23FF:
        return "Miscellaneous Technical"
    elif 0x2400 <= s <= 0x243F:
        return "Control Pictures"
    elif 0x2440 <= s <= 0x245F:
        return "Optical Character Recognition"
    elif 0x2460 <= s <= 0x24FF:
        return "Enclosed Alphanumerics"
    elif 0x2500 <= s <= 0x257F:
        return "Box Drawing"
    elif 0x2580 <= s <= 0x259F:
        return "Block Elements"
    elif 0x25A0 <= s <= 0x25FF:
        return "Geometric Shapes"
    elif 0x2600 <= s <= 0x26FF:
        return "Miscellaneous Symbols"
    elif 0x2700 <= s <= 0x27BF:
        return "Dingbats"
    elif 0x27C0 <= s <= 0x27EF:
        return "Miscellaneous Mathematical Symbols-A"
    elif 0x27F0 <= s <= 0x27FF:
        return "Supplemental Arrows-A"
    elif 0x2800 <= s <= 0x28FF:
        return "Braille Patterns"
    elif 0x2900 <= s <= 0x297F:
        return "Supplemental Arrows-B"
    elif 0x2980 <= s <= 0x29FF:
        return "Miscellaneous Mathematical Symbols-B"
    elif 0x2A00 <= s <= 0x2AFF:
        return "Supplemental Mathematical Operators"
    elif 0x2B00 <= s <= 0x2BFF:
        return "Miscellaneous Symbols and Arrows"
    elif 0x2C00 <= s <= 0x2C5F:
        return "Glagolitic"
    elif 0x2C60 <= s <= 0x2C7F:
        return "Latin Extended-C"
    elif 0x2C80 <= s <= 0x2CFF:
        return "Coptic"
    elif 0x2D00 <= s <= 0x2D2F:
        return "Georgian Supplement"
    elif 0x2D30 <= s <= 0x2D7F:
        return "Tifinagh"
    elif 0x2D80 <= s <= 0x2DDF:
        return "Ethiopic Extended"
    elif 0x2DE0 <= s <= 0x2DFF:
        return "Cyrillic Extended-A"
    elif 0x2E00 <= s <= 0x2E7F:
        return "Supplemental Punctuation"
    elif 0x2E80 <= s <= 0x2EFF:
        return "CJK Radicals Supplement"
    elif 0x2F00 <= s <= 0x2FDF:
        return "Kangxi Radicals"
    elif 0x2FF0 <= s <= 0x2FFF:
        return "Ideographic Description Characters"
    elif 0x3000 <= s <= 0x303F:
        return "CJK Symbols and Punctuation"
    elif 0x3040 <= s <= 0x309F:
        return "Hiragana"
    elif 0x30A0 <= s <= 0x30FF:
        return "Katakana"
    elif 0x3100 <= s <= 0x312F:
        return "Bopomofo"
    elif 0x3130 <= s <= 0x318F:
        return "Hangul Compatibility Jamo"
    elif 0x3190 <= s <= 0x319F:
        return "Kanbun"
    elif 0x31A0 <= s <= 0x31BF:
        return "Bopomofo Extended"
    elif 0x31C0 <= s <= 0x31EF:
        return "CJK Strokes"
    elif 0x31F0 <= s <= 0x31FF:
        return "Katakana Phonetic Extensions"
    elif 0x3200 <= s <= 0x32FF:
        return "Enclosed CJK Letters and Months"
    elif 0x3300 <= s <= 0x33FF:
        return "CJK Compatibility"
    elif 0x3400 <= s <= 0x4DBF:
        return "CJK Unified Ideographs Extension A"
    elif 0x4DC0 <= s <= 0x4DFF:
        return "Yijing Hexagram Symbols"
    elif 0x4E00 <= s <= 0x9FFF:
        return "CJK Unified Ideographs"
    elif 0xA000 <= s <= 0xA48F:
        return "Yi Syllables"
    elif 0xA490 <= s <= 0xA4CF:
        return "Yi Radicals"
    elif 0xA4D0 <= s <= 0xA4FF:
        return "Lisu"
    elif 0xA500 <= s <= 0xA63F:
        return "Vai"
    elif 0xA640 <= s <= 0xA69F:
        return "Cyrillic Extended-B"
    elif 0xA6A0 <= s <= 0xA6FF:
        return "Bamum"
    elif 0xA700 <= s <= 0xA71F:
        return "Modifier Tone Letters"
    elif 0xA720 <= s <= 0xA7FF:
        return "Latin Extended-D"
    elif 0xA800 <= s <= 0xA82F:
        return "Syloti Nagri"
    elif 0xA830 <= s <= 0xA83F:
        return "Common Indic Number Forms"
    elif 0xA840 <= s <= 0xA87F:
        return "Phags-pa"
    elif 0xA880 <= s <= 0xA8DF:
        return "Saurashtra"
    elif 0xA8E0 <= s <= 0xA8FF:
        return "Devanagari Extended"
    elif 0xA900 <= s <= 0xA92F:
        return "Kayah Li"
    elif 0xA930 <= s <= 0xA95F:
        return "Rejang"
    elif 0xA960 <= s <= 0xA97F:
        return "Hangul Jamo Extended-A"
    elif 0xA980 <= s <= 0xA9DF:
        return "Javanese"
    elif 0xA9E0 <= s <= 0xA9FF:
        return "Myanmar Extended-B"
    elif 0xAA00 <= s <= 0xAA5F:
        return "Cham"
    elif 0xAA60 <= s <= 0xAA7F:
        return "Myanmar Extended-A"
    elif 0xAA80 <= s <= 0xAADF:
        return "Tai Viet"
    elif 0xAAE0 <= s <= 0xAAFF:
        return "Meetei Mayek Extensions"
    elif 0xAB00 <= s <= 0xAB2F:
        return "Ethiopic Extended-A"
    elif 0xAB30 <= s <= 0xAB6F:
        return "Latin Extended-E"
    elif 0xAB70 <= s <= 0xABBF:
        return "Cherokee Supplement"
    elif 0xABC0 <= s <= 0xABFF:
        return "Meetei Mayek"
    elif 0xAC00 <= s <= 0xD7AF:
        return "Hangul Syllables"
    elif 0xD7B0 <= s <= 0xD7FF:
        return "Hangul Jamo Extended-B"
    elif 0xD800 <= s <= 0xDB7F:
        return "High Surrogates"
    elif 0xDB80 <= s <= 0xDBFF:
        return "High Private Use Surrogates"
    elif 0xDC00 <= s <= 0xDFFF:
        return "Low Surrogates"
    elif 0xE000 <= s <= 0xF8FF:
        return "Private Use Area"
    elif 0xF900 <= s <= 0xFAFF:
        return "CJK Compatibility Ideographs"
    elif 0xFB00 <= s <= 0xFB4F:
        return "Alphabetic Presentation Forms"
    elif 0xFB50 <= s <= 0xFDFF:
        return "Arabic Presentation Forms-A"
    elif 0xFE00 <= s <= 0xFE0F:
        return "Variation Selectors"
    elif 0xFE10 <= s <= 0xFE1F:
        return "Vertical Forms"
    elif 0xFE20 <= s <= 0xFE2F:
        return "Combining Half Marks"
    elif 0xFE30 <= s <= 0xFE4F:
        return "CJK Compatibility Forms"
    elif 0xFE50 <= s <= 0xFE6F:
        return "Small Form Variants"
    elif 0xFE70 <= s <= 0xFEFF:
        return "Arabic Presentation Forms-B"
    elif 0xFF00 <= s <= 0xFFEF:
        return "Halfwidth and Fullwidth Forms"
    elif 0xFFF0 <= s <= 0xFFFF:
        return "Specials"
    elif 0x10000 <= s <= 0x1007F:
        return "Linear B Syllabary"
    elif 0x10080 <= s <= 0x100FF:
        return "Linear B Ideograms"
    elif 0x10100 <= s <= 0x1013F:
        return "Aegean Numbers"
    elif 0x10140 <= s <= 0x1018F:
        return "Ancient Greek Numbers"
    elif 0x10190 <= s <= 0x101CF:
        return "Ancient Symbols"
    elif 0x101D0 <= s <= 0x101FF:
        return "Phaistos Disc"
    elif 0x10280 <= s <= 0x1029F:
        return "Lycian"
    elif 0x102A0 <= s <= 0x102DF:
        return "Carian"
    elif 0x102E0 <= s <= 0x102FF:
        return "Coptic Epact Numbers"
    elif 0x10300 <= s <= 0x1032F:
        return "Old Italic"
    elif 0x10330 <= s <= 0x1034F:
        return "Gothic"
    elif 0x10350 <= s <= 0x1037F:
        return "Old Permic"
    elif 0x10380 <= s <= 0x1039F:
        return "Ugaritic"
    elif 0x103A0 <= s <= 0x103DF:
        return "Old Persian"
    elif 0x10400 <= s <= 0x1044F:
        return "Deseret"
    elif 0x10450 <= s <= 0x1047F:
        return "Shavian"
    elif 0x10480 <= s <= 0x104AF:
        return "Osmanya"
    elif 0x104B0 <= s <= 0x104FF:
        return "Osage"
    elif 0x10500 <= s <= 0x1052F:
        return "Elbasan"
    elif 0x10530 <= s <= 0x1056F:
        return "Caucasian Albanian"
    elif 0x10600 <= s <= 0x1077F:
        return "Linear A"
    elif 0x10800 <= s <= 0x1083F:
        return "Cypriot Syllabary"
    elif 0x10840 <= s <= 0x1085F:
        return "Imperial Aramaic"
    elif 0x10860 <= s <= 0x1087F:
        return "Palmyrene"
    elif 0x10880 <= s <= 0x108AF:
        return "Nabataean"
    elif 0x108E0 <= s <= 0x108FF:
        return "Hatran"
    elif 0x10900 <= s <= 0x1091F:
        return "Phoenician"
    elif 0x10920 <= s <= 0x1093F:
        return "Lydian"
    elif 0x10980 <= s <= 0x1099F:
        return "Meroitic Hieroglyphs"
    elif 0x109A0 <= s <= 0x109FF:
        return "Meroitic Cursive"
    elif 0x10A00 <= s <= 0x10A5F:
        return "Kharoshthi"
    elif 0x10A60 <= s <= 0x10A7F:
        return "Old South Arabian"
    elif 0x10A80 <= s <= 0x10A9F:
        return "Old North Arabian"
    elif 0x10AC0 <= s <= 0x10AFF:
        return "Manichaean"
    elif 0x10B00 <= s <= 0x10B3F:
        return "Avestan"
    elif 0x10B40 <= s <= 0x10B5F:
        return "Inscriptional Parthian"
    elif 0x10B60 <= s <= 0x10B7F:
        return "Inscriptional Pahlavi"
    elif 0x10B80 <= s <= 0x10BAF:
        return "Psalter Pahlavi"
    elif 0x10C00 <= s <= 0x10C4F:
        return "Old Turkic"
    elif 0x10C80 <= s <= 0x10CFF:
        return "Old Hungarian"
    elif 0x10D00 <= s <= 0x10D3F:
        return "Hanifi Rohingya"
    elif 0x10E60 <= s <= 0x10E7F:
        return "Rumi Numeral Symbols"
    elif 0x10E80 <= s <= 0x10EBF:
        return "Yezidi"
    elif 0x10F00 <= s <= 0x10F2F:
        return "Old Sogdian"
    elif 0x10F30 <= s <= 0x10F6F:
        return "Sogdian"
    elif 0x10FB0 <= s <= 0x10FDF:
        return "Chorasmian"
    elif 0x10FE0 <= s <= 0x10FFF:
        return "Elymaic"
    elif 0x11000 <= s <= 0x1107F:
        return "Brahmi"
    elif 0x11080 <= s <= 0x110CF:
        return "Kaithi"
    elif 0x110D0 <= s <= 0x110FF:
        return "Sora Sompeng"
    elif 0x11100 <= s <= 0x1114F:
        return "Chakma"
    elif 0x11150 <= s <= 0x1117F:
        return "Mahajani"
    elif 0x11180 <= s <= 0x111DF:
        return "Sharada"
    elif 0x111E0 <= s <= 0x111FF:
        return "Sinhala Archaic Numbers"
    elif 0x11200 <= s <= 0x1124F:
        return "Khojki"
    elif 0x11280 <= s <= 0x112AF:
        return "Multani"
    elif 0x112B0 <= s <= 0x112FF:
        return "Khudawadi"
    elif 0x11300 <= s <= 0x1137F:
        return "Grantha"
    elif 0x11400 <= s <= 0x1147F:
        return "Newa"
    elif 0x11480 <= s <= 0x114DF:
        return "Tirhuta"
    elif 0x11580 <= s <= 0x115FF:
        return "Siddham"
    elif 0x11600 <= s <= 0x1165F:
        return "Modi"
    elif 0x11660 <= s <= 0x1167F:
        return "Mongolian Supplement"
    elif 0x11680 <= s <= 0x116CF:
        return "Takri"
    elif 0x11700 <= s <= 0x1173F:
        return "Ahom"
    elif 0x11800 <= s <= 0x1184F:
        return "Dogra"
    elif 0x118A0 <= s <= 0x118FF:
        return "Warang Citi"
    elif 0x11900 <= s <= 0x1195F:
        return "Dives Akuru"
    elif 0x119A0 <= s <= 0x119FF:
        return "Nandinagari"
    elif 0x11A00 <= s <= 0x11A4F:
        return "Zanabazar Square"
    elif 0x11A50 <= s <= 0x11AAF:
        return "Soyombo"
    elif 0x11AC0 <= s <= 0x11AFF:
        return "Pau Cin Hau"
    elif 0x11C00 <= s <= 0x11C6F:
        return "Bhaiksuki"
    elif 0x11C70 <= s <= 0x11CBF:
        return "Marchen"
    elif 0x11D00 <= s <= 0x11D5F:
        return "Masaram Gondi"
    elif 0x11D60 <= s <= 0x11DAF:
        return "Gunjala Gondi"
    elif 0x11EE0 <= s <= 0x11EFF:
        return "Makasar"
    elif 0x11FB0 <= s <= 0x11FBF:
        return "Lisu Supplement"
    elif 0x11FC0 <= s <= 0x11FFF:
        return "Tamil Supplement"
    elif 0x12000 <= s <= 0x123FF:
        return "Cuneiform"
    elif 0x12400 <= s <= 0x1247F:
        return "Cuneiform Numbers and Punctuation"
    elif 0x12480 <= s <= 0x1254F:
        return "Early Dynastic Cuneiform"
    elif 0x13000 <= s <= 0x1342F:
        return "Egyptian Hieroglyphs"
    elif 0x13430 <= s <= 0x1343F:
        return "Egyptian Hieroglyph Format Controls"
    elif 0x14400 <= s <= 0x1467F:
        return "Anatolian Hieroglyphs"
    elif 0x16800 <= s <= 0x16A3F:
        return "Bamum Supplement"
    elif 0x16A40 <= s <= 0x16A6F:
        return "Mro"
    elif 0x16AD0 <= s <= 0x16AFF:
        return "Bassa Vah"
    elif 0x16B00 <= s <= 0x16B8F:
        return "Pahawh Hmong"
    elif 0x16E40 <= s <= 0x16E9F:
        return "Medefaidrin"
    elif 0x16F00 <= s <= 0x16F9F:
        return "Miao"
    elif 0x16FE0 <= s <= 0x16FFF:
        return "Ideographic Symbols and Punctuation"
    elif 0x17000 <= s <= 0x187FF:
        return "Tangut"
    elif 0x18800 <= s <= 0x18AFF:
        return "Tangut Components"
    elif 0x18B00 <= s <= 0x18CFF:
        return "Khitan Small Script"
    elif 0x18D00 <= s <= 0x18D7F:
        return "Tangut Supplement"
    elif 0x1B000 <= s <= 0x1B0FF:
        return "Kana Supplement"
    elif 0x1B100 <= s <= 0x1B12F:
        return "Kana Extended-A"
    elif 0x1B130 <= s <= 0x1B16F:
        return "Small Kana Extension"
    elif 0x1B170 <= s <= 0x1B2FF:
        return "Nushu"
    elif 0x1BC00 <= s <= 0x1BC9F:
        return "Duployan"
    elif 0x1BCA0 <= s <= 0x1BCAF:
        return "Shorthand Format Controls"
    elif 0x1D000 <= s <= 0x1D0FF:
        return "Byzantine Musical Symbols"
    elif 0x1D100 <= s <= 0x1D1FF:
        return "Musical Symbols"
    elif 0x1D200 <= s <= 0x1D24F:
        return "Ancient Greek Musical Notation"
    elif 0x1D2E0 <= s <= 0x1D2FF:
        return "Mayan Numerals"
    elif 0x1D300 <= s <= 0x1D35F:
        return "Tai Xuan Jing Symbols"
    elif 0x1D360 <= s <= 0x1D37F:
        return "Counting Rod Numerals"
    elif 0x1D400 <= s <= 0x1D7FF:
        return "Mathematical Alphanumeric Symbols"
    elif 0x1D800 <= s <= 0x1DAAF:
        return "Sutton SignWriting"
    elif 0x1E000 <= s <= 0x1E02F:
        return "Glagolitic Supplement"
    elif 0x1E100 <= s <= 0x1E14F:
        return "Nyiakeng Puachue Hmong"
    elif 0x1E290 <= s <= 0x1E2BF:
        return "Toto"
    elif 0x1E2C0 <= s <= 0x1E2FF:
        return "Wancho"
    elif 0x1E800 <= s <= 0x1E8DF:
        return "Mende Kikakui"
    elif 0x1E900 <= s <= 0x1E95F:
        return "Adlam"
    elif 0x1EC70 <= s <= 0x1ECBF:
        return "Indic Siyaq Numbers"
    elif 0x1ED00 <= s <= 0x1ED4F:
        return "Ottoman Siyaq Numbers"
    elif 0x1EE00 <= s <= 0x1EEFF:
        return "Arabic Mathematical Alphabetic Symbols"
    elif 0x1F000 <= s <= 0x1F02F:
        return "Mahjong Tiles"
    elif 0x1F030 <= s <= 0x1F09F:
        return "Domino Tiles"
    elif 0x1F0A0 <= s <= 0x1F0FF:
        return "Playing Cards"
    elif 0x1F100 <= s <= 0x1F1FF:
        return "Enclosed Alphanumeric Supplement"
    elif 0x1F200 <= s <= 0x1F2FF:
        return "Enclosed Ideographic Supplement"
    elif 0x1F300 <= s <= 0x1F5FF:
        return "Miscellaneous Symbols and Pictographs"
    elif 0x1F600 <= s <= 0x1F64F:
        return "Emoticons"
    elif 0x1F650 <= s <= 0x1F67F:
        return "Ornamental Dingbats"
    elif 0x1F680 <= s <= 0x1F6FF:
        return "Transport and Map Symbols"
    elif 0x1F700 <= s <= 0x1F77F:
        return "Alchemical Symbols"
    elif 0x1F780 <= s <= 0x1F7FF:
        return "Geometric Shapes Extended"
    elif 0x1F800 <= s <= 0x1F8FF:
        return "Supplemental Arrows-C"
    elif 0x1F900 <= s <= 0x1F9FF:
        return "Supplemental Symbols and Pictographs"
    elif 0x1FA00 <= s <= 0x1FA6F:
        return "Chess Symbols"
    elif 0x1FA70 <= s <= 0x1FAFF:
        return "Symbols and Pictographs Extended-A"
    elif 0x1FB00 <= s <= 0x1FBFF:
        return "Symbols for Legacy Computing"
    elif 0x20000 <= s <= 0x2A6DF:
        return "CJK Unified Ideographs Extension B"
    elif 0x2A700 <= s <= 0x2B73F:
        return "CJK Unified Ideographs Extension C"
    elif 0x2B740 <= s <= 0x2B81F:
        return "CJK Unified Ideographs Extension D"
    elif 0x2B820 <= s <= 0x2CEAF:
        return "CJK Unified Ideographs Extension E"
    elif 0x2CEB0 <= s <= 0x2EBEF:
        return "CJK Unified Ideographs Extension F"
    elif 0x2F800 <= s <= 0x2FA1F:
        return "CJK Compatibility Ideographs Supplement"
    elif 0x30000 <= s <= 0x3134F:
        return "CJK Unified Ideographs Extension G"
    elif 0xE0000 <= s <= 0xE007F:
        return "Tags"
    elif 0xE0100 <= s <= 0xE01EF:
        return "Variation Selectors Supplement"
    elif 0xF0000 <= s <= 0xFFFFF:
        return "Supplementary Private Use Area-A"
    elif 0x100000 <= s <= 0x10FFFF:
        return "Supplementary Private Use Area-B"
    return "unknown"
