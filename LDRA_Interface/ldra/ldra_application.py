from __future__ import print_function
import os
import platform
import logging
import subprocess

class ldra_application(object):
    def __init__(self,toolsuite,workarea):
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger('ldra_application')
        
        if not hasattr(self, 'executable'):
            self.executable = "contestbed"        
        
        if platform.system() == "Windows":
            self.executable = self.executable + ".exe"

        #validate and store LDRA tool and Workarea
        self.toolsuite = self.validate_toolsuite(toolsuite)
        self.workarea = self.validate_workarea(workarea) 

        #default output configurations
        self.capture = True
        self.stream = False
        self.file = None

        if not hasattr(self,"exit_codes"):
            self.exit_codes = {
                0 : "Success",
            }
        if not hasattr(self,"results_files"):
            self.results_files = [".glh",".ldra"]
            
    def __str__(self):
        str = '''
        Toolsuite: {}
        Workarea: {}
        Exe: {}
        Exit Codes: {}
        '''.format(
        self.toolsuite,
        self.workarea,
        self.executable,
        self.exit_codes)
        return str

    def validate_toolsuite(self,toolsuite):
        #verify toolsuite directory
        if not os.path.isdir(toolsuite):
           raise ValueError("Invalid Directory - Does not exist: {}".format(toolsuite))
        if not os.path.exists(os.path.join(toolsuite,self.executable)):
            raise ValueError("Invalid Directory - {} Does not exist".format(os.path.join(toolsuite,self.executable)))
       
        return toolsuite

    def validate_workarea(self,workarea):
        #verify workarea directory
        if not os.path.isdir(workarea):
           raise ValueError("Invalid Directory - Does not exist: {}".format(workarea))
        #verify for expected direcotor in workarea
        if not os.path.isdir(os.path.join(workarea,"permdir")):
            raise ValueError("Invalid Directory - no permdir found: {}".format(workarea))
        
        return workarea

    def configure_output(self,capture=True,stream=False,file=None):
        self.capture = capture
        self.stream = stream

        if file != None:
            self.file_log = True
            self.file = file
        else:
            self.file_log = False
            self.file=None

        self.logger.debug("Output Configured: Capture:{} Stream:{} File:{}".format(str(self.capture),str(self.stream),self.file))

    def get_files(self,directory=None,file_lookup=None):
        if not directory:
            directory = self.workarea
        if not file_lookup:
            file_lookup = self.results_files

        #recurse the workarea looking for files
        results = {}

        for root,dirs,files in os.walk(directory):
            #print("{}:{}:{}".format(root,dirs,files))
            for file in files:
                if any(check in file for check in file_lookup):
                    if not ((file == "contents.ldra") or (file == "contents.glh")):
                        results[os.path.join(root,file)] = os.path.getmtime(os.path.join(root,file))
        if len(results) == 0:
            self.logger.warning("No files found ({}) found.  The workarea may be incorrect, or no analysis has been completed: {}".format(file_lookup,self.workarea))
        else:
            self.logger.debug("Found {} Results files From {}".format(len(results),directory))
        return results

    def _run_command(self,cmd,file_ext_list=None):

        #check for files from list if provided
        if file_ext_list:
            pre_list = self.get_files(file_lookup=file_ext_list)

        if self.file:
            fh = open(self.file,'a')
        
        result = self.execute_result(exit_codes=self.exit_codes)
        result.cmd = subprocess.list2cmdline(cmd)
        self.logger.info("Executing Command: {}".format(result.cmd))

        process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        with process.stdout:
            for line in iter(process.stdout.readline,b''):
                if self.capture:
                   result.stdout += line.decode()
                if self.file:
                    print(line.strip(),file=fh)
                if self.stream:
                    line = line.strip()
                    self.logger.info(line)
        process.wait()

        result.returncode = process.returncode
        self.logger.info("Command complete {}:{}".format(result.returncode,result.returntext))

        if self.file:
            fh.close()

        #check for updates to the files
        if file_ext_list:
            post_list = self.get_files(file_lookup=file_ext_list)
            pre_set = set(pre_list.items())
            cur_set = set(post_list.items())
            diff_set = cur_set - pre_set
            if len(diff_set) == 0:
                self.logger.warning("No Updated Files Found")
            else:
                self.logger.debug("Found {} Updated or New Results Files".format(len(diff_set)))
                for i in diff_set:
                    result.resultfiles = i[0]

        return result
    
    def run(func):
        def wrapper(self,*args, **kwargs):
            self.pre(*args,**kwargs)
            return_val = func(self,*args, **kwargs)
            self.post(*args,**kwargs)
            return return_val
        return wrapper
    
    def pre(self,*args, **kwargs):
        pass
    def post(self,*args, **kwargs):
        pass

    @run
    def run(self,*args, **kwargs):
        #build the command line arguments into a list
        cmd = list(args)
        for key,value in kwargs.items():
            cmd.append("-" + key)
            cmd.append(value)
            #cmd.append("-{}={}".format(key,value))

        app = os.path.join(self.toolsuite,self.executable)
        cmd.insert(0,app)

        return self._run_command(cmd,file_ext_list=self.results_files)
        

    class execute_result(object):
        """
        Class containing results from LDRA execution
        Using class instance in a boolean check will return true if returncode == 0, false otherwise
        ...

        Attributes
        -----------
        cmd: str
            Command as executed
        stdout: str
            Captured STDOUT output, STDERR is piped to STDOUT for simplicity
        returncode: int
            Exit code returned by process
        returntext: str
            Text equivelant of exit code based on LDRA exit codes
        resultfiles: list
            List of files generated a result of the execution
        """

        def __init__(self,exit_codes=None):
            
            if exit_codes:
                self._exit_codes = exit_codes
            else:
                self._exit_codes = {0:"Success"}

            self.cmd=None
            self.stdout=""
            self.returntext=None
            self._returncode=None
            self._resultfiles = []

        @property
        def returncode(self):
            return self._returncode
        @returncode.setter
        def returncode(self,a):
            self._returncode = a
            if a in self._exit_codes:
                self.returntext = self._exit_codes[a]
            else:
                self.returntext = "UNKNOWN"

        @property 
        def resultfiles(self):
            return self._resultfiles
        @resultfiles.setter
        def resultfiles(self,a):
            if isinstance(a,list):
                self._resultfiles.extend(a)
            else:
                self._resultfiles.append(a)

        def __str__(self):
            return ("Execution Complete: {}:{}".format(self._returncode,self.returntext))

        def __nonzero__(self):
            truth = False
            if not self._returncode == None:
                if self._returncode == 0:
                    truth = True
            print("Check Bool {}-{}".format(self._returncode,truth))
            return truth

if __name__ == '__main__':
    toolsuite = "C:\\agent\\_work\\LDRA\\LDRA_Toolsuite_C_CPP_10.0.3"
    workarea = "C:\\agent\\_work\\LDRA\\LDRA_Workarea_C_CPP_10.0.3"
    a = ldra_application(toolsuite,workarea)
    print(a)
    result = a.run()
    print("Finished")
    print(str(result))


