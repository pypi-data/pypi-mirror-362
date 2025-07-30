import shutil

from support import SupportFile, SupportYaml

from .setup import *

name = 'plugin'

class ModulePlugin(PluginModuleBase):
    
    def __init__(self, P):
        super(ModulePlugin, self).__init__(P, name=name, first_menu='list')
        self.all_plugin_list = None
        

    def process_menu(self, page, req):
        arg = P.ModelSetting.to_dict()
        try:
            return render_template(f'{__package__}_{name}_{page}.html', arg=arg)
        except Exception as e: 
            P.logger.error(f'Exception:{str(e)}')
            P.logger.error(traceback.format_exc())
            return render_template('sample.html', title=f"{__package__}/{name}/{page}")


    def process_command(self, command, arg1, arg2, arg3, req):
        ret = {'ret':'success'}
        if command == 'plugin_install':
            ret = F.PluginManager.plugin_install(arg1)
        elif command == 'get_plugin_list':
            data = []
            """
            for name, entity in F.PluginManager.plugin_list.items():
                if entity['version'] == '3':
                    data.append({'package_name':name})
                else:
                    data.append(entity['P'].plugin_info)
            """
            for name, entity in F.PluginManager.all_package_list.items():
                try:
                    if 'P' in entity:
                        data.append(entity['P'].plugin_info)
                        data[-1]['loading'] = entity.get('loading')
                        data[-1]['status'] = entity.get('status')
                        data[-1]['log'] = entity.get('log')
                    else:
                        data.append({'package_name':name})
                        data[-1]['loading'] = entity.get('loading')
                        data[-1]['status'] = entity.get('status')
                        data[-1]['log'] = entity.get('log')
                except Exception as e:
                    data.append({'package_name':name})
                    P.logger.error(f'Exception:{str(e)}')
                    P.logger.error(traceback.format_exc())
            ret['data'] = data
            #P.logger.debug(data)
        elif command == 'uninstall':
            info = F.PluginManager.all_package_list[arg1]
            if os.path.exists(info['path']):
                try:
                    shutil.rmtree(info['path'])
                    ret['msg'] = '삭제하였습니다.<br>재시작시 적용됩니다.'
                except Exception as e:
                    P.logger.error(f'Exception:{str(e)}')
                    P.logger.error(traceback.format_exc())
                    ret['msg'] = info['path'] + "<br>삭제에 실패하였습니다.<br>" + str(e)
                    ret['ret'] = 'danger'
            else:
                ret['msg'] = info['path'] + "<br>폴더가 없습니다."
                ret['ret'] = 'danger'
        elif command == 'get_plugin_list_all':
            if self.all_plugin_list == None:
                filepath = os.path.join(os.path.dirname(__file__), 'files', 'all_plugin.yaml')
                self.all_plugin_list = SupportYaml.read_yaml(filepath)
                
                def get_plugin(_name):
                    for _cate in self.all_plugin_list:
                        for _plugin in _cate['list']:
                            if _plugin['package_name'] == _name:
                                P.logger.info(_name)
                                if _name == 'ff_reystream':
                                    P.logger.info(_name)
                                return _plugin
                            
                
                for name, entity in F.PluginManager.all_package_list.items():
                    try:
                        _plugin = get_plugin(name)
                        if _plugin != None:
                            _plugin['loading'] = entity.get('loading')
                            _plugin['status'] = entity.get('status')
                            _plugin['log'] = entity.get('log')
                            
                            _plugin['version'] = entity['P'].plugin_info['version']
                            
                    except Exception as e:
                        data.append({'package_name':name})
                        P.logger.error(f'Exception:{str(e)}')
                        P.logger.error(traceback.format_exc())
            ret['data'] = self.all_plugin_list
        return jsonify(ret)


    def plugin_load(self):
        try:
            pass
        except Exception as e:
            P.logger.error(f'Exception:{str(e)}')
            P.logger.error(traceback.format_exc())


    