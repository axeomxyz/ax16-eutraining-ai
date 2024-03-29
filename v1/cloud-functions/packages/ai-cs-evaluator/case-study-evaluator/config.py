from prompt_message import fetch_prompt_message


class Settings:
    # Retrying Mechanism
    API_TRIES = 3
    API_BACKOFF = 2
    # OpenAI Environment Variables
    TIMEOUT = 90
    REQUEST_TIMEOUT = 180
    OPENAI_API_KEY = " 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"
    GPT_MODEL = "gpt3.5"
    # Prompt Messages
    BASE_MESSAGE = fetch_prompt_message("prompts/BASE_MESSAGE.txt")
    OVERALL_SCORE_SUMMARY_MESSAGE = BASE_MESSAGE + fetch_prompt_message("prompts/OVERALL_SCORE_SUMMARY_MESSAGE.txt")
    COMMUNICATION_SCORE_SUMMARY_MESSAGE = BASE_MESSAGE + fetch_prompt_message(
        "prompts/COMMUNICATION_SCORE_SUMMARY_MESSAGE.txt")
    TIPS_ERRORS_MESSAGE = BASE_MESSAGE + fetch_prompt_message("prompts/TIPS_ERRORS_MESSAGE.txt")
    OVERALL_SCORE_MESSAGE = BASE_MESSAGE + fetch_prompt_message("prompts/OVERALL_SCORE_MESSAGE.txt")
    OVERALL_SUMMARY_MESSAGE = BASE_MESSAGE + fetch_prompt_message("prompts/OVERALL_SUMMARY_MESSAGE.txt")
    COMMUNICATION_SCORE_MESSAGE = BASE_MESSAGE + fetch_prompt_message("prompts/COMMUNICATION_SCORE_MESSAGE.txt")
    COMMUNICATION_SUMMARY_MESSAGE = BASE_MESSAGE + fetch_prompt_message("prompts/COMMUNICATION_SUMMARY_MESSAGE.txt")
    SUMMARY_MESSAGE = fetch_prompt_message("prompts/SUMMARY_MESSAGE.txt")


settings = Settings()
