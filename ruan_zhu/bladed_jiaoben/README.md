#注意：本程序只适用于bladed4.3，其他版本可以自行编写

#一、Blade模板文件生成
![batchqueue](.README_images/440abfa6.png)

![Change batch directory](.README_images/406364db.png)

![选择模板文件夹](.README_images/32a335b6.png)

![F盘生成模板文件](.README_images/2c7a876b.png)

![](.README_images/10f58d56.png)

这里选择生成结果文件夹，不要选在batchin中，因为我们只需要中间文件，不需要结果文件,
可以随便选择一个文件夹，点击确定后，会生成如下文件

![](.README_images/2f0e24bf.png)

可以看到此时多出了两个文件Batch.1和BatchPrj.1，这两个文件都是用来存储我们设置的工
况的；batch.lst存储了bladed计算顺序。因此我们只需要编辑这三个文件，前两个文件中进
行参数替换，后一个文件写好计算顺序，然后把.lst文件导入bladed就可以进行计算了，关
于.lst文件导入，导入方法见下：

![](.README_images/7b4f4a4c.png)

选择batch.lst文件导入，然后Start Batch即可开始计算


#二、文件说明
CONF:配置文件
csv_generation:工况csv文件生成
Turbulent:湍流文件生成
DLC_xx:各个工况计算文件生成

#三、RUN
运行main.py函数即可，main函数会依次运行以下函数：
1.程序首先加载配置文件，所有工况信息和需要配置的信息都在./Conf/config.json文件下；

2.运行csv_generation类，生成所有的csv工况文件；

3.运行Turbulent类，生成湍流文件，湍流文件只和流速有关，不需要依照模板生成，直接生成即可；

4.运行DLC_XX类，开始生成各个工况的中间计算文件，程序会自动建立需要的文件夹，不需要预先建立（除root_path外）。

运行main之前，需要在/DLC_XX/compare_file中生成两种不同工况（用来对比得到需要修改的参数，中间文件生成过程见上）。

注意，流剪切，风流速、流向这三个参数直接设置一样的就可以，如果需要不同的参数，可修改DLC_XX/dlc_xx.py中的
param_num部分即可。






















