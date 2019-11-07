# coding=utf-8
from nlpedia.models import graph
import random

def naive_rule(username):
    """
    Given a username, automatically select a random fact or question that has not been viewed yet.
    Returns the node containing the fact or question.
    """

    query = '''
        MATCH (post)
        WHERE post:Fact OR post:Question
        MATCH (user:User)
        WHERE NOT (user)-[:VIEWED]->(post)
        AND user.username = {username}
        RETURN post
    '''

    results = graph.run(query, username=username)
    results = [x for x in results]

    try:
        return random.choice(results)
    except IndexError:
        pass

if __name__ == '__main__':
    random_node = naive_rule('Tyjchurchill')
    print(random_node)

