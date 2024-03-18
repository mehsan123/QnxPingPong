from .ldra_application import ldra_application
import logging

###Set Class Name to Application Name
class change_application_name(ldra_application):
    def __init__(self,toolsuite,workarea):
        ###Name Logger for log output###
        self.logger = logging.getLogger('change_application_name')
        ###Set executable name###
        self.executable = "change_application_name"
        ###Set exit codes###
        self.exit_codes = {
            0:"Success",
            1:"Change Exit Codes"
        }
        ##Set expected result files###
        #optional list of files/extensions.  These will be searched for after execution and returned as part of the result
        self.results_files = []
        
        super(change_application_name,self).__init__(toolsuite,workarea)

    ###Set pre/post if necessary, leave unmodified otherwise###
    def pre(self):
        #optional, add functionality to run prior to execution
        pass
    def post(self):
        #optional, add functionality to run post execution
        pass

if __name__ == '__main__':
    ##This Class Can be Tested by Adding code here###
    toolsuite = "C:\\agent\\_work\\LDRA\\LDRA_Toolsuite_C_CPP_10.0.3"
    workarea = "C:\\agent\\_work\\LDRA\\LDRA_Workarea_C_CPP_10.0.3"
    tb = change_application_name(toolsuite,workarea)
    print(tb)
    result = tb.run()
    print(str(result))
    print(result.resultfiles)