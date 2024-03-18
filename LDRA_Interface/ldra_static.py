from ldra.buildimport import buildimport
from ldra.contestbed import contestbed
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
    parser.add_argument("--startin",help="Start in Directory for build")
    parser.add_argument("--buildCommand",help="Build Command")

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

        bi = buildimport(args.TOOLSUITE,args.WORKAREA)
        bi.configure_output(stream=True)
        tb = contestbed(args.TOOLSUITE,args.WORKAREA)
        tb.configure_output(stream=True)
        gen = genxml(args.TOOLSUITE,args.WORKAREA)
        
        build_result = bi.run("-build","-quit",build_cmd=args.buildCommand,startin_dir=args.startin)
        
        if build_result:
            for btf in build_result.resultfiles:
                #run static analysis
                tb.run(btf,"94q")
                static_result = tb.run(btf,"112a34567q")
                if static_result:
                    for file in static_result.resultfiles:
                        print(file)
                        if ".ldra" in file:
                            #run genXML
                            xml_result = gen.run(file)
                            if xml_result:
                                for xml in xml_result.resultfiles:
                                    logger.info("xml:{}".format(xml))
                                    xml_info = gen_xml_to_prometheus(xml,args.PROMETHEUS_GATEWAY)
                                    #check for static analysis violations and trigger pipeline failure if they are found
                                    total_violations = xml_info.get_total_static_violations()
                                    if  total_violations > 0:
                                        return_code=3
                                        return_text="Static Analysis Violations Found: {}".format(total_violations)
                                        description = "To Many Static Analysis Violations Found by LDRA"
                            else:
                                return_code=xml_result.returncode
                                return_text=xml_result.returntext
                                description = "Issue Generating XML"
                        if ".rps." in file:
                            logger.debug("Report:{}".format(os.path.dirname(file)))
                            print("##vso[task.setvariable variable=rps_file;isSecret=false;isOutput=true;]{}".format((file)))
                else:
                    return_code=static_result.returncode
                    return_text=static_result.returntext
                    description = "Issue With Static Analysis"
        else:
            return_code=build_result.returncode
            return_text=build_result.returntext
            description = "Issue With Build Import"

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
