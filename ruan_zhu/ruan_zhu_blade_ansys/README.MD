#1.Introduction
 项目主要来源于两个包：pyansys与Geatpy
 用于ansys叶片建模和铺层优化，最后给出最佳铺层的Pareto解集
 
 ###pyansys
   这是一个与ansys可以做后台交互的包，实际上还是基于apdl命令流操作ansys。
 关于apdl，推荐视频b站“水哥ansys apdl”视频，关于pyansys的用法可以看
 [官方文档](https://akaszynski.github.io/pyansys/)，十分详细，这里只说
 明如何将本地ansys与pyansys关联起来。
 第一次使用时运行以下命令，new_path为电脑中ansys的路径:
 ```
import pyansys
new_path = 'C:\\Program Files\\ANSYS Inc\\v170\\ANSYS\\bin\\winx64\\ansys170.exe'
pyansys.change_default_ansys_path(new_path)
```

###Geatpy
详见[文档](http://geatpy.com/index.php/geatpy%E6%95%99%E7%A8%8B/)


#2.Install dependencies
python环境尽量使用较新的anaconda包，主要是numpy版本可能会出问题，anaconda
更新后一般不会有问题了（测试在win10下没有问题，Geatpy不支持linux）。其他依赖包在requirements.txt中，只需执行
```
pip install -r requirements.txt
```

#3.RUN
所有需要修改的参数都在main中的CONFIG中修改，具体参数说明详见Config包中CONFIG类说明。
先运行util.py，获得主梁帽腹板位置（自行选择关键点），默认为工字梁。
运行
```buildoutcfg
pythom util.py
```
开始叶片铺层优化部分                                    
运行
```buildoutcfg
pythom main.py
```
代码运行会自动输出所有的图片截图保存在项目路径下，如若不想保存只需plot_use=False




