import re
import logging
from langchain.schema.messages import HumanMessage, SystemMessage
from user_sim.utils.token_cost_calculator import calculate_cost, max_input_tokens_allowed, max_output_tokens_allowed
from user_sim.utils import config
from user_sim.utils.utilities import init_model
from user_sim.utils.register_management import save_register, load_register, hash_generate


logger = logging.getLogger('Info Logger')
model = None
llm = None


image_register_name = "image_register.json"

def init_vision_module():
    global model
    global llm
    model, llm = init_model()



def generate_image_description(image, url=True, detailed=False):

    if not url:
        image_parsed = f"data:image/png;base64,{image.decode('utf-8')}"
    else:
        image_parsed = image

    if detailed:
        prompt = ("""
                  Describe in detail this image and its content. 
                  If there's text, describe everything you read. don't give vague descriptions.
                  If there is content listed, read it as it is.
                  Be as detailed as possible.
                  """)
    else:
        prompt = "briefly describe this image, don't over explain, just give a simple and fast explanation of the main characteristics."

    if llm is None:
        logger.error("vision module not initialized.")
        return "Empty data"

    if max_input_tokens_allowed(prompt, model, image=image):
        logger.error(f"Token limit was surpassed")
        return None

    message = HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_parsed,
                            # "detail": "auto"
                        }
                    }
                ]
            )

    try:
        if config.token_count_enabled:
            llm.max_tokens = max_output_tokens_allowed(model)
            output = llm.invoke([message])
        else:
            output = llm.invoke([message])
        output_text = f"(Image description: {output.content})"
    except Exception as e:
        logger.error(e)
        logger.error("Couldn't get image description")
        output_text = "Empty data"
    logger.info(output_text)
    if config.token_count_enabled:
        calculate_cost(prompt, output_text, model=model, module="image recognition module", image=image)

    return output_text

def image_description(image, detailed=False, url=True):
    if config.ignore_cache:
        register = {}
        logger.info("Cache will be ignored.")
    else:
        register = load_register(image_register_name)

    image_hash = hash_generate(content=image)

    if image_hash in register:
        if config.update_cache:
            description = generate_image_description(image, url, detailed)
            register[image_hash] = description
            logger.info("Cache updated!")
        # description = register[image_hash]
        logger.info("Retrieved information from cache.")
        return register[image_hash]
    else:
        description = generate_image_description(image, url)
        register[image_hash] = description

    if config.ignore_cache:
        logger.info("Images cache was ignored")
    else:
        save_register(register, image_register_name)
        logger.info("Images cache was saved!")

    return description


def image_processor(text):

    def get_images(phrase):
        pattern = r"<image>(.*?)</image>"
        matches = re.findall(pattern, phrase)
        return matches

    def replacer(match):
        nonlocal replacement_index, descriptions
        if replacement_index < len(descriptions):
            original_image = match.group(1)
            replacement = descriptions[replacement_index]
            replacement_index += 1
            return f"<image>{original_image}</image> {replacement}"
        return match.group(0)  # If no more replacements, return the original match

    if text is None:
        return text
    else:
        images = get_images(text)
        if images:
            descriptions = []
            for image in images:
                descriptions.append(image_description(image))

            replacement_index = 0

            result = re.sub(r"<image>(.*?)</image>", replacer, text)
            return result
        else:
            return text