from ldra.buildimport import buildimport

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

        logger = logging.getLogger('buildimport.MAIN')

        bi = buildimport(args.TOOLSUITE,args.WORKAREA)
        bi.configure_output(stream=True)

        build_result = bi.run("-build","-quit",build_cmd=args.buildCommand,startin_dir=args.startin)
        
        if build_result:
            #copy the result files into an artifact directory
            pass
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

    return return_code
    
if __name__ == '__main__':
    sys.exit(main())

    