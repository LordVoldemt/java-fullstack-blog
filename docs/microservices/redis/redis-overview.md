# Redis 入门：缓存、分布式锁、排行榜 到底怎么用，为什么很多项目离不开它

<a class="presentation-link" href="../../presentations/redis-overview-ppt" target="_blank" rel="noopener">
  <span class="presentation-link__icon" aria-hidden="true">
    <span class="presentation-link__glyph">PPT</span>
  </span>
  <span>
    <strong>打开文章演示版</strong>
    <small>浏览器幻灯片版速览，支持方向键和空格切换</small>
  </span>
</a>

只要你做过稍微复杂一点的后端项目，大概率都会接触 `Redis`。

有人把它当缓存，有人拿它做计数器，有人用它做排行榜、会话存储、分布式锁，甚至有人拿它做消息队列和延迟任务。

它之所以常见，不只是因为“快”，更因为它刚好补上了传统数据库在高并发读写场景中的很多短板。

但 Redis 也是一个非常容易“看起来会用，实际上隐患不少”的组件。很多项目在刚开始引入 Redis 时都很顺手：查数据库前先查缓存，查不到再回源，逻辑一写就完。可一旦流量上来、数据一致性变复杂、缓存失效策略不清晰、并发打满，问题也会迅速浮现出来。

这篇文章会用更适合初学者的方式，帮你从工程角度重新认识 Redis：它到底解决了什么问题、有哪些最核心的使用模式、在 Java 项目里怎么写，以及有哪些高频坑必须早点建立直觉。

## Redis 是干嘛的

如果用最直白的话来讲，Redis 是一个**高性能的内存数据结构服务**。

你可以把它理解成：

- 不是替代数据库
- 而是给数据库和应用之间增加一层“更快、更轻量”的能力

它最常见的用途包括：

- 做缓存
- 做计数器
- 做排行榜
- 做分布式锁
- 做共享状态存储

## Redis 适合在哪些场景用

它特别适合这些高频场景：

- 商品详情、用户信息这类高频查询数据
- 登录状态、验证码、token 等短期状态
- 点赞数、浏览量、库存计数
- 热门排行榜
- 防止重复提交、分布式锁

✅ **建议**：初学者先把 Redis 理解成“高性能状态层”，比只记命令更有用。

## 先把地图看清：Redis 主要解决什么问题

| 场景 | Redis 在解决什么问题 | 你可以怎么理解 |
|---|---|---|
| 缓存 | 降低数据库压力 | 给热点数据加速 |
| 计数器 | 高并发统计 | 用内存快速计数 |
| 排行榜 | 排序和分数计算 | 高效有序集合 |
| 分布式锁 | 跨服务互斥控制 | 全局资源门锁 |
| 共享状态 | 多实例之间共享轻量数据 | 公共内存层 |

如果你先记住这张表，后面看 Redis 的各种用法就不容易乱。

## Redis 为什么快

很多文章提到 Redis，第一句话就是“Redis 很快”。这当然没错，但如果不继续问“为什么快”，这个认知就非常浅。

Redis 的快，主要来自几个方面：

- 基于内存操作
- 数据结构设计简单直接
- 单线程模型避免了大量上下文切换和锁竞争
- 网络模型和实现细节足够高效

你可以把它类比成：

- 数据库像一个大仓库，东西很多，很稳
- Redis 像一个前台小货架，只放高频要用的东西，拿取速度极快

⚠️ **重点**：Redis 快，不只是因为“内存在磁盘之上”，更因为它的设计目标就是高频读写场景下的极简高效。

## Redis 不只是 Key-Value：它还有不同数据结构

很多人第一次使用 Redis，会把它理解成“一个能存字符串的缓存”。可真正的 Redis 能力远不止于此。

它常见的数据结构包括：

- `String`
- `Hash`
- `List`
- `Set`
- `Sorted Set`

这些结构不是为了“让 API 更丰富”，而是为了让你用更接近业务语义的方式建模。

例如：

- 用户会话信息可以用 `Hash`
- 点赞用户集合可以用 `Set`
- 排行榜可以用 `Sorted Set`
- 简单计数器可以用 `String`

## 缓存：Redis 最常见、也最容易被低估的用法

在大多数系统里，Redis 首先是缓存。缓存最直接的目标是：

- 减轻数据库压力
- 降低响应时间

最常见的缓存模型通常是：

1. 先查 Redis
2. 命中则直接返回
3. 未命中则查数据库
4. 再把结果写回 Redis

### 最小缓存流程图

```text
用户请求 → 查 Redis
           ├─ 命中 → 直接返回
           └─ 未命中 → 查数据库 → 写回 Redis → 返回
```

看起来很简单，但真正难的是缓存策略，而不是“有没有查 Redis”。

你需要至少想清楚：

- 什么数据适合缓存
- 缓存多久
- 缓存失效后怎么回源
- 更新数据库后缓存如何同步处理

## 实战示例一：查询用户缓存

下面用一个简化版 Java 示例说明“查缓存再查数据库”。

```java
import java.util.HashMap;
import java.util.Map;

public class RedisCacheDemo {

    // 用 Map 模拟 Redis
    private static final Map<String, String> redisCache = new HashMap<>();

    // 用 Map 模拟数据库
    private static final Map<Long, String> database = new HashMap<>();

    static {
        database.put(1L, "Tom");
        database.put(2L, "Alice");
    }

    public static String getUserName(Long userId) {
        String key = "user:" + userId;

        // 第一步：先查缓存
        String cachedValue = redisCache.get(key);
        if (cachedValue != null) {
            System.out.println("命中 Redis 缓存");
            return cachedValue;
        }

        // 第二步：缓存没命中，查数据库
        System.out.println("缓存未命中，查询数据库");
        String dbValue = database.get(userId);

        // 第三步：数据库查到后写回缓存
        if (dbValue != null) {
            redisCache.put(key, dbValue);
        }

        return dbValue;
    }

    public static void main(String[] args) {
        System.out.println(getUserName(1L));
        System.out.println(getUserName(1L));
    }
}
```

### 这个例子在表达什么

- 第一次查：走数据库
- 第二次查：直接走缓存

真实项目里虽然不会这么手写 `Map` 模拟 Redis，但思路就是这个思路。

## 缓存穿透、击穿、雪崩：为什么缓存系统也会把数据库打挂

只要系统规模稍微上来，缓存相关问题几乎一定会被提到。

最典型的三个概念是：

- 缓存穿透
- 缓存击穿
- 缓存雪崩

### 缓存穿透

请求的数据本身就不存在，缓存里没有，数据库里也没有。大量这类请求会持续打到数据库。

#### 常见例子

比如有人不断请求一个根本不存在的用户 `userId=99999999`。

#### 常见解决思路

- 缓存空值
- 参数校验
- 布隆过滤器

### 缓存击穿

某个热点 key 在某一刻失效了，大量请求同时回源数据库，导致数据库压力陡增。

#### 常见例子

热门商品详情是热点 key，刚好过期，大量请求同时打进来。

#### 常见解决思路

- 热点 key 永不过期或逻辑过期
- 加互斥锁控制重建

### 缓存雪崩

大量 key 在某一时间段集中失效，导致大面积请求回源，数据库承压严重。

#### 常见解决思路

- 过期时间加随机值
- 多级缓存
- 限流降级

⚠️ **重点**：缓存不是“加一层就更稳”，缓存本身也有系统性风险。

## 实战示例二：订单场景里的库存缓存

假设你在做一个商品详情页，库存和价格查询非常频繁，这时可以考虑缓存。

流程：

1. 用户访问商品详情
2. 服务端先查 Redis 里的商品缓存
3. 命中则直接返回
4. 未命中则查数据库
5. 查到后写入 Redis
6. 返回给用户

ASCII 流程图：

```text
用户 → 商品服务 → Redis
               ├─ 命中 → 返回
               └─ 未命中 → 数据库 → 写回 Redis → 返回
```

这个场景为什么真实？

因为商品详情就是典型的“读多写少、热点明显”的数据，非常适合 Redis 缓存。

## 分布式锁：看起来简单，实际上最容易掉坑

Redis 另一个高频使用场景，是分布式锁。

比如：

- 防止重复下单
- 防止定时任务并发执行
- 控制某类全局资源只能被一个实例处理

你可以把它类比成“办公室门口的钥匙”：

- 谁先拿到钥匙，谁先进去办事
- 其他人必须等

### 一个简化版分布式锁示例

下面这个示例是为了帮助初学者理解思路，不是生产级锁实现。

```java
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

public class RedisLockDemo {

    // 模拟 Redis
    private static final Map<String, String> redis = new ConcurrentHashMap<>();

    public static boolean tryLock(String key, String requestId) {
        // putIfAbsent 模拟 setnx
        return redis.putIfAbsent(key, requestId) == null;
    }

    public static void unlock(String key, String requestId) {
        // 只有锁的持有者才能删除
        if (requestId.equals(redis.get(key))) {
            redis.remove(key);
        }
    }

    public static void main(String[] args) {
        String lockKey = "order:lock:1001";
        String requestId = UUID.randomUUID().toString();

        boolean locked = tryLock(lockKey, requestId);
        if (locked) {
            try {
                System.out.println("获取锁成功，开始创建订单");
            } finally {
                unlock(lockKey, requestId);
                System.out.println("释放锁成功");
            }
        } else {
            System.out.println("获取锁失败，请稍后重试");
        }
    }
}
```

### 这个例子表达了什么

- 获取锁时，只有第一个请求能成功
- 释放锁时，必须确认“是不是自己的锁”

### 分布式锁最容易踩的坑

- 锁没有过期时间，导致死锁
- 释放锁时误删别人的锁
- 业务执行时间太长，锁提前过期

⚠️ **重点**：分布式锁并不是“会写一个 `setnx` 就会了”，它本质上是一个边界条件很多的工程问题。

## 排行榜：Redis 很适合做这种业务

排行榜也是 Redis 很经典的场景。

因为它需要：

- 频繁更新分数
- 按分数排序
- 快速取 Top N

这正好适合 `Sorted Set`。

### 业务例子

- 游戏积分榜
- 热门文章排行
- 销量排行榜

你不一定现在就要会写完整命令，但要先知道：Redis 不只是缓存，它还是高性能数据结构服务。

## 初学者最常见的误区

### 误区一：Redis 就是缓存

缓存当然是 Redis 的重要角色，但不是全部。它还是高性能数据结构服务、共享状态层、流量治理工具和轻量协调组件。

### 误区二：缓存加上去就一定提速

如果缓存策略不合理、命中率不高、回源压力没控制好，Redis 可能并不会真正带来你想要的收益。

### 误区三：分布式锁很简单

表面上简单，细节上极其容易出问题。锁的获取、续期、释放、异常处理都必须谨慎设计。

### 误区四：不区分一致性要求

有些数据适合短暂不一致，有些数据不适合。不同业务对缓存的容忍度不同，不能一套策略打天下。

## 常见问题

### 1. Redis 和 MySQL 是什么关系

不是替代关系，而是分工关系。

- `MySQL` 负责核心持久化数据
- `Redis` 负责高频访问和轻量状态

### 2. Redis 为什么这么快

因为它基于内存、数据结构简单、实现高效，而且避免了很多复杂锁竞争。

### 3. 什么数据最适合缓存

通常是：

- 读多写少
- 热点明显
- 短时间内允许一定程度不一致

## 面试常问问题

### 1. Redis 常见数据结构有哪些

`String`、`Hash`、`List`、`Set`、`Sorted Set`。

### 2. 缓存穿透、击穿、雪崩有什么区别

- 穿透：查不存在的数据
- 击穿：热点 key 失效瞬间大量回源
- 雪崩：大量 key 同时失效

### 3. Redis 分布式锁为什么难

因为要考虑锁过期、锁释放、安全性和异常边界，不是简单“设置一个 key”就够了。

## 总结

Redis 之所以成为现代后端系统的标配，不只是因为它快，而是因为它刚好处在业务系统最常见的性能与状态管理交汇点上。

它能帮你减轻数据库压力、提升访问效率、管理轻量共享状态，也能在排行榜、限流、分布式锁等场景里发挥重要作用。

但 Redis 也绝不是“装上就好”的万能组件。真正有价值的能力，是理解它在系统里承担什么角色、适合什么场景、会带来哪些边界和风险。
