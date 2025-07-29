import itertools
from pydantic import BaseModel, ValidationError, field_validator
from typing import List, Union, Dict, Optional
from src.user_sim.core.interaction_styles import *
from src.user_sim.core.ask_about import *
from src.user_sim.utils.exceptions import *
from src.user_sim.utils.languages import languages
from src.user_sim.utils import config
from dataclasses import dataclass
from src.user_sim.handlers.image_recognition_module import init_vision_module
from src.user_sim.core.data_gathering import init_data_gathering_module
from src.user_sim.core.data_extraction import init_data_extraction_module
import logging
logger = logging.getLogger('Info Logger')


def replace_placeholders(phrase, variables):
    def replacer(match):
        key = match.group(1)
        if isinstance(variables, dict):
            return ', '.join(map(str, variables.get(key, [])))
        else:
            return ', '.join(map(str, variables))

    pattern = re.compile(r'\{\{(\w+)\}\}')
    return pattern.sub(replacer, phrase)



def list_to_str(list_of_strings):
    if list_of_strings is None:
        return ''
    try:
        single_string = ' '.join(list_of_strings)
        return single_string
    except Exception as e:
        # logging.getLogger().verbose(f'Error: {e}')
        return ''


class ConvFormat(BaseModel):
    type: Optional[str] = "text"
    config: Optional[str] = None

class LLM(BaseModel):
    model: Optional[str] = "gpt-4o"
    model_prov: Optional[str] = None
    temperature: Optional[float] = 0.8
    format: Optional[ConvFormat] = ConvFormat()  # text, speech, hybrid

class User(BaseModel):
    language: Optional[Union[str, None]] = 'English'
    role: str
    context: Optional[Union[List[Union[str, Dict]], Dict, None]] = ''
    goals: list


class ChatbotClass(BaseModel):
    is_starter: Optional[bool] = True
    fallback: str
    output: list


class Conversation(BaseModel):
    number: Union[int, str]
    max_cost: Optional[float]=10**9
    goal_style: Dict
    interaction_style: list

    @field_validator('max_cost', mode='before')
    @classmethod
    def set_token_count_enabled(cls, value):
        if value is not None:
            config.token_count_enabled = True
        return value

class RoleDataModel(BaseModel):
    test_name: str
    llm: Optional[LLM] = LLM()
    user: User
    chatbot: ChatbotClass
    conversation: Conversation

@dataclass
class ValidationIssue:
    field: str
    error: str
    error_type: str
    location: str

class RoleData:

    def __init__(self, yaml_file, project_folder=None, personality_file=None, validation=False):
        self.yaml = yaml_file
        self.validation = validation
        self.personality_file = personality_file
        self.project_folder = project_folder
        self.errors: List[ValidationIssue] = []

        # try:
        #     self.validated_data = RoleDataModel(**self.yaml)
        # except ValidationError as e:
        #     for err in e.errors():
        #         loc_path = '.'.join(str(part) for part in err['loc'])
        #         issue = ValidationIssue(
        #             field=err['loc'][-1],
        #             error=err['msg'],
        #             error_type=err['type'],
        #             location=loc_path
        #         )
        #         self.errors.append(issue)

    # Test Name
        try:
            self.test_name = self.yaml.get('test_name')
        except Exception as e:
            self.collect_errors(e, prefix='llm')

    # LLM
        self.model = self.model_provider = self.temperature = self.format_type = self.format_config = None
        try:
            self.llm = LLM(**self.yaml.get('llm', {}))
            self.model = config.model = self.llm.model
            self.model_provider = config.model_provider = self.llm.model_prov
            self.temperature = self.llm.temperature
            self.format_type = self.llm.format.type
            self.format_config = self.llm.format.config
        except Exception as e:
            self.collect_errors(e, prefix='llm')

        if not self.errors:
            self.init_llm_modules()

    # User
        self.language = self.role = self.raw_context = self.context = self.ask_about = None
        try:
            self.user = User(**self.yaml.get('user', {}))
            self.language = self.set_language(self.user.language)
            self.role = self.user.role
            self.raw_context = self.user.context
            self.context = self.context_processor(self.raw_context)
            self.ask_about = self.get_ask_about()
        except Exception as e:
            self.collect_errors(e, prefix='user')

    # Chatbot
        self.is_starter = self.fallback = self.output = None
        try:
            self.chatbot = ChatbotClass(**self.yaml.get('chatbot', {}))
            self.is_starter = self.chatbot.is_starter
            self.fallback = self.chatbot.fallback
            self.output = self.chatbot.output
        except Exception as e:
            self.collect_errors(e, prefix='chatbot')

    # Conversation
        self.conversation_number = self.max_cost = self.goal_style = self.interaction_styles = None
        try:
            self.conversation = Conversation(**self.yaml.get('conversation', {}))
            self.combinations_dict = {}
            self.conversation_number = self.get_conversation_number(self.conversation.number)
            self.max_cost = self.conversation.max_cost
            config.limit_cost = self.max_cost
            self.goal_style = self.pick_goal_style(self.conversation.goal_style)
            self.interaction_styles = self.pick_interaction_style(self.conversation.interaction_style)
        except Exception as e:
            self.collect_errors(e, prefix='conversation')

    # # Initialization of all LLM modules
    #     self.init_llm_modules()

    def init_llm_modules(self):

        init_vision_module()
        init_data_gathering_module()
        init_data_extraction_module()
        init_any_list_module()
        # init_asr_module()


    def collect_errors(self, e: ValidationError, prefix=""):

        if isinstance(e, ValidationError):
            for err in e.errors():
                loc_path = '.'.join(str(part) for part in err['loc'])
                full_path = f"{prefix}.{loc_path}" if prefix else loc_path
                self.errors.append(
                    ValidationIssue(
                        field=err['loc'][-1],
                        error=err['msg'],
                        error_type=err['type'],
                        location=full_path
                    )
                )
        else:
            self.errors.append(
                ValidationIssue(
                    field='unknown',
                    error=str(e),
                    error_type=type(e).__name__,
                    location=prefix
                )
            )


    def get_errors(self):
        error_list = []
        for error in self.errors:
            formated_error = {
                "field": error.location,
                "error": error.error,
                "type": error.error_type
            }
            error_list.append(formated_error)
        logger.warning(f"\n{len(self.errors)} errors detected.\n")

        return error_list, len(self.errors)


    def get_ask_about(self):
        if self.validation:
            try:
                return AskAboutClass(self.user.goals)
            except Exception as e:
                issue = ValidationIssue(
                    field="goals",
                    error=str(e),
                    error_type=type(e).__name__,
                    location="user.goals"
                )
                self.errors.append(issue)
        else:
            return AskAboutClass(self.user.goals)



    def set_language(self, lang):
        if isinstance(lang, type(None)):
            logger.info("Language parameter empty. Setting language to Default (English)")
            return "English"
        try:
            if lang in languages:
                logger.info(f"Language set to {lang}")
                return lang
            else:
                raise InvalidLanguageException(f'Invalid language input: {lang}. Setting language to default (English)')
        except InvalidLanguageException as e:
            issue = ValidationIssue(
                field= "language",
                error=str(e),
                error_type=type(e).__name__,
                location="user.language"
            )
            self.errors.append(issue)
            return "English"


    def reset_attributes(self):
        logger.info(f"Preparing attributes for next conversation...")
        self.init_llm_modules()
        self.fallback = self.chatbot.fallback
        # self.is_starter = self.validated_data.is_starter
        self.context = self.context_processor(self.raw_context)
        self.ask_about.reset()  # self.picked_elements = [], self.phrases = []

        self.goal_style = self.pick_goal_style(self.conversation.goal_style)
        self.language = self.set_language(self.user.language)
        self.interaction_styles = self.pick_interaction_style(self.conversation.interaction_style)

    @staticmethod
    def list_to_dict_reformat(conv):
        result_dict = {k: v for d in conv for k, v in d.items()}
        return result_dict

    def personality_extraction(self, context):
        if context["personality"]:
            personality = context["personality"]

            path_list = []
            if os.path.exists(config.custom_personalities_folder):
                custom_personalities_path = config.custom_personalities_folder
                path_list.append(custom_personalities_path)

            default_personalities_path = os.path.join(config.root_path, "config", "personalities")
            path_list.append(default_personalities_path)

            try:
                for path in path_list:
                    for file in os.listdir(path):
                        file_name, ext = os.path.splitext(file)
                        clean_personality, _ = os.path.splitext(personality)
                        if file_name == clean_personality and ext in ('.yml', '.yaml'):
                            personality_path = os.path.join(path, file)
                            personality_data = read_yaml(personality_path)

                            try:
                                self.personality = personality_data["name"]
                                logger.info(f"Personality set to '{file_name}'")
                                return personality_data['context']
                            except KeyError:
                                raise InvalidFormat(f"Key 'context' not found in personality file.")

                logger.error(f"Couldn't find specified personality file: '{personality}'")
                return ['']

            except Exception as e:
                logger.error(e)
                return ['']

        else:
            logger.error(f"Data for context is not a dictionary with context key: {context}.")
            return ['']

    def get_conversation_number(self, conversation):
        if isinstance(conversation, int):
            logger.info(f"{conversation} conversations will be generated")
            return conversation

        comb_pattern = r'^combinations(?:\(([^,()\s]+)(?:,\s*([^()]+))?\))?$'
        match = re.match(comb_pattern, conversation.strip())

        if self.validation:
            generators_list = self.ask_about.var_generators
            combinations_dict = []

            for generator in generators_list:
                if "matrix" in generator:
                    name = generator['name']
                    combination_matrix = []
                    combinations = 0
                    if generator['type'] == 'forward':
                        combination_matrix = [list(p) for p in itertools.product(*generator['matrix'])]
                        combinations = len(combination_matrix)
                    elif generator['type'] == 'pairwise':
                        combination_matrix = generator['matrix']
                        combinations = len(combination_matrix)

                    combinations_dict.append({'name':name,
                                 'matrix':combination_matrix,
                                 'combinations':combinations,
                                 'type': generator['type']})

            self.combinations_dict = combinations_dict

        if match:
            # func_name = "combinations"
            sample = match.group(1)
            iter_function = match.group(2)

            if iter_function == "forward":
                if self.ask_about.forward_combinations <= 0:
                    logger.error("Conversation number set to 'forward_all_combinations' but no combinations can be made.")
                    return 0
                conv_number = self.ask_about.forward_combinations

                if sample:
                    conv_number = round(conv_number * float(sample))
                logger.info(f"{conv_number} conversations will be generated.")
                return conv_number

            elif iter_function == "pairwise":
                if self.ask_about.pairwise_combinations <= 0:
                    logger.error("Conversation number set to 'pairwise_all_combinations' but no combinations can be made.")
                    return 0

                conv_number = self.ask_about.pairwise_combinations
                if sample:
                    conv_number = round(conv_number * float(sample))
                logger.info(f"{conv_number} conversations will be generated.")
                return conv_number

            else:
                conv_number = max(self.ask_about.forward_combinations, self.ask_about.pairwise_combinations)
                if conv_number < 1:
                    logger.error("Conversation number set to 'combinations' but no combinations can be made.")
                    return 0
                if sample:
                    conv_number = round(conv_number * float(sample))
                logger.info(f"{conv_number} conversations will be generated.")
                return conv_number

        else:
            logger.error(f"Conversation number can't be obtained due tu unrecognized value: {conversation}")
            issue = ValidationIssue(
                field= "language",
                error=f"Conversation number can't be obtained due tu unrecognized value: {conversation}",
                error_type=type(InvalidFormat).__name__,
                location="conversation.number"
            )
            self.errors.append(issue)
            return 0

    def context_processor(self, context):
        if isinstance(context, dict):
            personality_phrases = self.personality_extraction(context)
            return list_to_str(personality_phrases)

        res = len(list(filter(lambda x: isinstance(x, dict), context)))
        if res > 1:
            # raise InvalidFormat(f)
            issue = ValidationIssue(
                field="context",
                error=str("Too many keys in context list."),
                error_type=type(InvalidFormat).__name__,
                location="user.context"
            )
            self.errors.append(issue)
            return ""
        elif res <= 0 and not isinstance(context, dict):
            phrases = list_to_str(context)
            if self.personality_file is not None:
                personality = read_yaml(self.personality_file)
                personality_phrases = personality['context']
                phrases = phrases + list_to_str(personality_phrases)
            return phrases
        else:
            custom_phrases = []
            personality_phrases = []
            for item in context:
                if isinstance(item, str):
                    custom_phrases.append(item)
                elif isinstance(item, dict):
                    personality_phrases = personality_phrases + self.personality_extraction(item)
                else:
                    issue = ValidationIssue(
                        field="context",
                        error=str(f"Invalid data type in context list: {type(item)}:{item}"),
                        error_type=type(InvalidDataType).__name__,
                        location="user.context"
                    )
                    self.errors.append(issue)
                    return ""

            # If no personality is given, we use the one specified as input in the command line
            if len(personality_phrases) == 0 and self.personality_file is not None:
                personality = read_yaml(self.personality_file)
                personality_phrases = personality['context']

            total_phrases = personality_phrases + custom_phrases
            return list_to_str(total_phrases)

    def pick_goal_style(self, goal):

        if goal is None:
            return goal, False

        if 'max_cost' in goal:
            if goal['max_cost'] > 0:
                config.limit_individual_cost = goal['max_cost']
                config.token_count_enabled = True
            else:
                if self.validation:
                    issue = ValidationIssue(
                        field="goal_style",
                        error=str(f"Goal cost can't be lower than or equal to 0: {goal['cost']}"),
                        error_type=type(NoCostException).__name__,
                        location="conversation.goal_style"
                    )
                    self.errors.append(issue)
                    return ""
                else:
                    raise NoCostException(f"Goal cost can't be lower than or equal to 0: {goal['cost']}")
        else:
            config.limit_individual_cost = config.limit_cost

        if 'steps' in goal:
            if goal['steps'] <= 20 or goal['steps'] > 0:
                return list(goal.keys())[0], goal['steps']
            else:
                if self.validation:
                    issue = ValidationIssue(
                        field="goal_style",
                        error=str(f"Goal steps higher than 20 steps or lower than 0 steps: {goal['steps']}"),
                        error_type=type(OutOfLimitException).__name__,
                        location="conversation.goal_style"
                    )
                    self.errors.append(issue)
                    return ""
                else:
                    raise OutOfLimitException(f"Goal steps higher than 20 steps or lower than 0 steps: {goal['steps']}")

        elif 'all_answered' in goal or 'default' in goal:
            if isinstance(goal, dict):

                if 'export' in goal['all_answered']:
                    all_answered_goal = [list(goal.keys())[0], goal['all_answered']['export']]
                else:
                    all_answered_goal = [list(goal.keys())[0], False]

                if 'limit' in goal['all_answered']:
                    all_answered_goal.append(goal['all_answered']['limit'])
                else:
                    all_answered_goal.append(30)

                return all_answered_goal
            else:
                return [goal, False, 30]

        elif 'random steps' in goal:
            if goal['random steps'] < 20:
                return list(goal.keys())[0], random.randint(1, goal['random steps'])
            else:
                if self.validation:
                    issue = ValidationIssue(
                        field="goal_style",
                        error=str(f"Goal steps higher than 20 steps: {goal['random steps']}"),
                        error_type=type(OutOfLimitException).__name__,
                        location="conversation.goal_style"
                    )
                    self.errors.append(issue)
                    return ""
                else:
                    raise OutOfLimitException(f"Goal steps higher than 20 steps: {goal['random steps']}")

        else:
            if self.validation:
                issue = ValidationIssue(
                    field="goal_style",
                    error=str(f"Invalid goal value: {goal}"),
                    error_type=type(InvalidGoalException).__name__,
                    location="conversation.goal_style"
                )
                self.errors.append(issue)
                return ""
            else:
                raise InvalidGoalException(f"Invalid goal value: {goal}")


    def get_interaction_metadata(self):
        metadata_list = []
        for inter in self.interaction_styles:
            metadata_list.append(inter.get_metadata())

        return metadata_list

    def pick_interaction_style(self, interactions):

        inter_styles = {
            'long phrases': LongPhrases(),
            'change your mind': ChangeYourMind(),
            'change language': ChangeLanguage(self.language),
            'make spelling mistakes': MakeSpellingMistakes(),
            'single question': SingleQuestions(),
            'all questions': AllQuestions(),
            'default': Default()
        }

        def choice_styles(interaction_styles):
            count = random.randint(1, len(interaction_styles))
            random_list = random.sample(interaction_styles, count)
            # logging.getLogger().verbose(f'interaction style amount: {count} style(s): {random_list}')
            logger.info(f'interaction style count: {count}; style(s): {random_list}')
            return random_list

        def get_styles(interact):
            interactions_list = []
            try:
                for inter in interact:

                    if isinstance(inter, dict):
                        keys = list(inter.keys())
                        if keys[0] == "change language":
                            cl_interaction = inter_styles[keys[0]]
                            cl_interaction.languages_options = inter.get(keys[0]).copy()
                            cl_interaction.change_language_flag = True
                            interactions_list.append(cl_interaction)

                    else:
                        if inter in inter_styles:
                            interaction = inter_styles[inter]
                            interactions_list.append(interaction)
                        else:

                                raise InvalidInteractionException(f"Invalid interaction: {inter}")
            except InvalidInteractionException as e:
                issue = ValidationIssue(
                    field="interaction_style",
                    error=str(e),
                    error_type=type(e).__name__,
                    location="conversation.interaction_style"
                )
                self.errors.append(issue)
                logger.error(f"Error: {e}")

            return interactions_list

        # interactions_list = []
        if interactions is None:
            interaction_def = inter_styles['default']
            return [interaction_def]

        elif isinstance(interactions[0], dict) and 'random' in list(interactions[0].keys()):
            # todo: add validation funct to admit random only if it's alone in the list
            inter_rand = interactions[0]['random']
            choice = choice_styles(inter_rand)
            return get_styles(choice)

        else:
            return get_styles(interactions)

    def get_language(self):

        for instance in self.interaction_styles:
            if instance.change_language_flag:
                prompt = instance.get_prompt()
                return prompt

        return f"Please, talk in {self.language}"
