from Logger_module import logger
import requests
import json


add_object_task_url=r'http://127.0.0.1:2000/api/dispatch/tasks/object-tasks/target/'
check_object_task_url=r'http://127.0.0.1:2000/api/dispatch/tasks/object-tasks/'
pheaders={"Content-Type": "application/json"}

def api_check_object_task_by_status(status_id):
    try:
        new_check_object_task_url=check_object_task_url+'?status_id={}'.format(status_id)
        pr = requests.get(url= new_check_object_task_url, headers=pheaders)
        logger.info(f'-----url：{ new_check_object_task_url},返回：{pr.status_code}')
        if (pr.status_code == 200):
            return_dict = eval(pr.text.replace('null', 'None').replace('false', 'False').replace('true', 'True'))
            object_task_num=len(return_dict)
            return object_task_num
        else:
            logger.info(
                f'---------------check_id:{current_check_id}---------Failed :api_check_agv_commands! agv_list：{status_id},status_code:{pr.status_code}')
            return None

    except Exception  as e:
        logger.error(f'---------------check_id:{current_check_id}---------api_check_agv_commands Error!!results:{e}')
        return None

def api_del_object_task(object_task_id):
    #根据Object_task_id查询任务
    body={
    "data": [
        {
            "object_task_id": 1
        }
    ]
}

def common_post_agv_opt_api(data_dict):
    try:
        body ={"data": [] }
        suc_object_task_info=None
        if isinstance(data_dict,dict):
            if "object_id"in data_dict.keys() and "destination_location_id" in data_dict.keys():

                data_dict["task_type_id"]= 2
                data_dict["status_id"]=2
                body["data"].append(data_dict)


                payload = json.dumps(body)
                pr = requests.post(url=add_object_task_url, data=payload, headers=pheaders)
                logger.info(f'接口url：{add_object_task_url},下发指令body：{payload}')
                results = dict(eval(pr.text.replace('null', 'None').replace('false', 'False').replace('true', 'True')))[
                    "msg"]
                if (pr.status_code == 200 and results == 'success'):
                    suc_object_task_info = \
                    dict(eval(pr.text.replace('null', 'None').replace('false', 'False').replace('true', 'True')))["data"][
                        "success_list"]

                    if suc_object_task_info != []:
                        logger.info(f'api succ, and succ {caller_func_name},add_succ_object_task_info：{suc_object_task_info}')
                    error_info = \
                    dict(eval(pr.text.replace('null', 'None').replace('false', 'False').replace('true', 'True')))["data"][
                        "error_list"]
                    if error_info != []:
                        logger.info(f'api succ ,but error {caller_func_name},rertun error_object_task_info:{error_info}')
                else:
                    logger.info(f'api fail,and fail{caller_func_name}, data_dict：{data_dict},status_code:{pr.status_code}')
        else:
            logger.info(f'传入参数Error !!{data_dict} is not dict!')


        return suc_object_task_info
    except Exception as e:
        logger.error(f'Error ：commmon_post_agv_opt_api：{caller_func_name} !!results:{e}')
        return None


