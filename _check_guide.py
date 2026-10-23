import re, glob
p = 'content/guides/ai-study-abroad-application-guide.md'
t = open(p, encoding='utf-8').read()
body = t.split('---', 2)[2]
cn = len(re.findall(r'[\u4e00-\u9fa5]', body))
print('中文字数:', cn, '| 总字符:', len(body))
titles = []
for f in glob.glob('content/guides/*.md') + glob.glob('content/reviews/*.md'):
    for line in open(f, encoding='utf-8'):
        if line.startswith('title:'):
            titles.append((f, line.strip()))
dups = [x for x in titles if '留学' in x[1]]
print('含"留学"标题数:', len(dups))
for d in dups:
    print(' ', d)
