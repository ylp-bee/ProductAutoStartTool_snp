# -*- coding: utf-8 -*-
import os
import shutil
import time
from Logger_module import logger
from ConfigManager import configs
import configparser
import json
import ctypes,sys
from xml.dom import minidom
from Modify_xml_ts_layout import write_to_general_xml as w


class Opera_DB():
    def  __init__(self):
        self.ip = configs.database_host
        self.port = configs.database_port
        self.dbname = configs.database_name
        self.dbpassword = configs.database_password
        self.dbuser = configs.database_user_name

        self.pgpath = configs.pgpath
        self.backup_filepath = configs.backuppath
        self.clearpath = configs.clearpath
        self.role_sqlpath = configs.rolespath

        self.drop_path = os.path.join(self.pgpath, 'dropdb.exe')
        self.create_path = os.path.join(self.pgpath, 'createdb.exe')
        self.psql_path=os.path.join(self.pgpath,'psql.exe')
        self.restore_path = os.path.join(self.pgpath, 'pg_restore.exe')
        self.temp_file='temp.xml'


    def drop_db(self):
      try:
        drop_command = '''"{}" -h {} -p {} -U postgres --if-exists -w -e {}'''.format(self.drop_path, self.ip, self.port, self.dbname)
        logger.info('command:{}'.format(drop_command))
        results= os.system(drop_command)
        if(results==0):
            logger.info('------Drop DB:{} Success!! results:{}'.format(self.dbname,results))
        else:
            logger.info('------Drop DB:{} Fail!! results:{}'.format(self.dbname, results))
      except Exception as e:
            logger.info('Drop DB error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def create_db(self):
      try:
        create_command = '''"{}" -h {} -p {} -U postgres  -w -e {}'''.format(self.create_path, self.ip, self.port, self.dbname)
        logger.info('command:{}'.format(create_command))
        results=os.system(create_command)
        if (results == 0):
            logger.info('------Create DB:{} Success!! results:{}'.format(self.dbname, results))
        else:
            logger.info('------Create DB:{} Fail!! results:{}'.format(self.dbname, results))
      except Exception as e:
            logger.info('Create DB  error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def restore_db(self):
        try:
            restore_command=r'"{}"  -h {} -p {}  -U postgres -d {} {}'.format(self.restore_path,self.ip,self.port,self.dbname,self.backup_filepath)
            # command=r'"{}" --host {} --port {} --username "{}" --dbname "{}" --no-password  --verbose {}' .format(self.restore_path,self.ip,self.port,self.dbname,self.backup_filepath)
            logger.info('command:{}'.format(restore_command))
            results=os.system( restore_command)
            if (results == 0):
                logger.info('------Restore DB:{} Success!! results:{}'.format(self.dbname, results))
            else:
                logger.info('------Restore DB:{} Fail!! results:{}'.format(self.dbname, results))

        except Exception as e:
            logger.info('Restore DB  error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def psql_db(self,sql):
        try:
            psql_command=r'"{}"  -h {} -p {} -U postgres -d {} -f {}'.format(self.psql_path,self.ip,self.port,self.dbname,sql)
            logger.info('command:{}'.format(psql_command))
            results=os.system(psql_command)
            if (results == 0):
                logger.info('------Psql DB:{} Success!! results:{}'.format(self.dbname, results))
            else:
                logger.info('------Psql DB:{} Fail!! results:{}'.format(self.dbname, results))
        except Exception as e:
            logger.info('Psql DB  error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def db_kill(self):
        try:

            process_list = ['navicat.exe', 'pgAdmin3.exe']
            for i in process_list:
                logger.info('Star kill db process:{}!'.format(i))
                command = r'wmic process where name="{program}" delete'.format(program=i)
                # command='taskkill /f /t /im {}'.format(program=i)
                temp = os.system(command)
                logger.info('End kill db prcess:{} !return content:：{}'.format(i, temp))
        except Exception as e:
            logger.error('kill all db process error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def db_create(self):
        sql=self.role_sqlpath
        self.db_kill()
        self.drop_db()
        time.sleep(1)
        self.create_db()
        time.sleep(1)
        self.psql_db(sql)
        time.sleep(5)
        self.restore_db()
        time.sleep(5)

    def db_clear(self):
        sql = self.clearpath
        self.psql_db(sql)
        time.sleep(1)

class modify_general_config_and_process_opra():
    def  __init__(self):
        self.ip = configs.database_host
        self.port = configs.database_port
        self.dbname = configs.database_name
        self.dbpassword = configs.database_password
        self.dbuser = configs.database_user_name

        self.dispathpath=configs.dispathpath
        self.dispath_dbconfigpath=configs.dispath_dbconfigpath
        self.dispath_config_path =configs. dispath_config_path
        self.dispath_process_path=configs.dispath_process_path

        self.enginepath=configs.enginepath
        self.engine_dbconfigpath =configs.engine_dbconfigpath
        self.agv_info_path= configs.agv_info_path
        self.engine_process_path=configs.engine_process_path



        self.webmonitorpath=configs.webmonitorpath
        self.rest_api_path=configs.rest_api_path
        self.rest_api_dbconfigpath=configs.rest_api_dbconfigpath
        self.rest_api_process_path = configs.rest_api_process_path
        self.monitor_process_path=configs.monitor_process_path
        self.monitor_open_process_path=os.path.join(configs.webmonitorpath,'run.bat')


        self.dispath_process_name=configs.dispath_process_name
        self.engine_process_name=configs.engine_process_name
        self.monitor_process_name=configs.monitor_process_name
        self.rest_api_process_name=configs.rest_api_process_name
        # print(self.dispath_process_name,self.engine_process_name,self.monitor_process_name,self.rest_api_process_name)


        self.chromepath=configs.chromepath

        self.ompath=configs.ompath
        self.om_dbconfigpath=configs.om_dbconfigpath
        self.om_process_path=configs.om_process_path

        self.d=w()


        self.start_agv_id=int(configs.start_agv_id)
        self.shell_port = int(configs.shell_port)
        self.fts_port = int(configs.fts_port)
        self.jess_port = int(configs.jess_port)


    def modify_dispath_db_config(self):
        try:
            logger.info('Start modify dispath db config!')
            conf = configparser.ConfigParser()
            conf.read(self.dispath_dbconfigpath, encoding='utf-8')
            conf.set('database_connection', 'host', self.ip)
            conf.set('database_connection', 'port', self.port)
            conf.set('database_connection', 'database_name', self.dbname)
            conf.set('database_connection', 'user_name', self.dbuser)
            conf.set('database_connection', 'password', self.dbpassword)
            conf.write(open(self.dispath_dbconfigpath, 'w+', encoding='utf-8'))
            logger.info('End modify dispath db config!')
        except Exception as e:
            logger.error('Modify dispath db  error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def modify_engine_db_config(self):
        try:
            logger.info('Start modify engine db config!')
            node_modify_info={'Host':self.ip, 'db': self.dbname, 'Port': self.port, 'user':self.dbuser,
                                   'password':self.dbpassword}
            temp_file = 'temp.xml'
            xmlDom = minidom.parse(self.engine_dbconfigpath)
            root = xmlDom.documentElement
            for i, v in node_modify_info.items():
                node_key = i
                node_value = v
                old_value = root.getElementsByTagName('Server')[0].getAttribute(node_key)
                if (old_value != v):
                    # name[i].firstChild.data = 'screwnut'
                    root.getElementsByTagName('Server')[0].setAttribute(node_key, node_value)
                # current_value = root.getElementsByTagName('Server')[0].getAttribute(node_key)
                # logger.info('------Engine的db配置文件: node_key="{}", new_node_value="{}", old_value="{}", current_value ="{}"'.format(node_key, node_value, old_value,current_value ))
            f = open(temp_file, "w", encoding='utf-8')
            xmlDom.writexml(f)
            f.close()
            # os.unlink(temp_file)
            with open(temp_file, 'r', encoding='utf-8') as fr, open(self.engine_dbconfigpath, 'w', encoding='utf-8') as fw:
                for text in fr.readlines():
                    if text.split():
                        fw.write(text)
            f.close()
            os.unlink(temp_file)
            logger.info('End modify engine db config!')
        except Exception as e:
            logger.error('Modify engine db  error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def modify_rest_api_db_config(self):
        try:
            logger.info('Start modify rest_api db config!')
            with open(self.rest_api_dbconfigpath, "r", encoding='utf-8') as jsonFile:
                data = json.load(jsonFile)
            tmp = data["DBcon"]
    
            data["DBcon"]["host"]=self.ip
            data["DBcon"][ "port"]=self.port
            data["DBcon"]["database"] = self.dbname
            data["DBcon"]["user"]=self.dbuser
            data["DBcon"][ "password"]=self.dbpassword
            # logger.info('rest_api db_config：before：{}，after：{}'.format(tmp,data))
            with open(self.rest_api_dbconfigpath, "w") as jsonFile:
                json.dump(data, jsonFile, ensure_ascii=False)
            logger.info('End modify rest_api db config!')
        except Exception as e:
            logger.error('Modify rest_api db error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def modify_om_db_config(self):
        try:
            isexists = os.path.exists(self.om_dbconfigpath)
            if isexists:
                logger.info('Start modify om db config!')
                with open(self.om_dbconfigpath, "r", encoding='utf-8') as jsonFile:
                    data = json.load(jsonFile)
                tmp = data["DBcon"]

                data["DBcon"]["host"] = self.ip
                data["DBcon"]["port"] = self.port
                data["DBcon"]["database"] = self.dbname
                data["DBcon"]["user"] = self.dbuser
                data["DBcon"]["password"] = self.dbpassword
                # logger.info('rest_api db_config：before：{}，after：{}'.format(tmp,data))
                with open(self.om_dbconfigpath, "w") as jsonFile:
                    json.dump(data, jsonFile, ensure_ascii=False)
                logger.info('End modify om db config!')
            else:
                logger.info('not exists path:{}'.format(self.om_dbconfigpath))
        except Exception as e:
            logger.error('Modify om db error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def func_vehicles(self):
        try:
            if os.path.exists(configs.simpath ):
                logger.info('Start open vehicles process!')
                command = r'cd /d ' + configs.simpath + ' && start  ' + configs.sim_autostart_name
                results = os.system(command)
                # results=os.startfile(self.dispath_process_path)
                logger.info('End open vehicles process!,return content:{}'.format(results))
            else:
                logger.info('path:{} not exists!'.format(configs.simpath))
        except Exception as e:
            logger.error('open vehicles process error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def key_num(self,elem):
        return int(elem.split('-')[1])

    def func_new_vehicles(self):
        try:
            agv_type_id=int(configs.agv_type_id)
            if os.path.exists(configs.simpath):
                logger.info('Start open vehicles process!')
                agv_dir_list=[]

                if (agv_type_id in[4,9]):
                    #ants车
                    agv_dir_list=[i for i in os.listdir(configs.simpath) if i[0]=='A' and os.path.isdir(os.path.join(configs.simpath,i))]
                if (agv_type_id in [13,14]):
                    #fork车
                    agv_dir_list = [i for i in os.listdir(configs.simpath) if
                                    i[0] == 'F' and os.path.isdir(os.path.join(configs.simpath, i))]
                if (agv_type_id in [5,11,17,18]):
                    #picking车
                    agv_dir_list = [i for i in os.listdir(configs.simpath) if
                                    i[0] == 'P' and os.path.isdir(os.path.join(configs.simpath, i))]
                try:
                    agv_dir_list.sort(key=self.key_num)
                except:
                    logger.error(f'{agv_dir_list}排序失败!')

                start_agv_num=min(len(agv_dir_list),int(configs.agv_nums))

                if (start_agv_num>0):
                    start_jees_command= r'cd /d ' + os.path.join(configs.simpath,agv_dir_list[0]) + ' && start  /min jess.exe -P ' +str(self.jess_port)
                    results = os.system(start_jees_command)
                    logger.info(f'------start jess.exe command:{start_jees_command},return content:{results}')
                    time.sleep(2)

                    for i in range(start_agv_num):
                        current_agv_shell_port=(self.shell_port+self.start_agv_id+i)
                        command = r'cd /d ' + os.path.join(configs.simpath,agv_dir_list[i]) + ' && start  /min agv_shell.exe --shell-port '+str(current_agv_shell_port) +' --jess-port ' +str(configs.jess_port)
                        results = os.system(command)
                        if(results==0):
                            logger.info(f'-------start agv_shell.exe succ!!file:{agv_dir_list[i]},agv_id:{self.start_agv_id+i},command:{command},return content:{results}')
                        else:
                            logger.info(
                                f'-------start agv_shell.exe failed!! file:{agv_dir_list[i]},agv_id:{self.start_agv_id+i},command:{command},return content:{results}')
                        time.sleep(2)
                logger.info(f'End open vehicles process,agv_num:{start_agv_num}')
            else:
                logger.info('path:{} not exists!'.format(configs.simpath))
        except Exception as e:
            logger.error('open vehicles process error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def func_webvehicle(self):
        try:
            command = r'cd /d ' + os.path.join(configs.simpath) + ' && start  /min  webvehicle-go.exe'
            results = os.system(command)
            logger.info(f'------start webvehicle-go command:{command},return content:{results}')
            time.sleep(2)
        except Exception as e:
            logger.error('open webvehicle-go process error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def func_open_vehicles_web(self):
        try:
            logger.info('start open_vehicles_web!')
            command = r'cd /d ' + self.chromepath + ' && start chrome.exe http://127.0.0.1:4405'
            results = os.system(command)
            logger.info('End open_vehicles_web!return content:{}'.format(results))
        except Exception as e:
            logger.error('open_vehicles_web error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def func_dispath(self):
        try:
            logger.info('Start open dispath process!')
            command=r'cd /d '+self.dispathpath+' && start /min  '+self.dispath_process_name
            results = os.system(command)
            # results=os.startfile(self.dispath_process_path)
            logger.info('End open dispath process!,return content:{}'.format(results))
        except Exception as e:
            logger.error('open dispath process error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def func_engine(self):
        try:
            logger.info('Start open engine process!')
            # results=os.startfile(self.engine_process_path)
            command = r'cd /d ' + self.enginepath + ' && start /min  ' + self.engine_process_name
            results = os.system(command)
            logger.info('End open engine process!,return content:{}'.format(results))
        except Exception as e:
            logger.error('open engine process error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def func_om(self):
        try:
            logger.info('Start open om process!')
            # results=os.startfile(self.engine_process_path)
            command = r'cd /d ' + self.ompath + ' && start  /min ' + configs.om_process_name
            results = os.system(command)
            logger.info('End open om process!,return content:{}'.format(results))
        except Exception as e:
            logger.error('open om process error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))
    #
    # def func_io(self):
    #     try:
    #         logger.info('Start open io process!')
    #         # results=os.startfile(self.engine_process_path)
    #         command = r'cd /d ' + configs.iopath + ' && start  /min ' + configs.io_process_name
    #         results = os.system(command)
    #         logger.info('End open io process!,return content:{}'.format(results))
    #     except Exception as e:
    #         logger.error('open io process error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def func_open_webmonitor_web(self):
        try:
            logger.info('start webmonitor in  web!')
            command = r'cd /d ' + self.chromepath + ' && start chrome.exe http://127.0.0.1:5006'
            results = os.system(command)
            logger.info('End webmonitor in  web!return content:{}'.format(results))
        except Exception as e:
            logger.error('open webmonitor in web error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def func_rest_api(self):
        try:
            logger.info('start open rest_api process!')
            command1=r'cd /d ' + self.rest_api_path + ' && start /min  ' + self.rest_api_process_name
            results =os.system(command1)
            logger.info('End open rest_api process!return content:{}'.format(results))
        except Exception as e:
            logger.error('open rest_api error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def func_bsmonitor(self):
        try:
            logger.info('start open monitor')
            command = r'cd /d ' + self.webmonitorpath + ' && start  /min ' + self.monitor_process_name +' runserver  0.0.0.0:5006 --noreload'
            results =os.system(command)
            print(command)
            # print('monitor_open_process_path:{}'.format(self.monitor_open_process_path))
            logger.info('End open monitor process!return content:{}'.format(results))
        except Exception as e:
            logger.error('open monitor error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def Modify_new_general_config(self):
        self.modify_dispath_db_config()
        self.modify_engine_db_config()
        self.modify_rest_api_db_config()
        self.modify_om_db_config()

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False



    def kill_process(self, process_list):
        try:
            #
            for i in process_list:
                # print(i)
                logger.info('Star kill process:{}!'.format(i))
                if i.find('om.exe')>-1:
                    command = r'wmic process where name="{program}" delete'.format(program=i)
                else:
                    command = 'taskkill /f /t /im {program}'.format(program=i)
                temp = os.system(command)
                # if self.is_admin():
                #     print("以管理员权限运行")
                #     temp=os.system(command)
                # else:
                #     if sys.version_info[0] == 3:
                #         print("无管理员权限")
                #         ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

                logger.info('End kill prcess:{} !'.format(i))
        except Exception as e:
            logger.error('kill all process error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def kill_vehicles(self):
        process_list = [
                        'jess.exe', 'motion_template.exe', 'agv_shell.exe', 'custom_zhongwang.exe',
                        'custom_fork.exe', 'webvehicle-go.exe',
                        'custom_sim_server_demo.exe', 'custom_sim_server.exe', 'motion_net_test.exe',
                        'custom_picking.exe']
        self.kill_process(process_list)

    def kill_webmonitor(self):
        process_list = [self.monitor_process_name, self.rest_api_process_name]
        self.kill_process(process_list)

    def kill_general_all(self):
        process_list=[self.dispath_process_name,self.engine_process_name,self.monitor_process_name,self.rest_api_process_name,configs.om_process_name]
        self.kill_process(process_list)

    def onestart_webmonitor(self):
        process_list = [self.monitor_process_name, self.rest_api_process_name]
        self.kill_process(process_list)
        process_path = [self.rest_api_path]
        self.delete_log(process_path)
        self.func_rest_api()
        time.sleep(5)
        self.func_bsmonitor()
        time.sleep(5)
        self.func_open_webmonitor_web()


    def onestart_om(self):
        process_list=[configs.om_process_name]
        self.kill_process(process_list)
        time.sleep(1)
        process_path = [self.ompath]
        self.delete_log(process_path)
        self.func_om()

    def onestart_dispath(self):
        process_list=[configs.dispath_process_name]
        self.kill_process(process_list)
        time.sleep(1)
        process_path = [self.dispathpath]
        self.delete_log(process_path)
        self.func_dispath()

    def onestart_engine(self):
        process_list = [configs.engine_process_name]
        self.kill_process(process_list)
        time.sleep(1)
        process_path = [self.enginepath]
        self.delete_log(process_path)
        self.func_engine()

    # def onestart_io(self):
    #     process_list = [configs.io_process_name]
    #     self.kill_process(process_list)
    #     time.sleep(1)
    #     process_path = [configs.iopath]
    #     self.delete_log(process_path)
    #     self.func_io()


    def onestart_vehicles(self):
        self.kill_vehicles()
        self.delete_vehicles_log()
        self.func_vehicles()


    def Start_new_general_all(self):
        self.delete_new_general_log()
        self.func_engine()
        time.sleep(5)
        self.func_dispath()
        time.sleep(5)
        self.func_om()
        self.func_rest_api()
        time.sleep(5)
        self.func_bsmonitor()
        time.sleep(2)
        self.func_open_webmonitor_web()
        time.sleep(5)

    def delete_log(self,process_path):
        try:
            logger.info('start delete  process:{} log!'.format(process_path))
            for i in process_path:
                logpath = os.path.join(i, 'log')
                if os.path.exists(logpath):
                    shutil.rmtree(logpath)
                logpath2 = os.path.join(i, 'TSLogs')
                if os.path.exists(logpath2):
                    shutil.rmtree(logpath2)
            logger.info('end delete  process:{} log!'.format(process_path))
        except Exception as e:
            logger.error('delete process:{} log error!原因：{}'.format(process_path,e))


    def delete_new_general_log(self):
        process_path = [self.dispathpath, self.enginepath, self.ompath, self.rest_api_path]
        self. delete_log(process_path)

    def delete_vehicles_log(self):
        try:
            if os.path.exists(configs.simpath):
                logger.info('start delete vehicles_log!')
                for i in os.listdir(configs.simpath):
                    single_sim_path=os.path.join(configs.simpath,i)
                    logpath = os.path.join(single_sim_path, 'log')
                    if os.path.exists(logpath):
                        # self.d.detele_path(logpath)
                        shutil.rmtree(logpath)
                logger.info('end delete vehicles_log!')
            else:
                logger.info('path:{} not exists!'.format(configs.simpath))
        except Exception as e:
            logger.error('delete vehicles_log error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

#
# create_new_db=Opera_DB().db()


