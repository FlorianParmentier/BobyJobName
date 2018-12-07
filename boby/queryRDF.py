from rdflib import Graph


def createGraph(filePath):
    """This function create a graph from a file find with path from parameter"""
    graph = Graph()

    try:
        graph.parse(filePath, format="ttl")
    except FileNotFoundError:
        print("File <" + filePath + "> not found")

    return graph


def requestTriples(predicate, obj):
    """This function request a graph to find triples with an object similar from paramater

    The function request each triple which have an object where a word in the parameter appear"""
    graph = createGraph("rdf/generatedRdfV6.ttl")
    objWords = obj.split(" ")
    regex = ''
    for word in objWords:
        if regex == '':
            regex += word
        elif word != "":
            regex += '|' + word
    result = []
    query = "SELECT DISTINCT ?jobLabel ?predicateLabel " \
            "WHERE {?job a :Job. " \
            "?job rdfs:label ?jobLabel. " \
            "?predicate a :Action. " \
            "?predicate rdfs:label ?predicateLabel. " \
            "?job ?predicate ?action. " \
            "?action rdfs:label ?actionLabel. " \
            "FILTER regex(?actionLabel, \"" + regex + "\", \"i\")}"
    resultQuery = graph.query(query)
    for row in resultQuery:
        if str(row[1]) == predicate:
            result.append(str(row[0]))
    return result


# requestTriples("developper", "logiciel")
