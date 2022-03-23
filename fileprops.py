#!/usr/bin/env python3

import json
import os
import logging
import logging.config
from classes import file_props
from functions import get_json_config, open_config_file

# Maps from json configuration
variables = "variables"
custompaths = "custompaths"
configuration = "configuration"
images = "Imágenes"
extensions = "extensions"

app_path = get_json_config(configuration, "app_path")
config_file = app_path + "config.json"

logging.config.fileConfig(fname=app_path + "logging.conf", disable_existing_loggers=False)
logger = logging.getLogger('OrganizeFiles')


def get_properties_file(extension, file_name):
    data = open_config_file('r')
    exist_prefix = False
    folder_name = ""
    extension_file = ""

    node_data = data[extensions]
    for key in node_data:
        for items in key:
            if extension in key[items].split(","):
                folder_name = items
                extension_file = extension
    
    if folder_name == images and get_json_config(variables, "prefix_images") in file_name:
        exist_prefix = True

    _file_props(extension_file, folder_name, file_name)
    find_custom_paths(folder_name, exist_prefix)


def _file_props(extension_file, folder_name, file_name):
    global file_props 
    file_props.destination_path = get_json_config(configuration, "dest_path")
    file_props.source_path = get_json_config(configuration, "folder_path")
    file_props.prefix = get_json_config(variables, "prefix_images")
    file_props.folder_name = folder_name
    file_props.file_name = file_name
    file_props.extension_file = extension_file
    

def get_join_path(param_path):
    global file_props
    if param_path == "fp":
        return os.path.join(file_props.source_path, file_props.file_name)
    if param_path == "dp":
        return os.path.join(file_props.destination_path, file_props.folder_name)
    

def find_custom_paths(folder_name, without_folder_name):
    global file_props
    data = open_config_file('r')

    node_data = data[custompaths]
    for key in node_data:
        for items in key:
            if folder_name == items:
                file_props.destination_path = key[items]
            if without_folder_name == True:
                file_props.folder_name = ""

