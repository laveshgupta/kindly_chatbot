import logging

class Constants:
    APP_CONFIG_FILE_PATH = 'chatbot_config.json'
    LOG_LEVEL = 'DEBUG'
    LOGGING_LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    LOG_FILE = 'chatbot.log'
    APP_HOST = '0.0.0.0'
    APP_PORT = 80
    LANGUAGES = {
        'en': 'English',
        'nb': 'Norsk'
    }
    CHATBOT_KNOWLEDGE_FILE = 'kindly-bot.json'
    INTEGRATION_TESTS_CASES_FILE = 'ratestask_integration_tests.json'
    
