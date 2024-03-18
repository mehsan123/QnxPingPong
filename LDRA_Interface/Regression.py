import argparse
import logging
import os
import sys
import re
import shutil

from ldra.contestbed import contestbed
from ldra.contbrun import contbrun

#Run analysis and store artifacts
def handle_arguments():
    parser = argparse.ArgumentParser(description="Use PTF=>TCF Map to execute TBrun Test Sequences")
    parser.add_argument('TOOLSUITE', help="Location of LDRA tools")
    parser.add_argument('WORKAREA', help="Location of LDRA Workarea")
    parser.add_argument('OUTPUT',help="Output directory for results")
    parser.add_argument('BTF', help="BTF/PTF file to execute")
    parser.add_argument('--tcfs', nargs='+', help="List of TCF files to regress for the BTF/PTF")
    parser.add_argument('-d','--debug',help="Enable Debug Logging",action='store_true',default=False)
    
    args = parser.parse_args()

    #verify that that ptf and tcf files exist
    if not os.path.exists(args.BTF):
        print("ERROR BTF")
        args = None
    else:
        for tcf in args.tcfs:
            print("Test")
            if not os.path.exists(tcf):
                print("ERROR TCF")
                args = None
                break
        
    return args

def get_setname(ptf_filename):
    #get the set that is described by the PTF, this will be used by the delete and analysis phases
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
    args = handle_arguments()
    if args == None:
        return 2
    
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    logger = logging.getLogger('MAIN')
    logger.info("REGRESS: {}".format(args.BTF))
    for tcf in args.tcfs:
        logger.info("    TCF: {}".format(tcf))

    setname= get_setname(args.BTF)

    #setup output directories is they dont exist
    output = args.OUTPUT
    results = os.path.join(output,"RESULTS")
    ptf_results = os.path.join(results,setname)
    logs = os.path.join(ptf_results,"Logs")

    for dir in [output,results,ptf_results,logs]:
        if not os.path.isdir(dir):
            logger.info("Creating Directory: {}".format(dir))
            os.makedirs(dir)

    #create connections to testbed and tbrun
    tb = contestbed(args.TOOLSUITE,args.WORKAREA)
    tb.configure_output(stream=True,file=os.path.join(logs,"testbed.log"))
    tbrun = contbrun(args.TOOLSUITE,args.WORKAREA)
    tbrun.configure_output(stream=True,file=os.path.join(logs,"tbrun.log"))
    tbrun.results_files = ["0.tcf","thr.htm","dyn.htm"]

    static_result = tb.run(args.BTF,"-112n021q")
    if static_result:
        for tcf in args.tcfs:
            regression_result = tbrun.run(setname,"-tcf={tcf}".format(tcf=tcf),"-gentcf=0","-regress","-quit")
            if regression_result:
                for file in regression_result.resultfiles:
                    if "0.tcf" in file:
                        shutil.move(file,os.path.join(ptf_results,os.path.basename(tcf)))
                    else:
                        shutil.move(file,ptf_results)

if __name__ == '__main__':
    sys.exit(main())