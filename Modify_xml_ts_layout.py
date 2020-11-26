import xlrd
import shutil,os
from Logger_module import logger
from xml.dom import minidom
from xml.etree import ElementTree  # 导入ElementTree模块
from ConfigManager import configs
import xml.etree.ElementTree as ET



class write_to_general_xml():
    def __init__(self):

        self.temp_file='temp.xml'
        self.excelpath=configs.excelpath
        self.dispathpath=configs.dispathpath
        self.enginepath=configs.enginepath
        self.dispath_config_path=configs.dispath_config_path
        self.agv_info_path=configs.agv_info_path
        self.layoutpath=configs.layoutpath
        self.agv_type_id=int(configs.agv_type_id)
        #根据agv_type_id感知是配置picking调度还是其他的调度

    def prettyXml( self,element,level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
        indent= '\t'
        newline='\n'
        if element:  # 判断element是否有子元素
            if element.text == None or element.text.isspace():  # 如果element的text没有内容
                element.text = newline + indent * (level + 1)
            else:
                element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
                # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
        temp = list(element)  # 将elemnt转成list
        for subelement in temp:
            if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
                subelement.tail = newline + indent * (level + 1)
            else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
                subelement.tail = newline + indent * level
            self.prettyXml(subelement,level=level + 1)  # 对子元素进行递归操作

        # ElementTree.dump(element)  # 显示出美化后的XML内容

    def petty_filename(self,file,newfile):
        with open(file, 'r', encoding='utf-8') as f1 , open(newfile, 'w', encoding='utf-8')  as f2:
            for line in f1.readlines():
                if line.split():  # if li.strip():
                    f2.writelines(line)
        tree = ElementTree.parse(newfile)  # 解析test.xml这个文件，该文件内容如上文
        element= tree.getroot()  # 得到根元素，Element类
        self.prettyXml(element)
        tree.write(newfile)

    def get_excel_info(self):
        try:
            workbook = xlrd.open_workbook(self.excelpath)
            sheet_names=workbook.sheet_names()
            for i  in sheet_names:
                sheet=workbook.sheet_by_name(i)
                num=sheet.nrows-1
                title_list = sheet.row_values(0)
                logger.info('Excel表{}的标题栏是：{},内容有{}行'.format(i,title_list,num))
        except Exception as e:
            logger.error('get_excel_info error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))




    def create_agv_info_xml(self,file_name):
        try:
            a = ET.Element('agv_info')
            b1 = ET.SubElement(a, 'layouts')
            b2 = ET.SubElement(a, 'router')
            b3 = ET.SubElement(a, 'agvs')

            layout = ET.SubElement(b1, 'layout', {'dock': '/etc/docks.xml',"id":"1","path":"/etc/layout.xml","search_type":"1"})
            attribute = ET.SubElement(b2, 'attribute',{"detourByDock_enable":"0","detourByDock_timeout":"3000"})

            tree1 = ET.ElementTree(a)
            tree1.write(file_name, encoding='utf-8')
        except Exception as e:
            logger.error('create agv_info xml error!原因：{},filename：{},line:{}'.format(e,
                                                                                             e.__traceback__.tb_frame.f_globals[
                                                                                                 '__file__'],
                                                                                             e.__traceback__.tb_lineno))

    def create_dispatch_config_xml(self, file_name):
        try:
            a = ET.Element('Configs')
            b1 = ET.SubElement(a, 'Picking-Locaton')
            b2 = ET.SubElement(a, 'Common-Location')
            b3 = ET.SubElement(a, 'object_info')
            b1_1 = ET.SubElement(b1, 'Location')
            b1_2 = ET.SubElement(b1, 'location_relation')
            b1_3 = ET.SubElement(b1, 'section')
            b2_1 = ET.SubElement(b2, 'Location')
            b2_2 = ET.SubElement(b2, 'location_relation')
            tree1 = ET.ElementTree(a)
            tree1.write(file_name, encoding='utf-8')

        except Exception as e:
            logger.error('create dispatch_config xml error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))




    def modify_dispatchxml_location(self):
        excelfilepath=self.excelpath
        dispatchxmlpath=self.dispath_config_path
        for filepath in [excelfilepath, dispatchxmlpath]:
            if not os.path.exists(filepath):
                logger.error('error!!!文件：{}不存在！'.format(filepath))

        if os.path.exists(dispatchxmlpath) and os.path.exists(excelfilepath):
            xmlDom = minidom.parse(dispatchxmlpath)
            # excel表格为modify的内容，获取他要修改的行数和标题栏
            workbook = xlrd.open_workbook(excelfilepath)
            try:
                sheet_name='Location'
                sheet = workbook.sheet_by_name(sheet_name)
                config_location_num=sheet.nrows-1
                title_list= sheet.row_values(0)
                if(self.agv_type_id in[5,11,17,18]):
                    f=xmlDom.getElementsByTagName('Picking-Locaton')[0]
                else :
                    f = xmlDom.getElementsByTagName('Common-Location')[0]
                x = f.getElementsByTagName('Location')[0]
                if (config_location_num> 0):
                    logger.info(
                        '---------------------------------start Location config ....----------------------------------------------')
                    for j in range(0, config_location_num):
                        row_value = sheet.row_values(j + 1)

                        info_node = xmlDom.createElement("node")
                            # 这个属性类似map中key,value
                        # print(f'------第{j}行的标题栏：{title_list},值:{row_value}')
                        for title in title_list:
                            rawVal = row_value[title_list.index(title)]
                            if rawVal!='':
                                value = rawVal
                                if title in ['id', 'location_type','dock_id', 'shelf_layer', 'operation_parameter_fetch', 'operation_parameter_put',
                                             'priority',	'agv_type_filter_mode',	'fit_agv_type','agv_id_filter_mode','fit_agv_id', 'exit_dock_id',
                                             'max_tasking_agv_num']:
                                    value=int(rawVal)
                                elif title in['active','is_leaf']:
                                     if rawVal=='t'or rawVal=='T':
                                         value='true'
                                     elif rawVal=='f'or rawVal=='F':
                                         value = 'false'
                                info_node.setAttribute(title, str(value))
                            elif title in ['shelf_layer', 'operation_parameter_fetch','operation_parameter_put'] and self.agv_type_id in[5,11,17,18]:
                                # print(f'第{j}行的标题栏：{title},值:{value}')
                                value=0
                                info_node.setAttribute(title, str(value))

                        x.appendChild(info_node)

                    f = open(self.temp_file, "w", encoding='utf-8')
                    xmlDom.writexml(f)
                    f.close()
                    if os.path.exists(self.temp_file):
                        self.petty_filename(self.temp_file, dispatchxmlpath)
                        os.unlink(self.temp_file)

                    logger.info(
                        '---------------------------------end Location config ....----------------------------------------------')
                else:
                    logger.info('location 没有配置,不需要写入xml')


            except Exception as e:
                logger.error('modify_dispatchxml_location error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))
          
    def modify_dispatchxml_location_relation(self):
        excelfilepath = self.excelpath
        dispatchxmlpath = self.dispath_config_path

        for filepath in [excelfilepath, dispatchxmlpath]:
            if not os.path.exists(filepath):
                logger.error('error!!!文件：{}不存在！'.format(filepath))

        if os.path.exists(dispatchxmlpath) and os.path.exists(excelfilepath):
            xmlDom = minidom.parse(dispatchxmlpath)
            # excel表格为modify的内容，获取他要修改的行数和标题栏
            workbook = xlrd.open_workbook(excelfilepath)
            try:
                sheet_name='Location Relation'
                sheet = workbook.sheet_by_name(sheet_name)
                config_num = sheet.nrows - 1
                title_list = sheet.row_values(0)
                if (self.agv_type_id in [5, 11, 17, 18]):
                    f = xmlDom.getElementsByTagName('Picking-Locaton')[0]
                else:
                    f = xmlDom.getElementsByTagName('Common-Location')[0]
                x = f.getElementsByTagName('location_relation')[0]
                if (config_num > 0):
                    logger.info(
                        '---------------------------------start Location relation config ....----------------------------------------------')
                    for j in range(config_num):
                        row_value = sheet.row_values(j + 1)

                        info_node = xmlDom.createElement("node")
                        # 这个属性类似map中key,value
                        # print(f'------第{j}行的标题栏：{title_list},值:{row_value}')
                        for title in title_list:
                            rawVal = row_value[title_list.index(title)]
                            if rawVal != '':
                                if title in ['ancestor_node_id','distance','node_id']:
                                    value = int(rawVal)
                                # print(f'第{j}行的标题栏：{title},值:{value}')
                                info_node.setAttribute(title, str(value))
                        x.appendChild(info_node)

                    f = open(self.temp_file, "w", encoding='utf-8')
                    xmlDom.writexml(f)
                    f.close()
                    if os.path.exists(self.temp_file):
                        self.petty_filename(self.temp_file, dispatchxmlpath)
                        os.unlink(self.temp_file)
                    logger.info('---------------------------------end Location relation config ....----------------------------------------------')
                else:
                    logger.info('location_relation 没有配置,不需要写入xml')

            except Exception as e:
                logger.error('modify_dispatchxml_location_relation error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def modify_dispatchxml_section(self):

        excelfilepath = self.excelpath
        dispatchxmlpath = self.dispath_config_path
        for filepath in [excelfilepath, dispatchxmlpath]:
            if not os.path.exists(filepath):
                logger.error('error!!!文件：{}不存在！'.format(filepath))

        if os.path.exists(dispatchxmlpath) and os.path.exists(excelfilepath):
            xmlDom = minidom.parse(dispatchxmlpath)
            # excel表格为modify的内容，获取他要修改的行数和标题栏
            workbook = xlrd.open_workbook(excelfilepath)
            try:
                sheet_name = 'Section'
                sheet = workbook.sheet_by_name(sheet_name)
                config_location_num = sheet.nrows - 1
                title_list = sheet.row_values(0)
                if (self.agv_type_id in [5, 11, 17, 18]):
                    f = xmlDom.getElementsByTagName('Picking-Locaton')[0]
                    x = f.getElementsByTagName('section')[0]
                    if (config_location_num > 0):
                        logger.info(
                            '---------------------------------start section config ....----------------------------------------------')
                        for j in range(0, config_location_num):
                            row_value = sheet.row_values(j + 1)

                            info_node = xmlDom.createElement("node")
                            # 这个属性类似map中key,value
                            # print(f'------第{j}行的标题栏：{title_list},值:{row_value}')
                            for title in title_list:
                                rawVal = row_value[title_list.index(title)]

                                if rawVal != '':
                                    value = rawVal
                                    if title in ['id', 'dispatch_section_type', 'ancestor_node_id', 'rest_node_id',
                                                 'rest_base_score']:
                                        value = int(rawVal)
                                    elif title in ['can_rest']:
                                        if rawVal == 't' or rawVal == 'T':
                                            value = 'true'
                                        elif rawVal == 'f' or rawVal == 'F':
                                            value = 'false'
                                    info_node.setAttribute(title, str(value))

                                else :
                                    if title in ['id','name','dispatch_section_type', 'ancestor_node_id',
                                                 'rest_node_id','can_rest','rest_base_score',
                                                 'center_pos_x','center_pos_y','length','width','height']:
                                        value=rawVal
                                    # print(f'第{j}行的标题栏：{title},值:{value}')
                                        info_node.setAttribute(title, str(value))
                            x.appendChild(info_node)

                        f = open(self.temp_file, "w", encoding='utf-8')
                        xmlDom.writexml(f)
                        f.close()
                        if os.path.exists(self.temp_file):
                            self.petty_filename(self.temp_file, dispatchxmlpath)
                            os.unlink(self.temp_file)

                        logger.info(
                            '---------------------------------end section config ....----------------------------------------------')
                    else:
                        logger.info('section 没有配置,不需要写入xml')
                else:
                    logger.info('非picking不需要写section内容')

            except Exception as e:
                logger.error('modify_dispatchxml_section  error!原因：{},filename：{},line:{}'.format(e,
                                                                                   e.__traceback__.tb_frame.f_globals[
                                                                                       '__file__'],
                                                                                   e.__traceback__.tb_lineno))
    def modify_dispatchxml_object(self):
        try:
            excelfilepath = self.excelpath
            dispatchxmlpath = self.dispath_config_path
            for filepath in [excelfilepath, dispatchxmlpath]:
                if not os.path.exists(filepath):
                    logger.error('error!!!文件：{}不存在！'.format(filepath))

            if os.path.exists(dispatchxmlpath) and os.path.exists(excelfilepath):
                xmlDom = minidom.parse(dispatchxmlpath)
                # excel表格为modify的内容，获取他要修改的行数和标题栏
                workbook = xlrd.open_workbook(excelfilepath)


                # try:
                sheet_name='Object'
                sheet = workbook.sheet_by_name(sheet_name)
                config_num = sheet.nrows - 1
                title_list = sheet.row_values(0)
                x = xmlDom.getElementsByTagName('object_info')[0]
                if ( config_num>0):
                    logger.info(
                        '---------------------------------start object config ....----------------------------------------------')

                    for j in range(config_num):
                        row_value = sheet.row_values(j + 1)

                        info_node = xmlDom.createElement("node")
                        # 这个属性类似map中key,value
                        # print(f'------第{j}行的标题栏：{title_list},值:{row_value}')
                        for title in title_list:
                            rawVal = row_value[title_list.index(title)]

                            if rawVal != '':
                                value = rawVal
                                if title in   ['id', 'object_type', 'fit_node_id', 'error_code',
                                         'pallet_type', 'home_node_id', 'current_node_id']:
                                    value = int(rawVal)
                                info_node.setAttribute(title, str(value))

                            elif title in[ 'id','object_type','physical_label',
                                     'length','width','height',
                                     'fit_node_id','error_code',
                                     'pallet_type','home_node_id',
                                     'current_node_id'] :
                                    value = rawVal
                                    # print(f'第{j}行的标题栏：{title},值:{value}')
                                    info_node.setAttribute(title, str(value))
                        x.appendChild(info_node)

                    f = open(self.temp_file, "w", encoding='utf-8')
                    xmlDom.writexml(f)
                    f.close()
                    if os.path.exists(self.temp_file):
                        self.petty_filename(self.temp_file, dispatchxmlpath)
                        os.unlink(self.temp_file)
                    logger.info(
                        '---------------------------------end object_info config ....----------------------------------------------')


                else:
                    logger.info('object_info没有配置，不需要写入xml')


        except Exception as e:
            logger.error('object_info xml error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def modify_agv_info_xml(self):
        for filepath in [self.excelpath, self.agv_info_path]:
            if not os.path.exists(filepath):
                logger.error('error!!!文件：{}不存在！'.format(filepath))
                # 重新创建agv_info.xml

        if os.path.exists(self.temp_file):
            os.unlink(self.temp_file)
        self.create_agv_info_xml(self.temp_file)
        self.petty_filename(self.temp_file, self.agv_info_path)
        os.unlink(self.temp_file)

        if os.path.exists(self.agv_info_path) and os.path.exists(self.excelpath):
            xmlDom = minidom.parse(self.agv_info_path)
            # excel表格为modify的内容，获取他要修改的行数和标题栏
            workbook = xlrd.open_workbook(self.excelpath)
            try:
                sheet = workbook.sheet_by_name('Agv_info')
                config_agv_num = sheet.nrows - 1
                title_list = sheet.row_values(0)

                x = xmlDom.getElementsByTagName("agvs")[0]

                if (config_agv_num > 0):
                    logger.info(
                        '---------------------------------start agv info config ....----------------------------------------------')


                    for j in range(config_agv_num):
                        row_value = sheet.row_values(j + 1)
                        info_node = xmlDom.createElement("agv")
                        # 这个属性类似map中key,value
                        # print(f'------第{j}行的标题栏：{title_list},值:{row_value}')
                        for title in title_list:
                            rawVal = row_value[title_list.index(title)]

                            if rawVal != '':
                                value = rawVal

                                if title in ['id', 'type', 'port', 'fts_port','shell_port','jess_port',
                                              'simulation', 'layout_id']:
                                    value = int(rawVal)
                                info_node.setAttribute(title, str(value))


                                # print(f'第{j}行的标题栏：{title},值:{value}')

                        x.appendChild(info_node)

                    f = open(self.temp_file, "w", encoding='utf-8')
                    xmlDom.writexml(f)
                    f.close()
                    if os.path.exists(self.temp_file):
                        self.petty_filename(self.temp_file, self.agv_info_path)
                        os.unlink(self.temp_file)
                    logger.info(
                        '---------------------------------end agv info config----------------------------------------------')


                else:
                    logger.info('agv_ino没有配置，不需要写入xml')

            except Exception as e:
                logger.error('agv_info xml error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))



    def detele_path(self,path):
       try:
        if os.path.exists(path):

            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    if (name.find('dbconnect.xml') > -1):
                        logger.info('文件不删除！！')
                    else:
                        os.remove(os.path.join(root, name))
                        logger.info('start detele path :{} files:{}!'.format(path, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
                    logger.info('start detele path :{} dirs:{}!'.format(path, name))
        else:
            logger.info('path :{}not exists!'.format(path))
       except Exception as e:
           logger.error('detele path :{} dirs/files error!原因：{}'.format(path,e))

    def detele_path_files(self,path,de_file):
       try:
        de_path=os.path.join(path,de_file)
        if os.path.exists(de_path):
            os.remove(de_path)
            logger.info('start detele path :{} files:{}!'.format(path, de_file))
        else:
            logger.info('path :{}not exists!'.format(de_path))
       except Exception as e:
           logger.error('detele path :{} files error!原因：{}'.format(path,e))

    def copy_ts_to_OM(self):
        try:
            logger.info('start copy_ts_to_OM !')
            omtspath=os.path.join(configs.ompath,'TS')
            if os.path.exists(configs.tsfilespath):
                if os.path.exists(omtspath) and omtspath!=configs.tsfilespath:
                    self.detele_path(omtspath)
                if not os.path.exists(omtspath):
                    os.makedirs(omtspath)
                dirlist = os.listdir(configs.tsfilespath)
                for dir in dirlist:
                    if dir.find('.py')>-1:
                        source = os.path.join(configs.tsfilespath, dir)
                        shutil.copy(source,omtspath)
            logger.info('end copy_ts_to_OM !')
        except Exception as e:
            logger.error('copy_ts_to_OM error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))




    def copy_layout_to_general_process(self):
        try:
            logger.info('------start copy layout and eg.-----')
            dispath_l=os.path.join(self.dispathpath,'etc')
            enginepath_l=os.path.join(self.enginepath,'etc')
            if not os.path.exists(dispath_l):
                os.makedirs(dispath_l)
            if not os.path.exists(enginepath_l):
                os.makedirs(enginepath_l)
            # 清空文件
            self.detele_path(dispath_l)
            self.detele_path(enginepath_l)
            # 复制文件
            dirlist=os.listdir(self.layoutpath)
            for dir in dirlist:
                source=os.path.join(self.layoutpath,dir)
                if (dir == 'docks.xml' or dir == 'layout.xml'):
                    shutil.copy(source, dispath_l)
                    logger.info('copy dir:{} to "{}"'.format(source, dispath_l))
                    shutil.copy(source, enginepath_l)
                    logger.info('copy dir:{} to "{}"'.format(source, enginepath_l))
                else:
                    shutil.copy(source, enginepath_l)
                    logger.info('copy dir:{} to "{}"'.format(source, enginepath_l))
            logger.info('------end copy layout and eg.-----')
        except Exception as e:
            logger.error('copy layout error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))

    def copy_layout_to_vehicles(self):
        try:
            if os.path.exists(configs.simpath):
                logger.info('------start copy layout to vehicles-----')

                for i in os.listdir(configs.simpath):
                    vehiclespath = os.path.join(configs.simpath, i)
                    # print(configs.simpath,vehiclespath,os.path.isdir(vehiclespath))
                    if os.path.isdir(vehiclespath):
                        mappath = os.path.join(vehiclespath, 'etc\map')
                        if not os.path.exists(mappath):
                            os.makedirs(mappath)
                        # 清空文件
                        self.detele_path(mappath)
                        # 复制文件
                        dirlist=os.listdir(self.layoutpath)
                        for dir in dirlist:
                            source=os.path.join(self.layoutpath,dir)
                            if (dir == 'docks.xml' or dir == 'layout.xml'):
                                shutil.copy(source, mappath)
                                logger.info('copy dir:{} to "{}"'.format(source, mappath))
                logger.info('------end copy layout to vehicles-----')
            else:
                logger.info('path:{} not exists!'.format(configs.simpath))
        except Exception as e:
            logger.error('copy layout to vehicles error!原因：{},filename：{},line:{}'.format(e,e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno))


    def modify_all_dispatch_xml(self):
        #新新建一个xml
        logger.info('--重新创建一个新的dispath_config.xml文件--')
        if os.path.exists(self.temp_file):
            os.unlink(self.temp_file)
        self.create_dispatch_config_xml(self.temp_file)
        self.petty_filename(self.temp_file, self.dispath_config_path)
        os.unlink(self.temp_file)
        #然后更改location

        self.modify_dispatchxml_location()
        self.modify_dispatchxml_location_relation()
        self.modify_dispatchxml_section()
        self.modify_dispatchxml_object()


