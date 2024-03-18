import xml.etree.ElementTree as ET
import argparse
from .ldra_prometheus_client import ldra_prometheus_client

class gen_xml_to_prometheus():
    def __init__(self,metrics_file,gateway):
        pass
        self.metrics_file = metrics_file
        self.lp = ldra_prometheus_client(gateway)
        self.process_file()
        self.lp.push()

    def get_total_static_violations(self):
        return self.analysis_total_violations
    
    def process_file(self):
        root = ET.parse(self.metrics_file).getroot()
        self.analysis_total_violations = 0
        self.analysis_category_violations = {}

        for file in root.findall("./file"):
            filename = file.attrib["name"]
            path = file.attrib['path']

            #process file level violations
            file_violations = file.find("violations")
            self.process_violation_metrics(file_violations,file=filename)

            file_quality_metrics = file.find("metrics")
            self.process_quality_metrics(file_quality_metrics,file=filename)

            file_coverage_metrics = file.find("coverage")
            self.process_coverage_metrics(file_coverage_metrics,file=filename)

            functions = file.findall("./functions/function")

            for function in functions:
                
                function_name = function.attrib["name"]
                function_violations = function.find("violations")
                self.process_violation_metrics(function_violations,file=filename,function=function_name)

                function_quality_metrics = function.find("metrics")
                self.process_quality_metrics(function_quality_metrics,file=filename,function=function_name)

                function_coverage_metrics = function.find("coverage")
                self.process_coverage_metrics(function_coverage_metrics,file=filename,function=function_name)

        self.lp.set_gauge_metric("ldra_static_violations_full","Total violations identified for source analyzed",self.analysis_total_violations,{"scope":self.metrics_file})
        for category in self.analysis_category_violations:
            self.lp.set_gauge_metric("ldra_static_violations_full_category","Total violations identified for source analyzed in a given category",self.analysis_category_violations[category],{"scope":self.metrics_file,"category":category})
        #print("{}:{}".format(self.analysis_total_violations,self.analysis_category_violations))
    
    def process_violation_metrics(self,violations,file,function=None):
        total_violations = 0

        for attrib in violations.attrib:
            #get the count for each category and combine it into the total
            count = int(violations.attrib[attrib])
            total_violations += count
            
            #set the metrics for this category
            if function == None:
                self.lp.set_gauge_metric("ldra_static_violations_file_category","Total violations identified for file in a given category",
                                    count,{"scope":self.metrics_file,"file":file,"category":attrib})
                # add the totals to the global count
                if attrib in self.analysis_category_violations:
                    self.analysis_category_violations[attrib] += count
                else:
                    self.analysis_category_violations[attrib] = count
            else:
                self.lp.set_gauge_metric("ldra_static_violations_function_category","Total violations identified for a function in a given category",
                                    count,{"scope":self.metrics_file,"file":file, "function":function, "category":attrib})

        if function == None:
            self.lp.set_gauge_metric("ldra_static_violations_file","Total violations identified for file",
                                    total_violations,{"scope":self.metrics_file,"file":file,})
            #update the analysis total
            self.analysis_total_violations += total_violations
        else:
            self.lp.set_gauge_metric("ldra_static_violations_function","Total violations identified for file",
                                    total_violations,{"scope":self.metrics_file,"file":file,"function":function})

        #print("{}:{}:Total:{}".format(file,function,total_violations))

    def process_quality_metrics(self,metrics,file,function=None):
        metric_dict = {"scope":self.metrics_file,"file":file}
        scope = "FILE"

        if function != None:
            scope = "FUNCTION"
            metric_dict["function"]=function
        
        fail_count = 0

        for metric in metrics:
            metric_dict["name"] = metric.tag

            if "value" in metric.attrib:
                value = metric.attrib["value"]
            else:
                value = metric.attrib["count"]
            
            if "status" in metric.attrib:
                metric_dict["status"] = "PASS" if metric.attrib["status"] == "pass" else "FAIL"
                fail_count += 1 if metric.attrib["status"] =="fail" else 0
            else:
                metric_dict["status"] = "NA"

            if "lower" in metric.attrib:
                metric_dict["lower"] = metric.attrib["lower"]
            else:
                metric_dict["lower"] = "NA"

            if "upper" in metric.attrib:
                metric_dict["upper"] = metric.attrib["upper"]
            else:
                metric_dict["upper"] = "NA"

            metric_name = "ldra_quality_metric_{scope}".format(scope=scope.lower())
            metric_description = "Quality Metrics with {scope} scope".format(scope=scope.lower())

            self.lp.set_gauge_metric(metric_name,metric_description,value,metric_dict)
        
        over_metric = "ldra_quality_metric_failures_{scope}".format(scope=scope.lower())
        over_metric_desc = "Overall count of Quality metrics failuers at a given scope"
        
        if function == None:
            self.lp.set_gauge_metric(over_metric,over_metric_desc,fail_count,{"scope":self.metrics_file,"file":file})
        else:
            self.lp.set_gauge_metric(over_metric,over_metric_desc,fail_count,{"scope":self.metrics_file,"file":file,"function":function})

    def process_coverage_metrics(self,coverage,file,function=None):
        metric_dict = {"scope":self.metrics_file,"file":file}
        
        if function != None:
            metric_dict["function"] = function
        
        for metric in coverage:
            metric_dict["type"] = metric.attrib["name"]
            value = float(metric.attrib["value"])
            metric_dict["threshold"] = metric.attrib["threshold"]
            metric_dict["status"] = "PASS" if metric.attrib["status"] == "pass" else "FAIL"

            metric_name = "ldra_code_coverage_{scope}".format(scope = "function" if function != None else "file")
            metric_desc = "Code Coverage for {scope}".format(scope = "function" if function != None else "file")

            self.lp.set_gauge_metric(metric_name,metric_desc,value,metric_dict)

if __name__ == '__main__':
    file = r"D:\Projects\Prometheus\Cpp_tunnel_demo_Mingw.exe.gen.xml"
    gateway = 'localhost:9091'
    xml = gen_xml_to_prometheus(file,gateway)
