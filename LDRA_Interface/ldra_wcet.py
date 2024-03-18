import argparse
import logging
import os
import sys
import re
import shutil

from ldra.contestbed import contestbed
from ldra.contbrun import contbrun
from ldra.tbreports import tbreports

#Run analysis and store artifacts
def handle_arguments():
    parser = argparse.ArgumentParser(description="Use PTF=>TCF Map to execute TBrun Test Sequences")
    parser.add_argument('TOOLSUITE', help="Location of LDRA tools")
    parser.add_argument('WORKAREA', help="Location of LDRA Workarea")
    parser.add_argument('TCF', help="TCF file to regress")
    parser.add_argument('PUBLISH',help="Directory to publish too")
    parser.add_argument('-d','--debug',help="Enable Debug Logging",action='store_true',default=False)
    
    args = parser.parse_args()

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

def get_filename(file):
    relative_file = None
    with open(file) as fh:
        for line in fh:
            match = re.match("\s+RelativeFile\s=\s(.*)",line)
            if match:
                relative_file = match.group(1)
                break

def main():
    args = handle_arguments()
    
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    logger = logging.getLogger('MAIN')
    logger.info("REGRESS: {}".format(args.TCF))

    #create connections to testbed and tbrun
    tbrun = contbrun(args.TOOLSUITE,args.WORKAREA)
    tbrun.configure_output(stream=True)
    #rp = tbreports(args.TOOLSUITE,args.WORKAREA)
    #rp.configure_output(stream=True)

    unit_result = tbrun.run(args.TCF,"-tcf_mode=overwrite","-regress","-quit")
    if unit_result:
        logger.info("Test Complete")
        #for file in unit_result.resultfiles:
        #    if ".ldra" in file:
        #        #copy the .ldra file to the repo root for archive
        #        logger.info("Move LDRA file to {}".format(os.getcwd()))
        #        #shutil.copy(file,os.getcwd())
        #        #run ldra_reports against this file
        #        #gen_reports = rp.run(file, "-tbpublish", tbpublish_dir=args.PUBLISH)
        #        #if gen_reports:
        #        #    for file in gen_reports.resultfiles:
        #        #        logger.info(file)
    else:
        logger.error("Issue with unit test {}:{}-{}".format(args.TCF,unit_result.returncode,unit_result.returntext))
        errors_detected+=1

    return 0

if __name__ == '__main__':
    sys.exit(main())