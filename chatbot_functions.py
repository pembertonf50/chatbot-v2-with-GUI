import re
import os
path = r'{}'.format(os.getcwd())+r'/nltk_data'
path2 = r'{}'.format(os.getcwd())+r'\nltk_data'
import spacy
from random import randint
import nltk
nltk.data.path.append(path)
nltk.data.path.append(path2)
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer



nlp = spacy.load("en_core_web_md")
lemmatizer = WordNetLemmatizer()


def make_exit(name, user_message):
    exit_commands = ("quit", "goodbye", "exit", " bored", "to leave", "to go", "bye")

    exit_responses = ("Talk to you later {}!", "It's been nice getting to know you {}",
                      "Hopefully hear from you soon",
                      "Feel free to come back if you have anymore questions",
                      "Always here when you need me {}",
                      "Nice chatting, all the best {}")

    for exit_command in exit_commands:
        if exit_command in user_message.lower():
            exit_response_index = randint(0, len(exit_responses) - 1)
            chatbot_response = exit_responses[exit_response_index].format(name)
            return chatbot_response


def handle_initial_message(message, even_odd):
    a = r"name is ([a-zA-Z-']+( |\.)?([a-zA-Z-']+)?)"
    b = r"called ([a-zA-Z-']+( |\.)?([a-zA-Z-']+)?)"
    c = r"^([a-zA-Z-']+( |\.)?([a-zA-Z-']+)?)\.?$"
    abc = [a, b, c]
    name = ""
    i = 0
    while len(name) == 0:
        if make_exit(name, message):
            return "exiting", make_exit(name, message)

        elif i == 3:
            clarification_messages = ("I don't know what to call you :)\nPlease simplify\n",
                                      "I'm really sorry please can you retry.\nIf you type\
                                       just your firstname this should work.")
            chatbot_response = clarification_messages[even_odd]

            return None, chatbot_response


        elif re.search(abc[i], message.lower()):
            name = re.search(abc[i], message.lower()).group(1)
            break

        else:
            i += 1
    chatbot_response = f"""Great to be talking with you {name.title()} :)
Like I said earlier, I am Program Buddy and would love to talk with you.
What software skills have you been looking into recently?
"""
    return name.title(), chatbot_response


def question1(user_message, answer1_clarification):

    if answer1_clarification:
        if re.findall(r"[a-zA-Z-']+", user_message):
            entities = re.findall(r"[a-zA-Z-']+", user_message)
            return_entities = ""
            for entity in entities:
                return_entities += entity + ", "
            return_entities = return_entities.strip().strip(",")
            if len(entities) > 1:
                idx = return_entities.rfind(',')
                return_entities = return_entities[:idx] + " and " + return_entities[idx+1:]

            return return_entities

    list_user_message = word_tokenize(user_message)
    pos_user_message = pos_tag(list_user_message)
    answers_re = (r"looking into ([-a-zA-Z ']+)",
                  r"learning ([-a-zA-Z ']+)",
                  r"learnt ([-a-zA-Z ']+)",
                  r"learn ([-a-zA-Z ']+)")
    initial_phrase = ""
    for phrase in answers_re:
        if re.search(phrase, user_message.lower()):
            initial_phrase = re.search(phrase, user_message.lower()).group(1)
            break

    if len(initial_phrase) > 0:
        entities = re.findall(r"[a-z-']+", user_message.lower())
        for word, pos in pos_user_message:
            for entity in entities:
                if (word.lower() == entity) and (not pos[0] == "N"):
                    entities.remove(entity)
        if len(entities) == 1:
            return entities[0]
        elif len(entities) == 2:
            return entities[0] + " and " + entities[1]
        elif len(entities) > 2:
            first_entity = entities[0]
            last_entity = " and " + entities[-1]
            for entity in entities[1:-1]:
                first_entity += ", " + entity
            return_entities = first_entity + last_entity
            return return_entities
    # Keep the above code for now as otherwise larger sentences maybe captured.
    elif len(initial_phrase) == 0:
        entities = ""
        for word, pos in pos_user_message:
            if pos[0] == "N":
                entities += word + ", "
        entities = entities.strip().strip(",")
        double_check_return = [f"""I wasn't too sure what you have been working on but I thought it may be related to these:
        {entities}
        Please comma seperate the topics you've been working on."""]
        return double_check_return




def question2(user_message):
    answers_re = r"(\w+) (weeks|week|days|day|months|month|years|year|hours|hour|minutes|minute)"

    if re.search(answers_re, user_message.lower()):
        full_match = re.search(answers_re, user_message.lower())
        entity = full_match.group(1) + " " + full_match.group(2)
        return entity
    else:
        return ["""I'm sorry I couldn't quite understand how long you've been working for.
        Please may you rephrase."""]



def preprocess(input_sentence):
    input_sentence = input_sentence.lower()
    tokens = word_tokenize(input_sentence)
    pos_tagged_tokens = pos_tag(tokens)

    input_sentence = [lemmatizer.lemmatize(
        i, pos_swap(j)) for i, j in pos_tagged_tokens]
    return input_sentence


def pos_swap(pos):
    if re.search(r'VB.?', pos):
        return 'v'
    elif re.search(r'JJ.?', pos):
        return 'a'
    elif re.search(r'RB.?', pos):
        return 'r'
    else:
        return 'n'


def compare_overlap(user_message, possible_response):
    similar_words = 0
    for token in user_message:
        if token in possible_response:
            similar_words += 1
    return similar_words


def extract_nouns(tagged_message):
    message_nouns = list()
    for token, tag in tagged_message:
        if tag.startswith("N"):
            message_nouns.append(token)
    return message_nouns
