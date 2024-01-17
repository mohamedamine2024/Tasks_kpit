import sys
import pandas as pd
import xml.etree.ElementTree as et
import logging
import os

################################# logging ###############################
logging.basicConfig(
    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d]''%(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

#########################################################################

## Exracting data from the xml file
def extract_data(xml_file):
    
    try:
        load = et.parse(xml_file)
        root = load.getroot()
        namespace = {'a': 'http://autosar.org/schema/r4.0'}
        data_containers = []
        data_sub_containers = []
    
        ## CONTAINERS data extraction
        ## extracting SHORT-NAME and DEFINITION-REF from CONTAINERS/a:ECUC-CONTAINER-VALUE
        for container in root.findall('.//a:CONTAINERS/a:ECUC-CONTAINER-VALUE', namespaces=namespace):

            short_name = container.findall('a:SHORT-NAME', namespaces=namespace)
            for ref in root.findall('.//a:CONTAINERS/a:ECUC-CONTAINER-VALUE/a:SHORT-NAME', namespaces=namespace):
                def_ref = container.findall('a:DEFINITION-REF', namespaces=namespace)
            for element,element1 in zip (short_name,def_ref):
                data_containers.append({'shortname_containers':element.text,'definition_ref_cotainers':element1.text})
        data = pd.DataFrame(data_containers)
        
    
        ## SUB CONTAINERS data extraction
        ## extracting SHORT-NAME and DEFINITION-REF from SUB-CONTAINERS/a:ECUC-CONTAINER-VALUE
        for sub_container in root.findall('.//a:SUB-CONTAINERS/a:ECUC-CONTAINER-VALUE', namespaces=namespace):

            sub_short_name = sub_container.findall('a:SHORT-NAME', namespaces=namespace)
            for ref in root.findall('.//a:SUB-CONTAINERS/a:ECUC-CONTAINER-VALUE/a:SHORT-NAME', namespaces=namespace):
                sub_def_ref = sub_container.findall('a:DEFINITION-REF', namespaces=namespace)
            for sub_element,sub_element1 in zip (sub_short_name,sub_def_ref):
                data_sub_containers.append({'shortname_subcontainers':sub_element.text,'definition_ref_subcontainers':sub_element1.text})
    
        sub_data = pd.DataFrame(data_sub_containers)
        
        return data,sub_data

    except Exception as e:
            logging.error(f"error while extracting data{e}")

## exporting the extracting data to an excel file
def save_to_excel(containers_data,sub_containers_data,excel_file_path):
    excel_file_name = "task1_exported_data.xlsx"
    excel_output_path = os.path.join(excel_file_path,excel_file_name)
    try:
        # check if the file is existing and delete it if it does
        if os.path.exists (excel_output_path):
            os.remove (excel_output_path)
        
        # use Excelwriter to save containers_data and sub_containers_data in same excel file in separte sheets
        with pd.ExcelWriter(excel_output_path,engine='xlsxwriter') as writer:          
            containers_data.to_excel(writer,sheet_name='Containers DATA',index=False)
            sub_containers_data.to_excel(writer,sheet_name='SUB-Containers DATA',index=False)

    except Exception as e :
        logging.error(f"error while exporting data to excel:{e}")

if __name__ == "__main__":

    try:

       xml_file = input("please enter the xml file path: ")
       excel_file_path = input("please enter the destination path for extracted data: ")

       data_frame_containers = extract_data(xml_file)[0]
       data_frame_sub_containers = extract_data(xml_file)[1]
       save_to_excel(data_frame_containers,data_frame_sub_containers,excel_file_path)

    except Exception as e :
        logging.error(f"unexpected error:{e}")