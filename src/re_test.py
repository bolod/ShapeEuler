import re

s1 = ' a   '
rel = re.findall('([a-z]|[A-Z]|[0-9])+', s1)

if not(rel) or True:
    print 'yes', rel

else:
    print 'no', rel
