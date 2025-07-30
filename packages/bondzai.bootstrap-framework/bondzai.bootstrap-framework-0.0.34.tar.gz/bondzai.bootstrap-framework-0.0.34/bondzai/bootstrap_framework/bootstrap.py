##############################################
#    _              __   
#   | \ _     o __ (_  \/
#   |_/(_|\_/ | | |__) / 
#
###############################################
# This is DavinSy boot script
# The script is executed at the very beginning of the boot sequence
# At this time DavinSy is not ready to handle any command, still you can
# do some pure python initialization
# 
# Then, if this is the first time the system boot
# the boot function is called with 0 as a parameter
# At this time you should populate the database.
# 
# Later on the boot function is called again with 1 as a parameter
# just before the application starts.
# 
# And one time again with 2 as a parameter just after the application started
# At this time you should start running you simulation script/
# ########################################################

from pathlib import Path
import importlib
import importlib.util

from .dvs_agent import DvsAgent
from .logger import logger
from .dvs_com import DvsCom
from .self_test import SelfTest

class Bootstrap:
    _instance: "Bootstrap" = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            logger.debug("Bootstrap creating singleton")
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self.agent = DvsAgent(link=self.configure_communication())
        self.callbacks = {}
        self.custom_ops = {}
        
    def pre_boot(self,ini_path:Path = None):
        self.agent.pre_boot(ini_path)

    # super seed for FOREIGN
    def configure_communication(self):
        return DvsCom()

    def set_data_path(self,data_path):
        return self.agent.set_data_path(data_path)

    def set_max_nb_raw_data (self,max_nb_raw_data:int):
        self.agent.set_max_nb_raw_data(max_nb_raw_data)
        
    def set_agent_id(self,agent_id):
        self.agent.set_agent_id(agent_id)

    def enable_reload_raw_data(self):
        self.agent.enable_reload_raw_data()

    def disable_reload_raw_data(self):
        self.agent.disable_reload_raw_data()

    def register_external_op(self,opId,operation):
        self.custom_ops[opId] = operation

    def register_callbacks(self,step,callbackfunction:callable):

        if step in self.callbacks:
            logger.warning(f" bootstrap callback already defined for {step}, replaced")
        self.callbacks[step] = callbackfunction

    def boot_init(self):

        self.agent.init_and_load()
        
        data_path = self.agent.get_data_path()
        functions_file = data_path / "operations" / "functions.py"

        if Path.exists(functions_file) :
            spec = importlib.util.spec_from_file_location("functions", functions_file)
            functions = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(functions)
            table_association = functions.get_association()  # use get_association() if import directly the function
            for op_id in table_association:
                func_str = table_association.get(op_id)
                module_str, name = func_str.rsplit(".", 1)
                if module_str != "functions":
                    raise Exception(f"Trying to import private operation {name} from outside of 'functions' module")
                func = getattr(functions,name)
                self.register_external_op(op_id,func)

        self.agent.register_custom_ops_in_agent(self.custom_ops)

        if self.agent.lifecycle == 1 :
            # ---- LOAD INITIAL self.dataset ----
            self.agent.load_initial_data()
            logger.info("==> ending the init sequence")
            #self.agent.link.end_init()

    def boot_start(self):
        self.agent.configure_agent_id()

    def boot_ready(self):
        if self.agent.config.is_selftest():
            selftest = SelfTest.get_instance()
            selftest.on_boot_done(self.agent,self.agent.get_data_path(),self.agent.config.get_selftest_options())
    
        return

    def boot(self, step):
        try :
            if step == 0:
                self.boot_init()
            elif step == 1:
                self.boot_start()
            elif step == 2:
                self.boot_ready()
            elif step == -1:
                logger.debug("==> starting the init sequence")
                #self.pre_boot()

            if step in self.callbacks:
                self.callbacks[step]()
        except Exception as e :
            logger.error(" Exception during boot step "+str(step)+ " because " + str(e))


def boot(step):
    Bootstrap.get_instance().boot(step)
