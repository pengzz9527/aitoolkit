import urllib.request
from html.parser import HTMLParser

class GHParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_article = False
        self.in_h2 = False
        self.in_p = False
        self.in_a = False
        self.results = []
        self.current_repo = ''
        self.current_desc = ''
        self.current_lang = ''
        self.current_stars = ''
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get('class','')
        if tag == 'article' and 'Box-row' in cls:
            self.in_article = True
            self.current_repo = ''
            self.current_desc = ''
            self.current_lang = ''
            self.current_stars = ''
        if self.in_article:
            if tag == 'h2':
                self.in_h2 = True
            elif tag == 'p':
                self.in_p = True
            elif tag == 'a':
                self.in_a = True
            elif tag == 'span':
                if 'repo-language-color' in cls or 'd-inline' in cls:
                    self.current_lang = attrs_dict.get('aria-label','')
                if 'float-sm-right' in cls:
                    self.current_stars = attrs_dict.get('aria-label','')
                    
    def handle_data(self, data):
        if self.in_article and (self.in_h2 or self.in_p or self.in_a):
            text = data.strip()
            if text:
                if self.in_h2:
                    self.current_repo += text
                elif self.in_p:
                    self.current_desc += text
                elif self.in_a:
                    self.current_repo += text
                    
    def handle_endtag(self, tag):
        if tag == 'h2': self.in_h2 = False
        elif tag == 'p': self.in_p = False
        elif tag == 'a': self.in_a = False
        elif tag == 'article':
            if self.current_repo:
                self.results.append((self.current_repo.strip(), self.current_desc.strip()[:150], self.current_lang, self.current_stars))
            self.in_article = False

html = urllib.request.urlopen("https://github.com/trending?since=daily&spoken_language_code=en").read().decode('utf-8')
parser = GHParser()
parser.feed(html)
for i, (repo, desc, lang, stars) in enumerate(parser.results[:25], 1):
    print(f'{i}. {repo} | {lang} | {stars} | {desc}')
