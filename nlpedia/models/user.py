# coding=utf-8
from py2neo import Node, Relationship
from passlib.hash import bcrypt
from nlpedia.models import graph
from nlpedia.models.time import date, timestamp
from nlpedia.models.content import get_fact_from_id, get_question_from_id, get_node_from_id
import uuid


class User:

    def __init__(self, username):
        self.username = username

    # For Py2neo v3
    def find(self):
        user = graph.find_one("User", "username", self.username)
        return user

    # For Py2neo v4
    '''
    def find(self):
        user = graph.nodes.match("User", username=self.username).first()
        return user
    '''

    # AUTHORIZATION ====================================================================================================

    def register(self, password, role='Student'):

        if not self.find():
            user = Node(
                'User',
                role,
                username=self.username,
                password=bcrypt.encrypt(password)
            )
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    # FACTS ============================================================================================================

    def add_fact(self, title, tags, text):
        user = self.find()
        fact = Node(
            'Fact',
            id = str(uuid.uuid4()),
            title = title,
            text = text,
            timestamp = timestamp(),
            date = date()
        )

        rel = Relationship(user, 'PUBLISHED', fact)
        graph.create(rel)

        tags = [x.strip() for x in tags.lower().split(',')]
        for name in set(tags):
            tag = Node('Tag', name=name)
            graph.merge(tag, 'Tag', 'name')
            rel = Relationship(tag, 'TAGGED', fact)
            graph.merge(rel)

    def delete_fact(self, fact_id):
        query = '''
                MATCH (user:User)-[:PUBLISHED]->(fact:Fact)
                WHERE user.username = {username} AND fact.id = {fact_id}
                DETACH DELETE (fact)
                '''
        return graph.run(query, username=self.username, fact_id=fact_id)

    # For Py2neo v4
    '''
    def view_fact(self, fact_id):
        user = self.find()
        fact = graph.nodes.match('Fact', id=fact_id).first()
        graph.merge(Relationship(user, 'VIEWED', fact, timestamp=timestamp(), date=date()))
    '''

    # For Py2neo v3
    def view_fact(self, fact_id):
        user = self.find()
        fact = graph.find_one('Fact', 'id', fact_id)
        graph.merge(Relationship(user, 'VIEWED', fact, timestamp=timestamp(), date=date()))

    def edit_fact(self, fact_id, title, tags, text):
        user = self.find()
        fact = Node(
            'Fact',
            id = fact_id,
            title = title,
            text = text,
            timestamp = timestamp(),
            date = date()
        )

        rel = Relationship(user, 'EDITED', fact)
        graph.merge(rel, 'Fact', 'id')

        tags = [x.strip() for x in tags.lower().split(',')]
        for name in set(tags):
            tag = Node('Tag', name=name)
            graph.merge(tag, 'Tag', 'name')
            rel = Relationship(tag, 'TAGGED', fact)
            graph.merge(rel)

    # QUESTIONS ========================================================================================================

    def add_question(self, title, tags, text, answer):
        user = self.find()
        question = Node(
            'Question',
            id=str(uuid.uuid4()),
            title=title,
            text=text,
            answer=answer,
            timestamp=timestamp(),
            date=date()
        )

        rel = Relationship(user, 'PUBLISHED', question)
        graph.create(rel)

        tags = [x.strip() for x in tags.lower().split(',')]
        for name in set(tags):
            tag = Node('Tag', name=name)
            graph.merge(tag, 'Tag', 'name')
            rel = Relationship(tag, 'TAGGED', question)
            graph.create(rel)

    def delete_question(self, question_id):
        query = '''
                MATCH (user:User)-[:PUBLISHED]->(question:Question)
                WHERE user.username = {username} AND question.id = {question_id}
                DETACH DELETE (question)
                '''
        return graph.run(query, username=self.username, question_id=question_id)

    # For Py2neo v4
    '''
    def view_question(self, question_id):
        user = self.find()
        question = graph.nodes.match('Question', id=question_id).first()
        graph.merge(Relationship(user, 'VIEWED', question, timestamp=timestamp(), date=date()))
    '''

    # For Py2neo v3
    def view_question(self, question_id):
        user = self.find()
        question = graph.find_one('Question', 'id', question_id)
        graph.merge(Relationship(user, 'VIEWED', question, timestamp=timestamp(), date=date()))

    def edit_question(self, question_id, title, tags, text, answer):
        user = self.find()
        question = Node(
            'Question',
            id = question_id,
            title = title,
            text = text,
            answer = answer,
            timestamp = timestamp(),
            date = date()
        )

        rel = Relationship(user, 'EDITED', question)
        graph.merge(rel, 'Question', 'id')

        tags = [x.strip() for x in tags.lower().split(',')]
        for name in set(tags):
            tag = Node('Tag', name=name)
            graph.merge(tag, 'Tag', 'name')
            rel = Relationship(tag, 'TAGGED', question)
            graph.merge(rel)

    # For Py2neo v4
    '''
    def answer_correct(self, question_id):
        user = self.find()
        question = graph.nodes.match('Question', id=question_id).first()
        question = graph.find_one('Question', 'id', question_id)
        graph.merge(Relationship(user, 'ANSWERED_CORRECTLY', question, timestamp=timestamp(), date=date()))
    '''

    # For Py2neo v3
    def answer_correct(self, question_id):
        user = self.find()
        question = graph.find_one('Question', 'id', question_id)

        graph.merge(Relationship(user, 'ANSWERED_CORRECTLY', question, timestamp=timestamp(), date=date()))

    # For Py2neo v4
    '''
    def answer_incorrect(self, question_id):
        user = self.find()
        question = graph.nodes.match('Question', id=question_id).first()
        graph.merge(Relationship(user, 'ANSWERED_INCORRECTLY', question, timestamp=timestamp(), date=date()))
    '''

    # For Py2neo v3
    def answer_incorrect(self, question_id):
        user = self.find()
        question = graph.find_one('Question', 'id', question_id)

        graph.merge(Relationship(user, 'ANSWERED_INCORRECTLY', question, timestamp=timestamp(), date=date()))

    def answer_question(self, question_id, answer):
        user = self.find()
        question = graph.find_one('Question', 'id', question_id)
        graph.merge(Relationship(user, 'ANSWERED', question, timestamp=timestamp(), date=date(), answer=answer))

    # FEEDBACK =========================================================================================================

    # For Py2neo v4
    '''
    def give_feedback(self, primary_label, node_id, feedback):
        feedback_options = [
            'LIKE',
            'DISLIKE',
            'EASY',
            'HARD',
            'HELPFUL',
            'UNHELPFUL',
            'RELEVANT',
            'IRRELEVANT'
        ]

        if feedback not in feedback_options:
            raise ValueError
        else:
            user = self.find()
            node = graph.nodes.match(primary_label, id=node_id).first()
            graph.merge(Relationship(user, feedback, node, timestamp=timestamp(), date=date()))
    '''

    # For Py2neo v3
    def give_feedback(self, primary_label, node_id, feedback):
        feedback_options = [
            'LIKE',
            'DISLIKE',
            'EASY',
            'HARD',
            'HELPFUL',
            'UNHELPFUL',
            'RELEVANT',
            'IRRELEVANT'
        ]

        if feedback not in feedback_options:
            raise ValueError
        else:
            user = self.find()
            node = graph.find_one(primary_label, 'id', node_id)
            graph.merge(Relationship(user, feedback, node, timestamp=timestamp(), date=date()))

    # OTHER ============================================================================================================

    def get_recent_facts(self):
        query = '''
        MATCH (user:User)-[:PUBLISHED]->(fact:Fact)<-[:TAGGED]-(tag:Tag)
        WHERE user.username = {username}
        RETURN fact, COLLECT(tag.name) AS tags
        ORDER BY fact.timestamp DESC LIMIT 5
        '''
        return graph.run(query, username=self.username)

    def get_recent_questions(self):
        query = '''
        MATCH (user:User)-[:PUBLISHED]->(question:Question)<-[:TAGGED]-(tag:Tag)
        WHERE user.username = {username}
        RETURN question, COLLECT(tag.name) AS tags
        ORDER BY question.timestamp DESC LIMIT 5
        '''
        return graph.run(query, username=self.username)
