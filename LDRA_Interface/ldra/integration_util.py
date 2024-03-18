from ldra_application import ldra_application
import logging

class integration_util(ldra_application):
    def __init__(self,toolsuite,workarea):
        self.logger = logging.getLogger('integration_util')
        self.executable = "integration_util"
        self.exit_codes = {
            0:"Success",
        }

        #optional list of files/extensions.  These will be searched for after execution and returned as part of the result
        self.results_files = [".xml"]
        
        super(integration_util,self).__init__(toolsuite,workarea)

    def pre(self):
        #optional, add functionality to run prior to execution
        pass
    def post(self):
        #optional, add functionality to run post execution
        pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    toolsuite = "C:\\agent\\_work\\LDRA\\LDRA_Toolsuite_C_CPP_10.0.3"
    workarea = "C:\\agent\\_work\\LDRA\\LDRA_Workarea_C_CPP_10.0.3"

    tb = integration_util(toolsuite,workarea)
    tb.configure_output(stream=True)
    print(tb)
    result_file = 'C:\\agent\\_work\\LDRA\\LDRA_Workarea_C_CPP_10.0.3\\Cpp_Cashregister_tbwrkfls\\Cpp_Cashregister.ldra'
    output_file = 'C:\\agent\\_work\\LDRA\\LDRA_Workarea_C_CPP_10.0.3\\Cpp_Cashregister_tbwrkfls\\Cpp_Cashregister.xml'
    result = tb.run("/arg=3",'/1={}'.format(output_file),'/2={}'.format(result_file),'/3=')
    print(str(result))
    print(result.resultfiles)