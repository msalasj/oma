
from bokeh.plotting import curdoc

import importlib


class Controller(object):

    def __init__(self, user, cfg):
        self.user = user
        self.cfg = cfg

    def module_selection(self, select):
        modules = curdoc().roots
        if len(modules) == 1:
            module = modules[0]
        else:
            module = modules[1]
        if module.name != select:
            # delete previos module
            if module.name != 'header':
                curdoc().remove_root(module)
            # create the new module
            if select == 'monitoring':
                view = importlib.import_module('modules.monitoring.view')
                view.create_module(self.user, self.cfg)
            elif select == 'mantenimiento':
                view = importlib.import_module('modules.mantenimiento.view')
                view.create_module(self.user, self.cfg)
            elif select == 'testing':
                pass
            elif select == 'admin':
                view = importlib.import_module('modules.admin.view')
                view.create_module(self.user, self.cfg)
            elif select == 'login':
                curdoc().clear()
                view = importlib.import_module('modules.login.view')
                view.create_module(self.cfg)
