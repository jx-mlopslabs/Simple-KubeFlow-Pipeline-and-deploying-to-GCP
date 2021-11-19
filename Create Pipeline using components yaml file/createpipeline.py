import os
from kfp.v2 import compiler, components
from kfp.v2.dsl import pipeline

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Loading component definition from .yaml files
component1_data = components.load_component_from_file(os.path.join(__location__,'../../Create Components/component1yamlfile.yaml'))

@pipeline(
    name='simple-pipeline-wip',
    description='trying kubeflow',
    pipeline_root='root_path'
)

def pipelinefunction(
        
        #define all your input output parameters for all the components
        input1: str,
        input2: str,
        output1: str
):
    

    component1_data_op = component1_data(
        input1,
        input2,
        )    
    
    component2_data_op = component2_data(
        component2input1,
        component2input2,
        component1_data_op.outputs['output1'],
        )
    
    #for each component we should tell what all inputs it gets
    #what output from the previous component it will get

import json
parameters = {
    #here give all input path and all values
    "input1:"somepath",
    }

with open(os.path.join(__location__,'createpipelinejson.json'),'w') as f:
    json.dump(parameters,f,indent=4)