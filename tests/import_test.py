import os
import sys
from ast import parse, Name, Call, Str, Attribute

from base_test_case import BaseTestCase

sys.path.insert(0, os.path.abspath('../pyt'))
from cfg import CFG, generate_ast, Node, EntryExitNode, get_call_names_as_string
from project_handler import get_python_modules, get_directory_modules
from flask_adaptor import FlaskAdaptor

class ImportTest(BaseTestCase):
    def test_import(self):
        path = os.path.normpath('../example/import_test_project/main.py')
        
        project_modules = get_python_modules(os.path.dirname(path))
        local_modules = get_directory_modules(os.path.dirname(path))
        
        self.cfg_create_from_file(path, project_modules, local_modules)
        
        cfg_list = [self.cfg]
        
        #adaptor_type = FlaskAdaptor(cfg_list)

    def test_get_call_names_single(self):
        m = parse('hi(a)')
        call = m.body[0].value

        result = get_call_names_as_string(call.func)

        self.assertEqual(result, 'hi')

    def test_get_call_names_uselesscase(self):
        m = parse('defg.hi(a)')
        call = m.body[0].value

        result = get_call_names_as_string(call.func)

        self.assertEqual(result, 'defg.hi')


    def test_get_call_names_multi(self):
        m = parse('abc.defg.hi(a)')
        call = m.body[0].value

        result = get_call_names_as_string(call.func)

        self.assertEqual(result, 'abc.defg.hi')
