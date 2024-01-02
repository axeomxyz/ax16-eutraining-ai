from gpt_calls import generate_section_gpt, generate_summary_gpt
from models.models import CommunicationsExamInfo
from utils import read_docx, case_study_extract, fetch_prompt_message
from gpt_calls import generate_candidate_task_gpt, extract_point_of_views_gpt, extract_target_audience_gpt, post_process_subsections_gpt, improve_section_gpt
from config import settings

import re
from enum import Enum

class Sections(Enum):
    #OBSERVATIONS = "Key observations"
    CONVEYS_INFO = "Conveys Information and Opinions Clearly and Concisely"
    TAILORS_MESSAGE = "Tailors the message to respond to the needs of the person or persons with which they communicate"
    ARGUMENTS = "Uses Convincing Arguments and Solid Reasoning"
    POINT_OF_VIEWS = "Takes into Account the Point of View of Others"
    GRAMMAR = "Grammar errors"
    TIPS = "Key tips to improve"


def generate_full_text(candidate_response: str, exam_doc_path: str, perfect_response: str = "") -> str:
    """Generates the evaluation text and the summary text"""
    print("hh")
    # get abbrev and candidate task -> get_exam_info(exam_doc_path)
    exam_info = get_exam_info(exam_doc_path)

    # add abbreviations of the candidate
    add_candidate_abbreviations(candidate_response, exam_info)
 
    # generate evaluation text
    observations, grammar, tips = generate_evaluation_text(candidate_response, exam_info, perfect_response)


    observations = improve_section_gpt(observations)
    #grammar = improve_section_gpt(grammar)
    #tips = improve_section_gpt(tips)

    evaluation_text = observations + "\n\n" + grammar + "\n\n" + tips
    
    # generate summary text
    summary_text = generate_summary_gpt(evaluation_text)

    return evaluation_text, summary_text


def generate_evaluation_text(candidate_response: str, exam_info: CommunicationsExamInfo, perfect_response: str = ""):
    """Generates all sections of the evaluation text"""

    text_until_now = ""

    # 1. Generate observations section
    
    #OBSERVATIONS_GUIDELLINE: str = fetch_prompt_message(settings.OBSERVATIONS_GUIDELLINE_PATH)
    CONEYS_INFO_GUIDELINE: str = fetch_prompt_message(settings.CONVEYS_INFO_PATH)

    conveys_info = generate_section_gpt(
        Sections.CONVEYS_INFO.value, candidate_response, exam_info, text_until_now, CONEYS_INFO_GUIDELINE, perfect_response
    )

    final_conveys_info = post_process_subsections_gpt(conveys_info)    

    text_until_now = Sections.CONVEYS_INFO.value + ":\n" + final_conveys_info + "\n\n"

    TAILORS_MESSAGE_GUIDELINE: str = fetch_prompt_message(settings.TAILORS_MESSAGE_PATH)

    tailors_mess = generate_section_gpt(
        Sections.TAILORS_MESSAGE.value, candidate_response, exam_info, text_until_now, TAILORS_MESSAGE_GUIDELINE, perfect_response
    )

    final_tailors_mess = post_process_subsections_gpt(tailors_mess)

    text_until_now += Sections.TAILORS_MESSAGE.value + ":\n" + final_tailors_mess + "\n\n"

    ARGUMENTS_GUIDELINE: str = fetch_prompt_message(settings.CONVICING_ARGUMENTS_PATH)

    arguments = generate_section_gpt(
        Sections.ARGUMENTS.value, candidate_response, exam_info, text_until_now, ARGUMENTS_GUIDELINE, perfect_response
    )

    final_arguments = post_process_subsections_gpt(arguments)

    text_until_now += Sections.ARGUMENTS.value + ":\n" + final_arguments + "\n\n"

    POINTS_OF_VIEW_GUIDELINE: str = fetch_prompt_message(settings.POINTS_OF_VIEW_PATH)

    points_of_view = generate_section_gpt(
        Sections.POINT_OF_VIEWS.value, candidate_response, exam_info, text_until_now, POINTS_OF_VIEW_GUIDELINE, perfect_response
    )

    final_points_of_view = post_process_subsections_gpt(points_of_view)

    text_until_now += Sections.POINT_OF_VIEWS.value + ":\n" + final_points_of_view + "\n\n"

    observations = text_until_now

    # 2. Generate grammar section
    GRAMMAR_GUIDELINE: str = fetch_prompt_message(settings.GRAMMAR_GUIDELINE_PATH)

    grammar = generate_section_gpt(
        Sections.GRAMMAR.value, candidate_response, exam_info, text_until_now, GRAMMAR_GUIDELINE, perfect_response
    )

    final_grammar = post_process_subsections_gpt(grammar)

    text_until_now += final_grammar + "\n\n"

    # 3. Generate tips section
    TIPS_GUIDELINE: str = fetch_prompt_message(settings.TIPS_GUIDELINE_PATH)

    tips = generate_section_gpt(
        Sections.TIPS.value, candidate_response, exam_info, text_until_now, TIPS_GUIDELINE, perfect_response
    )

    final_tips = post_process_subsections_gpt(tips)

    #text_until_now += final_tips + "\n\n"

    # Add titles just for testing
    #observations = "Observations\n" + observations
    #grammar = "Grammar\n" + grammar
    #tips = "Tips\n" + tips
    
    return observations, grammar, tips

def add_candidate_abbreviations(cadidate_response, exam_info):
    pattern = r'\(([A-Z]{2,})\)\s*([\w\s]+)|([\w\s]+)\s*\(([A-Z]{2,})\)'

    # Search for all matches
    matches = re.findall(pattern, cadidate_response)

    # Create a dictionary to store the acronyms and their explanations
    acronyms_and_explanations = {}

    for match in matches:
        if match[0]:  # Acronyms followed by explanation
            acronyms_and_explanations[match[0]] = match[1].strip()
        else:  # Explanation followed by acronyms
            acronyms_and_explanations[match[3]] = match[2].strip()

    # Convert the dictionary of acronyms into a string
    acronyms_str = '\n'.join([f'{acronym}: {explanation}\n' for acronym, explanation in acronyms_and_explanations.items()])

    # Concatenate with exam_info.abbreviations
    exam_info.abbreviations += "\n" + acronyms_str

def get_exam_info(case_study_path: str) -> CommunicationsExamInfo:
    """Get all the info from the exam document"""

    # leer el examen de un path local
    case_study_info = read_docx(case_study_path)
    candidate_task, abbreviations, email, content = case_study_extract(case_study_info)

    #Not complete info without content
    candidate_task = generate_candidate_task_gpt(candidate_task + abbreviations + email)
    summary = generate_summary_gpt(content)
    point_of_views = extract_point_of_views_gpt(abbreviations + content)
    target_audience = extract_target_audience_gpt(candidate_task + abbreviations + email)

    return CommunicationsExamInfo(
        summary_text=summary,
        abbreviations=abbreviations,
        points_of_view=point_of_views,
        target_audience=target_audience,
        candidate_task=candidate_task,
    )
