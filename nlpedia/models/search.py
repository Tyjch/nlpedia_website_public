# coding=utf-8
from nlpedia.models import graph


def get_facts_by_title(title):
    query = '''
        MATCH (fact:Fact)
        WHERE fact.title = {title}
        RETURN fact
        '''
    return graph.run(query, title=title)

def get_facts_by_tag(tag):
    query = '''
        MATCH (fact:Fact)<-[:TAGGED]-(t:Tag)
        WHERE t.name = {tag}
        RETURN fact
        '''
    return graph.run(query, tag=tag)

def get_facts_by_text(text):
    query = '''
        MATCH (fact:Fact)
        WHERE fact.text CONTAINS {text}
        RETURN fact
        '''
    return graph.run(query, text=text)

def get_questions_by_title(title):
    query = '''
        MATCH (question:Question)
        WHERE question.title = {title}
        RETURN question
        '''
    return graph.run(query, title=title)

def get_questions_by_tag(tag):
    query = '''
        MATCH (question:Question)<-[:TAGGED]-(t:Tag)
        WHERE t.name = {tag}
        RETURN question
        '''
    return graph.run(query, tag=tag)

def get_questions_by_text(text):
    query = '''
        MATCH (question:Question)
        WHERE question.text CONTAINS {text}
        RETURN question
        '''
    return graph.run(query, text=text)