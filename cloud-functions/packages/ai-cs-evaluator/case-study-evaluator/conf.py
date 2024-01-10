from database.db_data import fetch_prompt_message


class Settings:
    # Retrying Mechanism
    API_TRIES = 3
    API_BACKOFF = 2
    # OpenAI Environment Variables
    TEMPERATURE = 0
    TIMEOUT = 90
    REQUEST_TIMEOUT = 180
    OPENAI_API_KEY = " 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"
    GPT_MODEL = "gpt_4_1106" # "gpt_4_1106"
    # Fine-Tuning Variables
    N_EPOCHS = 15

    # Prompt Messages
    GENERAL_TEMPLATE_PATH = "prompts/GENERAL_TEMPLATE.txt"
    SYSTEM_MESSAGES_PATH = "prompts/SYSTEM_MESSAGE.txt"
    GENERAL_MESSAGE_PATH = "prompts/GENERAL_MESSAGE.txt"
    EVALUATION_STRUCTURE_PATH = "prompts/EVALUATION_STRUCTURE.txt"
    EXAM_INFO_PATH = "prompts/EXAM_INFO.txt"
    GRAMMAR_GUIDELINE_PATH = "prompts/GRAMMAR_GUIDELINE.txt"
    OBSERVATIONS_GUIDELLINE_PATH = "prompts/OBSERVATIONS_GUIDELLINE.txt"
    TIPS_GUIDELINE_PATH = "prompts/TIPS_GUIDELINE.txt"
    TASK_PATH = "prompts/TASK.txt"
    WORKFLOW_PATH = "prompts/WORKFLOW.txt"
    SUMMARY_PATH = "prompts/SUMMARY.txt"
    TARGET_AUDIENCE_PATH = "prompts/TARGET_AUDIENCE.txt"
    VIEWS_PATH = "prompts/VIEWS.txt"
    CANDIDATE_TASK_PATH = "prompts/CANDIDATE_TASK.txt"
    USER_FEDDBACK_PATH = "prompts/USER_FEEDBACK.txt"

    # DB Variables
    # DB_PATH = "sqlite:///eutraining.db"


settings = Settings()
