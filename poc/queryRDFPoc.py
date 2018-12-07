from rdflib import Graph

g = Graph()
g.parse("poc/rdfMetier.ttl", format="ttl")


def trouverMetier(tache):
    result = []
    resultQuery = g.query(
        'SELECT DISTINCT ?metier WHERE { ?metier :Fait ?action . ?action rdfs:label "' + tache + '" .}')
    for row in resultQuery:
        result.append(row)

    return result


def getLabel(uris):
    result = []
    for uri in uris:
        resultQuery = g.query('SELECT DISTINCT ?label WHERE { ' + uri.n3() + ' rdfs:label ?label .}')
        for row in resultQuery:
            result.append(row)

    return result
