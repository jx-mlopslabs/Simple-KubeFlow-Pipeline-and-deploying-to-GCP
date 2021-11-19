import os
from kfp.v2.dsl import Dataset, Output, component, Input

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

@component(
    packages_to_install=['pandas==1.2.4','numpy==1.20.3'],
    base_image='python:3.9.5',
    output_component_file=os.path.join(__location__,'component1yamlfile.yaml'))

def functionname(
        input1:str,
        input2:Input[Dataset],
        output1:Output[Dataset],
):
    import logging
    import numpy as np
    import pandas as pd
    
    #write the logic here.....
    #....
    #.....
    df.to_csv(output1.path,index=False)

#for this function, it expects an input of dataset type and string type
#It is expected to return one output as Dataset type
#input1, input2, output1 are the variables.

