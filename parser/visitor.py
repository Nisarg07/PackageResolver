import ast
import imp
import sys
import importlib

sys.setrecursionlimit(10000)

class ParserVisitor(ast.NodeVisitor):
    def __init__(self):
        self.import_libraries = set()   
        self.import_names = []          
        self.mappings = {}              
        self.resources = set()          
        self.attrs = set()              

    def is_standard_library(self, name):
        if name is None:
            raise Exception('Name cannot be none')
        try:
            importlib.import_module(name)
            
            name = name.split('.')[0]
            path = imp.find_module(name)[1]
            return bool(imp.is_builtin(name) or ('site-packages' not in path and 'Extras' not in path))
        except ImportError:
            return False

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name and not self.is_standard_library(alias.name):
                self.import_libraries.add(alias.name)
                if alias.asname is not None:
                    self.mappings[alias.asname] = alias.name
                    self.import_names.insert(0, alias.asname)
                else:
                    self.import_names.insert(0, alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module and node.level == 0 and not self.is_standard_library(node.module):
            self.import_libraries.add(node.module)
            for alias in node.names:
                if alias.name != '*':
                    possible_module = '{}.{}'.format(node.module, alias.name)
                    self.resources.add(possible_module)

                    if alias.asname is not None:
                        self.mappings[alias.asname] = possible_module
                        self.import_names.insert(0, alias.asname)
                    else:
                        self.mappings[alias.name] = possible_module
                        self.import_names.insert(0, alias.name)

        self.generic_visit(node)
    def visit_Attribute(self, node):
        attr_name = self.get_variable_name(node)
        if attr_name != '':
            for name in self.import_names:
                if attr_name.startswith('{}.'.format(name)):
                    if name in self.mappings:
                        resource_name = '{}{}'.format(self.mappings[name], attr_name[len(name):])
                    else:
                        resource_name = attr_name                    
                    has_exist = False
                    for exist_res in self.attrs:
                        if exist_res.startswith('{}.'.format(resource_name)):
                            has_exist = True
                            break                    
                    if not has_exist:
                        self.attrs.add(resource_name)
                    break        
        self.generic_visit(node)
    

    def get_variable_name(self, node):
        t = type(node)

        if t is ast.Name:
            return node.id
        elif t is ast.Attribute:
            value = self.get_variable_name(node.value)
            if value == '':
                return value
            else:
                return '{}.{}'.format(value, node.attr)
        else:
            return ''