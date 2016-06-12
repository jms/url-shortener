class UrlShortener:
    def __init__(self):
        self.alphabet = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ_abcdefghijkmnopqrstuvwxyz'

    def encode(self, url_id):
        return self.numtosxg(url_id)

    def decode(self, code):
        return self.sxgtonum(code)

    # http://faruk.akgul.org/blog/tantek-celiks-newbase60-in-python-and-java/
    # encode number to base60
    def numtosxg(self, n):
        s = ''
        char_list = self.alphabet
        if not isinstance(n, (int, long)) or n == 0:
            return '0'
        while n > 0:
            n, i = divmod(n, 60)
            s = char_list[i] + s
        return s

    # number to base60, padding chars (string length)
    def numtosxgf(self, n, f):
        s = self.numtosxg(n)
        if not isinstance(f, (int, long)):
            f = 1
        f -= len(s)
        while f > 0:
            s = '0' + s
            f -= 1
        return s

    # convert string to number base60
    @staticmethod
    def sxgtonum(s):
        n = 0
        j = len(s)
        for i in xrange(0, j):
            c = ord(s[i])
            if 48 <= c <= 57:
                c -= 48
            elif 65 <= c <= 72:
                c -= 55
            elif c == 73 or c == 108:  # typo capital I, lowercase l to 1
                c = 1
            elif 74 <= c <= 78:
                c -= 56
            elif c == 79:  # error correct typo capital O to 0
                c = 0
            elif 80 <= c <= 90:
                c -= 57
            elif c == 95:
                c = 34
            elif 97 <= c <= 107:
                c -= 62
            elif 109 <= c <= 122:
                c -= 63
            else:
                c = 0  # treat all other noise as 0
            n = 60 * n + c

        return n
