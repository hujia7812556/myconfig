import yaml
import requests
from copy import deepcopy
from collections import OrderedDict

class Update:
    subscribeUrl = 'https://mymonocloud.com/clash/289378/oSm3fgYZPjT4'
    userConfigFileName = 'user.yaml'
    outConfigFileName = 'subscribe.yaml'
    proxies = {
        "http": "http://127.0.0.1:1080",
        "https": "http://127.0.0.1:1080",
    }

    def run(self):
        subscribeConfig = self.getSubscribeConfig() 
        userConfig = self.getUserConfig()
        if not subscribeConfig:
            print('invalid subscribeConfig')
            return
        newConfig = self.mergeConfg(subscribeConfig, userConfig)
        print(newConfig)
        if newConfig:
            f = open(self.outConfigFileName, 'w',encoding='utf-8')
            f.close()
            with open(self.outConfigFileName, 'a',encoding='utf-8') as f:      #'a'代表持续写入，‘w’代表覆盖写入
                yaml.dump(newConfig, f, sort_keys=False)
            print('well done')

    def getSubscribeConfig(self):
        try:
            data = yaml.safe_load(requests.get(self.subscribeUrl, proxies = self.proxies, timeout=5).text)
        except requests.RequestException as e:
            print(e)
            data = {}
        except Exception as e:
            print(e)
            data = {}
        return data
    def getUserConfig(self):
        userConfig = yaml.safe_load(open(self.userConfigFileName, 'r', encoding='utf-8'))
        return userConfig

    def mergeConfg(self, subscribeConfig, userConfig):
        newConfig = deepcopy(subscribeConfig)
        if not subscribeConfig or not subscribeConfig.get('rules'):
            print('invalid config')
            return {}
        if userConfig and userConfig.get('rules'):
            newConfig['rules'] = userConfig.get('rules') + subscribeConfig.get('rules', [])
        return newConfig
        

        
 

update = Update()
update.run()
