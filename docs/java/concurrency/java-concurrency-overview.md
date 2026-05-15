# Java 并发编程入门：线程、synchronized、volatile、线程池 到底怎么理解


<a class="presentation-link" href="../../presentations/java-concurrency-overview-ppt" target="_blank" rel="noopener">
  <span class="presentation-link__icon" aria-hidden="true">
    <span class="presentation-link__glyph">PPT</span>
  </span>
  <span>
    <strong>打开文章演示版</strong>
    <small>浏览器幻灯片版速览，支持方向键和空格切换</small>
  </span>
</a>

<a class="presentation-link" href="../../presentations/java-concurrency-overview-ppt" target="_blank" rel="noopener">
  <span class="presentation-link__icon" aria-hidden="true">
    <span class="presentation-link__glyph">PPT</span>
  </span>
  <span>
    <strong>打开文章演示版</strong>
    <small>浏览器幻灯片版速览，支持方向键和空格切换</small>
  </span>
</a>

Java 并发编程几乎是每个后端开发者都会遇到、但又很少有人真正学扎实的一块内容。

你可以不天天手写线程池，也可以暂时不碰底层同步器，但你很难完全避开并发问题。接口并发访问、缓存竞争、异步任务、消息消费、批处理调度、线程池配置，这些场景本质上都在和并发打交道。

很多人学并发会陷入两个极端：

- 只背概念：线程、锁、`volatile`、`AQS`、CAS，背了很多词，写代码时还是一脸模糊
- 只会调 API：线程池能用，`synchronized` 能写，线上一出问题就不知道为什么吞吐量掉了、为什么死锁了、为什么线程池堆满了

这篇文章想做的，不是一次性讲完并发所有细节，而是帮初学者建立一条更稳定的学习主线：并发编程到底在解决什么问题、有哪些核心模型、不同工具各自适合什么场景，以及为什么很多所谓“高阶问题”其实最终还是回到基础原理。

## 并发编程是干嘛的

先用最直白的话说：并发编程就是**让程序同时处理多个任务**，并且尽量保证结果是对的、系统是稳的。

比如这些场景都和并发有关：

- 多个用户同时访问同一个接口
- 订单系统同时处理大量下单请求
- 一个任务异步发送短信、邮件、站内通知
- 消费者程序同时处理多条消息

如果没有并发能力，系统吞吐量会很差；如果有并发能力但控制不好，系统又会很容易出错。

所以并发编程的核心目标是：

- 提高处理效率
- 保证共享数据正确
- 控制资源使用

## 并发编程适合在哪些场景用

对 Java 后端来说，并发常见在这些地方：

- Web 请求并发处理
- 线程池异步任务
- 缓存更新竞争
- 定时任务执行
- 消息队列消费
- 批量任务并行处理

✅ **建议**：初学者不要把并发理解成“只要会写线程就是会并发”。真正关键的是：多个线程一起工作时，数据会不会乱。

## 先把地图看清：并发到底在解决什么问题

很多初学者一上来就去背线程 API，结果越学越乱。其实并发编程真正要解决的问题，核心就三个：

- 可见性
- 原子性
- 有序性

### 可见性

一个线程修改了共享变量，另一个线程能不能及时看到？

如果不能，就会出现“明明改了，别人还像没改一样”的问题。

### 原子性

一个操作是不是不可分割？

比如 `count++` 看起来是一行代码，但底层不是原子操作，它通常会分成：

1. 读取 `count`
2. 计算 `count + 1`
3. 写回结果

多个线程同时执行时，就可能出现结果不符合预期的情况。

### 有序性

程序写出来的顺序，和 CPU 实际执行的顺序，是否完全一致？

为了优化性能，编译器和处理器可能会做指令重排。如果代码依赖某种执行顺序，而你没有建立正确并发约束，就会出现很隐蔽的问题。

⚠️ **重点**：你如果能把这三个问题真正理解透，后面再学 `synchronized`、`volatile`、Lock、CAS、线程池时，很多东西都会顺很多。

## 从线程开始理解并发

并发编程最表层的实体是线程。线程是 CPU 调度的基本单位，它让程序可以同时执行多条任务路径。

但很多人学线程时容易停留在“怎么创建线程”。实际上，创建线程本身并不难，难的是如何管理线程和线程间共享状态。

### 一个最小示例：为什么结果可能不是 20000

```java
public class CounterDemo {

    // 多个线程会共享这个变量
    private static int count = 0;

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 10000; i++) {
                count++;
            }
        });

        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 10000; i++) {
                count++;
            }
        });

        t1.start();
        t2.start();

        // 等待两个线程执行结束
        t1.join();
        t2.join();

        System.out.println("count = " + count);
    }
}
```

很多初学者第一次看到这段代码时，会以为输出一定是 `20000`。但实际上结果经常小于这个值。

原因不在于“线程不稳定”，而在于 `count++` 不是原子操作。

### 这个过程可以拆成这样

流程：

1. 线程 A 读取 `count`
2. 线程 B 也读取 `count`
3. 线程 A 做加 1 后写回
4. 线程 B 也做加 1 后写回
5. 其中一次更新被覆盖了

ASCII 流程图：

```text
线程A: 读 count → +1 → 写回
线程B: 读 count → +1 → 写回
```

## synchronized：最经典、也最容易被误解的关键字

只要学 Java 并发，几乎一定会最先接触 `synchronized`。

它的作用可以简单理解成：**在某一段代码执行时，先拿到一把锁，让别的线程暂时不能同时进入受保护区域。**

你可以把它类比成“卫生间门锁”：

- 一个人进去后先锁门
- 其他人要等它出来才能进

### 一个完整、可运行的线程安全计数器示例

```java
public class SafeCounter {

    private int count = 0;

    // synchronized 保证同一时间只有一个线程执行这个方法
    public synchronized void increment() {
        count++;
    }

    public synchronized int getCount() {
        return count;
    }

    public static void main(String[] args) throws InterruptedException {
        SafeCounter safeCounter = new SafeCounter();

        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 10000; i++) {
                safeCounter.increment();
            }
        });

        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 10000; i++) {
                safeCounter.increment();
            }
        });

        t1.start();
        t2.start();

        t1.join();
        t2.join();

        System.out.println("线程安全结果：" + safeCounter.getCount());
    }
}
```

### `synchronized` 解决了什么

- 原子性问题
- 可见性问题

### 初学者常见误区

- 以为哪里不安全就到处加锁
- 以为加了锁就一定高性能
- 以为只要线程安全，业务逻辑就一定正确

⚠️ **重点**：真正重要的是你在保护什么共享状态，而不是“有没有加锁”。

## volatile：它能解决什么，不能解决什么

`volatile` 经常和 `synchronized` 一起出现，但它们解决的问题并不一样。

`volatile` 的核心价值是：

- 保证可见性
- 在一定程度上限制重排序

但它**不保证复合操作的原子性**。

### 一个典型示例：停止线程

这个场景很适合用 `volatile`。

```java
public class VolatileFlagDemo {

    // volatile 保证一个线程修改后，另一个线程能及时看到
    private static volatile boolean running = true;

    public static void main(String[] args) throws InterruptedException {
        Thread worker = new Thread(() -> {
            while (running) {
                // 模拟工作
            }
            System.out.println("线程停止了");
        });

        worker.start();

        Thread.sleep(1000);

        // 主线程修改标志位
        running = false;
    }
}
```

### 为什么这个例子适合 `volatile`

因为这里的需求是：

- 一个线程改状态
- 另一个线程尽快看到

这正是 `volatile` 擅长的事。

### 但它不适合什么

下面这种就不适合：

```java
public class VolatileCountDemo {
    private volatile int count = 0;

    public void increment() {
        count++;
    }
}
```

因为 `count++` 仍然不是原子操作。

✅ **建议**：把 `volatile` 理解成“轻量级状态同步工具”，而不是“万能并发神器”。

## 线程池：并发里最容易“会用但不会配”的部分

Java 项目里比“手写线程”更常见的，是线程池。

因为线程创建和销毁成本不低，如果每来一个任务都新建线程，系统很快就会变得不可控。

线程池的价值在于：

- 复用线程
- 控制并发度
- 平衡资源和吞吐量
- 提供队列和拒绝策略

### 一个贴近业务的异步通知示例

假设用户下单后，需要异步发送短信和站内通知。

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ThreadPoolOrderDemo {

    public static void main(String[] args) {
        // 创建固定大小线程池
        ExecutorService executorService = Executors.newFixedThreadPool(2);

        // 模拟下单后异步发短信
        executorService.submit(() -> {
            System.out.println("发送短信通知...");
        });

        // 模拟下单后异步发站内信
        executorService.submit(() -> {
            System.out.println("发送站内信通知...");
        });

        executorService.shutdown();
    }
}
```

### 为什么线程池比 `new Thread()` 更推荐

传统写法：

```java
new Thread(() -> sendSms()).start();
```

优化写法：

```java
executorService.submit(() -> sendSms());
```

线程池的优势在于：

- 不会频繁创建线程
- 更容易统一管理
- 更适合高并发场景

### 线程池的基本流程

1. 任务提交到线程池
2. 线程池分配工作线程
3. 工作线程执行任务
4. 执行完成后线程返回池中复用

ASCII 流程图：

```text
任务提交 → 线程池队列 → 工作线程执行 → 返回线程池
```

⚠️ **重点**：初学者先理解线程池为什么存在，比先背一堆参数更重要。

## 并发容器：不是“线程安全版集合”这么简单

在多线程环境下，直接使用普通的 `HashMap`、`ArrayList`、`HashSet` 往往会有问题，这时你会接触到并发容器，比如：

- `ConcurrentHashMap`
- `CopyOnWriteArrayList`
- `BlockingQueue`

这些容器并不是简单给普通集合“加锁”而已，它们背后体现了不同场景下的权衡。

例如：

- `ConcurrentHashMap` 更适合高并发读写
- `CopyOnWriteArrayList` 更适合读多写少
- `BlockingQueue` 适合生产者消费者模型

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

这个例子虽然简单，但它想表达的重点是：并发环境下不要想当然地用普通集合。

## 一个真实业务场景：库存扣减为什么容易出问题

假设有一个商品库存是 `1`，两个用户同时下单。

如果你没有做并发保护，就可能出现：

1. 用户 A 读取库存为 `1`
2. 用户 B 也读取库存为 `1`
3. 用户 A 扣减后写回 `0`
4. 用户 B 也扣减后写回 `0`
5. 结果卖出了 `2` 件，但库存逻辑只记录了 `1` 次扣减

这就是典型的并发问题。

ASCII 流程图：

```text
用户A下单 → 读取库存1 → 扣减
用户B下单 → 读取库存1 → 扣减
结果：超卖
```

### 这类问题在实际开发里很常见

比如：

- 秒杀抢购
- 优惠券发放
- 余额扣减
- 重复提交订单

所以并发不是“只在面试里考”，而是和真实业务直接相关。

## 初学者最常见的误区

### 误区一：把并发等同于多线程 API

真正难的不是 `Thread`、`Runnable`、`ExecutorService` 这些名字，而是共享状态、同步语义和系统行为。

### 误区二：一学并发就直冲源码

源码当然值得看，但如果没有“为什么需要这个工具”的问题意识，源码很容易把你劝退。

### 误区三：只追求高性能，不先保证正确性

并发里最危险的不是慢，而是错。数据错乱、死锁、线程泄漏、任务丢失，这些问题往往比性能差更难处理。

### 误区四：线程池参数凭感觉配

很多线上问题不是不会用线程池，而是参数没有结合任务特征、机器资源和流量模型去设计。

## 常见问题

### 1. `synchronized` 和 `volatile` 有什么区别

- `synchronized` 更像“加锁保护临界区”
- `volatile` 更像“让线程及时看到状态变化”

### 2. 为什么 `count++` 不安全

因为它不是原子操作，底层要分多步执行。

### 3. 线程池是不是一定比 new Thread 好

在大多数真实项目里是的，因为线程池更适合资源复用和统一管理。

## 面试常问问题

### 1. 并发编程的三个核心问题是什么

可见性、原子性、有序性。

### 2. `volatile` 能保证线程安全吗

不能完全保证。它主要解决可见性问题，不保证复合操作原子性。

### 3. 为什么推荐使用线程池

因为线程池可以复用线程、控制并发度、降低线程创建销毁成本，并统一管理异步任务。

### 4. `synchronized` 能解决什么问题

它主要解决共享数据访问时的同步问题，保证临界区在同一时刻只被一个线程执行。

## 总结

Java 并发编程之所以难，不是因为概念多，而是因为它同时要求你理解程序行为、共享状态、工具语义和系统资源。

你只学语法，会停留在表面；你只看源码，又可能因为缺少问题背景而越学越乱。

真正好的学习方式，是先抓住可见性、原子性、有序性这三个核心问题，再逐步理解 `synchronized`、`volatile`、线程池和并发容器各自在解决什么。

当你开始用“这段并发逻辑到底保护了什么状态、会不会在高并发下出错”去思考问题时，你才算真正走进了 Java 并发的世界。
