# -*- coding: utf-8 -*-
from Opt_multiple_process import Opera_DB
from Opt_multiple_process import modify_general_config_and_process_opra as mgo
import time
from Modify_xml_ts_layout import write_to_general_xml as wg
from Logger_module import logger
from ConfigManager import configs
from version import program_version_no as v ,modify_content as mc,user_instruction as ui,opt_instruction as oi
from Api_opt_carts import Api_Add_Carts_To_Dispath as aac
from Auto_agv_infos_from_docks import Auto_write_agv_info as awa

def logger_tools_opt(opt=None):
    if opt==1:
        logger.info(oi)
    else:
        print(oi)

if __name__ == "__main__":
    logger.info(ui)

    time.sleep(0.1)
    while 1:
        time.sleep(0.5)
        put_num=input('''选择数字0-11。查看操作说明请输入i,请输入：''')
        try:
            if(int(put_num)==1):
                #写数据库配置

                mgo().Modify_new_general_config()


            elif(int(put_num)==2):
                # 数据库备份
                while 1:
                    put1=input("该操作将删除数据库，然后新建，创建角色，恢复备份！请确认需要一键创建，Y or N!!请输入：")
                    try:
                        if (put1== 'Y' or put1== 'y'):
                           Opera_DB().db_create()
                           break
                        else:
                            break
                    except:
                        print("请输入'Y'or 'N'!")
            elif(int(put_num)==3):
                #清理数据库
                Opera_DB().db_clear()
            elif(int(put_num)==4):
                #关闭所有的进程(不包含仿真车载进程)

                    mgo().kill_general_all()

            elif(int(put_num)==5):
                #5.一键启动进程（不包含仿真车载进程；先清理log，再启动进程；）；
                        mgo().Start_new_general_all()
            elif (int(put_num) == 51):
                # 51.一键重启dispath（关闭、清理log、启动）
                mgo().onestart_dispath()
            elif (int(put_num) == 52):
                # 52.一键重启engine（关闭、清理log、启动）
                mgo().onestart_engine()
            elif (int(put_num) == 55):
                #55.一键重启webmonitor（关闭、清理log、启动）
                   mgo().onestart_webmonitor()
            elif (int(put_num) == 56):
                # 56.一键重启om（关闭、清理log、启动）
                    mgo().onestart_om()

            elif (int(put_num) == 59):
                # 59.一键关闭谷歌浏览器
                    process_list = ['chrome.exe']
                    mgo().kill_process(process_list)
            elif (int(put_num) == 6):
                wg().get_excel_info()
            elif (int(put_num) == 7):

                    wg().modify_all_dispatch_xml()


            elif (int(put_num) == 8):
                wg().modify_agv_info_xml()
            elif (int(put_num) == 9):

                    wg().copy_layout_to_general_process()
                    wg().copy_layout_to_vehicles()


            elif (int(put_num) == 10):
                sql=input('请输入sql的完整路径：')
                Opera_DB().psql_db(sql)
            elif (int(put_num) == 11):
                current_update_content = [i for i in mc if i["vesion_id"] == v][0]["update_content"]
                print(f'当前版本号：{v};\n当前更新内容：{current_update_content}\n')
                print('历史版本信息：')
                for x in mc:
                    print(f'{x["vesion_id"]}:{x["update_content"]}')
            elif (int(put_num) == 12):

                    wg().copy_ts_to_OM()

            elif (int(put_num) == 13):
              ''' 13.一键重启车载（关闭、清理log、启动）
             '''
              mgo().onestart_vehicles()
            elif (int(put_num) == 131):
                '''131.
                一键关闭仿真车载
               '''
                mgo().kill_vehicles()
            elif(int(put_num) == 132):
                mgo().func_vehicles()
            elif (int(put_num) == 133):
                ''' 133.
                一键清理车载log'''
                mgo().delete_vehicles_log()
            elif (int(put_num) == 134):
                #134.一键启动仿真车载进程（根据config.ini中[auto_find_agv_info]启动车载路径里面的车载。
                mgo().func_new_vehicles()
            elif (int(put_num) == 135):
                #135.启动车载服务和网页配置页面
                mgo().func_webvehicle()
                mgo().func_open_vehicles_web()
            elif (int(put_num) == 14):

                 mgo().delete_new_general_log()
            elif (int(put_num) == 15):
                 print('根据配置文件里面的[auto_add_agv]模块配置的agv_id列表启动车载')
                 aac().Run_main()
            elif (int(put_num) == 151):
                 inputstr = input('请输入一个agv列表，比如[1,2,3],请输入：')
                 agv_list=(eval(inputstr))
                 if isinstance(agv_list,list):
                    aac().Run_main(list(agv_list))
                 else:
                     print('输入不是列表')
            elif (int(put_num) == 16):

                 awa().excel_main()

            elif(int(put_num)==0):
                print('退出程序')
                break
            else:
                print('输入错误，请继续输入!!')

        except:
            if (put_num == 'i'):
                logger_tools_opt()
            else:
                print('输入错误，请继续输入!!')



