##############################################
#    _              __   
#   | \ _     o __ (_  \/
#   |_/(_|\_/ | | |__) / 
#
###############################################
# This is DavinSy Self test script
# The script is executed at the end of the boot sequence
# ########################################################


from pathlib import Path
import importlib
import importlib.util
from time import time, sleep
from .dvs_agent import DvsAgent
from .file_handler import Tar, read_binary
from .logger import logger
from .dvs_com import DvsCom, simpleEventWaiter
import yaml

class SelfTest:
    _instance: "SelfTest" = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            logger.debug("SelfTest creating singleton")
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self.agent = None
        self.data_path = None
        
    def on_boot_done(self,agent: DvsAgent = None, data_path:Path = None, options:dict={"export_csv":0,"export_json":1,"kill_agent_after_test":0}):
        hb_filename = None

        logger.info(f"Starting SELF TEST with {data_path}")
        if agent != None:
            self.agent = agent

        if self.agent == None:
            return

        t0 = int(time()*1000)

        if "heart_beat_period" in options:
            all_results = one_test(agent, data_path, float(options["heart_beat_period"]))
        else:
            all_results = one_test(agent, data_path)

        # export results even if empty
        if "export_json" in options and options["export_json"] == 1:
            export_to_json(data_path,all_results)

        if "export_csv" in options and options["export_csv"] == 1:
            export_to_csv(data_path,all_results)
        

        t1 = int(time()*1000)
        dt = (t1-t0)/1000.0
        logger.info(f"SELF TEST :{len(all_results)} tests with DONE in {dt:.2f} s")

        if "kill_agent_after_test" in options and options["kill_agent_after_test"] == 1:
            agent.link.kill_agent()


def beat_heart_beat(cnt: int, wait_time: float = None):

    # useful to get the agent process the other events
    if wait_time is not None:
        sleep(wait_time)


def one_test(agent: DvsAgent, data_path:Path, heart_beat_period: float = 1.0 ):

    test_result = []
    cnt_dataset = 0
    data_cnt = 0

    if heart_beat_period > 0.0:
        heart_beat = time()
        beat_heart_beat(0)

    trainwaiter = simpleEventWaiter()
    remover_trainwaiter = agent.link.on_training_done(trainwaiter.on_event)
    inferwaiter = simpleEventWaiter()
    remover_inferwaiter = agent.link.on_local_infer_done(inferwaiter.on_event)
    agent.link.force_train(0)
    trainwaiter.wait(1)

    # check datapath
    path = data_path / "datasets_test"
    dataset_list = []
    if path.exists():
        dataset_list = [item for item in path.rglob("*.tar*") if item.is_file()]
        for x in path.iterdir():
            if x.is_dir():
                if x.match("*_testfolder"):
                    dataset_list.append(x)

    for dataset_path in dataset_list:
        is_tar = False
        if dataset_path.is_file():
            is_tar = True
            dataset_tar_path = dataset_path

        logger.debug(f"SELF TEST with {dataset_path}")
        sourceid = -1
        valid_file = False
        dataset_definition = None
        if is_tar:
            try:
                my_tar = Tar(dataset_tar_path)
                if my_tar.tar:
                    valid_file = True
            except Exception as e:
                valid_file = False
            if not valid_file:
                logger.warning(f"Trying to load dataset: {dataset_tar_path.name}, invalide file")
                continue
            dataset_definition = my_tar.read_yml("dataset.yml")
        else:
            try :
                with open(dataset_path / "dataset.yml") as f:
                    dataset_definition = yaml.safe_load(f)
                    valid_file = True
            except:
                dataset_definition = None

        if not dataset_definition:
            logger.warning("TEST DATASET HAVE NO DEFINITION")
            if is_tar:
                my_tar.__del__()
            continue

        cnt_dataset +=1
        outputs_definition = dataset_definition["outputs"]
        dataset = dataset_definition["dataset"]
        for my_data in dataset:
            data_cnt+=1

            if heart_beat_period > 0 and (time() - heart_beat) > heart_beat_period:
                # take time to flush all com. (and give time to get-life-cycle)
                beat_heart_beat(data_cnt, wait_time = heart_beat_period/1000)
                heart_beat = time()
 
            filename = my_data["data"]
            output = my_data["output"]
            valid_input = True
            valid_output = True
            is_classification = True

            result = {}
            result["signature"]=[]
            if "record_id" in my_data["metadata"]:
                result["record_id"] = my_data["metadata"]["record_id"]

            if "source_id" in my_data:
                sourceid_new = agent.config.get_item_id("sources", my_data["source_id"])
                result["source_id_str"]=my_data["source_id"]
                result["source_id_int"]=sourceid_new

                if not sourceid_new:
                    sourceid_new = my_data["source_id"]
                    logger.warning(f" Can not find source name for source ID {sourceid_new} during bootstrap")
            else: 
                # sourceid = 1
                logger.warning(f"issue during loading file {filename}, no source")
                break
            
            if sourceid != -1 and sourceid !=sourceid_new:
                logger.warning(f"multiple sources in a single dataset, ids {sourceid} and {sourceid_new}")
            sourceid = sourceid_new
            bootstrap_info = agent.config.get_bootstrap_info_from_sourceid(sourceid)
            if bootstrap_info == {}: # empty dict
                logger.warning(f"Unable to find bootstrap info for source id {sourceid}")
                break
            groundtruth_for_davinsy = []
            groundtruth_for_test = []
            for labeltype in output:
                single_output = {}
                # TODO- check if we need to manage the two cases
                label_type_id, label_desc = agent.config.get_item_by_name("labels", labeltype) # convert using look-up table
                if not label_type_id:
                    label_type_id = outputs_definition.get(labeltype,{}).get("id", None)
                if label_type_id is None:
                    logger.warning(f"Unable to find label type id for label type {labeltype}")
                    valid_output = False
                    break
                label_value = output[labeltype]
                single_output["label_type_str"]=labeltype
                single_output["label_type_id"]=label_type_id
                single_output["label_value_str"]=label_value
                if label_value == "unknown" : # reserved value for garbage
                    groundtruth_for_davinsy.append(label_type_id)
                    groundtruth_for_davinsy.append(0)
                    single_output["label_value_id"]=0
                elif label_value in outputs_definition.get(labeltype,{}):
                    label_value_id = outputs_definition.get(labeltype,{}).get(label_value, None)
                    if label_value_id is None:
                        logger.warning(f"Unable to find label value id for {label_value}")
                        valid_output = False
                        break
                    groundtruth_for_davinsy.append(label_type_id)
                    groundtruth_for_davinsy.append(label_value_id)
                    single_output["label_value_id"]=label_value_id
                else: # manage regression here
                    # only one vector supported for regression
                    groundtruth_for_davinsy = label_value
                    is_classification = False
                groundtruth_for_test.append(single_output)
            result["groundtruth"] = groundtruth_for_test
            result["result"] = []

            if valid_input and valid_output:
                info = {}
                try :
                    if is_tar:
                        raw_input = my_tar.read_binary(filename)
                    else:
                        raw_input = read_binary(dataset_path / filename)
                except Exception as e:
                    logger.error(f"Issue with filename {filename}, read fails because {e}")
                    continue

                if raw_input is None:
                    logger.warning(f"issue during loading file {filename}")
                    continue

                # MANAGE frame & hop len
                if not "source" in bootstrap_info:
                    logger.error(f"Issue with Bootstrap {bootstrap_info}, missing source information")
                    break
                frame_len = bootstrap_info["source"].get("frame_len",0)
                file_hop_len = bootstrap_info["source"].get("file_hop_len",0)
                if frame_len == 0 or frame_len >= len(raw_input):
                    inferwaiter.flush()
                    agent.link.force_infer(raw_input,sourceid)

                    waittime, info = inferwaiter.wait(nb_elts=1,polling_time=0.001)
                    if (info is None or len(info) == 0):
                        logger.error(f"Issue with Inference with file {filename}")
                        # SKIP, do not break
                    else:
                        for single_res in info:
                            try :
                                label = single_res["info"]["pst_label_out"]
                                confidence = single_res["info"]["pst_confidenceLevel"]
                                lut = single_res["info"]["lutlables"]
                                proba = single_res["info"]["proba"]
                                tmp_res = {"label":label,"confidence":confidence,"lut":lut,"proba":proba}
                                result["result"].append(tmp_res)
                            except Exception as e:
                                logger.error(f" TEST ERROR: malformed result {single_res}")

                elif file_hop_len == 0 :
                    raw_input = raw_input[-frame_len:] # remove first sample
                    inferwaiter.flush()
                    agent.link.force_infer(raw_input,sourceid)
                    
                    waittime, info = inferwaiter.wait(nb_elts=1,polling_time=0.001)
                    if (len(info) == 0):
                        logger.error(f"Issue with Inference with file {filename}")
                        break
                    for single_res in info:
                        try :
                            label = single_res["info"]["pst_label_out"]
                            confidence = single_res["info"]["pst_confidenceLevel"]
                            lut = single_res["info"]["lutlables"]
                            proba = single_res["info"]["proba"]
                            tmp_res = {"label":label,"confidence":confidence,"lut":lut,"proba":proba}
                            result["result"].append(tmp_res)
                        except Exception as e:
                            logger.error(f" TEST ERROR: malformed result {single_res}")
                else: # frames with over-lap
                    raw_input_rest = raw_input
                    while len(raw_input_rest) >= frame_len:
                        current_raw_input = raw_input_rest[:frame_len]
                        inferwaiter.flush()
                        agent.link.force_infer(current_raw_input,sourceid)
                        
                        waittime, info = inferwaiter.wait(nb_elts=1,polling_time=0.001)
                        if (len(info) == 0):
                            logger.error(f"Issue with Inference with file {filename}")
                            break
                        for single_res in info:
                            try :
                                label = single_res["info"]["pst_label_out"]
                                confidence = single_res["info"]["pst_confidenceLevel"]
                                lut = single_res["info"]["lutlables"]
                                proba = single_res["info"]["proba"]
                                tmp_res = {"label":label,"confidence":confidence,"lut":lut,"proba":proba}
                                result["result"].append(tmp_res)
                            except Exception as e:
                                logger.error(f" TEST ERROR: malformed result {single_res}")
                        raw_input_rest = raw_input_rest[file_hop_len:]

                test_result.append(result)
        if is_tar:
            my_tar.__del__()
    remover_inferwaiter()
    remover_trainwaiter()


    if heart_beat_period > 0.0:
        beat_heart_beat(-1)

    return test_result


def one_test_async(agent: DvsAgent,data_path:Path):

    test_result = []        

    trainwaiter = simpleEventWaiter()
    remover_trainwaiter = agent.link.on_training_done(trainwaiter.on_event)
    inferwaiter = simpleEventWaiter(_maxsize=10000)
    remover_inferwaiter = agent.link.on_local_infer_done(inferwaiter.on_event)
    print("TRY TO TRAIN")
    agent.link.force_train(0)
    trainwaiter.wait(1)
    print("TRAIN !!!")

    # check datapath
    path = data_path / "datasets_test"
    dataset_list = []
    if path.exists():
        dataset_list = [item for item in path.rglob("*.tar*") if item.is_file()]
        for x in path.iterdir():
            if x.is_dir():
                if x.match("*_testfolder"):
                    dataset_list.append(x)

    cnt_dataset = 0
    for dataset_path in dataset_list:
        is_tar = False
        if dataset_path.is_file():
            is_tar = True
            dataset_tar_path = dataset_path

        logger.debug(f"SELF TEST with {dataset_path}")
        sourceid = -1
        valid_file = False
        dataset_definition = None
        if is_tar:
            try:
                my_tar = Tar(dataset_tar_path)
                if my_tar.tar:
                    valid_file = True
            except Exception as e:
                logger.warning(f"Trying to load dataset: {dataset_tar_path.name}, invalide file")
            if not valid_file:
                logger.warning(f"Trying to load dataset: {dataset_tar_path.name}, invalide file")
                continue
            dataset_definition = my_tar.read_yml("dataset.yml")
        else:
            try :
                with open(dataset_path / "dataset.yml") as f:
                    dataset_definition = yaml.safe_load(f)
                    valid_file = True
            except:
                dataset_definition = None

        if not dataset_definition:
            logger.warning("TEST DATASET HAVE NO DEFINITION")
            if is_tar:
                my_tar.__del__()
            continue

        cnt_dataset +=1
        outputs_definition = dataset_definition["outputs"]
        dataset = dataset_definition["dataset"]
        for my_data in dataset:
            filename = my_data["data"]
            output = my_data["output"]
            valid_input = True
            valid_output = True
            is_classification = True

            result = {}
            result["signature"] = []
            if "record_id" in my_data["metadata"]:
                result["record_id"] = my_data["metadata"]["record_id"]
            if "source_id" in my_data:
                sourceid_new = agent.config.get_item_id("sources", my_data["source_id"])
                result["source_id_str"]=my_data["source_id"]
                result["source_id_int"]=sourceid_new

                if not sourceid_new:
                    sourceid_new = my_data["source_id"]
                    logger.warning(f" Can not find source name for source ID {sourceid_new} during bootstrap")
            else: 
                # sourceid = 1
                logger.warning(f"issue during loading file {filename}, no source")
                break
            
            if sourceid != -1 and sourceid !=sourceid_new:
                logger.warning(f"multiple sources in a single dataset, ids {sourceid} and {sourceid_new}")
            sourceid = sourceid_new
            bootstrap_info = agent.config.get_bootstrap_info_from_sourceid(sourceid)
            if bootstrap_info == {}: # empty dict
                logger.warning(f"Unable to find bootstrap info for source id {sourceid}")
                break
            groundtruth_for_davinsy = []
            groundtruth_for_test = []
            for labeltype in output:
                single_output = {}
                # TODO- check if we need to manage the two cases
                label_type_id, label_desc = agent.config.get_item_by_name("labels", labeltype) # convert using look-up table
                if not label_type_id:
                    label_type_id = outputs_definition.get(labeltype,{}).get("id", None)
                if label_type_id is None:
                    logger.warning(f"Unable to find label type id for label type {labeltype}")
                    valid_output = False
                    break
                label_value = output[labeltype]
                single_output["label_type_str"]=labeltype
                single_output["label_type_id"]=label_type_id
                single_output["label_value_str"]=label_value
                if label_value == "unknown" : # reserved value for garbage
                    groundtruth_for_davinsy.append(label_type_id)
                    groundtruth_for_davinsy.append(0)
                    single_output["label_value_id"]=0
                elif label_value in outputs_definition[labeltype]:
                    label_value_id = outputs_definition[labeltype].get(label_value, None)
                    if label_value_id is None:
                        logger.warning(f"Unable to find label value id for {label_value}")
                        valid_output = False
                        break
                    groundtruth_for_davinsy.append(label_type_id)
                    groundtruth_for_davinsy.append(label_value_id)
                    single_output["label_value_id"]=label_value_id
                else: # manage regression here
                    # only one vector supported for regression
                    groundtruth_for_davinsy = label_value
                    is_classification = False
                groundtruth_for_test.append(single_output)
            result["groundtruth"] = groundtruth_for_test
            result["result"] = []

            if valid_input and valid_output:
                info = {}
                try :
                    if is_tar:
                        raw_input = my_tar.read_binary(filename)
                    else:
                        raw_input = read_binary(dataset_path / filename)
                except Exception as e:
                    logger.error(f"Issue with filename {filename}, read fails because {e}")
                    continue

                if raw_input is None:
                    logger.warning(f"issue during loading file {filename}")
                    continue
                # MANAGE frame & hop len
                if not "source" in bootstrap_info:
                    logger.error(f"Issue with Bootstrap {bootstrap_info}, missing source information")
                    break
                frame_len = bootstrap_info["source"].get("frame_len",0)
                file_hop_len = bootstrap_info["source"].get("file_hop_len",0)
                if frame_len == 0 or frame_len >= len(raw_input):
                    agent.link.force_infer(raw_input,sourceid)

                elif file_hop_len == 0 :
                    raw_input = raw_input[-frame_len:] # remove first sample
                    agent.link.force_infer(raw_input,sourceid)
                    
                else: # frames with over-lap
                    logger.debug(f" READY TO INFER 3")
                    raw_input_rest = raw_input
                    while len(raw_input_rest) >= frame_len:
                        current_raw_input = raw_input_rest[:frame_len]
                        agent.link.force_infer(current_raw_input,sourceid)
                        
                        raw_input_rest = raw_input_rest[file_hop_len:]

                test_result.append(result)
        if is_tar:
            my_tar.__del__()


        waittime, info = inferwaiter.wait(len(test_result),polling_time=0.01)
        print(f"Getting {len(info)} results for {len(test_result)} tests ")
        cnt = 0
        for single_res in info:
            try :
                label = single_res["info"]["pst_label_out"]
                confidence = single_res["info"]["pst_confidenceLevel"]
                lut = single_res["info"]["lutlables"]
                proba = single_res["info"]["proba"]
                tmp_res = {"label":label,"confidence":confidence,"lut":lut,"proba":proba}
                test_result[cnt]["result"] = [tmp_res]
                cnt +=1
            except Exception as e:
                logger.error(f" TEST ERROR: malformed result {single_res}")

    remover_inferwaiter()
    remover_trainwaiter()

    return test_result

##########
# EXPORT #
##########

import json
def export_to_json(data_path,data):
    with open(data_path /'results.json', 'w') as fp:
        json.dump(data, fp,indent=4)


def export_to_csv(data_path,data):
    with open(data_path /'label.csv', 'w') as fp:
        for a in data:
            # to be improved
            expected_l = a["groundtruth"][0]["label_value_id"]
            predicted_l = a["result"][0]["label"]
            fp.write(f"{expected_l} {predicted_l}\n")

    with open(data_path /'pred.csv', 'w') as fp:
        for a in data:
            # to be improved
            confidence = a["result"][0]["confidence"]
            fp.write(f"{confidence}\n")
