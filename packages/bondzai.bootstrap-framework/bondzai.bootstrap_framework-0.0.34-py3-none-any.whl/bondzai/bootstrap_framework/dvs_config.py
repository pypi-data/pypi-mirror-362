import yaml
import json
from pathlib import Path
import configparser

from bondzai.davinsy_py.model import VirtualModel
from bondzai.davinsy_py.operations import OperationRegistry
from bondzai.davinsy_py.model import PreprocPhase

from .file_handler import Tar, handle_binary_file_data, write_json, read_json


class DvsConfig():
    """
    Define the config object
    """
    _instance: "DvsConfig" = None

    @classmethod
    def get_instance(cls, path: Path = Path(__file__).parent.resolve()):
        if not cls._instance:
            cls._instance = DvsConfig(path)
        return cls._instance

    def __init__(self, path: Path):
        """
        Constructs a new instance.
        Args:
            path: The path of the configuration file
        """
            
        self.rootPath = path       

        self.operation_registry = OperationRegistry.get_instance()

        self.vm = []
        self.nb_vm = 0

        self.association_table = None

        self.max_raw_data = 0
        self.max_input_data = 0
        self.bootstrap_info = {}
        self.max_models = 0
        self.max_labels = 0
        self.max_reg_len = 0
        self.max_nb_raw_data = 3000

        self.max_dbm_raw_data = int (0.5*(240 * 1024 * 1024)/4) # set DBM_TOTAL_ALLOCATED_PERSISTENT in platform_overload.h. limite to 50%

        self.agent_id = "dvs_agent"

        self.reload_raw_data = False
        self.enable_save_signatures = False
        
        self.self_test = False

        self.self_test_options = {"export_csv":0,"export_json":1,"kill_agent_after_test":0}

    def load_agent_ini(self,ini_path: Path = None) -> dict:

        ini_dict = {}
        if ini_path is None:
            ini_path = self.rootPath

        init_file = ini_path / "agent.ini"
        if not Path.exists(init_file):
            return ini_dict
        
        config_ini = configparser.ConfigParser()
        config_ini.read(init_file)

        sections = config_ini.sections()

        for sect in sections:
            ini_dict[sect] = config_ini[sect]

        return ini_dict

    def save_davinsy_ini(self,davinsy_ini_content:dict,davinsy_ini_path: Path = None):
        updated_keys = 0

        davinsy_ini = configparser.ConfigParser()
        davinsy_ini["dvs"] = {}

        davinsy_section = davinsy_ini['dvs']
        for key in davinsy_ini_content:
            value = davinsy_ini_content[key]
            davinsy_section[key] = value
            updated_keys +=1

        if davinsy_ini_path is None:
            filename = self.rootPath.parent / "bin" / "davinsy.ini"
        else:
            filename = davinsy_ini_path / "davinsy.ini"

        if updated_keys > 0:
            with open(filename, 'w') as configfile:
                davinsy_ini.write(configfile)

    def set_data_path(self,data_path):
        self.rootPath = data_path
    
    def get_data_path(self):
        return self.rootPath
    
    def set_agent_id(self,agent_id):
        self.agent_id = agent_id
    def get_agent_id(self) -> str:
        return self.agent_id

    def enable_reload_raw_data(self):
        self.reload_raw_data = True
    def disable_reload_raw_data(self):
        self.reload_raw_data = False

    def save_signatures(self, activate: bool):
        self.enable_save_signatures = activate

    def enable_selftest(self):
        self.self_test = True
    def disable_selftest(self):
        self.self_test = False
    def is_selftest(self) -> bool:
        return self.self_test

    def config_selftest(self,new_config):
        for key,value in new_config.items():
            self.self_test_options[key]=value
    def get_selftest_options(self) -> dict[str, int]:
        return self.self_test_options


    def preload_vms(self,vmFiles = None):

        if vmFiles is None:
            vmFiles = [ self.rootPath / "vm"] # 
        vmFiles_udpated = []
        for vmFile in vmFiles:
            pathvmfiles = Path(vmFile)
            if pathvmfiles.is_dir():
                for file in pathvmfiles.iterdir():
                    if file.is_file() and file.suffix=='.yml':
                        vmFiles_udpated.append(file)
            else:
                if pathvmfiles.is_file() and pathvmfiles.suffix=='.yml':
                    vmFiles_udpated.append(pathvmfiles)
            
            for vmFile in vmFiles_udpated:
                vmPath = self.rootPath / vmFile
                self.vm.append(VirtualModel(path=vmPath, templatePath=self.rootPath / "templates" ))

        # post-analysis
        self.max_models = 0
        self.max_labels = 0
        self.max_reg_len = 0
        self.nb_vm = 0
        all_axis = []
        for vm in self.vm:
            model = vm.get_model()
            self.nb_vm +=1
            # complete VM
            if model["deeplomath"]["nbInstances"] > 0:
                if model["deeplomath"]["mode"] == 0: # classification
                    axis = model["description"]["axis"]
                    isNew = True
                    for existing_axis in all_axis:
                        if existing_axis[0] == axis[0] and existing_axis[1] == axis[1]:
                            isNew = False
                            break
                    if isNew:
                        all_axis.append(model["description"]["axis"])
                        self.max_labels +=1
                else:
                    reg_len = model["deeplomath"]["mode"]["dim_out"]
                    if reg_len > self.max_reg_len:
                        self.max_reg_len = reg_len

                if model["description"]["maxsplit"] == 0:
                    self.max_models +=1    
                else:
                    self.max_models += model["description"]["maxsplit"]

            bootstrap_info = vm.get_bootstrap_info()
            if bootstrap_info is not None :
                self.bootstrap_info[vm.get_name()] =  bootstrap_info

                if bootstrap_info["isDataconditionning"] == 1 : # in this case, take the ouput
                    if "source" in bootstrap_info:
                        if self.max_raw_data < bootstrap_info["source"]["preproc_out_len"] :
                            self.max_raw_data = bootstrap_info["source"]["preproc_out_len"]
                        
                        input_len = bootstrap_info["source"]["frame_len"] * bootstrap_info["source"]["max_frames_number"]
                        if self.max_input_data < input_len :
                            self.max_input_data = input_len
        return self.vm
    
    def load_initial_dataset_definition(self,path : Path = None) -> dict:
        if path is None:
            path = self.rootPath / "dataset" /"myDataset.yml"

        if not Path.exists(path):
            return None
        
        with open(path, 'r') as file:
            dataset = yaml.safe_load(file)

        return dataset
    
    def load_data_from_dataset(self,filename,path : Path = None) -> tuple :
        if path is None:
            path = self.rootPath / "dataset" / filename

        if not Path.exists(path):
            return None
        
        with open(path, "rb") as f:
            if f is None:
                raise Exception(f" file {path} not found")
            data = f.read()
        
        return handle_binary_file_data(data)
    
    def load_association_table(self, path: Path = None) -> bool:
        if path is None:
            path = self.rootPath.parent / "config" / "lookup_table.json"

        if not path.exists():
            return 

        if self.association_table is None:
            self.association_table = {}

        try:
            table = {}
            with open(path, "r") as fp:
                table = json.load(fp)
            self.association_table.update(table)
        except Exception as e:
            raise Exception(f"Unable to load association table {path} : {str(e)}")
        
        return True

    def load_template_table(self, path: Path = None) -> list:
        table = []
        
        if path is None:
            path = self.rootPath.parent / "config" / "templates.json"

        if not path.exists():
            return table

        try:
            with open(path, "r") as fp:
                table = json.load(fp)
        except Exception as e:
            raise Exception(f"Unable to load template table {path} : {str(e)}")
        
        return table

    def get_item_id(self, item_type: str, label_key: str) -> int|None :
        if not self.association_table:
            if not self.load_association_table():
                return None
            
        for (label_id, key) in self.association_table.get(item_type, {}).items():
            if key == label_key:
                return int(label_id)
        
        return None
    
    def get_item_by_name(self, item_type: str, name: str) -> tuple[str, str|int]:
        if not self.association_table:
            if not self.load_association_table():
                return (None, None)
            
        for (key, val) in self.association_table.get(item_type, {}).items():
            if val.get("name","") == name:
                return (key, val)

        return (None, None)


    def get_item_by_item_type(self, item_type: str) -> any:
        if not self.association_table:
            if not self.load_association_table():
                return None
        return self.association_table.get(item_type, None)


    def get_targz_file_list(self, path: Path = None) -> list[Path]:
        if path is None:
            path = self.rootPath / "datasets"
        return [item for item in path.rglob("*.tar*") if item.is_file()]

    def get_folder_file_list(self, path: Path = None) -> list[Path]:
        if path is None:
            path = self.rootPath / "datasets"

        dataset_list = []
        if path.exists():
            for x in path.iterdir():
                if x.is_dir():
                    if x.match("*_trainfolder"):
                        dataset_list.append(x)
        return dataset_list

    def get_signature_dataset_file_list(self, path: Path = None) -> list[Path]:
        if path is None:
            path = self.rootPath / "datasets"
        return [item for item in path.rglob("*.dataset") if item.is_file()]

    def get_signature_dataset(self, path: Path = None) -> dict:
        return read_json(path)

    def preload_targz(self, path : Path = None) -> Tar:
        if path is None:
            path = self.rootPath / "datasets" / "dataset.tar.gz"
        my_tar = Tar(path)
        return my_tar
    
    def close_targz(self,my_tar):
        my_tar.__del__()

    def load_initial_dataset_definition_targz(self,my_tar,path : Path = None) -> dict:
        dataset_definition = my_tar.read_yml("dataset.yml")
        return dataset_definition

    def load_initial_dataset_definition(self,dataset_path : Path = None) -> dict:
        try :
            with open(dataset_path / "dataset.yml") as f:
                dataset_definition = yaml.safe_load(f)
        except:
            dataset_definition = None
        return dataset_definition

    def load_data_from_dataset_targz(self, my_tar: Tar, path: Path = None) -> tuple:
        
        bindata = my_tar.read_binary(path)

        return bindata

    def load_raw_data_from_json(self,filename = None, path : Path = None):
        if filename is None:
            filename = "raw_data.json"
        if path is None:
            path = self.rootPath / "datasets" / filename
        return read_json(path)

    def save_raw_data_to_json(self,raw_data: dict, filename: str = None, path : Path = None) -> bool:
        if filename is None:
            filename = "raw_data.json"
        if path is None:
            path = self.rootPath / "datasets" / filename
        write_json(path,raw_data)
        return True
    
    def save_signature_to_json(self,signatures: dict,filename: str = None, path : Path = None):
        if filename is None:
            filename = "signatures.json"
        if path is None:
            path = self.rootPath / "datasets" / filename
        write_json(path,signatures)
        return True

    def set_max_nb_raw_data (self, max_nb_raw_data: int):
        self.max_nb_raw_data = max_nb_raw_data

    def get_vms(self) -> list:
        return self.vm

    def get_max_raw_data(self) -> int:
        return self.max_raw_data
    
    def get_max_input_data(self) -> int:
        return self.max_input_data
    
    def get_max_models(self) -> int:
        return self.max_models

    def get_max_labels(self) -> int:
        return self.max_labels
    
    def get_max_reg_len(self) -> int:
        return self.max_reg_len
    
    def get_max_nb_raw_data(self) -> int:
        return self.max_nb_raw_data

    def get_nb_vm(self) -> int:
        return self.nb_vm
    
    def set_max_dbm_raw_data(self, max_dbm_raw_data: int):
        self.max_dbm_raw_data = max_dbm_raw_data

    def get_max_dbm_raw_data(self) ->int:
        return self.max_dbm_raw_data

    def get_bootstrap_info_list(self) -> dict:
        return self.bootstrap_info

    def get_bootstrap_info_from_sourceid(self,source_id,isDataconditionning = True) -> dict:
        for bootstrap_info in self.bootstrap_info.values():
            if bootstrap_info["source"]["id"] == source_id:
                if (bootstrap_info["isDataconditionning"] == 1 and isDataconditionning) \
                    or (bootstrap_info["isDataconditionning"] == 0 and not isDataconditionning):
                    return bootstrap_info
        return {}

    def get_bootstrap_dataconditionning(self,preproc) -> dict|None:
        if PreprocPhase.DATA_TRANSFORM in preproc:
            return preproc[PreprocPhase.DATA_TRANSFORM]
        elif PreprocPhase.INFERENCE in preproc:
            # LEGACY:
            return preproc[PreprocPhase.INFERENCE]
        else:
            return None

    def register_external_ops(self,opId: str,operation: callable):
        self.operation_registry.add_custom_operation(opId,operation)
