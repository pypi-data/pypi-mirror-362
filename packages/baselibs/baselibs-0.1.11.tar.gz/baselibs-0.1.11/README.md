# 通用基础库 

版本: v0.1.11
* 修正LLM_TASK类的BUG
* LLM_TASK类支持qwen3, qwq模型；
* 优化计时器类

版本: v0.1.10
* 增加了LLM_TASK类，用于大模型通用任务
* 修正 RedisCache类中 data_table 无效的bug
* 优化原有代码; 

版本: v0.1.9

* 扩展了对json格式文件的读写支持：readjson, readjsonp, savejson, savejsonp
* 增加了MutliTask 多进程任务类
* 优化了计时器类：TimeCount

版本: v0.1.5

* 修改了splitset方法，可用于拆分数据集
* 增加 split_dataframe方法，可对DataFrame进行拆分数据集；
* 增加 分层抽取方法: data_split, save_data_split

版本: v0.1.4

* 修改了TimeCount类

版本: v0.1.1

可对目录下的文件进行以下批量处理：

* 清除空格 空行 按句子分行；
* 删除空文件，找到后改名（改为"原文件名.del") 或者直接删除
* 删除重复的文件:   根据文件的MD5判断文件是否相同，找到后改名（原文件.same)或者直接删除
* 批量重命名:    可按序号进行重命名，默认从1开始，文件名会自动在前面补0，例如"0001.txt"
* 可统计文本文件的行数  [2019/1/18 添加]
* 对数据进行检查；
* 对数据重复数据检查并删除；
* 对数据进行随机抽样；
* 处理参数可以自定义顺序，
