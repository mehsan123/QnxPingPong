from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

class ldra_prometheus_client():
    def __init__(self,gateway):
        self.gateway = gateway
        self.registry = CollectorRegistry()
        self.metrics = {}

    def static_total(self,scope,total):
        if not hasattr(self,"static_scope_total"):
            self.static_scope_total = Gauge('ldra_static_analysis_violation_total', 'Total Static Analysis Violations Identified for Analysis Scope', registry=self.registry,labelnames=["scope"])
        self.static_scope_total.labels(scope).set(total)
    
    def static_total_file(self,scope,file,total):
        if not hasattr(self,"static_file_total"):
            self.static_file_total = Gauge('ldra_static_analysis_violation_file_total', 'Total Static Analysis Violations Identified for Analysis Scope', 
            labelnames=["scope","file"],registry=self.registry)
        self.static_file_total.labels(scope,file).set(total)

    def static_total_category(self,scope,category,total):
        if not hasattr(self,"static_cat_total"):
            self.static_cat_total = Gauge('ldra_static_analysis_violation_category_total', 'Total Static Analysis Violations Identified for Analysis Scope', registry=self.registry,labelnames=["scope","category"])
        self.static_cat_total.labels(scope,category).set(total)

    def static_violation(self,scope,file,line,code,desc):
        if not hasattr(self,"static_indv"):
            self.static_indv = Gauge('ldra_static_analysis_violation', 'Total Static Analysis Violations Identified for Analysis Scope', registry=self.registry,
                labelnames=["scope","file","line","code","desc"])
        self.static_indv.labels(scope,file,line,code,desc).inc()

    def code_coverage_total(self,scope,type,percent):
        if not hasattr(self,"dynamic_total"):
            self.dynamic_total = Gauge('ldra_code_coverage_total', 'Total Code Coverage Measured for Analysis Scope', registry=self.registry,
                labelnames=["scope","type"])
        self.dynamic_total.labels(scope,type).set(percent)

    def code_coverage_file_total(self,scope,file,type,percent):
        if not hasattr(self,"dynamic_file_total"):
            self.dynamic_file_total = Gauge('ldra_code_coverage_file_total', 'Total Code Coverage Measured per file in Analysis Scope', registry=self.registry,
                labelnames=["scope","file","type"])
        self.dynamic_file_total.labels(scope,file,type).set(percent)

    def code_coverage_procedure_total(self,scope,file,procedure,type,percent):
        if not hasattr(self,"dynamic_procedure_total"):
            self.dynamic_procedure_total = Gauge('ldra_code_coverage_procedure_total', 'Total Code Coverage Measured for Analysis Scope', registry=self.registry,
                labelnames=["scope","file","procedure","type"])
        self.dynamic_procedure_total.labels(scope,file,procedure,type).set(percent)

    def set_gauge_metric(self,name,description,value,label_dict=None):
        label_keys = []
        label_vals = []
        if label_dict != None:
            for label in label_dict:
                label_keys.append(label)
                label_vals.append(label_dict[label])

        if name not in self.metrics:
            #new metric, define it
            if label_dict == None:
                self.metrics[name] = Gauge(name,description,registry=self.registry)
            else:
                self.metrics[name] = Gauge(name,description,registry=self.registry,labelnames=label_keys)

        if label_dict == None:
            self.metrics[name].set(value)
        else:
            self.metrics[name].labels(*label_vals).set(value)

    def push(self):
        push_to_gateway(self.gateway, job='LDRA', registry=self.registry)

if __name__ == '__main__':
    gateway = 'localhost:9091'
    total = 301
    scope = ".\Cpp_tunnel_demo_Mingw.exe.ldra_output.xml"
    file = "somefile.cpp"
    lp = ldra_prometheus_client(gateway)
    lp.static_total(scope,total)
    lp.static_total_file(scope,file,total)
    lp.static_total_category(scope,"Required",100)
    lp.static_violation(scope,file,5,"1 S","Some Violation")
    lp.code_coverage_total(scope,"Statement",88.6)
    lp.code_coverage_file_total(scope,file,"Branch",99.9)
    lp.code_coverage_procedure_total(scope,file,"Something::procudure","MC/DC",20.22)
    lp.set_gauge_metric("test","test_metric",5,{"one":"two","three":"four"})
    lp.set_gauge_metric("test","test_metric",6,{"one":"two","three":"five"})
    print(lp.registry.get_sample_value("test",{"one":"two","three":"five"}))

    #lp.push()

