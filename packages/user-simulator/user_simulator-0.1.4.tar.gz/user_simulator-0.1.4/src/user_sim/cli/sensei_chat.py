import timeit
import yaml
import pandas as pd
from collections import Counter
from argparse import ArgumentParser
from colorama import Fore, Style
from src.technologies.chatbot_connectors import (Chatbot, ChatbotRasa, ChatbotTaskyto, ChatbotMillionBot,
                                             ChatbotServiceform)
from src.user_sim.core.data_extraction import DataExtraction
from src.user_sim.core.role_structure import *
from src.user_sim.core.user_simulator import UserSimulator
from src.user_sim.utils.show_logs import *
from src.user_sim.utils.utilities import *
from src.user_sim.utils.token_cost_calculator import create_cost_dataset
from src.user_sim.utils.register_management import clean_temp_files

check_keys(["OPENAI_API_KEY"])
current_script_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_script_dir, ".."))

def print_user(msg):
    clean_text = re.sub(r'\(Web page content: [^)]*>>\)', '', msg)
    clean_text = re.sub(r'\(PDF content: [^)]*>>\)', '', clean_text)
    clean_text = re.sub(r'\(Image description[^)]*\)', '', clean_text)
    print(f"{Fore.GREEN}User:{Style.RESET_ALL} {clean_text}")


def print_chatbot(msg):
    clean_text = re.sub(r'\(Web page content:.*?\>\>\)', '', msg, flags=re.DOTALL)
    clean_text = re.sub(r'\(PDF content:.*?\>\>\)', '', clean_text, flags=re.DOTALL)
    clean_text = re.sub(r'\(Image description[^)]*\)', '', clean_text)
    print(f"{Fore.LIGHTRED_EX}Chatbot:{Style.RESET_ALL} {clean_text}")

def load_yaml_arguments(project_path):
    files = os.listdir(project_path)

    run_file = next((f for f in files if f in ["run.yml", "run.yaml"]), None)

    if not run_file:
        raise FileNotFoundError(f"Couldn't find run.yml file.")

    run_yaml_path = os.path.join(project_path, run_file)

    with open(run_yaml_path, 'r', encoding='utf-8') as f:
        yaml_args = yaml.safe_load(f)

        if yaml_args:
            if "execution_parameters" in yaml_args.keys():
                parameters = yaml_args["execution_parameters"]
                dict_parameters = {param: True for param in parameters}
                del yaml_args["execution_parameters"]
                yaml_args.update(dict_parameters)

    yaml_args["project_path"] = project_path

    return yaml_args or {}


def load_yaml_files_from_folder(folder_path, existing_keys=None):
    types = {}
    for filename in os.listdir(folder_path):
        if filename.endswith((".yml", ".yaml")):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    name = data.get("name")
                    if name:
                        if not existing_keys or name not in existing_keys:
                            types[name] = data
            except yaml.YAMLError as e:
                logger.error(f"Error reading {file_path}: {e}")
    return types


def configure_project(project_path):
    config.project_folder_path = project_path
    config.profiles_path = os.path.join(project_path, "profiles")
    config.custom_personalities_folder = os.path.join(project_path, "personalities")

    custom_types_path = os.path.join(project_path, "types")
    default_types_path = os.path.join(config.root_path,"src", "config", "types")

    custom_types = load_yaml_files_from_folder(custom_types_path)
    default_types = load_yaml_files_from_folder(default_types_path, existing_keys=custom_types.keys())
    config.types_dict = {**default_types, **custom_types}

def configure_connector(*args):

    connec = args[0]
    with open(connec, 'r', encoding='utf-8') as f:
        con_yaml = yaml.safe_load(f)


    if len(args)<2 or not con_yaml["parameters"]:
        logger.warning("No parameters added for connector configuration. They may not have been set as input arguments "
                    "or declared as dynamic parameters in the connector file.")
        return con_yaml

    parameters = args[1]
    if isinstance(parameters, str):
        parameters = json.loads(parameters)

    param_key_list = list(parameters.keys())
    if Counter(con_yaml["parameters"]) != Counter(param_key_list):
        raise UnmachedList("Parameters in yaml don't match parameters input in execution")

    def replace_values(obj_dict, src_dict):
        for key in obj_dict:
            if isinstance(obj_dict[key], dict):
                replace_values(obj_dict[key], src_dict)
            elif key in src_dict:
                obj_dict[key] = src_dict[key]

    replace_values(con_yaml, parameters)
    return con_yaml


def get_conversation_metadata(user_profile, the_user, serial=None):
    def conversation_metadata(up):
        interaction_style_list = []
        conversation_list = []

        for inter in up.interaction_styles:
            interaction_style_list.append(inter.get_metadata())

        conversation_list.append({'interaction_style': interaction_style_list})

        if isinstance(up.yaml['conversation']['number'], int):
            conversation_list.append({'number': up.yaml['conversation']['number']})
        else:
            conversation_list.append({'number': up.conversation_number})

        if 'random steps' in up.yaml['conversation']['goal_style']:
            conversation_list.append({'goal_style': {'steps': up.goal_style[1]}})
        else:
            conversation_list.append(up.yaml['conversation']['goal_style'])

        return conversation_list

    def ask_about_metadata(up):
        if not up.ask_about.variable_list:
            return up.ask_about.str_list

        if user_profile.ask_about.picked_elements:
            user_profile.ask_about.picked_elements = [
        {clave: (valor[0] if isinstance(valor, list) and len(valor) == 1 else valor)
         for clave, valor in dic.items()}
        for dic in user_profile.ask_about.picked_elements
    ]

        return user_profile.ask_about.str_list + user_profile.ask_about.picked_elements

    def data_output_extraction(u_profile, user):
        output_list = u_profile.output
        data_list = []
        for output in output_list:
            var_name = list(output.keys())[0]
            var_dict = output.get(var_name)
            my_data_extract = DataExtraction(user.conversation_history,
                                             var_name,
                                             var_dict["type"],
                                             var_dict["description"])
            data_list.append(my_data_extract.get_data_extraction())

        data_dict = {k: v for dic in data_list for k, v in dic.items()}
        has_none = any(value is None for value in data_dict.values())
        if has_none:
            count_none = sum(1 for value in data_dict.values() if value is None)
            config.errors.append({1001: f"{count_none} goals left to complete."})

        return data_list

    def total_cost_calculator():
        encoding = get_encoding(config.cost_ds_path)["encoding"]
        cost_df = pd.read_csv(config.cost_ds_path, encoding=encoding)

        total_sum_cost = cost_df[cost_df["Conversation"]==config.conversation_name]['Total Cost'].sum()
        total_sum_cost = round(float(total_sum_cost), 8)

        return total_sum_cost


    data_output = {'data_output': data_output_extraction(user_profile, the_user)}
    context = {'context': user_profile.raw_context}
    ask_about = {'ask_about': ask_about_metadata(user_profile)}
    conversation = {'conversation': conversation_metadata(user_profile)}
    language = {'language': user_profile.language}
    serial_dict = {'serial': serial}
    errors_dict = {'errors': config.errors}
    total_cost = {'total_cost($)': total_cost_calculator()}
    metadata = {**serial_dict,
                **language,
                **context,
                **ask_about,
                **conversation,
                **data_output,
                **errors_dict,
                **total_cost
                }

    return metadata


def parse_profiles(user_path):
    def is_yaml(file):
        if not file.endswith(('.yaml', '.yml')):
            return False
        try:
            with open(file, 'r') as f:
                yaml.safe_load(f)
            return True
        except yaml.YAMLError:
            return False

    list_of_files = []
    if os.path.isfile(user_path):
        if is_yaml(user_path):
            yaml_file = read_yaml(user_path)
            return [yaml_file]
        else:
            raise Exception(f'The user profile file is not a yaml: {user_path}')
    elif os.path.isdir(user_path):
        for root, _, files in os.walk(user_path):
            for file in files:
                if is_yaml(os.path.join(root, file)):
                    path = root + '/' + file
                    yaml_file = read_yaml(path)
                    list_of_files.append(yaml_file)

            return list_of_files
    else:
        raise Exception(f'Invalid path for user profile operation: {user_path}')


def build_chatbot(technology, connector) -> Chatbot:
    chatbot_builder = {
        'rasa': ChatbotRasa,
        'taskyto': ChatbotTaskyto,
        'serviceform': ChatbotServiceform,
        'millionbot': ChatbotMillionBot
    }
    chatbot_class = chatbot_builder.get(technology, Chatbot)
    return chatbot_class(connector)



def generate_conversation(technology, connector, user,
                          personality, extract, project_folder):
    profiles = parse_profiles(user)
    serial = generate_serial()
    config.serial = serial
    create_cost_dataset(serial, extract)
    my_execution_stat = ExecutionStats(extract, serial)
    the_chatbot = build_chatbot(technology, connector)


    for profile in profiles:
        user_profile = RoleData(profile, project_folder, personality)
        test_name = user_profile.test_name
        config.test_name = test_name
        chat_format = user_profile.format_type
        start_time_test = timeit.default_timer()

        for i in range(user_profile.conversation_number):
            config.conversation_name = f'{i}_{test_name}_{serial}.yml'
            the_chatbot.fallback = user_profile.fallback
            the_user = UserSimulator(user_profile, the_chatbot)
            bot_starter = user_profile.is_starter
            response_time = []

            start_time_conversation = timeit.default_timer()
            response = ''

            if chat_format == "speech":
                from user_sim.handlers.asr_module import STTModule

                stt = STTModule(user_profile.format_config)

                def send_user_message(user_msg):
                    print_user(user_msg)
                    stt.say(user_msg)

                def get_chatbot_response(user_msg):
                    start_response_time = timeit.default_timer()
                    is_ok, response = stt.hear()
                    end_response_time = timeit.default_timer()
                    time_sec = timedelta(seconds=end_response_time - start_response_time).total_seconds()
                    response_time.append(time_sec)
                    return is_ok, response

                def get_chatbot_starter_response():
                    is_ok, response = stt.hear()
                    return is_ok, response

            else:

                if user_profile.format_config:
                    logger.warning("Chat format is text, but an SR configuration was provided. This configuration will"
                                   " be ignored.")

                def send_user_message(user_msg):
                    print_user(user_msg)

                def get_chatbot_response(user_msg):
                    start_response_time = timeit.default_timer()
                    is_ok, response = the_chatbot.execute_with_input(user_msg)
                    end_response_time = timeit.default_timer()
                    time_sec = timedelta(seconds=end_response_time - start_response_time).total_seconds()
                    response_time.append(time_sec)
                    return is_ok, response

                def get_chatbot_starter_response():
                    is_ok, response = the_chatbot.execute_starter_chatbot()
                    return is_ok, response

            start_loop = True
            if bot_starter:
                is_ok, response = get_chatbot_starter_response()
                if not is_ok:
                    if response is not None:
                        the_user.update_history("Assistant", "Error: " + response)
                    else:
                        the_user.update_history("Assistant", "Error: The server did not respond.")
                    start_loop = False
                print_chatbot(response)
                user_msg = the_user.open_conversation()
                if user_msg == "exit":
                    start_loop = False

            else:
                user_msg = the_user.open_conversation()
                if user_msg == "exit":
                    start_loop = False
                else:
                    send_user_message(user_msg)
                    is_ok, response = get_chatbot_response(user_msg)
                    if not is_ok:
                        if response is not None:
                            the_user.update_history("Assistant", "Error: " + response)
                        else:
                            the_user.update_history("Assistant", "Error: The server did not respond.")
                        start_loop = False
                    else:
                        print_chatbot(response)

            if start_loop:
                while True:
                    user_msg = the_user.get_response(response)
                    if user_msg == "exit":
                        break
                    send_user_message(user_msg)
                    is_ok, response = get_chatbot_response(user_msg)
                    if response == 'timeout':
                        break
                    print_chatbot(response)
                    if not is_ok:
                        if response is not None:
                            the_user.update_history("Assistant", "Error: " + response)
                        else:
                            the_user.update_history("Assistant", "Error: The server did not respond.")
                        break

            if extract:
                end_time_conversation = timeit.default_timer()
                conversation_time = end_time_conversation - start_time_conversation
                formatted_time_conv = timedelta(seconds=conversation_time).total_seconds()
                print(f"Conversation Time: {formatted_time_conv} (s)")

                history = the_user.conversation_history
                metadata = get_conversation_metadata(user_profile, the_user, serial)
                dg_dataframe = the_user.data_gathering.gathering_register
                csv_extraction = the_user.goal_style[1] if the_user.goal_style[0] == 'all_answered' else False
                answer_validation_data = (dg_dataframe, csv_extraction)
                save_test_conv(history, metadata, test_name, extract, serial,
                               formatted_time_conv, response_time, answer_validation_data, counter=i)

            config.total_individual_cost = 0
            user_profile.reset_attributes()

            if hasattr(the_chatbot, 'id'):
                the_chatbot.id = None

        end_time_test = timeit.default_timer()
        execution_time = end_time_test - start_time_test
        formatted_time = timedelta(seconds=execution_time).total_seconds()
        print(f"Execution Time: {formatted_time} (s)")
        print('------------------------------')

        if user_profile.conversation_number > 0:
            my_execution_stat.add_test_name(test_name)
            my_execution_stat.show_last_stats()

    if config.clean_cache:
        clean_temp_files()

    if extract and len(my_execution_stat.test_names) == len(profiles):
        my_execution_stat.show_global_stats()
        my_execution_stat.export_stats()
    elif extract:
        logger.warning("Stats export was enabled but couldn't retrieve all stats. No stats will be exported.")
    else:
        pass

    end_alarm()

def main():
    parser = ArgumentParser(description='Conversation generator for a chatbot')

    parser.add_argument('--run_from_yaml', type=str, help='Carga los argumentos desde un archivo YAML')

    parser.add_argument('--technology', required=False,
                        choices=['rasa', 'taskyto', 'ada-uam', 'millionbot', 'genion', 'lola', 'serviceform', 'kuki', 'julie', 'rivas_catalina', 'saic_malaga'],
                        help='Technology the chatbot is implemented in')
    # parser.add_argument('--chatbot', required=False, help='URL where the chatbot is deployed')
    parser.add_argument('--connector', required=False, help='path to the connector configuration file')
    parser.add_argument('--connector_parameters', required=False, help='dynamic parameters for the selected chatbot connector')
    parser.add_argument('--project_path', required=False, help='Project folder PATH where all testing data is stored')
    parser.add_argument('--user_profile', required=False, help='User profile file or user profile folder to test the chatbot')
    parser.add_argument('--personality', required=False, help='Personality file')
    parser.add_argument("--extract", default=False, help='Path to store conversation user-chatbot')
    parser.add_argument('--verbose', action='store_true', help='Shows debug prints')
    parser.add_argument('--clean_cache', action='store_true', help='Deletes temporary files.')
    parser.add_argument('--ignore_cache', action='store_true', help='Ignores cache for temporary files')
    parser.add_argument('--update_cache', action='store_true', help='Overwrites temporary files in cache')
    parser_args, unknown_args = parser.parse_known_args()

    if parser_args.run_from_yaml:
        if len(sys.argv) > 3:  # sys.argv[0] is script, sys.argv[1] is --run_from_yaml, sys.argv[2] is YAML
            parser.error("No other arguments can be provided when using --run_from_yaml.")

        yaml_args = load_yaml_arguments(parser_args.run_from_yaml)

        default_flags = {
            "connector_parameters": None,
            "personality": None,
            "verbose": False,
            "clean_cache": False,
            "ignore_cache": False,
            "update_cache": False
        }
        for flag, default in default_flags.items():
            yaml_args.setdefault(flag, default)

        class ArgsNamespace:
            def __init__(self, **entries):
                self.__dict__.update(entries)

        parser_args = ArgsNamespace(**yaml_args)

    else:
        required_args = ['technology', 'user_profile', 'connector']
        missing_args = [arg for arg in required_args if getattr(parser_args, arg) is None]

        if missing_args:
            parser.error(f"The following arguments are required when not using --run_from_yaml: {', '.join(missing_args)}")

    configure_project(parser_args.project_path)
    config.root_path = os.path.abspath(os.path.join(current_script_dir, "../../.."))
    profile_path = os.path.join(config.profiles_path, parser_args.user_profile)

    logger = create_logger(parser_args.verbose, 'Info Logger')
    logger.info('Logs enabled!')

    check_keys(["OPENAI_API_KEY"])
    config.test_cases_folder = parser_args.extract
    config.ignore_cache = parser_args.ignore_cache
    config.update_cache = parser_args.update_cache
    config.clean_cache = parser_args.clean_cache

    if parser_args.connector_parameters:
        connector = configure_connector(parser_args.connector, parser_args.connector_parameters)
    else:
        connector = configure_connector(parser_args.connector)

    generate_conversation(parser_args.technology, connector, profile_path,
                          parser_args.personality, parser_args.extract, parser_args.project_path)


if __name__ == '__main__':
    main()