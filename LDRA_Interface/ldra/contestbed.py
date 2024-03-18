from .ldra_application import ldra_application
import logging

class contestbed(ldra_application):
    def __init__(self,toolsuite,workarea):
        self.logger = logging.getLogger('contestbed')

        #self.toolsuite = self.validate_toolsuite(toolsuite)
        #self.workarea = self.validate_workarea(workarea)
        self.executable = "contestbed"
        self.exit_codes = {
            0:"Success",
            64:"Invalid command line",
            65:"Input data was incorrect",
            66:"Input file does not exist or is not readable",
            70:"Internal software limitation detected",
            73:"Output file or directory not found",
            80:"Main static analysis incomplete",
            81:"Instrumentation incomplete",
            82:"Dynamic coverage analysis incomplete",
            83:"Other analysis incomplete",
            84:"Build failure due to execution of command",
            85:"Failed to execute instrumented program",
            86:"Build command returned a non-zero value",
            87:"Error in sysppvar generation phase.",
            90:"Regression Failure",
            91:"Build Failure",
            92:"Unable to execute harness program",
            103:"Licensing error",
            }

        self.results_files = [".glh",".ldra",".htm"]

        super(contestbed,self).__init__(toolsuite,workarea)

    #def pre(self):
    #    print("contestbed pre")
    #def post(self):
    #    print("contestbed post")

if __name__ == '__main__':
    toolsuite = "C:\\agent\\_work\\LDRA\\LDRA_Toolsuite_C_CPP_10.0.3"
    workarea = "C:\\agent\\_work\\LDRA\\LDRA_Workarea_C_CPP_10.0.3"
    tb = contestbed(toolsuite,workarea)
    tb.configure_output(stream=True)
    print(tb)
    result = tb.run("C:\\agent\\_work\\LDRA\\LDRA_Workarea_C_CPP_10.0.3\\Examples\\Toolsuite\\Cpp_Cashregister_6.0\\Cpp_Cashregister.tcf","-112aq")
    print(str(result))
    print(result.resultfiles)