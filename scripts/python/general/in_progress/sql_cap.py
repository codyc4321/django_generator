#!/user/bin/env python


current_point = 0

sql_list = ['if','then', 'while', 'select', 'distinct', 'and', 'or', 'between', 'like', 'join', 'from', 'inner', 'left',
            'right', 'full', 'union', 'not', 'null', 'primary', 'key', 'set', 'use', 'database', 'variable', 'table',
            'truncate', 'as', 'group', 'by', 'on', 'into', 'alter', 'default', 'identity', 'constraint',   ]



sql_dict = {'if': 'IF', 'then': 'IF', 'while': 'IF', 'select': 'IF', 'distinct': 'IF', 'and': 'IF', 'or': 'IF', 'between': 'IF', 'in': 'IF',
            'like': 'IF', 'if': 'IF', 'if': 'IF', 'if': 'IF', 'if': 'IF', 'if': 'IF', 'if': 'IF', 'if': 'IF', 'if': 'IF',}


commands_insert = "|".join(sql_list)


To find lower case commands:

find_regex = "\b(?=%s))(?P<command>[a-z]+)\b" % commands_insert

replace if|not|select with a variable that is a join of all commands in sql_list





In [25]: x = "if then(stuff)"

m = re.search("(^|\s|[.()*])(?P<command>[a-z]+)(\s|[.*()])", x)


In [43]: m.group('command')
Out[43]: 'if'

In [44]: m.start('command')
Out[44]: 0

In [45]: m.end('command')
Out[45]: 2

go one by one, updating current start point with the new m.end('command')