import re
a='https://csgo.fastcup.net/match4213265/stats'

result = re.findall(r"match(.*?)/", a)
print (result)