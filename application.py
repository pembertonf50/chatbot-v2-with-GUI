from flask import Flask, render_template, request
from chatbot_script import ChatBot

application = Flask(__name__)


chatbot = ChatBot()
chats = []
chats_counter = 0
even_odd = 0
refresh = False

@application.route("/", methods=["GET", "POST"])
def main():
    global chatbot, even_odd, chats_counter, refresh

    if request.method == "POST":
        user_input = request.form["user_input"]
        chats.append([user_input, "green"])
        chatbot.user_response = user_input



        if not chatbot.intro_complete:
            chatbot.intro(even_odd % 2)
            if chatbot.name == "exiting":
                chats.append([chatbot.chatbot_response, "exiting"])
                chatbot = ChatBot()
                even_odd = 0
                refresh = True

            elif not chatbot.name:
                even_odd += 1
            else:
                chatbot.intro_complete = True


        elif not chatbot.first_question_complete:
            chatbot.first_question(chatbot.user_response)
            if chatbot.name == "exiting":
                chats.append([chatbot.chatbot_response, "exiting"])
                chatbot = ChatBot()
                even_odd = 0
                refresh = True
            elif chatbot.chatbot_response[0] == "O":
                chatbot.first_question_complete = True


        elif not chatbot.second_question_complete:
            chatbot.second_question()
            if chatbot.name == "exiting":
                chats.append([chatbot.chatbot_response, "exiting"])
                chatbot = ChatBot()
                even_odd = 0
                refresh = True
            elif type(chatbot.chatbot_response) is list:
                chatbot.chatbot_response = chatbot.chatbot_response[0]
            else:
                chatbot.second_question_complete = True

        else:
            chats_counter += 1
            chatbot.chat(chatbot.user_response)
            if chatbot.name == "exiting":
                chats.append([chatbot.chatbot_response, "exiting"])
                chatbot = ChatBot()
                even_odd = 0
                refresh = True

        if not refresh:
            chats.append([chatbot.chatbot_response, "pink"])
        if chatbot.second_question_complete and chats_counter > 0:
            chats.append(["What else do you like?", "pink"])

    elif request.method == "GET" and refresh:
        chats.clear()
        chats.append([chatbot.chatbot_response, "pink"])
        refresh = False

    else:
        chats.append([chatbot.chatbot_response, "pink"])

    return render_template("webpage.html", template_chat_list=chats)

if __name__ == '__main__':
    application.debug = True
    application.run()

