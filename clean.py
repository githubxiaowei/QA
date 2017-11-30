import re
from langconv import *

with open('pages/text_20',encoding='utf8') as f:
	s = f.read()
regs = []
regs.append(re.compile(r'{[{|].*?[|}]}',re.S))
regs.append(re.compile(r'\[http.*?\]'))

s = Converter('zh-hans').convert(s)
for reg in regs:
	s = reg.sub('',s)
print(s)