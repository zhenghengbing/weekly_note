# REDIS

### 测试环境

#### redis-python 交互环境

- 安装py-redis `pip install redis`
- python 解释器交互界面 
    ```python
    >>> import redis
    >>> conn = redis.Redis()
    >>> conn.set("foo", "bar")
    >>> conn.get("foo")
    b'bar'
    ```

### 字符串
redis 字符串可以存储【字符串、整数、浮点数】三种类型

#### 键值(VALUE)数值增减操作
> 键：key-name, 键值：value
- INCR: `INCR key-name` == `value+1`
- DECR: `DECR key-name` == `value-1`
- INCRBY: `INCRBY key-name amount` == `value+amount`
- DECRBY: `DECRBY key-name amoutn` == `value-amount`

    ```python
    >>> conn.get('key')  # 如果对一个不存在的key或者key的value为空串
    >>> conn.incr('key') # 那么自增自减操作，redis默认把该key的value作0处理
    1
    >>> conn.incr('key', 15)
    16
    >>> conn.decr('key')
    15
    >>> conn.decr('key', 10)
    5
    ```

#### 键值(VALUE)字符串操作
> 键：key-name, 键值：value
- APPEND: `APPEND key-name v1` == `value+v1`
- GETRANGE: `GETRANGE key-name start end` == `value[start:end]` 包括start和end
- SETRANGE: `SETRANGE key-name offset v1` == `value[offset]=v1`
- GETBIT: `GETBIT key-name offset` == `bytes(value)[offset]`
- SETBIT: `SETBIT key-name offset v1` == `bytes(value)[offset]=v1`
- BITCOUNT: `BITCOUNT key-name [start end]` == `bytes(value)[start:end].count(1)` 
- BITOP: `BITOP operation dest-key keyname [key-name ...] ` 获取多个值，并将值做位运算(operation)，将最后的结果保存至dest-key对应的值.operation,AND/OR/NOT/XOR

    ```python
    >>> conn.append('key-name', 'hello ') # 如果key-name不存在，==conn.set()
    6                                     # 返回值为键值value的长度
    >>> conn.append('key-name', 'world!')
    12 
    >>> conn.getrange('key-name', 3, 7)
    b'lo wo'
    >>> conn.setrange('key-name', 0, 'H')
    12
    >> conn.getrange('key-name', 0, 15)
    b'Hello world!'
    >>> conn.setrange('key-name', 20, 'x')
    21
    ```
    > 使用getrange, getbit时，若offset超出字符串长度，不抛异常，超出字符串的内容视为空串；若使用setrange, setbit时，若offset超出字符串长度，不抛异常，redis会自动使用空字节(null)将字符串扩展至所需长度，然后才执行写入或者更新操作。

### 列表

#### 单列表

- RPUSH: `RPUSH key-name v1 [v2 ...]` 将一个值或多个值推入列表右端
- LPUSH: `LPUSH key-name v1 [v2 ...]` 将一个值或多个值推入列表左侧
- RPOP: `RPOP key-name` 移除并返回列表最右端元素
- LPOP: `LPOP key-name` 移除并返回列表最左端元素
- LINDEX: `LINDEX key-name offset` 返回索引为offset的元素
- LRANGE: `LRANGE key-name start end` 返回列表start-end的元素包含start, end。列表元素不变
- LTRIM: `LTRIM key-name start end` 截取并保留列表start-end之间的元素，包含start,end。列表元素改变。  
    ```python
    >>> conn.rpush('list-key', 'last', 'test')
    1
    >>> conn.lpush('list-key', 'first')
    2
    >>> conn.lrange('list-key', 0, -1)
    [b'first', b'last', b'test']
    >>> conn.lindex('list-key', 0)
    b'first'
    >>> conn.ltrim('list-key', 0, 1)
    True
    >>> conn.lpop('list-key')
    b'first'
    >>> conn.rpop('list-key')
    b'last'
    ```
#### 列表阻塞

- BLPOP: `BLPOP key-name [k1 ...] timeout` 从第一个非空列表弹出位于最左端的元素，或者对于空列表在timeout秒内阻塞弹出元素
- BRPOP: `BRPOP key-name [k1 ...] timeout` 从第一个非空列表弹出位于最右端的元素，或者对于空列表在timeout秒内阻塞弹出元素
- RPOPLPUSH: `RPOPLPUSH source-key dest-key` 从source-key列表弹出位于最右端的元素，然后将这个元素推入dest-key列表的最左端
- BRPOPLPUSH: `BRPOPLPUSH source-key dest-key timeout` 从source-key列表弹出位于最右端的元素，然后将这个元素推入dest-key列表的最左端。如果source-key为空，则在timeout秒内阻塞弹出元素
    ```python
    >>> conn.rpush('list1', 'v1', 'v2')
    2
    >>> conn.rpush('list2', 'v3')
    1
    >>> conn.brpoplpush('list1', 'list2', 1)
    b'v3'
    >>> conn.brpoplpush('list2', 'list1', 1)
    b'v2'
    >>> conn.lrange('list2', 0, -1)
    [b'v3', b'v1']
    >>> conn.blpop(['list1', 'list2'], 1) # 第一个非空列表弹出元素
    (b'list1', b'v2')
    >>> conn.blpop(['list1', 'list2'], 1)
    (b'list2', b'v3')
    >>> conn.blpop(['list1', 'list2'], 1)
    (b'list2', b'v1')
    >>> conn.blpop(['list1', 'list2'], 1) # 如果列表为空，在1秒内阻塞等待
    >>>
    ```

### 集合

#### 单集合

- SADD: `SADD key-name v1 [v2 ...]` 将一个或者多个元素添加到集合
- SREM: `SREM key-name v1 [v2 ...]` 从一个集合移除一个或者多个元素
- SISMEMBER: `SISMEMBER key-name v1` 检查元素v1是否在集合中
- SCARD: `SCARD key-name` 返回集合包含的元素的数量
- SMEMBERS: `SMEMBERS key-name` 返回集合包含的所有元素
- SRANDMEMBER: `SRANDMEMBER key-name [count]` 从集合里面随机返回一个或者多个元素，当count为正数时，返回的元素不会重复，当count为负数时，返回的随机数可能会重复
- SPOP: `SPOP key-name` 随机移除集合一个元素，并返回被移除的元素
- SMOVE: `SMOVE source-key dest-key v1` 如果source-key集合包含元素v1,那么从集合source-key移除元素v1，并将v1添加到dest-key中。
    ```python
    >>> conn.sadd('set1', 'a', 'b', 'c')
    3
    >>> conn.srem('set1', 'c', 'd')
    True
    >>> conn.scard('set1')
    2
    >>> conn.smembers('set1')
    {b'a', b'b'}
    >>> conn.smove('set1', 'set2', 'a')
    True
    >>> conn.smemebers('set2')
    {b'a'}
    ```

#### 多集合
- SDIFF: `SDIFF key-name [key-name ...]` == set1-set2(差集)
- SDIFFSTORE: `SDIFFSTORE dest-key key-name [key-name ...]` == set1=(set2-set3)(差集转存)
- SINTER: `SINTER key-name [key-name ...]` == set1&set2(交集)
- SINTERSTORE: `SINTERSTORE dest-key key-name [key-name ...]` == set1=set2&set3(交集转存)
- SUNION: `SUNION key-name [key-name ...]` == set1|set2(并集)
- SUNIONSTORE: `SUNIONSTORE dest-key key-name [key-name ...]` == set1=set2|set3(并集转存)
    ```python
    >>> conn.sadd('skey1', 'a', 'b', 'c', 'd')
    4
    >>> conn.sadd('skey2', 'c', 'd', 'e', 'f')
    4
    >>> conn.sdiff('skey1', 'skey2')
    {b'a', b'b'}
    >>> conn.sinter('skey1', 'skey2')
    {b'd', b'c'}
    >>> conn.sunion('skey1', 'skey2')
    {b'e', b'a', b'f', b'b', b'd', b'c'}
    ```

### 散列

#### 键值对操作
- HMGET: `HMGET key-name key [key ...]` 从一个散列中获取一个或多个键的值
- HMSET: `HMSET key-name key value  [key value, ...]` 为散列里一个或多个键设置值
- HDEL: `HDEL key-name key [key ...]` 删除散列里面的一个或多个键值对
- HLEN: `HLEN key-name` 返回散列包含的键值对数量
    ```python
    >>> conn.hmset('hash-key', {'k1':'v1', 'k2':'v2', 'k3':'v3'})
    True
    >>> conn.hmget('hash-key', ['k1', 'k2'])
    [b'v1', b'v2']
    >>> conn.hlen('hash-key')
    3
    >>> conn.hdel('hash-key', 'k1', 'k2')
    2
    ```

#### 复杂操作
- HEXISTS: `HEXISTS key-name key` 检查给定键是否存在散列中
- HKEYS: `HKEYS key-name` 获取散列包含的所有键
- HVALS: `HVALS key-name` 获取散列包含的所有值
- HGETALL: `HGETALL key-name` 获取散列包含的所有键值对
- HINCRBY: `HINCRBY key-name key increment` 将key保存的值加上整数increment
- HINCRBYFLOAT: `HINCRBYFLOAT key-name key increment` 将key保存的值加上浮点数increment
  ```python
  >>> conn.hmset('hash-key2', {'k1':'v1', 'k2':1000*'v2'})
  True
  >>> conn.hkeys('hash-key2')
  [b'k1', b'k2']
  >>> conn.hexists('hash-key2', 'num')
  False
  >>> conn.hincrby('hash-key2', 'num', 2)
  2
  ```