import random
import re

from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger
from python_sdk_remote.utilities import get_environment_name, get_brand_name, generate_otp, get_current_datetime_string
from smartlink_local.smartlink import SmartlinkLocal
from smartlink_remote_restapi.smartlink_remote import SmartlinkRemote
from url_remote.our_url import OurUrl

from .constants import variable_local_logger_init_object
from .variables_local import VariablesLocal


class ReplaceFieldsWithValues(metaclass=MetaLogger, object=variable_local_logger_init_object):
    def __init__(self, message: str, lang_code: LangCode, variables: VariablesLocal = None, is_test_data: bool = False):
        # TODO: we don't need message & lang_code in the constructor (breaking change)
        #  -> def __init__(self, variables: VariablesLocal = None, is_test_data: bool = False)
        self.message = message
        self.lang_code = lang_code
        self.variables = variables or VariablesLocal(is_test_data=is_test_data)
        self.is_test_data = is_test_data
        self.smartlink_local = None  # For performance reasons

    def get_smartlink_url_by_variable_name_and_kwargs(self, variable_name: str, **kwargs) -> str:
        self.smartlink_local = self.smartlink_local or SmartlinkLocal()
        smartlink_regex = r"smartlinkUrl\(smartlinkType=([0-9]+)\)"
        smartlink_type_id = re.search(smartlink_regex, variable_name).group(1)
        url_redirect_template = self.smartlink_local.get_smartlink_type_dict_by_id(
            smartlink_type_id, select_clause_value="url_redirect_template").get("url_redirect_template")
        if url_redirect_template:
            url_redirect = self.get_formatted_message(message=url_redirect_template)
        else:
            url_redirect = None
        smartlink_details = self.smartlink_local.insert(
            smartlink_type_id=smartlink_type_id, campaign_id=kwargs.get('campaign_id'),
            url_redirect=url_redirect,
            from_recipient_dict=kwargs.get('from_recipient'), to_recipient_dict=kwargs.get('to_recipient'))
        smartlink_url = SmartlinkRemote(is_test_data=self.is_test_data).get_smartlink_url(
            identifier=smartlink_details['identifier'])
        return smartlink_url

    # TODO variable_name: VariableNameEnum / SpecialVariableEnum
    def get_variable_value_by_variable_name_and_kwargs(self, variable_name: str, **kwargs) -> str or None:
        # TODO: use worker actions instead, using message_template.message_template_function_table
        """Returns a special variable value by variable name"""
        # TODO: test each case
        smartlink_regex = r"smartlinkUrl\(smartlinkType=([0-9]+)\)"

        # TODO Use message_template.message_template_function_table
        if variable_name == 'otp':
            variable_value = generate_otp()
        elif variable_name == 'dateSortable':
            variable_value = get_current_datetime_string()
        elif variable_name == 'environmentName':
            variable_value = get_environment_name()
        elif variable_name == 'brandName':
            variable_value = get_brand_name()
        elif variable_name == 'appUrl':
            variable_value = OurUrl.app_url(environment_name=get_environment_name(), brand_name=get_brand_name())
        elif re.match(smartlink_regex, variable_name):
            variable_value = self.get_smartlink_url_by_variable_name_and_kwargs(variable_name, **kwargs)
        else:  # TODO: add more special variables
            return

        variable_value = str(variable_value)
        return variable_value

    def get_variable_values_and_chosen_option(self, profile_id: int = None, **kwargs) -> str:
        self.logger.warning("get_variable_values_and_chosen_option is deprecated. Use get_formatted_message instead.")
        formatted_message = self.get_formatted_message(profile_id, **kwargs)
        return formatted_message

    # @staticmethod
    # def __preprocess_template(template_str):  # TODO: use jinja2
    #     variable_pattern = re.compile(r'\${{[^}]*}}')
    #     variables = set(re.findall(variable_pattern, template_str))
    #     return variables

    # used by Dialog workflow and message local
    # TODO: rename to format_text(self, *, original_text, lang_code, profile_id, **kwargs)
    def get_formatted_message(self, profile_id: int = None, **kwargs) -> str:
        """Returns:
            A string that's a copy of the message but without the variable names inside curly braces
            and a randomly chosen parameter out of each curly braces options:
            "Hello ${{First Name}}, how are you ${{feeling|doing}}?" --> "Hello Tal, how are you doing?"
            Please include in the kwargs any additional variables / context that are needed to replace the variables.
        """
        kwargs = kwargs.get('kwargs', kwargs)  # in case someone sent the kwargs in a diff way
        original_text = kwargs.get("message", self.message)
        formatted_text = original_text  # this is the message that will be returned after formatting

        pattern = re.compile(r'\${{[^}]*}}')  # ${{vraiable}}
        matches = pattern.findall(formatted_text)
        for exact_match in matches:
            match = exact_match[3:-2].strip()  # remove '${{' and '}}'
            if '|' in match:  # # choose random option from {A|B|C}
                # pick random choice
                options = match.split('|')
                random_option = random.choice(options)
                formatted_text = formatted_text.replace(exact_match, random_option, 1)

            elif match in kwargs:
                formatted_text = formatted_text.replace(
                    exact_match, str(kwargs[match] if match in kwargs else kwargs[match]), 1)

            elif match in self.variables.name2id_dict.keys():
                # replace variable name with variable_value
                variable_id = self.variables.get_variable_id_by_variable_name(match)
                variable_value = self.variables.get_variable_value_by_variable_id(
                    variable_id=variable_id, lang_code=self.lang_code, profile_id=profile_id)
                formatted_text = formatted_text.replace(exact_match, variable_value, 1)

            else:
                variable_value = self.get_variable_value_by_variable_name_and_kwargs(match, **kwargs)
                if variable_value:
                    formatted_text = formatted_text.replace(exact_match, variable_value, 1)
                else:
                    error_msg = "Unknown special variable name `" + match + "` in message: " + original_text
                    self.logger.error(error_msg, object=kwargs)
                    raise ValueError(error_msg)

        return formatted_text
