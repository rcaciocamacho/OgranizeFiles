#!/usr/bin/python3

import json
import os
import logging
import logging.config

# Maps from json configuration
configuration = "configuration"

def get_json_config(group, key):
    with open('/home/rccamacho/.config/ogranize_download/config.json') as file:
        data = json.load(file)
    
    for node in data[group]:
        return node[key]


app_path = get_json_config(configuration, "app_path")
config_file = app_path + "config.json"

logging.config.fileConfig(fname=app_path + "logging.conf", disable_existing_loggers=False)
logger = logging.getLogger('OrganizeFiles')


def create_dir_path(dir_path):
    try:
        logger.debug("Creando directorio: " + dir_path)
        os.makedirs(dir_path)
    except OSError:
        logger.error("La creación del directorio %s falló" % dir_path)


def change_and_write_config_json(node_name, item_name, item_value):
    data = open_config_file('r')
    data[node_name][0][item_name] = item_value

    logger.debug(data)
    logger.info("Modified: " + node_name + " - Key: " + item_name + " - Value: " + item_value)
    json.dump(data, open(config_file, 'w'), indent = 6)


def open_config_file(mode):
    logger.info("Config file open as " + mode + " ('r'=read, 'w'=write)")
    with open(config_file, mode) as file:
        return json.load(file)


def arguments_actions(read_arguments):
    if "edit" in read_arguments and len(read_arguments) == 4:
        node_name = read_arguments[2]
        item_name = read_arguments[3].split("=")[0]
        item_value = read_arguments[3].split("=")[1]

        change_and_write_config_json(node_name, item_name, item_value)

    elif "help" in read_arguments:
        list_config_tree()
        print("*********************************************************")
        print("*** Formato de parámetros del comando:")
        print("*** --> py main.py <edit/help> <node_name> <key>=<value>")
        print("*********************************************************")
    else:
        print("Argumento no válido.")


def list_config_tree():
    data = open_config_file('r')
    data_group = "configuration,variables,extensions,custompaths"

    for node in data_group.split(","):
        print("#### " + node)
        print("-----------------------------")
        for node in data[node]:
            for key in node:
                print(" - " + key + " = " + node[key])
        print("")
