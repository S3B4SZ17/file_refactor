#!/usr/bin/env python3
import os, regex, yaml

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('templates/'))
all_template = env.get_template('all.yml.j2')

# folder path
dir_path = r'/Users/sebastianzumbado/path_to_dir'

# list to store files name
def search_file(dir_path: str, file_name: str ,template: Template):
    '''
    Search subdirectories that matches the file_name given starting from the dir_path
    '''
    val_list = read_vals_from_yml("values.yml")
    res = []
    for (dir_path, dir_names, file_names) in os.walk(dir_path):
        for file in file_names:
            if file == file_name:
                res.append(os.path.join(dir_path,file))
    transform_file(res, template, val_list)

def transform_file(file_list: list, template: Template, val_list: list):
    '''
    For every file in the file_list we will transform it applyin the jinja template.
    '''
    for file_name in file_list:
        with open(file_name, 'r') as file:
            content = file.readlines()
            print(file_name)
            res : dict = {}
            vals : dict = {}
            # Once we have an idividual file we will first look up for any important value keys to store them in the vals dict
            for line in content:
                if file_name.find("other_template") > 0:
                    if not bool(get_vals_from_file(line, res, val_list)): 
                        vals = get_vals_from_file(line, res, val_list)
                if file_name.find("all") > 0:
                    if not bool(get_vals_from_file(line, res, val_list)): 
                        vals = get_vals_from_file(line, res, val_list)
            print(vals)
            filer_rendered = template.render(
                vals
            )
            # We apply the jinja template with values obtained in the vals dictionary
        with open(file_name, mode="w", encoding="utf-8") as file:
            file.write(filer_rendered)

def get_vals_from_file(line: str, res_dir: dict, values_list: dict) -> dict:
    '''
    Returns a dict of the searched values.
    '''
    for i in values_list:
        for name_app, reg in i.items():
            value = regex.search(reg, line)
            if value != None:
                res_dir.update({name_app: value.group(0)})

    return res_dir

def read_vals_from_yml(yaml_file: str) -> list:
    with open(yaml_file,mode="r") as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        val_list = yaml.load(file, Loader=yaml.FullLoader)

    return val_list

search_file(dir_path, 'all.yml', all_template)

