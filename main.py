from boby.queryRDF import requestJobName, requestActionFromJob
from boby.createRDF import createGraph, insertTripleV6, formatTriple, createTripleSpacyLefff
from boby.candidate import Candidate

import logging

graph = createGraph("rdf/generatedRdf.ttl")

# Disable logger from spacy_lefff package
LOGGER = logging.getLogger("spacy_lefff").setLevel(logging.CRITICAL)


def feedGraph():
    """
    This function create interaction with user in console to train the system
    """
    finish = False
    print('Enchanté, je suis BOBI, un agent DAVEO. Je souhaiterais vous poser des questions sur votre métier.')
    print('Tout d\'abord, quel est votre métier ?')
    job = input()
    print('Quelles sont les tâches que vous réalisez en tant que ' + job + '  ? ')
    # This boolean is here to allow user to quit conversation by entering two empty lines in console.
    keyboardEntry = False
    while not finish:
        action = input()
        # If line is empty, verify if user want to exit conversation
        if action == "":
            if keyboardEntry:
                finish = True
            else:
                keyboardEntry = True
        # If line is too long, inform user (System is more efficient with simple phrases)
        elif len(action) > 140:
            keyboardEntry = False
            print('Je suis encore jeune et aie beaucoup à apprendre, pourriez vous écrire moins de 140 caractères '
                  's\'il vous plait ?')
        else:
            keyboardEntry = False
            insertTripleV6(graph, "rdf/generatedRdf.ttl", action, job)


def findJob():
    """
    This function create interaction with user in console to find the job of his dreams

    How it works :
    - User enter phrase to describe an action in work
    - This phrase is compare to rdf graph of the system and corresponding job names are recovered
    - Each time a job name appear, its score increase
    - When user has finish to give informations, if best scores are close, user has to answer a short form where he
    choose a proposal between several.
    - At the end, the system determine which correspond better to user's description
    """
    candidate = Candidate()
    print('Enchanté, je suis BOBI, un agent DAVEO. Je souhaiterais savoir quelles sont les tâches que vous voulez '
          'faire dans votre prochain métier. Pouvez vous me les lister ?')
    finish = False

    jobsPointsCount = dict()
    # This boolean is here to allow user to quit conversation by entering two empty lines in console.
    keyboardEntry = False
    while not finish:
        action = input()
        # If line is empty, verify if user want to exit conversation
        if action == "":
            if keyboardEntry:
                finish = True
            else:
                keyboardEntry = True
        # If line is too long, inform user (System is more efficient with simple phrases)
        elif len(action) > 140:
            keyboardEntry = False
            print('Je suis encore jeune et aie beaucoup à apprendre, pourriez vous écrire moins de 140 caractères '
                  's\'il vous plait ?')
        else:
            keyboardEntry = False
            # Create triples from user phrase to match with rdf graph
            triples = createTripleSpacyLefff(action, "")
            for triple in triples:
                triple = formatTriple(triple)
                # Request rdf graph to check if triple match with known triple and get job name associate
                results, usedTriples = requestJobName(triple[1], triple[2], candidate.usedTriples)
                candidate.usedTriples.append(usedTriples)
                # For each job name found, increment score
                for result in results:
                    if result in jobsPointsCount:
                        jobsPointsCount[result] += 1
                    else:
                        jobsPointsCount[result] = 1
    topPoints = []
    while len(topPoints) < 3 and len(jobsPointsCount) > 0:
        bestScore = -1
        bestJob = ""
        for job in jobsPointsCount:
            if jobsPointsCount[job] > bestScore:
                bestJob = job
                bestScore = jobsPointsCount[job]
        del jobsPointsCount[bestJob]
        topPoints.append((bestJob, bestScore))

    print(topPoints)

    formCount = 0
    noMoreProposals = False
    while not noMoreProposals and len(topPoints) >= 2 and topPoints[1][1] >= (topPoints[0][1] * 0.5) and \
            topPoints[0][1] < 3 and formCount < 3:
        proposals = []
        for index, job in enumerate(topPoints):
            action = requestActionFromJob(job[0], candidate.usedTriples)
            if action:
                proposals.append(str(index + 1) + " : " + action[1] + " " + action[2])
        if proposals:
            print("\nQue préférez-vous entre les propositions suivantes ?")
            for prop in proposals:
                print(prop)
        else:
            noMoreProposals = True
        selectedIndex = int(input()) - 1
        if len(topPoints) > selectedIndex >= 0:
            topPoints[selectedIndex] = (topPoints[selectedIndex][0], topPoints[selectedIndex][1] + 1)
        formCount += 1
        print(topPoints)
    return topPoints


user = ''
while user != '1' and user != '2':
    print('Bonjour, qui êtes-vous ? (Indiquez le chiffre correspondant à la réponse)\n1 - Collaborateur Daveo\n2 '
          '- Candidat')
    user = input()
if user == '1':
    feedGraph()
else:
    jobs = findJob()

# file = open("rdf/dotGraph.dot", 'w')
# rdf2dot.rdf2dot(graphV6, file)
# render('dot', 'png', "rdf/dotGraph.dot")


# requestV6(graphV6, "Predicate", "logiciels équipe agile")
