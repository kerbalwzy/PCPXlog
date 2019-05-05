# PCPXlog
Python版-复合日志模块,  通过简单的配置即可以将日志同时输出到控制台、文件、数据库等.

Python version of the composite log module, through simple configuration, can output the log to the console, file, database at the same time.

-----

### 第一步: 安装模块

### Installation

目前你可以通过两种方式安装,推荐使用第一种.

At present, you can install it in two ways. The first one is recommended.

第一种通过pip直接安装, 只需要在终端中输入如下命令即可安装这个模块的最新稳定版本.

The first one is installed directly through pip, and the latest stable version of this module can be installed only by typing the following commands in the terminal.

```shell
pip3 install pcpxlog 
```

第二种通过git仓库源代码安装.

The second is installed through git repository source code.

```
pip3 install git+https://github.com/kerbalwzy/PCPXlog.git@master
```

----

### 第二步: 使用模块

### Quick start

在安装好cpxlog包后可通过在终端中输入命令 “ cpxConfigDemo ” 在当前路径下立即得到一个默认的配置文件, 这个文件的名称叫做 [cpxLogConfig.py](<https://github.com/kerbalwzy/PCPXlog/blob/master/pcpxlog/configDemo.py>), 文件详细内容见链接.

After installing the cpxlog package, a default configuration file named [cpxLogConfig.py](<https://github.com/kerbalwzy/PCPXlog/blob/master/pcpxlog/configDemo.py>), can be obtained immediately by typing the command "cpxConfigDemo" in the terminal under the current path. The details of the file can be found in the link.

目前我认为cpxlog能被使用到的情况主要有以下两种, 第一种是直接通过CPXLogger获取到logger对象使用, 示例代码如下:

At present, I think there are two main situations in which cpxlog can be used. The first one is to get logger objects directly through CPXLogger. The sample code is as follows:

```python
from pcpxlog import CPXLogger

from cpxLogConfig import CPXLogConfigDemo  
# from the cpxLogConfig.py import the config demo class

# load config information from class
CPXLogger.config_from_class(CPXLogConfigDemo)
# ... also support load config from dict and json file.

# create logger
logger = CPXLogger.create_logger()

# use logger to record log information
logger.debug("This is a test for DEBUG level")
logger.info("This is a test for INFO level")
# ... more log level are supported
```

第二种是在配合其他框架使用时,将CPXLogger创建的所有hander对象,添加到全局的logger对象中去, 这样让其他框架在运行中保存log信息时也能按照我们给CPXLogger配置的规则保存.

The second is to add all hander objects created by CPXLogger to the global logger object when used with other frameworks, so that other frameworks can save log information in operation according to the rules we configure CPXLogger.

```python
import logging
from pcpxlog import CPXLogger
from cpxLogConfig import CPXLogConfigDemo  

CPXLogger.config_from_class(CPXLogConfigDemo)

# get global_logger
global_logger = logging.getLogger()
# add handler from CPXLogger.handlers
for handler in CPXLogger.handlers:
    global_logger.addHandler(handler)
```



