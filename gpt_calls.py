from apis.gpt_api import call_gpt_api
import openai

def generate_section_gpt(
    section: str,
    candidate_response: str,
    exam_info: CommunicationsExamInfo,
    text_until_now: str,
    guideline: str
) -> str:
    """Generates a specific evaluation section"""

    SYSTEM_MESSAGES: str = fetch_prompt_message(settings.SYSTEM_MESSAGES_PATH)

    PROMPT_TEMPLATES: str = fetch_prompt_message(settings.PROMPT_TEMPLATES_PATH)

    GENERAL_MESSAGES: str = fetch_prompt_message(settings.GENERAL_MESSAGE_PATH)

    EVALUATION_STRUCTURE: str = fetch_prompt_message(settings.EVALUATION_STRUCTURE_PATH)

    #EXAM_INFO: str = fetch_prompt_message(settings.EXAM_INFO_PATH)

    TASKS: str = fetch_prompt_message(settings.TASKS_PATH)

    WORKFLOW: str = fetch_prompt_message(settings.WORKFLOW_PATH)

    EXAM_INFO: str = fetch_prompt_message(settings.EXAM_INFO_PATH)

    prompt = PROMPT_TEMPLATES

    # region Add the exam info to prompt
    exam_info_filled = exam_info.replace("{exam_summary}", exam_info.summary_text)
    exam_info_filled = exam_info.replace("{point_of_views}", exam_info.points_of_view)
    exam_info_filled = exam_info.replace("{target_audience}", exam_info.target_audience)
    exam_info_filled = exam_info.replace("{candidate_task}", exam_info.candidate_task)
    # endregion
    
    prompt = prompt.replace("{general_message}", GENERAL_MESSAGES)
    prompt = prompt.replace("{evaluation_structure}", EVALUATION_STRUCTURE)
    prompt = prompt.replace("{workflow}", WORKFLOW)
    prompt = prompt.replace("{task}", TASKS)
    prompt = prompt.replace("{exam_info}", exam_info_filled)
    prompt = prompt.replace("{abbreviations}", exam_info.abbreviations)
    prompt = prompt.replace("{candidate_response}", candidate_response)
    prompt = prompt.replace("{evaluation_until_now}", text_until_now)
    prompt = prompt.replace("{guideline}", guideline)
    #prompt = prompt.replace("{user_feedback}", USER_FEEDBACK)

    # Set the actual section name
    prompt = prompt.replace("{section}", section)

    section_text = call_gpt_api(SYSTEM_MESSAGES, prompt)

    return section_text

def generate_summary_gpt(evaluation_text: str) -> str:
    """Generates the summary text"""

    SUMMARY: str = fetch_prompt_message(settings.SUMMARY_PATH)

    prompt = SUMMARY
    prompt = prompt.replace("{evaluation_text}", evaluation_text)

    summary_text = call_gpt_api(prompt)

    return summary_text