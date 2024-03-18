from ldra.buildimport import buildimport
from ldra.contestbed import contestbed
from ldra.contbrun import contbrun
from ldra.genxml import genxml
from ldra.genxml_to_prometheus import gen_xml_to_prometheus

import logging
import os
import argparse
import sys
import traceback
import re

def arguments():
    parser = argparse.ArgumentParser(description="Run Build Import and Static Analysis")
    parser.add_argument('TOOLSUITE', help="Location of LDRA tools")
    parser.add_argument('WORKAREA', help="Location of LDRA Workarea")
    parser.add_argument('PROMETHEUS_GATEWAY', help="Promethues gateway address for metrics")
    parser.add_argument("--startin",help="Start in Directory for build")
    parser.add_argument("--buildCommand",help="Build Command")
    parser.add_argument("--tcf",help="TCF To Regress")

    parser.add_argument('-d','--debug',help="Enable Debug Logging",action='store_true')

    return parser.parse_args()

def get_tcfs(dir):
    for item in os.listdir(dir):
        if os.path.isfile(os.path.join(dir,item)):
            if item.endswith(".tcf"):
                yield os.path.join(dir,item)

#get the set that is described by the PTF, this will be used by the delete and analysis phases
def get_setname(ptf_filename):
   setname = None
   ptf = open(ptf_filename,"r")
   
   for cnt, line in enumerate(ptf):
      #SET_NAME = 
      match = re.match("\s+SET_NAME\s=\s(.*)",line)
      if match:
         setname = match.group(1)
         break
   ptf.close()
   
   return setname

def main():
    try:
        return_code=0
        return_text="Success"
        description = None

        args = arguments()

        if args.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        logger = logging.getLogger('MAIN')
        
        azure_logger =logging.getLogger('Azure')
        azure_log = logging.StreamHandler()
        azure_log.setLevel(logging.INFO)
        formatter = logging.Formatter('%(message)s')
        azure_log.setFormatter(formatter)
        azure_logger.addHandler(azure_log)

        bi = buildimport(args.TOOLSUITE,args.WORKAREA)
        bi.configure_output(stream=True)
        tb = contestbed(args.TOOLSUITE,args.WORKAREA)
        tb.configure_output(stream=True)
        tbrun = contbrun(args.TOOLSUITE,args.WORKAREA)
        tbrun.configure_output(stream=True)
        gen = genxml(args.TOOLSUITE,args.WORKAREA)

        build_result = bi.run("-build","-quit",build_cmd=args.buildCommand,startin_dir=args.startin)
        
        if build_result:
            for btf in build_result.resultfiles:
                setname = get_setname(btf)

                #run static analysis
                tb.run(btf,"94q")
                static_result = tb.run(btf,"112aq")
                if static_result:
                    if args.tcf:
                        if os.path.isfile(args.tcf):
                        
                            logger.info("Execute Unit Test {}".format(args.tcf))
                            #run static analysis on the file/set
                            unit_result = tbrun.run(setname, "-tcf={}".format(args.tcf), "-tcf_mode=overwrite", "-regress","-quit")

                            if unit_result:
                                #use process results to set exit status
                                return_code = unit_result.returncode
                                return_text = unit_result.returntext
                                description = unit_result.stdout

                                for file in unit_result.resultfiles:
                                    if ".thr." in file:
                                        #logger.debug("Report:{}".format(os.path.dirname(report)))
                                        azure_logger.info("##vso[task.setvariable variable=thr_file;isSecret=false;isOutput=true;]{}".format((file)))
                                        continue
                                    if ".ms3." in file:
                                        #logger.info("[task.setvariable variable=ms3_file;isSecret=false;isOutput=true;]{}".format((file)))
                                        azure_logger.info("##vso[task.setvariable variable=ms3_file;isSecret=false;isOutput=true;]{}".format((file)))
                                        continue
                                    if ".ldra" in file:
                                        xml_result = gen.run(file)
                                        if xml_result:
                                            for xml in xml_result.resultfiles:
                                                xml_info = gen_xml_to_prometheus(xml,args.PROMETHEUS_GATEWAY)
                                        else:
                                            return_code = xml_result.returncode
                                            return_text = xml_result.returntext
                                            description = xml_result.stdout
                            else:
                                return_code = unit_result.returncode
                                return_text = unit_result.returntext
                                description = unit_result.stdout
                        else:
                            return_code = 1
                            return_text = "TCF Not Found {}".format(args.tcf)
                            description = ""

    except Exception as e:
        return_code = 1
        return_text = str(e)
        traceback.print_exc()
    
    #store status text to variable
    azure_logger.info("##vso[task.setvariable variable=ldra_text;isSecret=false;isOutput=true;]{}".format(return_text))
    if description:
        print("##vso[task.setvariable variable=ldra_output;isSecret=false;isOutput=true;]{}".format(description))
    
    return return_code
    
if __name__ == '__main__':
    sys.exit(main())
