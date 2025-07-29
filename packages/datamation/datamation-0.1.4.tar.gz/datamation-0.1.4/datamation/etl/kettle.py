from lxml import objectify,etree
import lxml
from pathlib import Path
import uuid
from itertools import product

from mako.template import Template
from mako import exceptions

import networkx as nx

def xml_pars(node):
    '''xml格式解析转化'''
    sd = []
    for n in node:
        if n.countchildren():
            sor = {}
            for x in n.getchildren():
                sor[x.tag] = x if x.countchildren() else x.text
            sd.append(sor)
    return sd
        
class ktr_parse(object):
    def __init__(self,file):
        '''解析ktr文件'''
        with open(file,'r') as f:
            xml = objectify.parse(f)
        self.root = xml.getroot()
        self.ktr_name = Path(file).stem
        self.kuid = str(uuid.uuid1())
        self.__file = file
        
    def get_info(self):
        '''获取ktr的基本信息'''
        
        data = xml_pars(self.root.iterdescendants(tag= 'info'))
        for n in data:
            n['ktr'] = n.pop("name")
            n['kuid'] = self.kuid
        return data

    def get_parameters(self):
        '''ket的参数信息'''
        parameter = xml_pars(self.root.iterdescendants(tag= 'parameter'))
        for n in parameter:
            n['ktr'] = self.ktr_name
            n['kuid'] = self.kuid
        return parameter

    def get_hops(self,graph = False,directed = False):
        '''步骤顺序关联
        
        Args:
        -----
        grap: bool
            是否返回图的格式
        directed：bool
            返回的图是否为有向图 默认为无向图
        '''
        hop = xml_pars(self.root.iterdescendants(tag= 'hop'))
        if graph:
            G = nx.DiGraph() if directed else nx.Graph()
            for n in hop:
                G.add_edge(n['from'], n['to'])
                hop = G
        
        return hop 
    
    def get_steps(self,mark_x= None,mark_y = None,valid= True):
        '''步骤节点'''
        step = xml_pars(self.root.iterdescendants(tag= 'step'))
        stepclas = {}
        for n in step:
            n['ktr'] = self.ktr_name
            n['kuid'] = self.kuid
            
            # 节点类型归类
            if n.get('type',None) in stepclas:
                stepclas[n.get('type',None)].append(n['name'])
            else:
                 stepclas[n.get('type',None)] = [n['name']]
                    
            # 对表输出的子内容处理        
            if n.get('type',None) == 'TableOutput':
                if isinstance(n['fields'],lxml.objectify.ObjectifiedElement):
            
                    fields = xml_pars(n['fields'].getchildren())
                    for x in fields:
                        x['table'] = n['table']
                    n['fields_content'] = fields
                
        # 标记节点关系
        if mark_x and mark_y:
            hop = xml_pars(self.root.iterdescendants(tag= 'hop'))
            G = nx.Graph()
            for n in hop:
                G.add_edge(n['from'], n['to'])
                
            # 取连接有效的节点
            if valid:
                valid_step = set()
                for n in hop:
                    if n['enabled'] =='Y':
                        valid_step.add(n['from'])
                        valid_step.add(n['to'])
                
                step_valid = []
                for n in step:
                    if n['name'] in valid_step:
                        step_valid.append(n)
                step = step_valid
                
            if mark_x in stepclas and mark_y in stepclas:
                nexus = product(stepclas[mark_x],stepclas[mark_y])
                for n in nexus:
                    if nx.has_path(G,n[0],n[1]):
                        step_uuid = str(uuid.uuid1())
                        for sp in step:
                            if sp.get('name',None) in [n[0],n[1]]:
                                sp['suid'] = step_uuid
                        
        return step

    def get_conn(self):
        '''数据源连接信息'''
        conn = xml_pars(self.root.iterdescendants(tag= 'connection'))
        for n in conn:
            n['ktr'] = self.ktr_name
            n['kuid'] = self.kuid
        return conn
    
    def set_step(self,name='TableInput',value= {},inplace =False):
        '''修改ktr文件step步骤中的标签值
        
        Parameters
        ----------
        name: str
            标签
        value: 
            值
        '''
        step = self.root.xpath(f"/transformation/step[type='{name}']")
        if step:
            for x,y in  value.items():
                setattr(step[0],'sql',y)
            if inplace:
                self.save(self.__file)
            return True
        else:
            return False
        
    def to_string(self,obj=None):
        '''root根对象xml文档输出为字符串
        '''
        data = obj if obj else self.root    
        objectify.deannotate(data, cleanup_namespaces=True)
        xml_str = str(etree.tostring(data, encoding="utf-8", pretty_print=True),encoding='UTF-8')
        return xml_str
    
    def save(self,path):
        '''root输出保存到指定路径文件
        '''
        xml_str = self.to_string()
        Path(path).write_bytes(bytes(xml_str,encoding = "utf8") ) 
        return True
        
class ktr(object):
    def __init__(self):
        '''生成ktr文件
        '''
        self.data = {'connection':[],'step':[]}
        
    def create_info(self,name,directory = '',trans_type='Normal',trans_status=0,created_date= None,modified_date =None,
                    created_user='-',modified_user='-'):
        '''ktr主体信息
        
        name:str
            ktr转换名称
        directory:str
            路径
        '''
        data = {"name":name,'trans_type':trans_type,'directory':directory,
                'created_user':created_user,'trans_status':trans_status,
                'created_date':created_date,'modified_user':modified_user,'modified_date':modified_date}
        self.data.update(data)
        return data
        
    def create_parameters(self,data=[]):
        '''参数
        data:list
            列表元素为字典
            name: str
                变量名称
            default_value: str
                默认值
            description：str
                变量说明
        '''
        self.data['parameters'] = data
        return data
        
    def create_order(self,data):
        '''步骤顺序连接
        
        data: dict
            {from:step1,to:stpe2,enabled:'Y'}
        '''
        self.data['order'] = data
        return data
    
    def create_conn(self,name,server='',type='',access='',database='',port='',username='',password='',attributes=''):
        '''数据库连接
        
        server:str
            ip
        types:str
            数据库类型 ORACLE
        access:str
            Native
        database:str
            数据库名
        port:str
            端口
        username: str
            用户名
        password:str
            密码
        attributes: dict
            相关属性 
        '''
        data = locals()
        data.pop('self')
        data['name'] = name
        if not data['attributes']:
            data['attributes'] = [{'code':'FORCE_IDENTIFIERS_TO_LOWERCASE','attribute':'N'},
                                  {'code':'FORCE_IDENTIFIERS_TO_UPPERCASE','attribute':'N'},
                                  {'code':'IS_CLUSTERED','attribute':'N'},
                                  {'code':'PORT_NUMBER','attribute':port},
                                  {'code':'PRESERVE_RESERVED_WORD_CASE','attribute':'Y'},
                                  {'code':'QUOTE_ALL_FIELDS','attribute':'N'},
                                  {'code':'SUPPORTS_BOOLEAN_DATA_TYPE','attribute':'Y'},
                                  {'code':'SUPPORTS_TIMESTAMP_DATA_TYPE','attribute':'Y'},
                                  {'code':'USE_POOLING','attribute':'N'}]
        else:
            data['attributes'] = attributes
        self.data['connection'].append(data)
        return  data
    
    def create_step_execsql(self,name,conn,sql,execute_each_row='N',single_statement='N',replace_variables='N',
                            quoteString='N',set_params ='N',
                            xloc = 120,yloc = 80,draw='Y'):
        '''表输入
        '''
        data = locals()
        data.pop('self')
        data['name'] = name
        data ['connection'] = conn
        data ['sql'] = sql
        data ['type'] = 'ExecSQL'
        self.data['step'].append(data)
        return data
        
    def create_step_tableinput(self,name,conn,sql,limit = 0,distribute = 'Y',copies=1,execute_each_row='N',variables_active='Y',lazy_conversion_active='N',
                               xloc = 320,yloc = 80,draw='y'):
        data = locals()
        data.pop('self')
        data ['name'] = name
        data['connection'] = conn
        data['sql'] = sql
        data ['type'] = 'TableInput'
        self.data['step'].append(data)
        return data
    
    def create_step_tableoutput(self,name,conn,table,fields,commit =100,tablename_in_table='Y',truncate='N',ignore_errors='N',
                                use_batch='Y',specify_fields='Y',partitioning_enabled='N',partitioning_daily = 'N',
                                partitioning_monthly='Y',tablename_in_field = 'N',return_keys ='',xloc = 520,yloc = 80,draw='y'):
        '''表输出
        name: str
            表输出名字
        conn: 
            数据库连接
        table: str
            表名
        '''
        data = locals()
        data.pop('self')
        data['name'] = name
        data['connection'] = conn
        data['table'] = table
        data['tablename_in_table'] = tablename_in_table
        
        data ['type'] = 'TableOutput'
        self.data['step'].append(data)
        return data
    
    def render(self):
        '''生成ktr xml文件'''
        mytemplate = Template(filename=str(Path(__file__).parent/'template'/'ktr.xml'))
        try:
            res = mytemplate.render(**self.data)
            return res
        except:
            raise Exception(exceptions.text_error_template().render())
    
    def save(self,path):
        '''保存ktr xml文件对象
        '''
        ktr_string = self.render()
        Path(path).write_text(ktr_string)
        
class ktr_parses():
    def __init__(self,files):
        '''同时解析多个ktr文件'''
        self.__files = files
        
    def get_info(self):
        '''获取ktr的基本信息
        '''
        data = []
        for n in self.__files:
            kr = ktr_parse(n)
            data.extend(kr.get_info())
        return data 
    
    def get_parameters(self):
        '''ket的参数信息
        '''
        data = []
        for n in self.__files:
            kr = ktr_parse(n)
            data.extend(kr.get_parameters())
        return data
        
    def get_hops(self,graph = False,directed = False):
        '''步骤顺序关联
        '''
        data = {}
        for n in self.__files:
            kr = ktr_parse(n)
            data.update({self.kuid:kr.get_hops(graph = graph,directed = directed)})
        return data
    
    def get_steps(self,mark_x= None,mark_y = None):
        '''步骤节点
        '''
        data = []
        for n in self.__files:
            kr = ktr_parse(n)
            data.extend(kr.get_steps(mark_x = mark_x,mark_y = mark_y))
        return data
    
    def get_conn(self):
        '''数据源连接信息
        '''
        data = []
        for n in self.__files:
            kr = ktr_parse(n)
            data.extend(kr.get_conn())
        return data
