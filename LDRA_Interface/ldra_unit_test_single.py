from ldra.contestbed import contestbed
from ldra.contbrun import contbrun

import logging
import os
import argparse
import sys
import traceback

def arguments():
    parser = argparse.ArgumentParser(description="Run Build Import and Static Analysis")
    parser.add_argument('TOOLSUITE', help="Location of LDRA tools")
    parser.add_argument('WORKAREA', help="Location of LDRA Workarea")
    #parser.add_argument('PROMETHEUS_GATEWAY', help="Promethues gateway address for metrics")
    #parser.add_argument("--setname",help="Name of the set to run analysis against")
    #parser.add_argument("--tcf",help="TCF To Regress")
    parser.add_argument("BUILD_DIR",help="Build directory, location of LDRA build import BTF/PTF files")
    parser.add_argument("TCF",help="TCF File to regress")

    parser.add_argument('-d','--debug',help="Enable Debug Logging",action='store_true')

    return parser.parse_args()

def get_tcfs(dir):
    for item in os.listdir(dir):
        if os.path.isfile(os.path.join(dir,item)):
            if item.endswith(".tcf"):
                yield os.path.join(dir,item)

def log_result(result):

    log_string = "{} - {}".format(result.returncode,result.returntext)
    if result.returncode > 0:
        logging.error(log_string)
    else:
        logging.info(log_string)

    return result.returncode

def main():
    try:
        errors_detected = 0
        return_code=0
        return_text="Success"
        description = None

        args = arguments()

        if args.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        logger = logging.getLogger('MAIN')
        
        if not os.path.isdir(args.BUILD_DIR):
            raise argparse.ArgumentTypeError("BUILD_DIR: {} is not a valid directory".format(args.BUILD_DIR))
        if not os.path.isfile(args.TCF):
            raise argparse.ArgumentTypeError("TCF: {} is not a valid file".format(args.TCF))
        
        #azure_logger =logging.getLogger('Azure')
        #azure_log = logging.StreamHandler()
        #azure_log.setLevel(logging.INFO)
        #formatter = logging.Formatter('%(message)s')
        #azure_log.setFormatter(formatter)
        #azure_logger.addHandler(azure_log)

        tb = contestbed(args.TOOLSUITE,args.WORKAREA)
        tb.configure_output(stream=True)
        tbrun = contbrun(args.TOOLSUITE,args.WORKAREA)
        tbrun.configure_output(stream=True)

        build_file_lookup = ["btf","ptf"]

        for file in os.listdir(args.BUILD_DIR):
            if any(check in file for check in build_file_lookup):
                build_file = os.path.join(args.BUILD_DIR,file)
                #delete any existing results
                #tb.run(build_file,"94q")
                #create the set based on the build configuration
                static_result = tb.run(build_file,"-112n021q")
                
                if static_result:
                    errors_detected += log_result(static_result)
                    logger.info("Execute Unit Test {} : {}".format(file,args.TCF))
                    #unit_result = tbrun.run(args.setname, "-tcf={}".format(tcf_file), "-tcf_mode=overwrite", "-regress","-quit")
                    unit_result = tbrun.run(build_file, "-tcf={}".format(args.TCF), "-tcf_mode=overwrite", "-regress","-quit")
                    if unit_result:
                        errors_detected += log_result(unit_result)
                    else:
                        logger.error("Issue with unit test {} - {}".format(build_file,args.TCF))
                        errors_detected+=1
                else:
                    logger.error("Issue with static analysis {}".format(build_file))
                    errors_detected+=1

    except Exception as e:
        errors_detected += 1
        return_text = str(e)
        traceback.print_exc()
        logger.error("Unexpected exception:{}".format(return_text))
    
    #store status text to variable
    # azure_logger.info("##vso[task.setvariable variable=ldra_text;isSecret=false;isOutput=true;]{}".format(return_text))
    # if description:
    #     print("##vso[task.setvariable variable=ldra_output;isSecret=false;isOutput=true;]{}".format(description))
    
    #return errors_detected
    return 0
if __name__ == '__main__':
    sys.exit(main())
