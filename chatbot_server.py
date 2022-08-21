from flask import Flask, session, request, g, current_app, json, make_response, jsonify, Response
from constants import Constants
from logger import Logger
from config import Config
import secrets
from chatbot_helper import ChatBotHelper as cbh

class ChatBotServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = secrets.token_bytes(32)

        self.create_routes()

    def server_run(self):
        """
        Starting flask server
        """
        flask_config = config.get('flask', {})
        flask_host = flask_config.get('host', Constants.APP_HOST)
        flask_port = flask_config.get('port', Constants.APP_PORT)
        self.app.run(
            host=flask_host,
            port=flask_port,
            debug=True
        )

    def create_routes(self):
        """
        Create routes in application
        """
        @self.app.route('/api/conversation/<conv_type>', methods=['POST'])
        def conversation(conv_type):
            chatbot_params = cbh.validate_request(conv_type=conv_type)
            if isinstance(chatbot_params, Response):
                return chatbot_params

            if conv_type == 'start':
                if 'user_id' not in session:
                    user_id = cbh.generate_userid()
                    session['user_id'] = user_id
                else:
                    user_id = session.get('user_id')
                language = chatbot_params.get('language')
                session['language'] = language
                id, reply = cbh.get_greeting(language)
                session['id'] = id

                response_dict = {'user_id': user_id, 'message': reply}
                response_obj = cbh.create_response(res_body=response_dict, res_code=200)
                return response_obj
            elif conv_type == 'message':
                user_id = chatbot_params.get('user_id')
                message = chatbot_params.get('message')
                language = session.get('language')
                id = session.get('id')
    
                reply_id, reply = cbh.get_reply(question=message, language=language, prev_reply_id=id)
                if not reply_id and not reply:
                    reply_id, reply = cbh.get_fallback(language=language)

                session['id'] = reply_id
                response_dict = {'message': reply}
                response_obj = cbh.create_response(res_body=response_dict, res_code=200)
                return response_obj



if __name__ == '__main__':
    config = Config()
    __builtins__.config = config
    logger = Logger()
    __builtins__.logger = logger
    knowledge_dict = cbh.create_data_structures()
    __builtins__.knowledge_dict = knowledge_dict
    cbs = ChatBotServer()
    cbs.server_run()
