# REDIS

### Redis五大数据结构
#### STRING

- 结构存储的值：字符串、整数、浮点数；数字支持自增自减。
- GET 获取存储在给定键中的值 `>set key value`
- SET 设置存储在给定键中的值 `>get key`
- DEL 删除存储在给定键中的值（适用所有命令）`>del key`
#### LIST

- 结构存储的值：一个链表，节点包含字符串。
- RPUSH/LPUSH 将给定值推入列表右端/左端 `>rpush list-key item`
- LRANGE 获取列表在给定范围上的所有值 `>lrange list-key 0 -1`
- LINDEX 获取列表在给定位置上的单个元素 `>lindex list-key 0`
- LPOP/RPOP 从列表的左端/右端弹出一个值，并返回弹出的值 `>lpop list-key`
#### SET

- 结构存储的值：包含无序的字符串，且字符串具有唯一性 。
- SADD 将给定元素添加到集合 `>sadd set-key item`
- SMEMBERS 返回集合包含的所有元素 `>smembers set-key`
- SISMEMBER 检查给定元素是否存在于集合中 `>sismember set-key item`
- SREM 如果给定的元素在集合中，那么移除这个元素 `>srem set-key item`
- SINTER 计算两个集合的交集 `>sinter set-key1 set-key2`
- SUNION 计算两个集合并集 `>sunion set-key1 set-key2`
- SDIFF 计算两个集合差集 `>sdiff set-key1 set-key2`
#### HASH

- 结构存储的值：包含键值对的无序散列表，散列存储的值可为字符串、整数、浮点数；数字支持自增自减。
- HSET 在散列里面关联起给定的键值对 `>hset hash-key sub-key value`
- HGET 获取指定散列键的值 `>hget hash-key sub-key value`
- HGETALL 获取散列包含的所有键值对 `>hgetall hash-key `
- HDEL 如果给定键存在于散列里面，那么移除这个键 `>hdel hash-key sub-key`
#### `ZSET`

- 结构存储的值：字符串成员(member)与浮点数分值(score)之间的有序映射，元素的排列顺序由分值(score)的大小决定；member具有唯一性，score必须为浮点数。redis中唯一一个既可以根据成员访问元素（如散列），又可以根据分值以及分值的排列顺序来访问元素的结构。
- ZADD 将一个带有给定分值的成员添加到有序集合里面 `>zadd zset-key 234 member0`
- ZRANGE 根据元素在有序排列中所处的位置，从有序集合里面获取多个元素 `>zrange zset-key 0 -1 withscores`
- ZRANGEBYSCORE 获取有序集合在给定分值范围内的所有元素 `>zrangebyscore zset-key 234 255 withscores`
- ZREM 如果给定成员存在于有序集合，那么移除这个成员 `>zrem zset-key membre0`







