# -*- coding: UTF-8 -*-
program_version_no = 'General.snp_V1.0.2.0(build5)'
modify_content=[{"vesion_id":"General.snp_V1.0.2.0(build5)",
                 "update_content":"修改功能：写dispatch_config.xml按照车载类型区别picking和非picking的调度，然后写xml；"},
                {"vesion_id":"General.snp_V1.0.1.2(build4)",
                 "update_content":"增加功能：1.启动车载服务进程并打开网页；"},
                {"vesion_id":"General.snp_V1.0.1.1(build3)",
                 "update_content":"修改功能：1.调整操作说明；2.车载自启动目录文件识别修改。"},

                {"vesion_id":"General.snp_V1.0.1.0(build2)",
                 "update_content":"增加功能：1.自动从docks里面找坐标；2.增加自动启车，不依赖路径中的启车脚本。"},

                {"vesion_id":"General.snp_V1.0.0.0(build1)",
                 "update_content":"飞雁项目部署工具的第一个版本,基于General.meite_V1.8.1.0(build19)进行删减。"}
                ]
user_instruction='''***************************************    使用说明   ************************************************
【简介】该工具为飞雁项目部署使用的ProductAutoStartTool。
      .exe文件：主程序，双击打开，在界面上按照“操作说明 ”提示输入数字，程序自动执行相对应的步骤；
      .ini文件记录各个程序的文件路径和信息。
【.ini文件配置方法】
  1.模块[database_connection]：记录数据库的ip、port、用户和密码，database_name为我们要使用的数据库实例名。
  2.模块[dbpath]:记录postgresql的安装路径（一般找pgAdmin3.exe所在的路径即可），以及数据库备份包、角色创建文件、数据库清除脚本路径。
    （1）若是postgresql的安装路径在C:\Program Files目录下，则应该将postgresql的安装路径添加道环境变量里；
    （2）数据库备份包、角色创建文件、数据库清除脚本完整路径不能带空格，否则执行出错。
  3.模块[layoutpath]：记录地图所在文件夹路径（文件夹只包含地图文件），系统会把这个文件里的内容拷贝到各个子程序的地图存放位置中。
  4.模块[tspath]:记录TS脚本所在文件夹路径（文件夹只包含ts文件），系统会把这个文件里的内容拷贝到OM的TS存放位置中。
  5.模块[path]：记录子程序的路径，分两种：
    （1）记录子程序(调度、引擎、rest_api、webmonitor、om)的路径：执行程序.exe的所在路径；
    （2）记录子程序（车载路径simpath）的路径：多个仿真车载程序包的根路径，若无仿真车载包，这个路径可以随意写。
  6.模块[excelpath]：导入excle的文件路径，包含文件名。
    包含Location\Location_relation\Object\Agv_info几个表格，格式固定，必须按照模板文件填写。
  7.模块[process_name]：记录子程序配置的文件路径以及配置文件名、程序名，一般不需要修改。
  8.模块[logger]:工具日志的文件夹名，全日志名还会加上当前工具的版本信息。
  9.模块[iepath]：谷歌浏览器的安装路径（chrome.exe的所在目录）。
  10.模块[auto_add_agv]：可以通过api自动加入调度的车载，填写一个list格式比如agv_ids=[101,102,103,104]或者None。
  11.模块[auto_find_agv_info]：可以指定agv的数量，开始agv的编号；自动从docks.xml里面找坐标，并且写入到excel里面。
  
注：所有的路径都不带双引号。
********************************************************************************************************************'''
opt_instruction='''***************************************    操作说明     ***************************************
在界面根据提示输入数字，含义分别表示：
    1.一键更改数据库配置文件；
       [功能介绍]：将配置文件的数据库配置写到各个子程序（dispatch、engine、om、rest_api）的数据库配置文件里。
    2.一键创建恢复数据库backup；
       [功能介绍]：从配置文件获取数据库实例名database_name、获取角色创建脚本路径、获取数据库备份路径，使用postgresql自带的应用程序执行下面4个动作：
            .删除已有的数据库实例database_name；
            .创建数据库实例；
            .执行创建角色脚本；
            .恢复数据库备份。
    3.一键清理数据库；
       [功能介绍]：获取清理数据脚本路径，使用postgresql自带的应用程序执行清理数据库脚本。
    4.关闭所有的进程(不包含仿真车载进程)；
       [功能介绍]：关闭子程序（dispatch、engine、om、rest_api）。
    5.一键启动进程（不包含仿真车载进程；先清理log，再启动进程;）；
      [功能介绍]：清理子程序（dispatch、engine、om、rest_api）的log文件夹，再启动子程序（dispatch、engine、om、rest_api、webmonitor、打开谷歌浏览器网页）。
        51.一键重启dispath（关闭、清理log、启动）
        52.一键重启engine（关闭、清理log、启动）
        55.一键重启webmonitor（关闭、清理log、启动）
        56.一键重启OM（关闭、清理log、启动）
        59.一键关闭谷歌浏览器
    6.查询需要配置的xml文件；
    7.修改dispatch_config.xml文件（包含location、location_relation、object，可为空）；
    8.修改agv_info.xml文件；
    9.复制layout（程序进程目录会优先进行清理）；
    10.执行sql脚本路径；
    11.获取当前版本号；
    12.复制OM的TS模板；
    13.一键重启车载（关闭、清理log、启动）
      131.一键关闭仿真车载
      132.一键启动仿真车载进程（根据车载路劲的启车脚本启车）。
            [功能介绍]:执行配置文件中读取到的启车脚本，会在开启一个窗口执行程序
      133.一键清理车载log
      134.一键启动仿真车载进程（自启动）
        [功能介绍]: 从配置文件中[auto_find_agv_info]读取agv的开始编号、agv的个数、agv的类型，读取车载路径simpath；
              .根据agv_type_id=4/9识别车载路径中A开头的文件夹,agv_type_id=13/14识别F开头的文件夹,agv_type_id=5/11/17/18识别P开头的文件夹；
              .在满足的文件夹中,按照agv_id启动固定的agv的个数。启动的shell_port为“40000+agv_id”
                 若是满足的文件夹个数少于配置的agv的个数，则按照agv_id启动满足的文件夹内已有的文件。
      135.启动车载服务和网页配置页面;
         [功能介绍]: 默认车载服务webvehicle-go.exe在车载路径下，车载的网页配置url都是127.0.0.1：4405.
    14.清理调度引擎log。
    15.一键加载车到调度（读取agv_id的列表）
       [功能介绍]：从配置文件的[auto_add_agv]模块配置获取agv_id列表,按照agv_id自动add、create、setready、run 车载。
      151.一键加载车到调度(手动输入agv_id的列表）。
         [功能介绍]：手动输入agv_id列表,按照agv_id自动add、create、setready、run 车载
    16.自动获取agv的坐标
       [功能介绍]:执行下面4步：
            .从配置文件的layoutpath路径里面读取docks.xml文件；
            .从配置文件的auto_find_agv_info读取agv的开始编号，agv的个数，agv的类型；
            .根据配置个数随机读取坐标信息；
            .按配置agv开始编号，shell_port为“40000+agv_id”，jess_port固定为“2009”，写入excelpath路径excel的“Agv_info”表格中。
       
        
0.退出。

注释：配置文件是指当前.exe所在目录下的config_xxx.ini文件。
********************************************************************************************************************'''