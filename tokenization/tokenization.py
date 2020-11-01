import re
from collections import namedtuple

class Tokenizer:

    Token = namedtuple('Token', 'name text span')

    def __init__(self, tokens):
        self.tokens = tokens
        pat_list = []
        for tok, pat in self.tokens:
            pat_list.append('(?P<%s>%s)' % (tok, pat))
            self.re = re.compile('|'.join(pat_list))

    def iter_tokens(self, input, ignore_ws=True):
        for match in self.re.finditer(input):
            if ignore_ws and match.lastgroup == 'WHITESPACE':
                continue
            yield Tokenizer.Token(match.lastgroup, match.group(0), match.span(0))
    
    def iter_sentences(self, input, ignore_ws=True):
        for sentence in re.compile('[.;!?] ').split(input):
            yield ('SENTENCE', list(self.iter_tokens(sentence, ignore_ws)))
            
    def tokenize(self, input, ignore_ws=True):
        return list(iter_sentences(input, ignore_ws))

# test program
if __name__ == "__main__":

    TOKENS = [
        ('NIL'        , r"nil|\'()"),
        ('TRUE'       , r'true|#t'),
        ('FALSE'      , r'false|#f'),
        ('NUMBER'     , r'\d+'),
        ('STRING'     , r'"(\\.|[^"])*"'),
        ('WORD'     , r'[A-ZĄĆĘŁŃÓŚŹŻa-ząćęłńóśźż]+'),
        ('QUOTE'      , r"'"),
        ('LPAREN'     , r'\('),
        ('RPAREN'     , r'\)'),
        ('DOT'        , r'\.'),
        ('WHITESPACE' , r'\w+'),
    ]

    for t in Tokenizer(TOKENS).iter_sentences('Linux 5.9 miał być mniejszą aktualizacją niż ostatecznie jest. Na większą liczbę nowinek nikt chyba jednak nie będzie narzekać. Szczególnie, że są to nowinki nie bez znaczenia, takie jak (dodana po ponad 5 latach prób) obsługa FSGSBASE, oznaczająca spory wzrost wydajności – zarówno w przypadku platform opartych na procesorach Intela, jak i tych, których sercami są układy AMD. Najbardziej odczujesz to w sytuacjach dużego obciążenia.'):
        print(t)