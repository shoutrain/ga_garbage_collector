# readme

## 代码说明

tools.py: 包含了几个使用的工具类
    - Strategy: 策略，其中包括了基因数量、基因映射索引表、动作
    - Square：广场，其上随机有垃圾，Collector可以在Square上收集垃圾
    - BreedingWay：繁殖方式的积累，所有具体繁殖方式都要从此类继承
    - SingleBreeding: 单性繁殖方式，通过选取上一代最优Collector个体，指定变异几率后，随机生成本代；此方式在命令行被编码为1
    - CoupleBreeding：双性繁殖方式，从上一代所有Collector中按照score高低作为概率选取两个Collector，然后通过拼接这两个Collector的基因生成本代；此方式在命令行被编码为2
    - Collector：垃圾回收机器人，每个Collector有不同的基因，通过BerrdingWay指定的繁殖方式繁殖后代

run.py: 运行算法的入口文件，在项目根目录下运行命令如下（在Linux平台上需要使用python3命令，使用python一般默认为python2）：

```bash
python ./run.py [breeding way: 1-single breeding; 2-couple breeding]
```

## 实验记录

广场大小：10*10
不同的广场数量：100个
垃圾回收机器人数量：100个
垃圾回收机器人一次清扫行动步数：200步
遗传代数：1000代

### 第一次

日期：2021年10月20日
遗传方法：SingleBreeding
变异率：0.1
结果：不收敛，被环境淘汰

### 第二次

日期：2021年10月21日
遗传方法：SingleBreeding
变异率：0.01
结果：收敛，可以在环境生存
