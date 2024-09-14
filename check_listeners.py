import os
import xml.etree.ElementTree as ET

def check_listeners_disabled(jmx_file):
    try:
        tree = ET.parse(jmx_file)
        root = tree.getroot()

        # JMeter files may not have a namespace; adjust as necessary
        namespace = {}
        listeners = root.findall(".//ResultCollector", namespaces=namespace)

        all_disabled = True
        for listener in listeners:
            enabled = listener.attrib.get('enabled')
            if enabled != 'false':  # Checking if 'enabled' is not 'false'
                all_disabled = False
                testname = listener.attrib.get('testname', 'Unnamed Listener')
                print(f"Listener '{testname}' in {jmx_file} is enabled.")

        return all_disabled
    except ET.ParseError as e:
        print(f"Error parsing {jmx_file}: {e}")
        return False

# Directory where .jmx files are located
jmx_dir = os.getenv('JMX_DIR', '.')

# Loop through all .jmx files in the directory
all_safe = True
for filename in os.listdir(jmx_dir):
    if filename.endswith(".jmx"):
        file_path = os.path.join(jmx_dir, filename)
        if not check_listeners_disabled(file_path):
            all_safe = False

if all_safe:
    print("All listeners in all .jmx files are disabled. Safe to upload.")
else:
    print("Some listeners are enabled. Please disable them before uploading.")
    exit(1)  # Exit with a non-zero status code to fail the action
