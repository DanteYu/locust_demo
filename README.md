#### 什么是locust
> Locust is an easy-to-use, distributed, user load testing tool. It is intended for load-testing web sites (or other systems) and figuring out how many concurrent users a system can handle.

使用简单的，分布式的，用户负载测试工具。使用 Python 代码来定义用户行为。用它可以模拟百万计的并发用户访问你的系统

#### locust使用思路
1. 先写一个locustfile，也就是一个普通的python file。 可以参考本repo的demo目录下。locustfile至少要拥有一个`HttpLocust`的子类(代表用户，设置测试)，一个`TaskSet`的子类(模拟用户行为)
2. 使用命令去执行locust文件，并且观察结果
    * 如果是web模式，可以打开web界面进行设置、运行和观察
    * 如果是no web模式，直接在终端可以运行和观察

#### 测试执行

大概执行思路是：对于每一个用户
1. 从task_set里面随机选择一个task
2. 执行该task
3. 执行wait_time
4. 重复步骤1

使用类似`locust -f locustfile.py --host=http://www.126.com`的命令可以启动locust monitor，然后在monitor中进行设置执行。

如果希望请求数量维持在一定的情况，可以使用--no-web形式 `locust -f load_test.py --host=https://www.baidu.com --no-web -c 10 -r 2 -t 1m`
* --no-web 表示不使用Web界面运行测试。
* -c 设置虚拟用户数。
* -r 设置每秒启动虚拟用户数。
* -t 设置设置运行时间

如果一个locustfile同时定义多个HttpLocust 可以执行  `locust -f load_test.py UserOne UserTwo`

##### Step Load Mode
执行时，如果你想看到在不同user load的情况下的系统性能，可以使用 `--step-load` 以及配套的 `--step-clients` & `--step-time`

`locust -f locust_files/my_locust_file.py --step-load`

也可以和no web模式一起使用
`$ locust -f --no-web -c 1000 -r 100 --run-time 1h30m --step-load --step-clients 300 --step-time 20m`


###### 执行顺序
使用`TaskSequence`可以指定task执行的顺序

```
class MyTaskSequence(TaskSequence):
    @seq_task(1)
    def first_task(self):
        pass

    @seq_task(2)
    def second_task(self):
        pass

    @seq_task(3)
    @task(10)
    def third_task(self):
        pass
```

#### 分布式执行

一旦单台机器不够模拟足够多的用户时，Locust支持运行在多台机器中进行压力测试

对于master机器
1. 使用`--master`标记来启用一个 Locust 实例。这个实例将会运行你启动测试的 Locust 交互网站并查看实时统计数据
2. master节点的机器自身不会模拟任何用户
3. `--master-bind-host=X.X.X.X`  可选项，与 `--master` 一起结合使用。决定在master模式下将会绑定什么网络接口。默认设置为*(所有可用的接口)
4. `--master-bind-port=5557` 可选项，与 --master 一起结合使用。决定哪个网络端口 master 模式将会监听。默认设置为 5557。注意 Locust 会使用指定的端口号，同时指定端口+1的号也会被占用。因此，5557 会被使用，Locust 将会使用 5557 和 5558
5. `--expect-slaves=X`  在 no-web 模式下启动 master 时使用。master 将等待X连接节点在测试开始之前连接


对于slave机器
1. 使用 `--slave` 标记启动一台到多台 Locustslave 机器节点
2. 标记 `--master-host=X.X.X.X`   与 --slave 一起结合使用，用于设置 master 模式下的 master 机器的IP/hostname(默认设置为127.0.0.1)
3. 标记 `--master-port=5557` 与 --slave 一起结合使用，用于设置 master 模式下的 master 机器中 Locust 的端口(默认为5557)。注意，locust 将会使用这个指定的端口号，同时指定端口+1的号也会被占用。因此，5557 会被使用，Locust将会使用 5557 和 5558。


在 master 模式下启动 Locust: `locust -f my_loucstfile.py --master --master-bind-host=192.168.0.14`

在每个 slave 中执行: `locust -f my_locustfile.py --slave --master-host=192.168.0.14`


#### 常用参数

参数 | 	说明
------------ | -------------
-h, --help	| 查看帮助
-H HOST, --host=HOST	| 指定被测试的主机，采用以格式：http://10.21.32.33
--web-host=WEB_HOST	| 指定运行 Locust Web 页面的主机，默认为空 ''。
-P PORT, --port=PORT, --web-port=PORT	| 指定 --web-host 的端口，默认是8089
-f LOCUSTFILE, --locustfile=LOCUSTFILE	| 指定运行 Locust 性能测试文件，默认为: locustfile.py
--csv=CSVFILEBASE, --csv-base-name=CSVFILEBASE	| 以CSV格式存储当前请求测试数据。
--master	| Locust 分布式模式使用，当前节点为 master 节点。
--slave	| Locust 分布式模式使用，当前节点为 slave 节点。
--master-host=MASTER_HOST	| 分布式模式运行，设置 master 节点的主机或 IP 地址，只在与 --slave 节点一起运行时使用，默认为：127.0.0.1.
--master-port=MASTER_PORT	| 分布式模式运行， 设置 master 节点的端口号，只在与 --slave 节点一起运行时使用，默认为：5557。注意，slave 节点也将连接到这个端口+1 上的 master 节点。
--master-bind-host=MASTER_BIND_HOST	Interfaces (hostname, ip)  | that locust master should bind to. Only used when running with --master. Defaults to * (all available interfaces).
--master-bind-port=MASTER_BIND_PORT	Port | that locust master should bind to. Only used when running with --master. Defaults to 5557. Note that Locust will also use this port + 1, so by default the master node will bind to 5557 and 5558.
--expect-slaves=EXPECT_SLAVES	| How many slaves master should expect to connect before starting the test (only when --no-web used).
--no-web	| no-web 模式运行测试，需要 -c 和 -r 配合使用.
-c NUM_CLIENTS, --clients=NUM_CLIENTS	| 指定并发用户数，作用于 --no-web 模式。
-r HATCH_RATE, --hatch-rate=HATCH_RATE	| 指定每秒启动的用户数，作用于 --no-web 模式。
-t RUN_TIME, --run-time=RUN_TIME	| 设置运行时间, 例如： (300s, 20m, 3h, 1h30m). 作用于 --no-web 模式。
-L LOGLEVEL, --loglevel=LOGLEVEL	| 选择 log 级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）. 默认是 INFO.
--logfile=LOGFILE	| 日志文件路径。如果没有设置，日志将去 stdout/stderr
--print-stats	| 在控制台中打印数据
--only-summary	| 只打印摘要统计
--no-reset-stats	| Do not reset statistics once hatching has been completed。
-l, --list	| 显示测试类, 配置 -f 参数使用
--show-task-ratio	| 打印 locust 测试类的任务执行比例，配合 -f 参数使用.
--show-task-ratio-json	 |以 json 格式打印 locust 测试类的任务执行比例，配合 -f 参数使用.
-V, --version	| 查看当前 Locust 工具的版本.