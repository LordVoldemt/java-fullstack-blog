# Java 集合入门：List、Set、Map 到底怎么选，为什么这不只是“装数据的容器”

Java 后端开发里，集合几乎无处不在。

- 查出来的一批数据，要放进 `List`
- 按 key 聚合信息，要用 `Map`
- 做判重，要用 `Set`
- 做并发缓存，又会碰到 `ConcurrentHashMap`

很多人对集合的第一印象是“会用就行”，可真正写业务、读源码、排性能问题时，你会发现集合远不只是一个存数据的容器。

这篇文章会从初学者视角帮你把 Java 集合重新理一遍。你看完后，至少应该搞清楚：

- `List`、`Set`、`Map` 分别适合什么场景
- `ArrayList`、`LinkedList`、`HashMap`、`ConcurrentHashMap` 到底有什么区别
- 真实项目里为什么不能“随便选一个能装数据的集合”
- 常见易错点和面试点有哪些

## Java 集合是干嘛的

如果用最白话的话来讲，Java 集合就是：**帮你批量管理数据的一套工具。**

你可以把它理解成现实里的收纳盒：

- `List` 像一个有顺序的清单
- `Set` 像一个“不允许重复”的名单
- `Map` 像一个“编号 -> 信息”的字典

集合真正重要的地方，不是“能存东西”，而是它能让你用合适的方式组织数据。

## 集合适合在哪些场景用

几乎所有 Java 业务代码都离不开集合。

例如：

- 用户列表查询：`List`
- 标签去重：`Set`
- 订单按用户分组：`Map`
- 本地缓存：`ConcurrentHashMap`

✅ **建议**：初学阶段不要只问“这个集合能不能用”，而要开始问“这个场景最适合哪个集合”。

## 先把地图看清：Java 集合主要分哪几类

Java 集合主要可以分成三大体系：

- `List`：有序、可重复
- `Set`：无重复
- `Map`：键值对存储

| 类型 | 特点 | 典型场景 |
|---|---|---|
| `List` | 有顺序、可重复 | 查询结果、文章列表、订单明细 |
| `Set` | 不允许重复 | 标签去重、权限集合、用户去重 |
| `Map` | 键值映射 | 本地缓存、按 ID 查数据、按用户分组 |

如果你先把这张表记住，后面很多集合问题都会简单很多。

## List：为什么它这么常用

`List` 最大的特点是：

- 有顺序
- 可重复

最常见的实现有两个：

- `ArrayList`
- `LinkedList`

### ArrayList：最常用的列表

`ArrayList` 底层基于数组，因此它的特点是：

- 按索引访问快
- 尾部追加高效
- 中间插入和删除成本较高

### 一个最小示例

```java
import java.util.ArrayList;
import java.util.List;

public class ArrayListDemo {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>();

        names.add("Alice");
        names.add("Bob");
        names.add("Carol");

        // 按下标读取，速度很快
        System.out.println(names.get(1));
    }
}
```

### 适合什么场景

- 查询结果集
- 页面列表数据
- 大部分读多于改的业务场景

## LinkedList：为什么面试常见，但业务里没那么常见

`LinkedList` 底层是链表结构。

理论上它在中间插入、删除节点时更有优势，因为不需要像数组那样整体搬移。

但很多人学到这里就会误以为：那我以后大量插入删除就该优先用 `LinkedList`。

现实里没这么简单。因为你插入删除前，通常还得先找到那个位置，而链表定位本身就不快。

### 一个简单示例

```java
import java.util.LinkedList;
import java.util.List;

public class LinkedListDemo {
    public static void main(String[] args) {
        List<String> tasks = new LinkedList<>();

        tasks.add("task-1");
        tasks.add("task-2");
        tasks.add(1, "task-middle");

        System.out.println(tasks);
    }
}
```

### 初学者要记住什么

- 面试里经常拿它和 `ArrayList` 对比
- 项目里大多数情况默认还是用 `ArrayList`

⚠️ **重点**：不要只背“谁插入快、谁查询快”，还要看真实业务环境。

## Set：为什么它适合做去重

`Set` 最核心的特点是：**元素不能重复。**

常见实现包括：

- `HashSet`
- `LinkedHashSet`
- `TreeSet`

### 一个最小去重示例

```java
import java.util.HashSet;
import java.util.Set;

public class SetDemo {
    public static void main(String[] args) {
        Set<String> tags = new HashSet<>();

        tags.add("Java");
        tags.add("Redis");
        tags.add("Java");

        // Java 只会保留一次
        System.out.println(tags);
    }
}
```

### 真实业务场景

- 标签去重
- 用户 ID 去重
- 权限编码去重

## Map：后端开发里最重要的集合之一

在后端开发里，`Map` 往往比 `List` 还要重要。

因为很多业务本质上都在做“key -> value”的映射。

最常见的实现包括：

- `HashMap`
- `LinkedHashMap`
- `TreeMap`
- `ConcurrentHashMap`

### HashMap：最常用的映射结构

你可以把 `HashMap` 理解成一个高效字典：

- 通过 key 快速找到 value
- 平均查找效率高

### 一个最小示例

```java
import java.util.HashMap;
import java.util.Map;

public class HashMapDemo {
    public static void main(String[] args) {
        Map<String, Integer> scoreMap = new HashMap<>();

        scoreMap.put("Tom", 90);
        scoreMap.put("Jerry", 95);

        System.out.println(scoreMap.get("Tom"));
    }
}
```

### 它适合什么场景

- 本地缓存
- 通过 ID 查对象
- 分组统计
- 数据映射

## 实战示例一：订单按用户分组

这是一个特别贴近真实开发的例子。

假设你查出了一批订单，现在要按用户分组。

### 订单类

```java
class Order {
    private Long id;
    private Long userId;

    public Order(Long id, Long userId) {
        this.id = id;
        this.userId = userId;
    }

    public Long getId() {
        return id;
    }

    public Long getUserId() {
        return userId;
    }

    @Override
    public String toString() {
        return "Order{id=" + id + ", userId=" + userId + "}";
    }
}
```

### 分组代码

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class OrderGroupDemo {
    public static void main(String[] args) {
        List<Order> orders = List.of(
                new Order(1L, 1001L),
                new Order(2L, 1001L),
                new Order(3L, 1002L)
        );

        Map<Long, List<Order>> userOrders = new HashMap<>();

        for (Order order : orders) {
            // 如果当前用户还没有列表，就先创建一个
            userOrders
                    .computeIfAbsent(order.getUserId(), key -> new ArrayList<>())
                    .add(order);
        }

        System.out.println(userOrders);
    }
}
```

### 这个例子说明了什么

- `Map` 负责按用户编号做映射
- `List` 负责保存同一个用户的多条订单

流程：

1. 遍历订单列表
2. 取出订单所属用户 ID
3. 按用户 ID 找到对应列表
4. 把订单放入该列表

ASCII 流程图：

```text
订单列表 → 取 userId → Map 找分组 → 放入对应 List
```

## ConcurrentHashMap：并发场景下为什么不能直接用 HashMap

很多人第一次接触线程安全集合时，会下意识觉得：并发问题嘛，加锁不就好了？

但如果你真的这么做，很快会遇到：

- 吞吐量下降
- 锁竞争严重
- 性能不稳定

`ConcurrentHashMap` 的价值就在于，它不是简单地给整个结构套一把大锁，而是通过更细粒度的控制，让并发读写在大多数时候更高效。

### 一个简单示例

```java
import java.util.concurrent.ConcurrentHashMap;

public class ConcurrentMapDemo {
    public static void main(String[] args) {
        ConcurrentHashMap<String, Integer> stockMap = new ConcurrentHashMap<>();

        stockMap.put("book", 100);
        stockMap.put("phone", 50);

        System.out.println(stockMap.get("book"));
    }
}
```

### 常见业务场景

- 本地缓存
- 并发统计
- 请求级数据聚合

⚠️ **重点**：并发场景里不要想当然地用普通 `HashMap`。

## 实战示例二：商品去重

假设用户购物车里可能重复添加同一个商品 ID，现在你要快速做一次去重。

```java
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class ProductDeduplicateDemo {
    public static void main(String[] args) {
        List<Long> productIds = List.of(1001L, 1002L, 1001L, 1003L, 1002L);

        Set<Long> uniqueProductIds = new HashSet<>(productIds);

        System.out.println(uniqueProductIds);
    }
}
```

这个例子非常简单，但很贴近真实业务：

- 原始列表可能重复
- `Set` 非常适合做唯一性过滤

## 集合怎么选：给初学者的一个实用判断法

你可以先问自己这几个问题：

### 1. 你关不关心顺序

- 关心：优先考虑 `List`
- 不关心：再看是否需要唯一性或映射

### 2. 你要不要去重

- 要：优先考虑 `Set`
- 不要：再看是 `List` 还是 `Map`

### 3. 你是不是在做 key-value 查找

- 是：优先考虑 `Map`

### 4. 你有没有并发场景

- 有：考虑 `ConcurrentHashMap` 等并发集合

✅ **建议**：先按“场景”选集合，再去考虑底层实现细节。

## 初学者最常见的误区

### 误区一：只记接口，不理解底层结构

知道 `List`、`Set`、`Map` 的定义当然重要，但如果不知道它们背后为什么这样设计，很容易在实际使用时选错结构。

### 误区二：觉得复杂度就是全部

时间复杂度很重要，但不是唯一标准。真实系统里还要看：

- 内存占用
- 并发行为
- 扩容成本
- 使用习惯

### 误区三：把线程安全理解成“能在多线程里用”

线程安全不仅仅是“不报错”，还包括语义是否正确、复合操作是否原子、性能是否能接受。

### 误区四：看源码只盯细节，不看设计意图

很多人看 `HashMap` 源码时，容易陷在位运算和链表树化细节里，但真正更重要的问题是：它为什么这么设计？

## 常见问题

### 1. 默认用 `ArrayList` 还是 `LinkedList`

大多数业务场景默认用 `ArrayList`。

### 2. 默认用 `HashMap` 还是 `TreeMap`

大多数场景默认用 `HashMap`，只有你真的需要排序时再考虑 `TreeMap`。

### 3. 做去重为什么首选 `Set`

因为 `Set` 的语义就是“不允许重复”，比你手工判断更清晰。

## 面试常问问题

### 1. `List`、`Set`、`Map` 的区别是什么

- `List`：有序、可重复
- `Set`：无重复
- `Map`：键值对映射

### 2. `ArrayList` 和 `LinkedList` 有什么区别

- `ArrayList` 底层是数组，查询快，尾部追加快
- `LinkedList` 底层是链表，中间插入删除理论上更灵活，但实际项目里使用较少

### 3. `HashMap` 为什么常用

因为它能基于 key 高效查找 value，适合大部分键值映射场景。

### 4. 并发场景下为什么不能直接用 `HashMap`

因为它不是线程安全的，并发读写可能出问题。

## 总结

Java 集合看起来是最“日常”的一块内容，但恰恰因为它日常，才更值得系统学习。你写的每个业务方法、每个缓存结构、每个聚合逻辑，几乎都绕不开集合。

如果你只会“把数据塞进去再拿出来”，那集合只是工具；如果你理解了它背后的结构、性能和并发语义，集合就会变成你理解 Java 设计哲学的一扇门。
