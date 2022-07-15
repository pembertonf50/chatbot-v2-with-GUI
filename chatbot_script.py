from scipy.spatial.distance import cosine
from chatbot_responses import responses
from chatbot_functions import preprocess, compare_overlap, \
    extract_nouns, nlp, \
    handle_initial_message, make_exit, question1, \
    question2, pos_tag


class ChatBot:
    name = None
    intro_complete = False
    first_question_complete = False
    answer1_clarification = False
    second_question_complete = False

    chatbot_response = """
    Hello there! My name is Program Buddy.
    What is your name?
    (if at any point you wish to leave please type 'exit')
    """
    user_response = None

    def intro(self, even_odd):
        self.name, self.chatbot_response = handle_initial_message(self.user_response, even_odd)

    def first_question(self, user_message):
        if make_exit(self.name, user_message):
            self.chatbot_response = make_exit(self.name, user_message)
            self.name = "exiting"
        else:
            answer1 = question1(user_message, self.answer1_clarification)

            if type(answer1) is list:
                self.chatbot_response = answer1[0]
                self.answer1_clarification = True
            else:
                self.chatbot_response = "Oh nice! How long have you been studying {}?".format(answer1)



    def second_question(self):
        if make_exit(self.name, self.user_response):
            self.chatbot_response = make_exit(self.name, self.user_response)
            self.name = "exiting"
        else:
            answer2 = question2(self.user_response)
            if type(answer2) is list:
                self.chatbot_response = answer2
            else:
                self.chatbot_response = f"""{answer2}, that's pretty solid.
I have most experience in Python but also things such as Java, C++, Command line, SQL and Git.
Do you know any of these?"""



    def chat(self, user_message):
        if make_exit(self.name, user_message):
            self.chatbot_response = make_exit(self.name, user_message)
            self.name = "exiting"
        else:
            self.chatbot_response = self.respond(user_message)

    def find_intent_match(self, responses, user_message):
        bow_user_message = set(preprocess(user_message))
        processed_responses = [set(preprocess(j)) for i, j, k in responses]
        similarity_list = [compare_overlap(bow_user_message, response) for response in processed_responses]
        response_index = similarity_list.index(max(similarity_list))
        return responses[response_index][2], response_index

    def find_entities(self, user_message, index):
        tagged_user_message = pos_tag(preprocess(user_message))
        message_nouns = extract_nouns(tagged_user_message)
        message_nouns_vectors = [nlp(noun).vector for noun in message_nouns]
        topic = responses[index][0]
        topic_vector = nlp(topic).vector
        best_match = ""
        closest_vector = 1
        for i, vector in enumerate(message_nouns_vectors):
            a = cosine(vector, topic_vector)
            if a < closest_vector:
                closest_vector = a
                best_match = message_nouns[i]
        return best_match

    def respond(self, user_message):
        best_response, best_response_index = self.find_intent_match(responses, user_message)
        entity = self.find_entities(user_message, best_response_index)
        return best_response.format(entity)
