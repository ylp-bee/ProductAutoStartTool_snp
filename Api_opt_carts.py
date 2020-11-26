from Logger_module import logger
from ConfigManager import configs
import requests
import json
import inspect
import threading
import time

class Api_Add_Carts_To_Dispath:
    def __init__(self):
        self.__messy = 0
        base_url=r'http://127.0.0.1:2000'
        self.check_table_agvs_url=r'{}/api/engine/config-data/agvs/'.format(base_url)
        self.check_agv_commands_url=r'{}/api/engine/agv-commands/agvs/'.format(base_url)
        self.check_agvs_url = r'{}/api/engine/basic-data/agvs/'.format(base_url)
        self.add_agvs_url=r'{}/api/engine/ctrl-mgr/add/'.format(base_url)
        self.create_agvs_url=r'{}/api/engine/ctrl-mgr/create/'.format(base_url)
        self.setready_agvs_url='{}/api/engine/ctrl-mgr/set-ready/'.format(base_url)
        self.run_agvs_url=r'{}/api/engine/ctrl-mgr/run/'.format(base_url)


        self.agv_ids=configs.agv_ids

        if self.agv_ids:
            self.agv_ids=list(self.agv_ids)

        self.pheaders={"Content-Type": "application/json"}
        self.current_indispathlogic_agv_id=[]
        self.check_id=1




    def api_opt_check_agvs_info(self,agv_ids):
        try:
            if isinstance(agv_ids, list):
                check_agvs_url=self.check_agvs_url
            else:
                check_agvs_url = self.check_agvs_url + '{}/'.format(agv_ids)
            pr = requests.get(url=check_agvs_url, headers=self.pheaders)
            if (pr.status_code == 200):
                return_dict= eval(pr.text.replace('null', 'None').replace('false', 'False').replace('true', 'True'))
                check_agv_status_info = []
                key_names = {"agv_id", "agv_management_status_id"}
                if isinstance(agv_ids, list):
                    for singe_agv_info in return_dict["data"]:
                        need_agv_dict={key:value for key,value in singe_agv_info.items() if key in key_names and singe_agv_info["agv_id"] in agv_ids}
                        if need_agv_dict != {}:
                            check_agv_status_info.append(need_agv_dict)
                elif isinstance(agv_ids, int ):
                        singe_agv_info=return_dict["data"][0]
                        need_agv_dict = {key:value for key,value in singe_agv_info.items() if key in key_names and singe_agv_info["agv_id"]==agv_ids }
                        if need_agv_dict != {}:
                            logger.info(f'----succ! agv_id:{agv_ids},agv_status_id:{need_agv_dict}')
                            check_agv_status_info.append(need_agv_dict)
                if check_agv_status_info==[]:
                    check_agv_status_info=None
                return check_agv_status_info
            else:
                logger.info(f'Failed :api_opt_check_agvs_info! agv_list：{agv_ids},status_code:{pr.status_code}')
                return None
        except Exception  as e:
            logger.error(f'api_opt_check_agvs_info Error!!results:{e}')
            return None

    def common_post_agv_opt_api(self, api_agv_opt_url, agv_list, caller_func_name):
        try:
            body={"agv_list": agv_list}
            if isinstance(agv_list, list):
                body["agv_list"]=agv_list
                payload = json.dumps(body)
                pr = requests.post(url=api_agv_opt_url, data=payload, headers=self.pheaders)
                logger.info(f'接口url：{api_agv_opt_url},下发指令body：{payload}')
                results = dict(eval(pr.text.replace('null', 'None').replace('false', 'False').replace('true', 'True')))["msg"]
                if (pr.status_code == 200 and results == 'success'):
                    suc_info = dict(eval(pr.text.replace('null', 'None').replace('false', 'False').replace('true', 'True')))["data"]["success_list"]
                    suc_agv_id= [i["agv_id"] for i in suc_info]
                    if suc_info != []:
                        logger.info(f'api succ, and succ {caller_func_name},add_succ_agv_ids：{suc_info}')
                    error_info=dict(eval(pr.text.replace('null', 'None').replace('false', 'False').replace('true', 'True')))["data"]["error_list"]
                    if error_info!=[]:
                        logger.info(f'api succ ,but error {caller_func_name},rertun error_agv_ids:{error_info}')
                else:
                    logger.info(f'api fail,and fail{caller_func_name}, agv_list：{agv_list},status_code:{pr.status_code}')
            else:
                logger.info(f'传入参数Error !!{agv_list} is not list!')
            if suc_agv_id:
                return suc_agv_id
            else:
                return None
        except Exception as e:
            logger.error(f'Error ：commmon_post_agv_opt_api：{caller_func_name} !!results:{e}')
            return None
    def api_check_agv_commands(self,agv_id,command_type_id=None,command_status_id=None):
        try:
            '''10000;"AGV_COMMAND_TYPE_ADD";"vehicle management";"add agv into dispath engine"
            10001;"AGV_COMMAND_TYPE_DELETE";"vehicle management";"delete agv from dispath engine"
            10002;"AGV_COMMAND_TYPE_CREATE";"vehicle management";"create agv in dispath engine"
            10003;"AGV_COMMAND_TYPE_DISTORY";"vehicle management";"distory agv in dispath engine"
            10004;"AGV_COMMAND_TYPE_SET_READY";"vehicle management";"set ready agv"
            10005;"AGV_COMMAND_TYPE_RUN";"vehicle management";"run agv"'''
            current_check_id=self.check_id+1
            self.check_id=current_check_id
            logger.info(f'---------------check_id:{current_check_id}----start check agv commands----agv_id:{agv_id} command_type_id：{command_type_id}-----')
            check_agv_commands_url=self.check_agv_commands_url+'{}/'.format(agv_id)
            pr = requests.get(url=check_agv_commands_url, headers=self.pheaders)
            logger.info(f'-----url：{check_agv_commands_url},返回：{pr.status_code}')
            if (pr.status_code == 200):
                return_dict = eval(pr.text.replace('null', 'None').replace('false', 'False').replace('true', 'True'))
                need_info=[]

                for i in return_dict["data"]:

                    singe_agv_commands=i
                    temp_name={"command_id","command_type_id","command_status_id"}
                    if command_type_id and command_status_id :
                        if  isinstance(command_status_id,int):
                            need_agv_dict = {key: value for key, value in singe_agv_commands.items() if
                                         key in temp_name and singe_agv_commands["command_status_id"] == command_status_id and singe_agv_commands["command_type_id"] ==command_type_id }
                        elif isinstance(command_status_id,list):
                            need_agv_dict = {key: value for key, value in singe_agv_commands.items() if
                                             key in temp_name and singe_agv_commands[
                                                 "command_status_id"] in command_status_id  and singe_agv_commands[
                                                 "command_type_id"] == command_type_id}
                            a={key: value for key, value in singe_agv_commands.items() if key in temp_name and
                               singe_agv_commands[ "command_status_id"] in command_status_id and singe_agv_commands[
                                                 "command_type_id"] == command_type_id}
                            # print(a)
                    elif  not command_type_id and command_status_id:
                        if isinstance(command_status_id, int):
                            need_agv_dict = {key:value  for key ,value in singe_agv_commands.items() if key in temp_name and singe_agv_commands["command_status_id"]== command_status_id}
                        elif isinstance(command_status_id, list):

                            need_agv_dict = {key: value for key, value in singe_agv_commands.items() if
                                             key in temp_name and singe_agv_commands[
                                                 "command_status_id"] in command_status_id}
                    elif  command_type_id and not  command_status_id:

                        need_agv_dict = {key:value  for key ,value in singe_agv_commands.items() if key in temp_name and singe_agv_commands["command_type_id"] ==command_type_id}

                    else:
                        need_agv_dict = {key: value for key, value in singe_agv_commands.items() if  key in temp_name }
                    if need_agv_dict!={}:
                        logger.info(
                            f'---------------check_id:{current_check_id}--succ！！！agv_id:{agv_id}, command_type_id：{command_type_id},command_status:{command_status_id},agv_command：{need_agv_dict}')
                        need_info.append(need_agv_dict)
                logger.info(f'---------------check_id:{current_check_id}---------end check agv commands!!!')
                if need_info==[]:
                    need_info=None

                return need_info
            else:
                logger.info(f'---------------check_id:{current_check_id}---------Failed :api_check_agv_commands! agv_list：{agv_id},status_code:{pr.status_code}')
                return None

        except Exception  as e:
            logger.error(f'---------------check_id:{current_check_id}---------api_check_agv_commands Error!!results:{e}')
            return None


    def api_opt_add_agv(self,agv_list):
        caller_func_name = inspect.stack()[1][3]
        self.common_post_agv_opt_api(self.add_agvs_url, agv_list, caller_func_name)
    def api_opt_create_agv( self,agv_list):
        caller_func_name = inspect.stack()[1][3]
        self.common_post_agv_opt_api(self.create_agvs_url, agv_list, caller_func_name)
    def api_opt_setready_agv(self,agv_list):
        caller_func_name = inspect.stack()[1][3]
        self.common_post_agv_opt_api(self.setready_agvs_url, agv_list, caller_func_name)
    def api_opt_run_agv(self,agv_list):
        caller_func_name = inspect.stack()[1][3]
        self.common_post_agv_opt_api(self.run_agvs_url, agv_list, caller_func_name)


    def auto_start_main(self,agv_id):
        '''1;"in_system"
        2;"out_system"
        3;"online"
        4;"offline"
        5;"ready"
        6;"not_ready"
        7;"in_dispatch"
        8;"out_dispatch"
        9;"running"
        10;"not_running"
        '''

        '''10000;"AGV_COMMAND_TYPE_ADD";"vehicle management";"add agv into dispath engine"
        10001;"AGV_COMMAND_TYPE_DELETE";"vehicle management";"delete agv from dispath engine"
        10002;"AGV_COMMAND_TYPE_CREATE";"vehicle management";"create agv in dispath engine"
        10003;"AGV_COMMAND_TYPE_DISTORY";"vehicle management";"distory agv in dispath engine"
        10004;"AGV_COMMAND_TYPE_SET_READY";"vehicle management";"set ready agv"
        10005;"AGV_COMMAND_TYPE_RUN";"vehicle management";"run agv"'''

        logger.info(f'===start auto start agv_id :{agv_id}===')
        while 1:
            agv_list=[]
            d=self.api_opt_check_agvs_info(agv_id)
            if d:
                agv_id=d[0]["agv_id"]
                agv_list.append(agv_id)
                status_id=d[0]["agv_management_status_id"]
                if (status_id==2):
                    if not (self.api_check_agv_commands(agv_id,10000,[10,11])) :
                        self.api_opt_add_agv(agv_list)
                if (status_id==1):
                    if not (self.api_check_agv_commands(agv_id, 10002,[10,11])):
                        self.api_opt_create_agv(agv_list)
                if (status_id==3):
                    if not (self.api_check_agv_commands(agv_id, 10004,[10,11])):
                        self.api_opt_setready_agv(agv_list)
                if (status_id==5):
                    if not (self.api_check_agv_commands(agv_id, 10005,[10,11])):
                        self.api_opt_run_agv(agv_list)
                if(status_id==7 or status_id==9):
                    if agv_id not in self.current_indispathlogic_agv_id:
                        self.current_indispathlogic_agv_id.append(agv_id)
                    break

            time.sleep(3)

        logger.info(f'===end auto start agv_id :{agv_id}===')

    def check_messy(self):
      while 1:
        if [i for i in self.agv_ids if i not in self.current_indispathlogic_agv_id ]==[]:
            self.__messy=1
            break
        time.sleep(5)


    def Run_main(self,agv_list=None):
        try:
            logger.info('Start check carts status and auto add carts to dispathlogic.')
            Threads = []
            if agv_list==None:
                agv_list=self.agv_ids
            if agv_list:
                for agv_id in agv_list:
                    t = threading.Thread(target=self.auto_start_main, args=(agv_id,))
                    t.daemon = 1
                    Threads.append(t)

                t1 = threading.Thread(target=self.check_messy)
                t1.daemon = 1
                Threads.append(t1)

                # 启动所有线程
                for i in Threads:
                    i.start()
                # 当标志位【 messy 】时所有多线程结束
                while 1:
                    if self.__messy:
                        break
                logger.info('End check carts status and auto add carts to dispathlogic Threads')
            else:
                logger.error('No need check and auto add.文件config.ini模块[auto_add_agv]agv_ids设置为None,若要自动启动请重新配置后重启。')
        except Exception as e:
            logger.error('check carts status and auto add carts to dispathlogic error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

