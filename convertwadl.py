import json
import xml.etree.ElementTree as ET

def parse_json_wadl(json_wadl):
    # Load JSON data
    with open(json_wadl, 'r') as file:
        data = json.load(file)
    
    # Debugging: Print the loaded JSON data
    print("Loaded JSON WADL data:", json.dumps(data, indent=2))
    
    # Create the root XML element for WADL
    root = ET.Element('application', xmlns="http://wadl.dev.java.net/2009/02")
    
    # Generate the resources XML structure
    resources = ET.SubElement(root, 'resources', base=data.get('base', ''))
    
    for resource in data.get('resources', []):
        if isinstance(resource, dict):
            parse_resource(resource, resources)
        else:
            print(f"Skipping invalid resource: {resource}")
    
    # Convert the XML tree to a string
    xml_str = ET.tostring(root, encoding='utf-8', method='xml').decode()
    return xml_str

def parse_resource(resource, parent):
    # Debugging: Print the current resource
    print("Processing resource:", resource)
    
    # Create a resource element
    resource_element = ET.SubElement(parent, 'resource', path=resource.get('path', ''))
    
    # Add methods to the resource
    for method in resource.get('methods', []):
        parse_method(method, resource_element)
    
    # Recursively add child resources
    for sub_resource in resource.get('resources', []):
        parse_resource(sub_resource, resource_element)

def parse_method(method, parent):
    # Debugging: Print the current method
    print("Processing method:", method)
    
    # Create a method element
    method_element = ET.SubElement(parent, 'method', name=method.get('name', ''))
    
    # Add request information if available
    if 'request' in method:
        request_element = ET.SubElement(method_element, 'request')
        parse_request(method['request'], request_element)
    
    # Add response information if available
    if 'responses' in method:
        for response in method['responses']:
            response_element = ET.SubElement(method_element, 'response', status=str(response.get('status', '')))
            parse_response(response, response_element)

def parse_request(request, parent):
    # Debugging: Print the current request
    print("Processing request:", request)
    
    # Add request parameters
    for param in request.get('params', []):
        ET.SubElement(parent, 'param', name=param.get('name', ''), style=param.get('style', ''), type=param.get('type', ''))

def parse_response(response, parent):
    # Debugging: Print the current response
    print("Processing response:", response)
    
    # Add response representation
    for rep in response.get('representations', []):
        ET.SubElement(parent, 'representation', mediaType=rep.get('mediaType', ''))

if __name__ == "__main__":
    json_wadl = 'input_wadl.json'  # Path to the JSON WADL file
    xml_wadl = parse_json_wadl(json_wadl)
    
    # Write the output to an XML file
    with open('output_wadl.xml', 'w') as file:
        file.write(xml_wadl)
    
    print("XML WADL generated successfully!")
