from gpt_calls import generate_section_gpt, generate_summary_gpt
from models.models import CommunicationsExamInfo
from utils import read_docx, case_study_extract, fetch_prompt_message
from gpt_calls import generate_candidate_task_gpt, extract_point_of_views_gpt, extract_target_audience_gpt
from config import settings

import re
from enum import Enum

class Sections(Enum):
    OBSERVATIONS = "Key observations"
    GRAMMAR = "Grammar errors"
    TIPS = "Key tips to improve"


def generate_full_text(candidate_response: str, exam_doc_path: str, perfect_response: str = "") -> str:
    """Generates the evaluation text and the summary text"""

    # get abbrev and candidate task -> get_exam_info(exam_doc_path)
    exam_info = get_exam_info(exam_doc_path)

    # add abbreviations of the candidate
    add_candidate_abbreviations(candidate_response, exam_info)
 
    # generate evaluation text
    evaluation_text = generate_evaluation_text(candidate_response, exam_info, perfect_response)

    # generate summary text
    summary_text = generate_summary_gpt(evaluation_text)

    return evaluation_text, summary_text


def generate_evaluation_text(candidate_response: str, exam_info: CommunicationsExamInfo, perfect_response: str = ""):
    """Generates all sections of the evaluation text"""

    text_until_now = ""

    # 1. Generate observations section
    OBSERVATIONS_GUIDELLINE: str = fetch_prompt_message(settings.OBSERVATIONS_GUIDELLINE_PATH)

    observations = generate_section_gpt(
        Sections.OBSERVATIONS.value, candidate_response, exam_info, text_until_now, OBSERVATIONS_GUIDELLINE, perfect_response
    )

    text_until_now = observations + "\n\n"

    # 2. Generate grammar section
    GRAMMAR_GUIDELINE: str = fetch_prompt_message(settings.GRAMMAR_GUIDELINE_PATH)

    grammar = generate_section_gpt(
        Sections.GRAMMAR.value, candidate_response, exam_info, text_until_now, GRAMMAR_GUIDELINE, perfect_response
    )

    text_until_now = text_until_now + grammar + "\n\n"

    # 3. Generate tips section
    TIPS_GUIDELINE: str = fetch_prompt_message(settings.TIPS_GUIDELINE_PATH)

    tips = generate_section_gpt(
        Sections.TIPS.value, candidate_response, exam_info, text_until_now, TIPS_GUIDELINE, perfect_response
    )

    text_until_now = text_until_now + tips + "\n\n"

    # Add titles just for testing
    #observations = "Observations\n" + observations
    #grammar = "Grammar\n" + grammar
    #tips = "Tips\n" + tips
    
    return text_until_now

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
