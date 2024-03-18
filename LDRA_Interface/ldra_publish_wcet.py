from ldra.tbreports import tbreports
from ldra.genxml import genxml

import logging
import os
import argparse
import sys
import traceback
import xml.etree.ElementTree as ET

def arguments():
    parser = argparse.ArgumentParser(description="Run Build Import and Static Analysis")
    parser.add_argument('TOOLSUITE', help="Location of LDRA tools")
    parser.add_argument('WORKAREA', help="Location of LDRA Workarea")
    parser.add_argument("LDRA",help=".ldra file to generate reports from")
    parser.add_argument("PUBLISH",help="Location to publish files")

    parser.add_argument('-d','--debug',help="Enable Debug Logging",action='store_true')

    return parser.parse_args()

def process_coverage(file,logger):
        root = ET.parse(file).getroot()

        overall_value = 0.0
        overall_threshold = 0.0
        total_coverage = 0.0

        for file in root.findall("./file"):
            filename = file.attrib["name"]
            coverage = file.find("coverage")
            for metric in coverage:
                type = metric.attrib["name"]
                value = float(metric.attrib["value"])
                threshold = float(metric.attrib["threshold"])
                status = "PASS" if metric.attrib["status"] == "pass" else "FAIL"

                overall_value+=value
                overall_threshold+=threshold

                logger.info("{}::{} -- {} : {}/{}".format(filename,type,status,value,threshold))
        
        #calculate overall coverage data
        if overall_threshold != 0:
            total_coverage = (overall_value/overall_threshold) *100
            logger.info("TOTAL Coverage {:.2f}".format(total_coverage))
            logger.info("Code coverage: {:.2f}".format(total_coverage))

        

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

        rp = tbreports(args.TOOLSUITE,args.WORKAREA)
        rp.configure_output(stream=True)

        publish_result = rp.run(args.LDRA, "-wcet_report","-tbpublish", tbpublish_dir=args.PUBLISH)
        if publish_result:
            for file in publish_result.resultfiles:
                print(file)
        else:
            return_code=publish_result.returncode
            return_text=publish_result.returntext

        gen = genxml(args.TOOLSUITE,args.WORKAREA)
        xml_result = gen.run(args.LDRA)
        if xml_result:
            for xml in xml_result.resultfiles:
                process_coverage(xml,logger)

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