import operator
ops = {
    'eq':operator.eq,
    'ne':operator.ne,
    'lt':operator.lt,
    'gt':operator.gt,
    'le':operator.le,
    'ge':operator.ge
}


def search(data,query):

    key, op, typ, val = query.split(':', 3)
    if typ=='int':
        val = float(val)
    elif typ == 'bool':
        val = bool(val)
    op = ops[op]
    for d in data:
        d = data[d]
        if op(d.get(key, None), val):
            yield d

def search_list(data, query):
    op, typ,val  = query.split(':', 2)
    op = ops[op]
    if typ=='int':
        val = float(val)
    elif typ=='bool':
        val = bool(val)

    for d in data:
        if op(d, val):
            yield d



