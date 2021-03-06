import json
from os import path
import threading
import sys

class Config:
    save_path,file_name_format,headers = [None,None,None]

    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with Config._instance_lock:
                if not hasattr(cls, '_instance'):
                    Config._instance = super().__new__(cls)
                    Config._instance.read_config()
        return Config._instance

    def set(self,key,value)->bool:
        if key in dir(Config):
            self.__setattr__(key,value)
            return True
        return False

    def read_config(self,config_file_path=None)->bool:
        if config_file_path is None or len(config_file_path)==0:
            config_file_path = path.join(path.dirname(path.realpath(sys.argv[0])),"config.json")
        try:
            config_content = ''
            with open(config_file_path, 'r', -1, 'utf-8') as file:
                for line in file.readlines():
                    if len(line)>0 and line.startswith('//'):
                        continue
                    config_content = config_content+line
                config_json = json.loads(config_content)
                for key,value in config_json.items():
                    self.set(key,value)
                print("读取配置文件成功[save_path=%s,file_name_format=%s,headers=%s]"%(self.save_path,self.file_name_format,self.headers))
                return True
        except Exception as e:
            print("读取配置文件出错[%s]"%e)
            self.create_config()
            return False

    def create_config(self):
        self.set('save_path',path.dirname(path.realpath(sys.argv[0])))
        self.set('file_name_format','Id')
        self.set('headers',{'cookie':''})
        config_file_path = path.join(path.dirname(path.realpath(sys.argv[0])),"config.json")
        if path.exists(config_file_path):
            print("创建配置文件失败[文件已存在]")
        else:
            try:
                with open(config_file_path, 'w+', -1, 'utf-8') as file:
                    file.write("//file_name_format是下载的图片文件名格式。其中可用的有：Url,Artist,Tag,Id,Posted,Size,Source,Rating,Score。\n")
                    file.write("//file_name_format的例子（注意大小写）：[Artist]-Id-Tag，下载的图片大概会这样：[作者名]-12322-tag1,tag2\n")
                    file.write("//注意文件夹分割符为\\\\\n")
                    config_content = {"save_path":self.save_path,"file_name_format":self.file_name_format,"headers":self.headers}
                    file.write(json.dumps(config_content,ensure_ascii=False))
                print("创建配置文件成功[path=%s]" % config_file_path)
            except Exception as e:
                print("创建配置文件失败[%s]"%e)
        print("使用默认配置[save_path=%s,file_name_format=%s,headers=%s]"%(self.save_path,self.file_name_format,self.headers))


