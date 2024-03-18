from .ldra_application import ldra_application
import logging

class buildimport(ldra_application):
    def __init__(self,toolsuite,workarea):
        self.logger = logging.getLogger('buildimport')
        self.executable = "contbbuildimport"
        self.exit_codes = {
            0:"Success",
        }

        #optional list of files/extensions.  These will be searched for after execution and returned as part of the result
        self.results_files = [".ptf","btf"]
        
        super(buildimport,self).__init__(toolsuite,workarea)

    def pre(self,*args, **kwargs):
        #build import needs to look into the start-in directory for btf/ptf files.  Set this as the application Workarea
        if "startin_dir" in kwargs:
            self.workarea = kwargs["startin_dir"]

    def post(self,*args, **kwargs):
        #optional, add functionality to run post execution
        pass

if __name__ == '__main__':
    toolsuite = "C:\\agent\\_work\\LDRA\\LDRA_Toolsuite_C_CPP_10.0.3"
    workarea = "C:\\agent\\_work\\LDRA\\LDRA_Workarea_C_CPP_10.0.3"
    tb = buildimport(toolsuite,workarea)
    tb.configure_output(stream=True)
    print(tb)
    result=tb.run("-build","-quit",build_cmd="mingw32-make.exe -f cpp_cashregister.mak clean all",startin_dir="C:\\agent\_work\LDRA\LDRA_Workarea_C_CPP_10.0.3\Examples\Toolsuite\Cpp_Cashregister_6.0\Source")
    print(str(result))
    print(result.resultfiles)