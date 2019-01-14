from rdflib import Graph


def createGraph(filePath):
    """This function create a graph from a file find with path from parameter"""
    graph = Graph()

    try:
        graph.parse(filePath, format="ttl")
    except FileNotFoundError:
        print("File <" + filePath + "> not found")

    return graph


graph = createGraph("rdf/generatedRdf.ttl")


def requestJobName(predicate, obj, alreadyUsedTriple=[]):
    """This function request a graph to find triples with an object similar from paramater

    The function request each triple which have an object where a word in the parameter appear"""
    usedTriples = alreadyUsedTriple
    objWords = obj.split(" ")
    regex = ''
    for word in objWords:
        if regex == '':
            regex += word
        elif word != "":
            regex += '|' + word
    result = []
    query = "SELECT DISTINCT ?jobLabel ?predicateLabel ?objectLabel " \
            "WHERE {?job a :Job. " \
            "?job rdfs:label ?jobLabel. " \
            "?predicate a :Action. " \
            "?predicate rdfs:label ?predicateLabel. " \
            "?job ?predicate ?object. " \
            "?object rdfs:label ?objectLabel. " \
            "FILTER regex(?objectLabel, \"" + regex + "\", \"i\")}"
    resultQuery = graph.query(query)
    alreadyMatchedJob = []
    for row in resultQuery:
        if str(row[1]) == predicate and row[0] not in alreadyMatchedJob:
            result.append(str(row[0]))
            alreadyMatchedJob.append(row[0])
            usedTriples.append(row)
    return result, usedTriples


def requestActionFromJob(jobName, alreadyUsedTriple=[]):
    query = "SELECT DISTINCT ?jobLabel ?predicateLabel ?objectLabel " \
            "WHERE {?job a :Job. " \
            "?job rdfs:label ?jobLabel. " \
            "?job ?predicate ?object." \
            "?predicate rdfs:label ?predicateLabel. " \
            "?object rdfs:label ?objectLabel. " \
            "?job rdfs:label \"" + jobName + "\".}"
    result = graph.query(query)
    for row in result:
        if row not in alreadyUsedTriple:
            alreadyUsedTriple.append(row)
            return jobName, str(row[1]), str(row[2])
    return ()

# print(requestActionFromJob(["Developpeur", "Recruteur"]))
