from .ldra_application import ldra_application
import logging

class tbreports(ldra_application):
    def __init__(self,toolsuite,workarea):
        self.logger = logging.getLogger('tbreports')
        self.executable = "tbreports"
        self.exit_codes = {
            0:"Success",
            1:"Change Exit Codes"
        }

        #optional list of files/extensions.  These will be searched for after execution and returned as part of the result
        self.results_files = [".htm",".txt"]
        
        super(tbreports,self).__init__(toolsuite,workarea)

    #def pre(self):
    #    #optional, add functionality to run prior to execution
    #    pass
    #def post(self):
    #    #optional, add functionality to run post execution
    #    pass

if __name__ == '__main__':
    toolsuite = "C:\\agent\\_work\\LDRA\\LDRA_Toolsuite_C_CPP_10.0.3"
    workarea = "C:\\agent\\_work\\LDRA\\LDRA_Workarea_C_CPP_10.0.3"
    tb = tbreports(toolsuite,workarea)
    print(tb)
    result = tb.run("C:\\agent\\_work\\LDRA\\LDRA_Workarea_C_CPP_10.0.3\\Cpp_Cashregister_tbwrkfls\\Cpp_Cashregister.ldra", "-codereview_report")
    print(str(result))
    print(result.resultfiles)