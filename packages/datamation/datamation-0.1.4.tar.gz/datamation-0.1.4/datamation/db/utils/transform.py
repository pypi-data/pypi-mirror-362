
import uuid
import datetime
import itertools
import functools
import operator
import collections
import sys

__all__=['Tint','Tstr','Tfloat','Tbool','Tupper','Tlower','Filterfalse','Filtertrue','First_true',
         'Transform','Tpairwise_seq','Mergejoin','Hashkjoin','Join','Prepend','Tsplitchunk','Filter_dict']

Filterfalse = itertools.filterfalse
Filtertrue = filter
Transform = map
eq = operator.eq

def First_true(iterable,pred=None,default=False):
    return next(filter(pred, iterable), default)

def Tsplitchunk(start,end,num_blocks=None,chunk_size=None):
    """Split a range into a list of ranges.
    example:
    Tsplitchunk(0,100,num_blocks=10) -> [(0,10),(10,20),(20,30),...,(90,100)]
    """
    if not num_blocks and not chunk_size:
        raise ValueError("num_blocks or chunk_size must be specified")
                
    if num_blocks:
        if (end-start)<=num_blocks:
            num_blocks = 1
        else:
            num_blocks = int((end-start)/num_blocks)
        return Tpairwise_seq(list(range(start,end,num_blocks)) +[end] )
    else:
        num_blocks = int(int((end-start)/chunk_size))
        return Tpairwise_seq(list(range(start,end,num_blocks)) +[end])

def Tpairwise_seq(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return list(zip(a, b))

def Prepend(value, iterator):
    "Prepend a single value in front of an iterator"
    # prepend(1, [2, 3, 4]) -> 1 2 3 4
    return itertools.chain([value], iterator)

def dict_compare(x, y, key_maps = {},compare_keys=[]):
    if compare_keys:
        if key_maps:
            return all(x[key] ==y[key_maps.get(key,key)] for key in compare_keys)
        else:
            return all(x[key] ==y[key] for key in compare_keys)
    else:
        if key_maps:
            return all(x[key] == y[key_maps.get(key,key)] for key in x.keys())
        else:
            return all(x[key] == y[key] for key in x.keys())

def Mergejoin(src1,src2,join_keys = {}):
    """
    Mergejoin([{'a':1,'b':2}], [{'a':1,'c':3}]) -> [{'a':1,'b':2,'c':3}]
    """
    # 获取join_keys的键
    compare_keys = list(join_keys.keys())
    # 遍历src1中的每个元素
    for x in src1:
        # 使用functools.partial函数创建一个部分函数，用于比较x和src2中的元素
        f = functools.partial(dict_compare,x,key_maps = join_keys,compare_keys=compare_keys)
        # 使用First_true函数找到src2中第一个满足条件的元素
        y = First_true(src2,f)
        # 如果找到了满足条件的元素，则使用collections.ChainMap函数将x和y合并，并返回
        if y:
            yield collections.ChainMap(x,y)

def Hashkjoin(src1,src2,keys = {}):
    """
    Hashkjoin([{'a':1,'b':2}], [{'a':1,'c':3}]) -> [{'a':1,'b':2,'c':3}]
    """
    src1_keys = keys.keys()
    src2_keys = keys.values()
    _hash = collections.defaultdict(list)
    for row in src2:
        _hash[hash(tuple(v for k,v in row.items() if k in src2_keys))].append(row)

    for row in src1:
        for row_src2 in _hash[hash(tuple(v for k,v in row.items() if k in src1_keys))]:
            yield collections.ChainMap(row,row_src2)

Join = Hashkjoin

def T(function,v,default = None):
    try:
        return function(v)
    except (ValueError,TypeError):
        if not default:
            default = v
        return default

Tint = functools.partial(T,int)
Tstr = functools.partial(T,str)
Tfloat = functools.partial(T,float)
Tbool = functools.partial(T,bool)
Tupper = functools.partial(T,operator.methodcaller('upper'))
Tlower = functools.partial(T,operator.methodcaller('lower'))
Tstrip = functools.partial(T,operator.methodcaller('strip'))

def Filter_dict(d,keys):
    """extract_dict({'a':1,'b':2},['a']) -> {'a':1}
    """
    return dict(tuple((k,v) for k,v in d.items() if k in keys))
