import os
import sys
import xml.dom.minidom
from shutil import copy2

#check  if source_path != destination_path
#       if source_path is a dir & exist
#       if destination_path is a dir & exist
#       if file_name is a file and exist
def check(source_path, destination_path, file_name):
    if os.path.normpath(source_path) == os.path.normpath(destination_path):
        return False
    if not os.path.exists(source_path+'/'+file_name):
        return False
    if not os.path.exists(destination_path):
        return False
    if not os.path.isfile(source_path+'/'+file_name):
        return False
    return True

def handle_error(f, source_path, destination_path, file_name):
    if os.path.normpath(source_path) == os.path.normpath(destination_path):
        print("ELEMENT ERROR: source path and destinaion path are the same")
    if not (os.path.exists(source_path) & os.path.isdir(source_path)):
        print("ELEMENT ERROR: source path '"+source_path+"' doesn't exist or not a directory")
    if not (os.path.exists(destination_path) & os.path.isdir(destination_path)):
        print("ELEMENT ERROR: destination path '"+destination_path+"' does not exist or not a directory")
    if not os.path.exists(source_path+'/'+file_name) or not os.path.isfile(source_path+'/'+file_name):
        print("ELEMENT ERROR: file '"+file_name+"' doesn't exist or not a file")

all_input = raw_input("Enter config file name or a path to config file: ")
# check if config filename is entered
if all_input.isspace() or not all_input:
    sys.exit("INPUT ERROR: no config filename enetered")
all_filenames = all_input.lower().split(' ')

for config_file in all_filenames:
    # check if one of config files is a whitespace
    if not config_file:
        continue
    print("...Copying with '"+config_file+"' file...")
    config_file_name, config_file_extension = os.path.splitext(config_file)

    #check if entered file exist
    if not os.path.exists(config_file):
        print("INPUT ERROR: '"+config_file+"' doesn't exist")
        continue

    # check if entered config file is a .xml
    if not config_file_extension == '.xml':
        print("INPUT ERROR: "+config_file+" is not a .xml file")
        continue

    # check if entered config file can be parsed
    try:
        xml.dom.minidom.parse(config_file)
    except:
        print("PARSE ERROR: '"+config_file+"' can't be parsed")
        continue
    dom = xml.dom.minidom.parse(config_file)
    dom.normalize()

    # check if entered config file contains <file> tag
    files = dom.getElementsByTagName('file')
    if not files:
        print("PARSE ERROR: '"+config_file+"' doesn't contain <file> tag")
        continue
    for f in files:
        source_path = f.getAttribute('source_path')
        destination_path = f.getAttribute('destination_path')
        file_name = f.getAttribute('file_name')
        # check all attributes
        if not check(source_path, destination_path, file_name):
            handle_error(f, source_path, destination_path, file_name)
            continue
        # copy if everything is alright
        copy2(source_path+'/'+file_name, destination_path)
        print("SUCCESS: file '"+file_name+"' was successfully copied from "+source_path+" to "+destination_path)