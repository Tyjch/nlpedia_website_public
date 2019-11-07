# coding=utf-8
from nlpedia.models import graph
from nlpedia.models.time import date, timestamp
from py2neo import Relationship


def get_todays_recent_facts():
    query = '''
        MATCH (user:User)-[:PUBLISHED]->(fact:Fact)<-[:TAGGED]-(tag:Tag)
        WHERE fact.date = {today}
        RETURN user.username AS username, fact, COLLECT(tag.name) AS tags
        ORDER BY fact.timestamp DESC LIMIT 5
        '''
    return graph.run(query, today=date())

def get_todays_recent_questions():
    query = '''
        MATCH (user:User)-[:PUBLISHED]->(question:Question)<-[:TAGGED]-(tag:Tag)
        WHERE question.date = {today}
        RETURN user.username AS username, question, COLLECT(tag.name) AS tags
        ORDER BY question.timestamp DESC LIMIT 5
        '''
    return graph.run(query, today=date())

def get_fact_from_id(fact_id):
    query = '''
    MATCH (fact:Fact)
    WHERE fact.id = {fact_id}
    RETURN fact
    '''
    return graph.run(query, fact_id=fact_id)

def get_question_from_id(question_id):
    query = '''
        MATCH (question:Question)
        WHERE question.id = {question_id}
        RETURN question
        '''
    return graph.run(query, question_id=question_id)

def get_node_from_id(primary_label, node_id):
    query = f'''
        MATCH (node:{primary_label})
        WHERE node.id = '{node_id}'
        RETURN node
        '''
    return graph.run(query) #, primary_label=primary_label, node_id=node_id)

def get_fact_tags_from_id(fact_id):
    query = '''
            MATCH (fact:Fact)<-[:TAGGED]-(tag:Tag)
            WHERE fact.id = {fact_id}
            RETURN COLLECT(tag.name) AS tags
            '''
    return graph.run(query, fact_id=fact_id)

def get_question_tags_from_id(question_id):
    query = '''
            MATCH (question:Question)<-[:TAGGED]-(tag:Tag)
            WHERE question.id = {question_id}
            RETURN COLLECT(tag.name) AS tags
            '''
    return graph.run(query, question_id=question_id)

# For Py2neo v4
'''
def connect_nodes(id1, label1, id2, label2):
    node1 = graph.nodes.match(label1, id=id1).first()
    node1.__primarylabel__ = label1
    node1.__primarykey__ = 'id'

    node2 = graph.nodes.match(label2, id=id2).first()
    node2.__primarylabel__ = label2
    node2.__primarykey__ = 'id'

    RELATED_TO = Relationship.type('RELATED_TO')

    graph.merge(RELATED_TO(node1, node2))
'''

# For Py2neo v3
def connect_nodes(id1, label1, id2, label2):
    node1 = graph.find_one(label1, 'id', id1)
    node1.__primarylabel__ = label1
    node1.__primarykey__ = 'id'

    node2 = graph.find_one(label2, 'id', id2)
    node2.__primarylabel__ = label2
    node2.__primarykey__ = 'id'

    graph.merge(Relationship(node1, 'RELATED_TO', node2))

def get_related_facts(primary_label, node_id):
    query = f'''
        MATCH (node:{primary_label})-[:RELATED_TO]-(fact:Fact)
        WHERE node.id = '{node_id}'
        RETURN fact
        ORDER BY fact.timestamp DESC LIMIT 5
        '''
    return graph.run(query)

def get_related_questions(primary_label, node_id):
    query = f'''
        MATCH (node:{primary_label})-[:RELATED_TO]-(question:Question)
        WHERE node.id = '{node_id}'
        RETURN question
        ORDER BY question.timestamp DESC LIMIT 5
        '''
    return graph.run(query)