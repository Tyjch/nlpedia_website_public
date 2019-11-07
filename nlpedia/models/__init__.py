# coding=utf-8
from configparser import ConfigParser
from py2neo import Graph, authenticate
import os

config = ConfigParser().read('config.ini')
is_local = config.getboolean('ogm', 'is_local')

if is_local:
    # For Local Neo4j & Py2neo v4
    bolt_url       = config.get('local', 'bolt_uri')
    neo4j_user     = config.get('local', 'neo4j_user')
    neo4j_password = config.get('local', 'neo4j_password')

    graph = Graph(bolt_url, user=neo4j_user, password=neo4j_password)

    graph.schema.create_uniqueness_constraint("User", "username")
    graph.schema.create_uniqueness_constraint("Tag", "name")
    graph.schema.create_uniqueness_constraint("Fact", "id")
    graph.schema.create_uniqueness_constraint("Question", "id")


elif not is_local:
    # For GrapheneDB Neo4j & Py2neo v3
    graphene_uri      = config.get('remote', 'graphene_uri')
    graphene_user     = config.get('remote', 'graphene_user')
    graphene_password = config.get('remote', 'graphene_password')

    authenticate(graphene_uri, graphene_user, graphene_password)
    graph = Graph("https://" + graphene_uri, bolt=False)

    def create_uniqueness_constraint(label, prop):
        query = "CREATE CONSTRAINT ON (n:{label}) ASSERT n.{property} IS UNIQUE"
        query = query.format(label=label, property=prop)
        graph.cypher.execute(query)
    
    create_uniqueness_constraint("User", "username")
    create_uniqueness_constraint("Tag", "name")
    create_uniqueness_constraint("Fact", "id")
    create_uniqueness_constraint("Question", "id")


