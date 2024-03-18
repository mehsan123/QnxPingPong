from ldra.contestbed import contestbed
from ldra.tbreports import tbreports
from ldra.genxml import genxml
from ldra.genxml_to_prometheus import gen_xml_to_prometheus

import logging
import os
import argparse
import sys
import traceback

def arguments():
    parser = argparse.ArgumentParser(description="Run Build Import and Static Analysis")
    parser.add_argument('TOOLSUITE', help="Location of LDRA tools")
    parser.add_argument('WORKAREA', help="Location of LDRA Workarea")
    parser.add_argument('PROMETHEUS_GATEWAY', help="Promethues gateway address for metrics")
    parser.add_argument("SETNAME",help="Name of the set to run analysis against")

    parser.add_argument('-d','--debug',help="Enable Debug Logging",action='store_true')

    return parser.parse_args()

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

        report = tbreports(args.TOOLSUITE,args.WORKAREA)
        report.configure_output(stream=True)
        gen = genxml(args.TOOLSUITE,args.WORKAREA)

        ldra_file = None
        #find the .ldra file for setname
        for root,d_names,f_names in os.walk(args.WORKAREA):
            for file in f_names:
                if args.SETNAME in file:
                    if ".ldra" in file:
                        #found, set the name and exit
                        ldra_file = os.path.join(root,file)
                        logger.debug("Found LDRA file: {}".format(ldra_file))
                        break
            if ldra_file != None:
                break
        
        report_result = report.run(ldra_file,"-coverage_report")
        if report_result:
            for file in report_result.resultfiles:
                print(file)
                if ".ms3" in file:
                    print("##vso[task.setvariable variable=ms3_file;isSecret=false;isOutput=true;]{}".format((file)))

    except Exception as e:
        return_code = 1
        return_text = str(e)
        traceback.print_exc()

    if return_code > 0:
        logger.error("{}:{}:{}".format(description,return_code,return_text))
    else:
        logger.info("{}:{}".format(return_code,return_text))

    #store status text to variable
    print("##vso[task.setvariable variable=ldra_text;isSecret=false;isOutput=true;]{}".format(return_text))
    if description:
        print("##vso[task.setvariable variable=ldra_output;isSecret=false;isOutput=true;]{}".format(description))
    
    return return_code
    
if __name__ == '__main__':
    sys.exit(main())