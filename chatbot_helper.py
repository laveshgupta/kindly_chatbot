import json
from flask import current_app, session
from flask import request as frequest
from constants import Constants
import uuid
import random

class ChatBotHelper:

    @staticmethod
    def create_response(res_body: str, res_code: int=200):
        """
        Function to create response for request
        """
        output = res_body
        mime_type = 'text/plain'
        separators = (", ", ": ")
        try: #if json dumps is successful then mimetype is changed to json.
            output = json.dumps(res_body, indent=4, separators=separators)
            mime_type = 'application/json'
        except Exception as e:
            logger.warning("Error in json dumps. Hence creating message as plain text.")
        return current_app.response_class(
            response=output,
            status=res_code,
            mimetype=mime_type
        )


    @staticmethod
    def generate_userid():
        return(str(uuid.uuid4()))

    @staticmethod
    def validate_request(conv_type: str):
        """
        Function which validates the input
        for conv_type: start, it returns language
        for conv_type:: meesage, it return user_id and message
        """
        parameters_not_present = []
        return_dict = None
        request_data = {}
        if frequest.args:
            request_data = frequest.args
        elif frequest.form:
            request_data = frequest.form
        elif frequest.json:
            request_data = frequest.json
        else:
            request_data = json.loads(frequest.data)

        if conv_type == 'start':
            language = request_data.get('language')
            if not language:
                parameters_not_present.append('language')
            if not parameters_not_present:
                if language not in Constants.LANGUAGES.keys():
                    return ChatBotHelper.create_response(
                        res_body=f"Request cannot be processed as wrong language {language} is passed",
                        res_code=400
                    )
                return_dict = {'language': language}
        elif conv_type == 'message':
            user_id = request_data.get('user_id')
            message = request_data.get('message')
            if not user_id:
                parameters_not_present.append('user_id')
            if not message:
                parameters_not_present.append('message')
            if not parameters_not_present:
                if 'user_id' not in session:
                    return ChatBotHelper.create_response(
                        res_body=f"User Id has not been set in server.Please start your conversation again",
                        res_code=400
                    )
                if session['user_id'] != user_id:
                    return ChatBotHelper.create_response(
                        res_body=f"Wrong user_id: {user_id} passed in request",
                        res_code=400
                    )
                return_dict = {'user_id': user_id, 'message': message}

        if parameters_not_present:
            return ChatBotHelper.create_response(
                res_body=f"Request cannot be processed as these parameters {parameters_not_present} are not passed",
                res_code=400
            )
        return return_dict


    @staticmethod
    def get_greeting(language):
        greetings = knowledge_dict.get('greetings')[0]
        id = greetings.get('id')
        replies = greetings.get('replies')[language]
        reply = random.choice(replies)
        return id, reply


    @staticmethod
    def get_fallback(language):
        fallbacks = knowledge_dict.get('fallbacks')[0]
        id = fallbacks.get('id')
        replies = fallbacks.get('replies')[language]
        reply = random.choice(replies)
        return id, reply


    @staticmethod
    def get_reply(question, language, prev_reply_id):
        logger.debug(f"Searching for '{question}' in knowledge base")
        string_to_search = question.lower()
        samples = knowledge_dict.get('samples')

        matched_ids = samples[language].get(string_to_search)

        if not matched_ids:
            keywords = knowledge_dict.get('keywords')
            matched_ids = keywords[language].get(string_to_search)
            if not matched_ids:
                kw_search = string_to_search.split(' ')
                prev_matched_ids = None
                i = 0
                while i < len(kw_search) and not matched_ids:
                    matched_ids = keywords[language].get(kw_search[i])
                    i += 1
                if matched_ids:
                    j = i + 1
                    i -= 1
                    prev_matched_ids = matched_ids

                    while j < len(kw_search) + 1:
                        str1 = ' '.join(kw_search[i:j])
                        matched_ids = keywords[language].get(str1)
                        if prev_matched_ids and not matched_ids:
                            break
                        prev_matched_ids = matched_ids
                        j += 1
                    matched_ids = prev_matched_ids

        return_parent_match_id = None
        none_parent_match_ids = []
        if matched_ids:
            for match_id in matched_ids:
                id = match_id['id']
                parent_id = match_id['parent_id']
                if prev_reply_id == parent_id:
                    return_parent_match_id = id
                    break
                if parent_id is None:
                    none_parent_match_ids.append(id)

        logger.debug(f"\n\n MATCHED_IDS: {matched_ids}")
        logger.debug(f" return_parent_match_id: {return_parent_match_id}")
        logger.debug(f" none_parent_match_ids: {none_parent_match_ids}")

        replies_dict = knowledge_dict.get('replies')
        if return_parent_match_id:
            replies = replies_dict.get(return_parent_match_id)[language]
            reply = random.choice(replies)
            logger.debug(f" RETURN_PARENT_MATCHED_ID: {return_parent_match_id}      reply: {reply}")
            return return_parent_match_id, reply
        else:
            if none_parent_match_ids:
                reply_id = random.choice(none_parent_match_ids)
                replies = replies_dict.get(reply_id)[language]
                reply = random.choice(replies)
                logger.debug(f" REPLY_ID: {reply_id}      reply: {reply}")
                return reply_id, reply
        return None, None


    @staticmethod
    def create_data_structures():
        logger.info("Creating data structures")
        with open(config.get('chatbot_knowledge_file'), 'r') as f:
            knowledge_file_content = json.load(f)

        dialogues_content = knowledge_file_content.get('dialogues')

        keywords_dict = {}
        samples_dict = {}
        replies_dict = {}
        for dialogue in dialogues_content:
            id = dialogue['id']
            parent_id = dialogue.get('parent_id')
            dialogue_type = dialogue.get('dialogue_type')
            id_dict = {'id': id, 'parent_id': parent_id}

            if dialogue_type == 'SAMPLES':
                # print(f"dialogue.get(dialogue_type.lower()).keys(): {dialogue.get(dialogue_type.lower()).keys()}")
                languages = dialogue.get(dialogue_type.lower()).keys()
                for language in languages:
                    if language not in samples_dict:
                        samples_dict[language] = {}
                    samples = dialogue.get(dialogue_type.lower())[language]
                    for sample in samples:
                        sample = sample.lower()
                        if sample not in samples_dict[language]:
                            samples_dict[language][sample.lower()] = []
                        samples_dict[language][sample.lower()].append(id_dict)

            if dialogue_type == 'KEYWORDS':
                languages = dialogue.get(dialogue_type.lower()).keys()
                for language in languages:
                    if language not in keywords_dict:
                        keywords_dict[language] = {}
                    keywords = dialogue.get(dialogue_type.lower())[language]
                    for keyword in keywords:
                        kws = keyword.split(' ')
                        for i in range(1, len(kws)+1):
                            str1 = ' '.join(kws[0: i]).lower()
                            if str1 not in keywords_dict[language]:
                                keywords_dict[language][str1] = []
                            keywords_dict[language][str1].append(id_dict)

            replies_dict[id] = dialogue.get('replies')


        greetings_dict = knowledge_file_content.get('greetings')
        fallbacks_dict = knowledge_file_content.get('fallbacks')
        knowledge_dict = {
            'greetings': greetings_dict,
            'fallbacks': fallbacks_dict,
            'samples': samples_dict,
            'keywords': keywords_dict,
            'replies': replies_dict
        }
        logger.info("Done creating data structures")
        return knowledge_dict
