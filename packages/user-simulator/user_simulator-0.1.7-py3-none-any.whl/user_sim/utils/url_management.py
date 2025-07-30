import re
from typing import List, Dict
from src.user_sim.handlers.pdf_parser_module import pdf_processor
from src.user_sim.handlers.image_recognition_module import image_description
from src.user_sim.handlers.html_parser_module import webpage_reader


def classify_links(message: str) -> Dict[str, List[str]]:
    url_pattern = re.compile(r'https?://\S+')  # Capture URLs
    links = url_pattern.findall(message)

    classified_links = {
        "images": [],
        "pdfs": [],
        "webpages": []
    }

    for link in links:
        if re.search(r'\.(jpg|jpeg|png|gif|webp|bmp|tiff)$', link, re.IGNORECASE) or '<image>' in message:
            clean_link = re.sub(r'</?image>', '', link)
            classified_links["images"].append(clean_link)
        elif re.search(r'\.pdf$', link, re.IGNORECASE) or 'application/pdf' in message:
            classified_links["pdfs"].append(link)
        else:
            classified_links["webpages"].append(link)

    return classified_links


def process_with_llm(link: str, category) -> str:

    if category == "pdfs":
        description = pdf_processor(link)
        message_replacement = f"{link} {description}"
        return message_replacement

    elif category == "images":
        description = image_description(link, detailed=True)
        message_replacement = f"{link} {description}"
        return message_replacement
    else:
        description = webpage_reader(link)
        message_replacement = f"{link} {description}"
        return message_replacement


def get_content(message: str) -> str:
    classified_links = classify_links(message)
    for category in classified_links:
        for link in classified_links[category]:
            description = process_with_llm(link, category)
            message = message.replace(link, description)

    return message


# def clean_temp_files():
#     clear_pdf_register()
#     clear_image_register()
#     clear_webpage_register()
