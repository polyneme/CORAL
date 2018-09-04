

class Neo4JService:
    def __init__(self, neo4j_client):
        self.__neo4j_client = neo4j_client

    def delete_all(self, type_name):
        with self.__neo4j_client.session() as session:
            session.run('MATCH (n : %s) DETACH DELETE n' % type_name)

    def index_entities(self, data_holder):
        type_def = data_holder.type_def
        type_name = type_def.name
        pk_property_def = type_def.pk_property_def

        id_value = data_holder.data[pk_property_def.name]
        with self.__neo4j_client.session() as session:
            session.run(
                'CREATE (n : %s{id:"%s"})' % (type_name, id_value))

    def index_processes(self, data_holder):
        match_query_items = []
        create_query_items = []

        # create process
        create_query_items.append('(p:Process{id:"%s"})' % ('1'))

        # match input objects
        for i, input_object in enumerate([]):
            type_name = ''
            obj_id = ''
            match_query_items.append(
                '(s%s: %s{id:"%s"})' % (i, type_name, obj_id))
            create_query_items.append(
                '(p)<-[:PARAM_IN]-(s%s),' % i)

        # match ouput objects
        for i, output_object in enumerate([]):
            type_name = ''
            obj_id = ''
            match_query_items.append(
                '(r%s: %s{id:"%s"})' % (i, type_name, obj_id))
            create_query_items.append(
                '(p)-[:HAS_OUTPUT]->(r%s),' % i)

        query = 'match %s create %s ' % (
            ','.join(match_query_items), ','.join(create_query_items))
        with self.__neo4j_client.session() as session:
            session.run(query)


# match
# 	(t1:Well{id:'Well0003186'}),
# 	(t2:Well{id:'Well0003190'}),
#     (s1:Sample{id:'Sample0006577'})
# create
# 	(p:Process{id:'Process000001',name:'QQQ'}),
#     (p)<-[:PARAM_IN]-(t1),
#     (p)<-[:PARAM_IN]-(t2),
#     (p)-[:PRODUCED]->(s1)
