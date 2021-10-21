# readme

## 代码说明

tools.py: 包含了几个使用的工具类
    - Strategy: 策略，其中包括了基因数量、基因映射索引表、动作
    - Square：广场，其上随机有垃圾，Collector可以在Square上收集垃圾
    - BreedingWay：繁殖方式的积累，所有具体繁殖方式都要从此类继承
    - SingleBreeding: 单性繁殖方式，通过选取上一代最优Collector个体，指定变异几率后，随机生成本代
    - Collector：垃圾回收机器人，每个Collector有不同的基因，通过BerrdingWay指定的繁殖方式繁殖后代

run.py: 使用vscode的jupyter插件运行

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
