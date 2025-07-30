# TODO rename file to variables.py?
import time

from database_mysql_local.generic_crud import GenericCRUD
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger
from user_context_remote.user_context import UserContext
from fields_local.fields_local import FieldsLocal

from .constants import variable_local_logger_init_object, VARIABLE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID

cache_with_timeout = {}


class VariablesLocal(GenericCRUD, metaclass=MetaLogger, object=variable_local_logger_init_object):
    # Note: field_id reffering to a field in the database, while variable_id reffering to any variable in the system
    def __init__(self, is_test_data: bool = False):
        super().__init__(default_schema_name="logger",
                         is_test_data=is_test_data)
        self.fields_local = FieldsLocal(is_test_data=is_test_data)
        self.name2id_dict = {}
        self.id2name_dict = {}
        self.next_variable_id = 1
        variable_names_dict = self.load_variable_names_dict_from_variable_table()
        for variable_id in variable_names_dict:
            self.add(variable_id=variable_id,
                     variable_name=variable_names_dict[variable_id])

    def add(self, variable_id: int, variable_name: str) -> None:
        if variable_id is not None and variable_name is not None:
            self.name2id_dict[variable_name] = variable_id
            self.id2name_dict[variable_id] = variable_name

    def get_variable_id_by_variable_name(self, variable_name: str) -> int:
        variable_id = self.name2id_dict.get(variable_name)
        return variable_id

    def get_variable_name_by_variable_id(self, variable_id: int) -> str:
        variable_name = self.id2name_dict[variable_id]
        return variable_name

    def get_variable_value_by_variable_name_and_lang_code(self, variable_name: str, lang_code: LangCode) -> str:
        variable_id = self.get_variable_id_by_variable_name(
            variable_name=variable_name)
        variable_value = self.get_variable_value_by_variable_id(
            lang_code=lang_code, variable_id=variable_id)

        return variable_value

    def set_variable_value_by_variable_id(self, variable_id: int, variable_value: str, profile_id: int,
                                          state_id: int) -> None:
        # TODO I believe we should keep more fields  [like what?]
        data_dict = {'variable_id': variable_id, 'variable_value_new': variable_value, 'profile_id': profile_id,
                     'state_id': state_id, 'record': '{}', 'message': '', 'path': '',
                     'component_id': VARIABLE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID}
        self.insert(schema_name="logger", table_name='logger_table', data_dict=data_dict)

    def get_variable_value_by_variable_id(self, variable_id: int, lang_code: LangCode, profile_id: int = None) -> str:
        timeout = 60  # seconds
        cache_key = (variable_id, lang_code, profile_id)
        if cache_key in cache_with_timeout:
            if cache_with_timeout[cache_key]["time"] > time.time() - timeout:
                return cache_with_timeout[cache_key]["result"]

        where = ("variable_id= %s AND variable_value_new IS NOT NULL " +
                 (f"AND profile_id= %s " if profile_id is not None else ""))
        params = (variable_id, profile_id) if profile_id is not None else (variable_id,)
        result = self.select_one_dict_by_where(schema_name='logger',
                                               view_table_name="logger_dialog_workflow_state_history_view",
                                               select_clause_value="variable_value_new",
                                               where=where, params=params, order_by="timestamp DESC")
        if not result:
            if profile_id is not None:
                variable_value = self.get_variable_value_by_variable_id(variable_id=variable_id, lang_code=lang_code)
                return variable_value
            else:
                self.logger.warning(f"No variable value found for "
                                    f"variable_id {variable_id}, lang_code {lang_code}, profile_id {profile_id}")
        variable_value = result.get("variable_value_new")
        cache_with_timeout[cache_key] = {"result": variable_value, "time": time.time()}

        return variable_value

    def load_variable_names_dict_from_variable_table(self, profile_id: int = None, person_id: int = None) -> dict:
        profile_id = profile_id or UserContext().get_real_profile_id()
        # TODO: move cache to SDK
        timeout = 60  # seconds
        cache_key = (profile_id, person_id)
        if cache_key in cache_with_timeout:
            if cache_with_timeout[cache_key]["time"] > time.time() - timeout:
                return cache_with_timeout[cache_key]["result"]

        rows = self.fields_local.select_multi_dict_by_where(
            view_table_name="variable_view",
            where="person_id = %s or profile_id=%s OR profile_id IS NULL" if person_id is not None else "profile_id=%s OR profile_id IS NULL",
            params=(person_id, profile_id) if person_id is not None else (profile_id,),
            select_clause_value="variable_id, name",
        )

        data = {}
        for row in rows:
            data[row['variable_id']] = row['name']

        cache_with_timeout[cache_key] = {"result": data, "time": time.time()}

        return data
