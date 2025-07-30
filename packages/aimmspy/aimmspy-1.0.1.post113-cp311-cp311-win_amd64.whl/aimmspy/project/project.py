import os
import json
import platform
from typing import Any

import pandas as pd
import polars as pl

import pyarrow
import sys
import shutil

for path in pyarrow.get_library_dirs():
    if path not in sys.path:
        sys.path.append(path)

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import aimmspy_cpp as aap

from aimmspy.model.library import AimmsLibrary
from aimmspy.model.module import Module
from aimmspy_cpp import AimmsException as AimmsException
from aimmspy_cpp import AimmsPyException as AimmsPyException

from aimmspy.model.enums.me_identifier_types import IdentifierType
from aimmspy.model.enums.me_attribute_types import AttributeType
from aimmspy.model.identifiers.data_identifiers import DataIdentifier, DataReturnTypes
from aimmspy.model.identifiers.identifier import Identifier
from aimmspy.model.identifiers.parameter import NumericParameter, Parameter, StringParameter, ElementParameter
from aimmspy.model.identifiers.set import Set
from aimmspy.model.identifiers.variable import Variable
from aimmspy.model.identifiers.index import Index
from aimmspy.model.identifiers.constraint import Constraint
from aimmspy.model.procedure import Procedure

class Model:
    
    
    
    def __init__(self, aimms_api : aap.AimmsAPI):
        """
        The `aimms` class provides a wrapper around the AIMMS API to interact with AIMMS projects.

        Arguments:
            aimms_api (aap.AimmsAPI): An instance of the AIMMS API.
        """
        self.aimms_api = aimms_api
    
    def multi_assign(self, data : pd.DataFrame | pl.DataFrame | pyarrow.Table, options: dict[str, bool] = None):
        if options is None:
            options = {}
        if ('update' not in options):
            options["update"] = False

        if isinstance(data, pd.DataFrame):
            self.aimms_api.multi_add_values_dataframe_arrow( pyarrow.Table.from_pandas(data), options)
        elif isinstance(data, pl.DataFrame):
            self.aimms_api.multi_add_values_dataframe_arrow( data.to_arrow(), options)
        elif isinstance(data, pyarrow.Table):
            self.aimms_api.multi_add_values_dataframe_arrow(data, options)
    

class Project:
    """
    The `Project` class represents an AIMMS project and provides functionality to interact with it programmatically.

    Arguments:
        aimms_path (str): Path to the AIMMS executable.
        aimms_project_file (str): Path to the AIMMS project file.
        exposed_identifier_set_name (str, optional): Name of the exposed identifier set. Defaults to an empty string.
        create_project (bool, optional): Whether to create a new project. Defaults to False.
        checked (bool, optional): Whether the project is in a checked state. Defaults to False.
        license_folder_path (str, optional): Path to the license folder. Defaults to None.
        license_url (str, optional): URL for the AIMMS license server. Defaults to None.
        webui_port (int, optional): Port for the WebUI server. Defaults to 0.
        index_restriction (bool, optional): Whether to turn on index restrict. Defaults to False.
        data_type_preference (DataReturnTypes, optional): Preferred data return type. Defaults to DataReturnTypes.DICT.
    """
    
    prefix_map = {}
    identifier_class_map : dict[IdentifierType, Any] = {
        IdentifierType.PARAMETER_NUMERIC: NumericParameter,
        IdentifierType.PARAMETER_ELEMENT: ElementParameter,
        IdentifierType.PARAMETER_STRING: StringParameter,
        IdentifierType.SET: Set,
        IdentifierType.VARIABLE_NUMERIC: Variable,
        IdentifierType.INDEX: Index,
        IdentifierType.CONSTRAINT: Constraint,
        IdentifierType.PROCEDURE: Procedure,
    }
    
    identifier_with_prefix : dict[IdentifierType, Any] = {
        IdentifierType.LIBRARY: AimmsLibrary,
        IdentifierType.MODULE: Module,
    }
    
    def __init__(self, aimms_path : str = "" , aimms_project_file : str = "", exposed_identifier_set_name : str = "AllIdentifiers", checked : bool=False, license_folder_path : str = None, license_url: str = None, webui_port : int = 0, index_restriction : bool = False, data_type_preference : DataReturnTypes = DataReturnTypes.DICT):
        self.aimms_path = os.path.abspath(aimms_path)
        self.aimms_project_file = aimms_project_file

        self.exposed_identifier_set_name : list[str] = exposed_identifier_set_name
        self.exposed_identifier_set : set[str] = set()
        
        self.checked = checked
        self.data_type_preference = data_type_preference
        
        self.webui_port = webui_port
        
        if os.path.exists(os.path.join(aimms_path, "..", "build-parameters.json")):
            with open(os.path.join(aimms_path, "..", "build-parameters.json"), "r") as file:
                build_parameters = json.load(file)
                self.aimms_version = build_parameters["aimmsversion"]
        else:
            self.aimms_version = "24.6"

        # aimms_path should be an existing path containing in the Bin folder the aimms or aimms.exe file
        
        if not (aimms_path == "" and aimms_project_file == ""):
            if not os.path.exists(aimms_path):
                raise Exception(f"Path to AIMMS {aimms_path} does not exist")
            if not os.path.exists(aimms_project_file):
                raise Exception(f"AIMMS Project file {aimms_project_file} does not exist")
        else:
            print("Seems like aimms is in the lead so using that")

        extra_args = ""

        if not license_folder_path and not license_url:
            license_folder_path = os.getenv("AIMMS_LICENSE_FOLDER", None)
            if license_folder_path:
                print (f"Using AIMMS license folder from AIMMS_LICENSE_FOLDER environment variable: {license_folder_path}")

        if license_folder_path:
            print (f"Using license folder: {license_folder_path}")
            license_folder_path = os.path.abspath(license_folder_path)
            if platform.system() == "Windows":
                extra_args += f"--alluser-dir \"{license_folder_path}\" "
            elif platform.system() == "Linux":
                extra_args += f"--aimms-root-path \"{license_folder_path}\" "
        elif license_url:
            print (f"Using license URL: {license_url}")
            # if license_url is provided, we need to create a temporary folder to store the license config
            import tempfile
            self.tmp_license_config_folder = tempfile.mkdtemp(prefix="aimms_license_config_")
            if not os.path.exists(self.tmp_license_config_folder):
                os.makedirs(self.tmp_license_config_folder)
            licenses_file_name = os.path.join(self.tmp_license_config_folder, "licenses.cfg")
            with open(licenses_file_name, "w") as licenses_file:
                licenses_file.write(f"1\tnetwork\t{license_url}\n")

            extra_args += f"--config-dir \"{self.tmp_license_config_folder}\" "   
        
        user_args = ""

        if webui_port:
            user_args += f"--webui-listen-uri tcp://:{webui_port} "
            user_args += f"--webui::listenuri tcp://:{webui_port} "

        aimms_arguments = "--as-server " + extra_args + f"\"{self.aimms_project_file}\" " + user_args
        print (f"{aimms_path} {aimms_arguments}")
        self.aimms_api = aap.AimmsAPI( aimms_path, aimms_arguments, self, index_restriction)
        self.reflected_identifiers = []
        self.libraries : set[AimmsLibrary] = set()
        self.aimms_model = Model(self.aimms_api)
        self.add_identifiers()

    def __del__(self):
        if hasattr(self, 'tmp_license_config_folder') and os.path.exists(self.tmp_license_config_folder):
            shutil.rmtree(self.tmp_license_config_folder)

    def get_model(self, file : str = "") -> Model:
        """
        Returns the AIMMS model instance associated with this project.
        
        Returns:
            aimms_model: The AIMMS model instance.
        """
        self.generate_stub_file(os.path.join( os.path.dirname(file), f"{os.path.splitext(os.path.basename(file))[0]}.pyi"))
        return self.aimms_model

    def tab_generate(self, count : int):
        return " " * count * 4
    
    def generate_stub_file(self, stub_file : str):
        
        def write_class(file, variables, nested_count):
            for key in variables.keys():
                # make sure the key is a valid python variable name
                # get the python keywords 
                keywords = [
                    "and", "as", "assert", "break", "class", "continue", "def", "del", "elif", "else", "except", 
                    "False", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "None", 
                    "nonlocal", "not", "or", "pass", "raise", "return", "True", "try", "while", "with", "yield"
                ]
                
                if key in keywords:
                    continue
                
                variable = variables[key]
                
                if isinstance(variable, (Set, Parameter, Variable, Index, Constraint, Procedure)):
                    file.write(f"{self.tab_generate(nested_count)}{key} : {type(variable).__name__} = ...\n")
                    # also write a pydoc string with the comment of the identifier
                    comment = variable.comment
                    file.write(f"{self.tab_generate(nested_count)}\"\"\"\n")
                    if isinstance(variable, DataIdentifier) and variable.index_domain_attr:
                        file.write(f"@index domain: {variable.index_domain_attr}\n")
                        file.write(f"@unit:{variable.unit_attr}\n")
                    if isinstance(variable, Index):
                        file.write(f"@range: {variable.range}\n")
                    if comment:
                        file.write(f"{comment}\n")
                    file.write("\"\"\"\n")
                    
                elif isinstance(variable, (Module, AimmsLibrary)):
                    file.write(f"{self.tab_generate(nested_count)}class {key}:\n")
                    sub_variables = {k: v for k, v in vars(variable).items() if isinstance(v, (Set, Parameter, Variable, Index, Constraint, Procedure, Module, AimmsLibrary))}
                    if sub_variables:
                        write_class(file, sub_variables, nested_count + 1)
                    else:
                        file.write(f"{self.tab_generate(nested_count + 1)}pass\n")
        
        with open(stub_file, "w", encoding="utf-8") as file:
            file.write("from aimmspy.model.identifiers.set import Set\n")
            file.write("from aimmspy.model.identifiers.parameter import Parameter, NumericParameter, StringParameter, ElementParameter\n")
            file.write("from aimmspy.model.identifiers.variable import Variable\n")
            file.write("from aimmspy.model.identifiers.index import Index\n")
            file.write("from aimmspy.model.identifiers.constraint import Constraint\n")
            file.write("from aimmspy.model.identifiers.mathematical_program import MathematicalProgram\n")
            file.write("from aimmspy.model.procedure import Procedure\n")
            file.write("from aimmspy.model.module import Module\n")
            file.write("from aimmspy.model.library import AimmsLibrary\n")
            file.write("import pyarrow\n")
            
            variables = {k: v for k, v in vars(self.aimms_model).items() if isinstance(v, (Set, Parameter, Variable, Index, Constraint, Procedure, Module, AimmsLibrary))}
            
            file.write("class Model:\n")
            file.write(f"    def multi_assign(self, data : pyarrow.Table): ...\n")
            nested_count = 1
            
            write_class(file, variables, nested_count)
    
    
    # --------------------- this part is for the model reflection ---------------------
    
    def find_identifier_info(self, identifier : str, initialize_handles : bool):
        try:
            return self.aimms_api.get_identifier_info(identifier, initialize_handles)
        except:
            return None
    
    def find_libraries(self, exposed_identifier_set : list[str]):
        for identifier in exposed_identifier_set:
            
            identifier_info = self.find_identifier_info(identifier, False)
            if identifier_info is None:
                continue
            identifier_type = IdentifierType(identifier_info.me_type)
            if identifier_type in self.identifier_with_prefix.keys():
                prefix = self.aimms_api.get_attribute(identifier_info.me_handle, AttributeType.PREFIX.value)
                if prefix == "":
                    # split the identifier in parts ::
                    prefix = identifier
                
                new_prefixed_identifier = self.identifier_with_prefix[identifier_type](
                    name=identifier,
                    prefix=prefix,
                    project=self,
                    aimms_version=self.aimms_version,
                    model_reflection_handle=identifier_info.me_handle,
                    aimms_api=self.aimms_api
                )

                self.prefix_map[prefix] = new_prefixed_identifier
                if identifier_type == IdentifierType.LIBRARY:
                    self.libraries.add(new_prefixed_identifier)
                setattr(self.aimms_model, prefix, new_prefixed_identifier)
                
        for library in self.libraries:
            exposed_identifier_set.remove(library.name)
        
        return exposed_identifier_set
    
    def add_identifiers_to_self(self, identifiers_set : list[str]):
        # walk over all the identifiers in the main project
        for identifier in identifiers_set:
            
            identifier_info = self.find_identifier_info(identifier, False)
            if identifier_info is None:
                continue
            identifier_type = IdentifierType(identifier_info.me_type)
            
            if identifier_type in self.identifier_class_map.keys():
                setattr(self.aimms_model, identifier, self.identifier_class_map[identifier_type](
                    name=identifier,
                    index_domain=[],
                    parent_me_handle=0,
                    model_reflection_handle=identifier_info.me_handle,
                    project=self,
                ))
                self.reflected_identifiers.append(getattr(self.aimms_model, identifier))
    
    def add_identifiers(self):
        if self.exposed_identifier_set_name:
            self.exposed_identifier_set = self.aimms_api.get_exposed_identifiers(self.exposed_identifier_set_name)
            
            # print (f"Exposed identifiers: {self.exposed_identifier_set}")
            # split the rest of the identifiers into a prefix list and a normal identifier list
            prefixed_identifiers = []
            normal_identifiers = []
            
            for identifier in self.exposed_identifier_set:
                if "::" in identifier:
                    prefixed_identifiers.append(identifier)
                else:
                    normal_identifiers.append(identifier)      

            self.aimms_api.walk_model(0)
            # first find all the libraries and add them to the project and remove them from the normal identifiers
            normal_identifiers = self.find_libraries(normal_identifiers)
    
            self.add_identifiers_to_self(normal_identifiers)          
                
            # sort the to_add_identifiers by amount of :: such that we first add the libraries that are necessary for the other identifiers
            to_add_identifiers = sorted(prefixed_identifiers, key=lambda x: x.count("::"))
            # print(f"Adding identifiers: {to_add_identifiers}\n")
            # print(f"Prefix map: {self.prefix_map}\n")
            
            # make a dictatory with the prefix as key and all the identifiers that need to be added to that library
            for identifier in to_add_identifiers:
                prefix_parts = identifier.split("::")
                prefix = "::".join(prefix_parts[:-1])
                name = prefix_parts[-1]
                object_to_add_to = self.prefix_map[prefix]

        
                identifier_info = self.find_identifier_info(identifier, False)
                if identifier_info is None:
                    # print(f"Identifier {identifier} was deemed not necessary to add to the project, could be an index declared in a set for example")
                    continue
                identifier_type = IdentifierType(identifier_info.me_type)

                if identifier_type in self.identifier_class_map.keys():
                    setattr(object_to_add_to, name, self.identifier_class_map[identifier_type](
                        name=name,
                        prefix=prefix,
                        parent_me_handle=object_to_add_to.me_handle,
                        index_domain=[],
                        model_reflection_handle=identifier_info.me_handle,
                        project=self,
                    ))
                    self.reflected_identifiers.append(getattr(object_to_add_to, name))
                    
                elif identifier_type in self.identifier_with_prefix.keys():
                    new_prefixed_identifier = self.identifier_with_prefix[identifier_type](
                        name=name,
                        prefix=prefix_parts[-2],
                        project=self,
                        aimms_version=self.aimms_version,
                        model_reflection_handle=identifier_info.me_handle,
                        aimms_api=self.aimms_api
                    )
                    
                    self.prefix_map[prefix + "::" + new_prefixed_identifier.prefix] = new_prefixed_identifier
                    if identifier_type == IdentifierType.LIBRARY:
                        self.libraries.add(new_prefixed_identifier)
                    setattr(object_to_add_to, new_prefixed_identifier.prefix_attr, new_prefixed_identifier)
                
            # after adding all the identifiers to the project, we can fill the index domain
            for identifier in self.reflected_identifiers:
                
                if isinstance(identifier, Index):
                    identifier.fill_range()           
    
    def multi_assign(self, data : pd.DataFrame | pl.DataFrame | pyarrow.Table, options: dict[str, bool] = None):
        if options is None:
            options = {}
        if ('update' not in options):
            options["update"] = False

        if isinstance(data, pd.DataFrame):
            self.aimms_api.multi_add_values_dataframe_arrow( pyarrow.Table.from_pandas(data), options)
        elif isinstance(data, pl.DataFrame):
            self.aimms_api.multi_add_values_dataframe_arrow( data.to_arrow(), options)
        elif isinstance(data, pyarrow.Table):
            self.aimms_api.multi_add_values_dataframe_arrow(data, options)
    


