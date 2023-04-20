conftest 配置文件 不要做修改操作！！

目前一共四个yaml文件
1.test_configuration  存放域名，账号密码信息，不建议修改（除非密码被他人修改）
2.test_params  存放初始化参数 例如CUToken，银行卡信息
3.test_params2 存放临时参数，例如traceID,单号 ps. 自己的用例执行前记得清除
4.test_input 输入参数，具体内容可以进去查看，需要按照说明格式修改参数！！

conftest 里配置的一些需要常用的函数

read_yaml() 读取yaml文件，目前有四个读取函数，需要哪个yaml里面的参数用这个函数

eg.  我需要密码，read_yaml1()[read_yaml4("Pas")]

write_yaml()  写入到yaml文件  目前配置了写入2，3。常用的只有write_yaml3(),不要使用write_yaml2()写入

eg.  我后面的函数需要TraceID，write_yaml3({"TraceID": TraceID}) 后一个是接口返回的值

clear_yaml3()  目前只有清空3 直接调用即可