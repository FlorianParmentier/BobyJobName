from boby.queryRDF import requestTriples
from boby.createRDF import createGraph, insertTripleV6, formatTriple, createTripleSpacyLefff

graph = createGraph("rdf/generatedRdf.ttl")


def feedGraph():
    finish = False
    print('Enchanté, je suis BOBI, un agent DAVEO. Je souhaiterais vous poser des questions sur votre métier.')
    print('Tout d\'abord, quel est votre métier ?')
    job = input()
    print('Quelles sont les tâches que vous réalisez en tant que ' + job + '  ? ')
    while not finish:
        action = input()

        if action == "exit":
            finish = True
        elif len(action) > 140:
            print('Je suis encore jeune et aie beaucoup à apprendre, pourriez vous écrire moins de 140 caractères '
                  's\'il vous plait ?')
        else:
            insertTripleV6(graph, "rdf/generatedRdf.ttl", action, job)


def findJob():
    print('Enchanté, je suis BOBI, un agent DAVEO. Je souhaiterais savoir quelles sont les tâches que vous voulez '
          'faire dans votre prochain métier. Pouvez vous me les lister ?')
    finish = False
    ranking = dict()
    while not finish:
        action = input()
        if action == "exit":
            finish = True
        elif len(action) > 140:
            print('Je suis encore jeune et aie beaucoup à apprendre, pourriez vous écrire moins de 140 caractères '
                  's\'il vous plait ?')
        else:
            triples = createTripleSpacyLefff(action, "")
            for triple in triples:
                triple = formatTriple(triple)
                # print(triple)
                results = requestTriples(triple[1], triple[2])
                for result in results:
                    if result in ranking:
                        ranking[result] += 1
                    else:
                        ranking[result] = 1
    print(ranking)
    return ranking


user = ''
while user != '1' and user != '2':
    print('Bonjour, qui êtes-vous ? (Indiquez le chiffre correspondant à la réponse)\n1 - Collaborateur Daveo\n2 '
          '- Candidat')
    user = input()
if user == '1':
    feedGraph()
else:
    ranking = findJob()


# file = open("rdf/dotGraph.dot", 'w')
# rdf2dot.rdf2dot(graphV6, file)
# render('dot', 'png', "rdf/dotGraph.dot")


# requestV6(graphV6, "Predicate", "logiciels équipe agile")


