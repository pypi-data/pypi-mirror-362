
'''
解析Control-M作业的xml文件
'''

from lxml import objectify

class xml_pars(object):
    def __init__(self):
        pass
    
    def transform_attr_dict(self,job,key = ''):
        '''xml文件转为dict
        '''
        jobs = {}
        name = job.tag
        jobs[name] = [dict(job.attrib)]
        ns = job.getchildren()
        for n in ns:
            if n.tag not in jobs:
                jobs[n.tag] = []
            if n.getchildren():
                jobs[n.tag].append(self.transform_attr_dict(n))
            else:
                jobs[n.tag].append(dict(n.attrib))
        return jobs
    
class control_m(xml_pars):
    def __init__(self,file,encoding='utf-8'):
        with open(file,'r',encoding=encoding) as f:
            xml = objectify.parse(file)
            self.root = xml.getroot()
            self.root_dict = self.transform_attr_dict(self.root.SMART_FOLDER)
            self.info = dict(self.root.SMART_FOLDER.attrib)
            self.incond = self.transform_attr_dict(self.root.SMART_FOLDER.INCOND)
            self.outcond = self.transform_attr_dict(self.root.SMART_FOLDER.OUTCOND)
            self.rule = self.transform_attr_dict(self.root.SMART_FOLDER.RULE_BASED_CALENDAR)
            
    def get_folder_info(self,node = None,tag = 'SUB_FOLDER'):
        '''查看目录结构
        '''
        if node is None:
            node = self.root.SMART_FOLDER
        node_dir = {}
        nodes = [n for n in node.iterchildren(tag= tag)]
        if nodes:
            for n in nodes:
                node_sub = self.get_folder_info(n,tag)
                node_dir[n.attrib.get('JOBNAME')] = (n,node_sub)
            return node_dir
        else:
            return None
        
    def get_folder_all(self):
        '''获取所有目录展开
        '''
        data = [dict(n.attrib) for n in self.root.SMART_FOLDER.iterdescendants(tag = 'SUB_FOLDER')]
        return data
    
    def get_hops(self,show_variable = True):
        '''解析所有依赖
        '''
        hops = []
        for n in ['INCOND','OUTCOND']:
            data = [self.transform_attr_dict(n) for n in self.root.SMART_FOLDER.iterdescendants(tag = n)]
            hops.extend([x[n][0]['NAME'].split('-TO-') for x in data])
        #hops = [n['INCOND'][0]['NAME'].split('-TO-') for n in hops]
        hops = [tuple(n) for n in hops]
        return hops
    
    def get_jobs(self,show_variable = True):
        '''从文件夹中解析job
        '''
        data = [self.transform_attr_dict(n) for n in self.root.SMART_FOLDER.iterdescendants(tag = 'JOB')]
        if show_variable:
            for n in data:
                n['JOB'][0]['VARIABLE'] = self.join_param(n)
        return data
        
    def join_param(self,job):
        res = '|'.join(['"'+n['NAME']+'"="'+n['VALUE']+'"' for n in job['VARIABLE']])
        return res
