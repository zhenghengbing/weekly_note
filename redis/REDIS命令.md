# REDIS

### 测试环境

#### redis-python 交互环境

- 安装py-redis `pip install redis`
- python 解释器交互界面 
    ```python
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
    10
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