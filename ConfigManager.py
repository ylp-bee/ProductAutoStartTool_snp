# -*- coding: utf-8 -*-
import os
import sys
import configparser
from version import program_version_no

class ConfigPara:
    database_host = 'localhost'
    database_port = '5432'
    database_name = 'postgres'
    database_user_name = 'postgres'
    database_password = '123456'
    pgpath = r"C:\Program Files\PostgreSQL\9.5.15\bin"

    rest_api_configpath = r'config\DBconfig.json'
    rest_api_process_name = 'rest_api.exe'
    monitor_process_name = 'manage.exe'
    dispath_dbconfigpath =r'config\config.ini'
    dispath_config_name = 'dispatch_config.xml'
    dispath_process_name = 'dispatch.exe'
    engine_dbconfigname = 'rex_server_connect.xml'
    agv_info_name = 'agv_info.xml'
    engine_process_name = 'dispatch_engine.exe'


    @classmethod
    def load_config(cls):
        config_file_path = ''
        try:
            current_path = os.getcwd()
            config_file_path = os.path.join(current_path , "config_snp.ini")
            print('loading config file at path: ' + config_file_path)
            config_reader = configparser.ConfigParser()
            config_reader.read(config_file_path,encoding='UTF-8')


            '''读取本地数据库的配置信息'''
            cls.database_host = config_reader.get('database_connection', 'host')  # '127.0.0.1'
            cls.database_port = config_reader.get('database_connection', 'port')  # '5432'
            cls.database_name = config_reader.get('database_connection', 'database_name')  # 'jiliangyuan'
            cls.database_user_name = config_reader.get('database_connection', 'user_name')  # 'postgres'
            cls.database_password = config_reader.get('database_connection', 'password')  # 'admin'

            '''读取本地数据库的安装路径'''
            cls.pgpath = config_reader.get('dbpath', 'pgpath')


            '''读取数据库脚本相关的路径'''
            cls.rolespath =config_reader.get('dbpath', 'rolespath')
            cls.backuppath =config_reader.get('dbpath', 'backuppath')
            cls.clearpath=config_reader.get('dbpath', 'clearpath')


            '''读取各个程序的安装路径,包含根路径：
            1、调度、引擎
            2、rest_api,webmonitor
            3、工业的monitor,
            4、DBAI路径、csmonitor、GUI的安装路径不包含根路径
            5、其他工具的路径Database_Simulatorpath
            6、OM'''
            cls.dispathpath=config_reader.get('path', 'dispathpath')
            cls.enginepath=config_reader.get('path', 'enginepath')
            cls.rest_api_path = config_reader.get('path', 'rest_api_path')
            cls.webmonitorpath = config_reader.get('path', 'webmonitorpath')



            cls.simpath = config_reader.get('path', 'simpath')

            '''读取OM相关的信息路径'''
            cls.ompath =config_reader.get('path', 'ompath')

            # '''读取io相关的信息路径'''
            # cls.iopath = config_reader.get('path', 'iopath')

            '''读取excelpath获取配置excel 的路径'''
            cls.excelpath=config_reader.get('excelpath', 'excelpath')
            '''读取ts的存放路径'''
            cls.tsfilespath = config_reader.get('tspath', 'tsfilespath')

            '''读取excelpath获取地图的路径'''
            cls.layoutpath = config_reader.get('layoutpath', 'layoutpath')

            '''读取process_name得到调度相关信息的路径'''
            #通用
            cls.dispath_dbconfigpath = config_reader.get('process_name', 'dispath_dbconfigpath')
            #通用框架调度信息
            cls.dispath_config_name = config_reader.get('process_name', 'dispath_config_name')
            cls.dispath_process_name =config_reader.get('process_name', 'dispath_process_name')


            '''读取process_name得到引擎相关信息的路径'''
            cls.engine_dbconfigname =config_reader.get('process_name', 'engine_dbconfigname')
            cls.agv_info_name = config_reader.get('process_name', 'agv_info_name')
            cls.engine_process_name = config_reader.get('process_name', 'engine_process_name')

            '''读取process_name得到monitor相关信息的路径'''
            #通用cs架构
            cls.rest_api_configpath=config_reader.get('process_name', 'rest_api_configpath')
            cls.rest_api_process_name=config_reader.get('process_name', 'rest_api_process_name')
            cls.monitor_process_name=config_reader.get('process_name', 'monitor_process_name')


            '''读取process_name得到OM相关信息的路径'''
            cls.om_dbconfigpath =config_reader.get('process_name', 'om_dbconfigpath')
            cls.om_process_name=config_reader.get('process_name', 'om_process_name')


            # cls.io_process_name=config_reader.get('process_name', 'io_process_name')
            cls.sim_autostart_name=config_reader.get('process_name', 'sim_autostart_name')


            '''组合得到通用的bs架构的monitor的路径'''
            cls.rest_api_dbconfigpath=os.path.join(cls.rest_api_path , cls.rest_api_configpath)
            cls.rest_api_process_path = os.path.join(cls.rest_api_path ,cls.rest_api_process_name)
            cls.monitor_process_path=os.path.join(cls.webmonitorpath , cls.monitor_process_name)

            '''组合得到通用的架构的OM的路径'''
            cls.om_dbconfigpath=os.path.join(cls.ompath,cls.om_dbconfigpath)
            cls.om_process_path=os.path.join(cls.ompath,cls.om_process_name)



            '''组合得到通用架构的dispath的路径'''
            cls.dispath_dbconfigpath = os.path.join(cls.dispathpath, cls.dispath_dbconfigpath)
            cls.dispath_config_path = os.path.join(cls.dispathpath, cls.dispath_config_name)
            cls.dispath_process_path = os.path.join(cls.dispathpath, cls.dispath_process_name)



            '''组合得到架构的engine的路径'''
            cls.engine_dbconfigpath = os.path.join(cls.enginepath , cls.engine_dbconfigname)
            cls.agv_info_path = os.path.join(cls.enginepath , cls.agv_info_name)
            cls.engine_process_path = os.path.join(cls.enginepath , cls.engine_process_name )

            cls.logger_name =  config_reader.get('logger', 'logger_name')+'_' + program_version_no+'.log'
            cls.chromepath=config_reader.get('iepath', 'chromepath')

            '''需要自动加入调度的车载'''
            cls.agv_ids=eval(config_reader.get('auto_add_agv', 'agv_ids'))

            '''自动找车载的信息'''
            cls.agv_nums = config_reader.get('auto_find_agv_info', 'agv_nums')
            cls.start_agv_id  = config_reader.get('auto_find_agv_info', 'start_agv_id')
            cls.agv_type_id= config_reader.get('auto_find_agv_info', 'agv_type_id')

            cls.shell_port = 40000
            cls.fts_port = 4411
            cls.jess_port = 2009
            return cls

        except Exception as e:
            print('Error: failed to read configuration file! File path should be at: ' + config_file_path)
            print(e)
            sys.exit(1)  # fatal error, need exit the program

configs =  ConfigPara.load_config()

# class DatabaseConnectionConfig:
#     def __init__(self, host, port, database_name, user_name, password):
#         self.host = host
#         self.port = port
#         self.database_name = database_name
#         self.user_name = user_name
#         self.password = password


# if __name__ == "__main__":
#     # print(configs.database_host)
#     # print(configs.database_port)
#     # print(configs.database_name)
#     # print(configs.database_password)
#     # print(configs.database_user_name)
#     print(configs.rolespath)
#     print(configs.shell_port)