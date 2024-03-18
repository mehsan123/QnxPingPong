from ldra.contestbed import contestbed

import logging
import os
import argparse
import sys
import traceback
import platform

def arguments():
    parser = argparse.ArgumentParser(description="Run Build Import and Static Analysis")
    parser.add_argument('TOOLSUITE', help="Location of LDRA tools")
    parser.add_argument('WORKAREA', help="Location of LDRA Workarea")
    parser.add_argument("BUILD_DIR",help="Build directory, location of LDRA build import BTF/PTF files")
    parser.add_argument("-tcf",help="TCF File to regress")

    parser.add_argument('-d','--debug',help="Enable Debug Logging",action='store_true')

    return parser.parse_args()

def delete_results(tb,to_delete):
    delete_string = "94q"
    if platform.system() == "Windows":
        delete_string = "-{}".format(delete_string)
    delete_results = tb.run(to_delete,delete_string)

    return delete_results

def main():
    try:
        results_to_clean = []

        args = arguments()

        if args.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        logger = logging.getLogger('MAIN')

        if not os.path.isdir(args.BUILD_DIR):
            raise argparse.ArgumentTypeError("BUILD_DIR: {} is not a valid directory".format(args.BUILD_DIR))
        if args.tcf:
            if not os.path.isfile(args.tcf):
                raise argparse.ArgumentTypeError("TCF: {} is not a valid file".format(args.TCF))
            else:
                results_to_clean.append(args.tcf)
        
        tb = contestbed(args.TOOLSUITE,args.WORKAREA)
        tb.configure_output(stream=True)
        
        build_file_lookup = ["btf","ptf"]
        #find any btf/ptf files to use for deleting 
        for file in os.listdir(args.BUILD_DIR):
            if any(check in file for check in build_file_lookup):
                results_to_clean.append(os.path.join(args.BUILD_DIR,file))
        
        for result in results_to_clean:
            delete_results(tb,result)

    except Exception as e:
        errors_detected += 1
        return_text = str(e)
        traceback.print_exc()
        logger.error("Unexpected exception:{}".format(return_text))

    return 0
if __name__ == '__main__':
    sys.exit(main())
