from .ldra_application import ldra_application
import logging
import platform

class genxml(ldra_application):
    def __init__(self,toolsuite,workarea):
        self.logger = logging.getLogger('Generate_xml')
        if platform.system() == "Windows":
            self.executable = "Generate_xml"
        else:
            self.executable = "generate_xml"
            
        self.exit_codes = {
            0:"Success",
        }

        #optional list of files/extensions.  These will be searched for after execution and returned as part of the result
        self.results_files = [".xml"]
        
        super(genxml,self).__init__(toolsuite,workarea)

    #def pre(self):
    #    #optional, add functionality to run prior to execution
    #    pass
    #def post(self):
    #    #optional, add functionality to run post execution
    #    pass

if __name__ == '__main__':
    toolsuite = "C:\\agent\\_work\\LDRA\\LDRA_Toolsuite_C_CPP_10.0.3"
    workarea = "C:\\agent\\_work\\LDRA\\LDRA_Workarea_C_CPP_10.0.3"
    tb = genxml(toolsuite,workarea)
    print(tb)
    file = r"C:\agent\_work\LDRA\LDRA_Workarea_C_CPP_10.0.3\Cpp_tunnel_demo_Mingw.exe_tbwrkfls\Cpp_tunnel_demo_Mingw.exe.ldra"
    result = tb.run(file)
    print(str(result))
    print(result.resultfiles)