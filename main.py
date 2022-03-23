#!/usr/bin/python3

import os, sys
import shutil
import time
import logging
import logging.config
from functions import *
from fileprops import _file_props, get_properties_file, get_join_path 
from classes import file_props

# Maps from json configuration
configuration = "configuration"
extensions = "extensions"

app_path = get_json_config(configuration, "app_path")
read_arguments = sys.argv
config_file = app_path + "config.json"

logging.config.fileConfig(fname=app_path + "logging.conf", disable_existing_loggers=False)
logger = logging.getLogger('OrganizeFiles')


def organize_files():
    global file_props
    file_name, extension = os.path.splitext(file_props.file_name)

    logger.debug("Filename: " + file_name + extension)

    if not os.path.exists(get_join_path("dp")) and not extension in get_json_config(extensions, "Isos").split(","): 
        create_dir_path(get_join_path("dp"))

    logger.debug("Copiando archivo en destino: " + get_join_path("fp") + " -> " + get_join_path("dp"))
    shutil.copy2(get_join_path("fp"), get_join_path("dp"))

    if os.path.exists(get_join_path("fp")):
        logger.debug("Eliminando archivo de origen: " + get_join_path("fp"))
        os.remove(get_join_path("fp"))


def main():
    if len(read_arguments) >= 2:
        arguments_actions(read_arguments) 
    else:
        folder_path = get_json_config(configuration, "folder_path")
        exceptions = get_json_config(extensions, "Excepciones")

        logger.debug("Ignored files: " + exceptions)
        logger.debug(folder_path)
        logger.debug(read_arguments)

        _file_props("", "", "")
        for nFile in os.listdir(folder_path):
            file_name, extension = os.path.splitext(nFile)
            if extension not in exceptions.split(",") and extension != "" and extension.find("~") < 0:
                get_properties_file(extension, file_name + extension)
                organize_files()


main()
