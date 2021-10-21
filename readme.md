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
python ./run.py [required - breeding way: 1-single breeding; 2-couple breeding] [optional - processor number, default: 8]
```

## 实验记录

**环境大小（长x宽）：** 10x10
**不同的环境数量：** 100个
**机器人基因数量：** 162个
**机器人单位基因表达不同指令最大个数：** 7个
**机器人数量：** 100个
**机器人一次行动步数：** 200步
**遗传代数：** 1000代

### 2021年10月20日

**遗传方法：** SingleBreedingx2
**变异率：** 0.1
**结果：** 50代后看到没有收敛趋势，且发散范围扩大，因为运行时间较长（当时未支持多进程，运算速度较慢），故中止

### 2021年10月21日

**遗传方法：** SingleBreedingx3，CoupleBreedingx3
**变异率：** 0.01
**结果：** 明显收敛（已支持多进程，运算速度较快）。单性繁殖普遍收敛的较慢，且较不稳定，1000代后适应环境的分数在25-45之间，离理想值500还很远；两性繁殖普遍收敛的较快，且较稳定，1000代后适应环境的分数在440-460之间，接近理想值500

![Single Breeding GA第一次](./img/ga_single_breeding_01.png)
![Single Breeding GA第二次](./img/ga_single_breeding_02.png)
![Single Breeding GA第三次](./img/ga_single_breeding_03.png)
![Couple Breeding GA第一次](./img/ga_couple_breeding_01.png)
![Couple Breeding GA第二次](./img/ga_couple_breeding_01.png)
![Couple Breeding GA第三次](./img/ga_couple_breeding_01.png)