from nltk.parse import CoreNLPParser
from nltk.tree import Tree
from spacy.lang.fr import French
from rdflib import Graph, Literal, RDF, RDFS, Namespace, BNode, URIRef
import pathlib
import os
from unidecode import unidecode
import treetaggerwrapper

# Get access to the Stanford Parser server (don't forget to start the server before)
# Unable to catch exception  if the server is not started. (Exception occur inside the function and can not be catched
# with try/ except block
parser = CoreNLPParser(url='http://localhost:9004')

# Load spacy french model
nlp = French()
# Add some words to "stop words" list because spaCy doesn't integrate them
nlp.vocab["l"].is_stop = True
nlp.vocab["d"].is_stop = True
nlp.vocab["'"].is_stop = True
nlp.vocab["n"].is_stop = True
nlp.vocab["m"].is_stop = True
nlp.vocab["je"].is_stop = True


def createGraph(filePath):
    """This fonction createa rdflib graph from a rdf file.

    :param filePath: Path of the file which is read to create graph.
    :return: The rdflib graph.

    """
    graph = Graph()
    try:
        graph.parse(filePath, format="ttl")
    except FileNotFoundError:
        open(filePath, 'w').close()
        ns = Namespace(pathlib.Path(os.path.abspath(filePath)).as_uri() + '#')
        graph.namespace_manager.bind("", ns, replace=True, override=True)
        graph.parse(filePath, format="ttl")
        graph.add((ns.Job, RDF.type, RDFS.Class))
        graph.add((ns.Action, RDF.type, RDF.Property))
        graph.serialize(destination=filePath, format="turtle")

    return graph


def formatTriple(triple):
    """This function format a triple to make it general.

    Format operation are :
        - decode to remove special character
        - upper case first letter and remove space for """
    subjectFormat = unidecode(upperCaseFirstLetter(triple[0])).replace(" ", "")
    predicateFormat = unidecode(upperCaseFirstLetter(getLemma(triple[1]))).replace(" ", "")
    objFormat = unidecode(getLemma(triple[2]))
    return subjectFormat, predicateFormat, objFormat


def removeStopWords(sent):
    """This function remove french stop words from a sentence."""
    doc = nlp(sent)
    tokens = []
    for token in doc:
        if not token.is_stop:
            tokens.append(token.text)
    newSent = ''
    for token in tokens:
        newSent += token + ' '
    return newSent[:len(newSent) - 1]


def getLemma(sent):
    """This function return lemma of each words of the sentence in parameter"""
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr')
    tags = tagger.tag_text(sent)
    tags = treetaggerwrapper.make_tags(tags)
    newSent = ""
    for tag in tags:
        newSent += tag.lemma + ' '
    return newSent


def upperCaseFirstLetter(strToUpperCase):
    """This fonction uppercase first letter of each words of a string."""
    strLower = strToUpperCase.lower()
    index = [ind for ind, char in enumerate(strLower) if char == ' ']
    newStr = ""
    for ind, char in enumerate(strLower):
        if ind == 0 or (ind - 1) in index:
            newStr += char.upper()
        else:
            newStr += char
    return newStr


def createTripleV6(sent, jobName):
    """This function create triples from a sentence to describe a job activity.

    This function create one or more triples. These triples describes a job activity.
    This function implements version 6 of BOBI extraction triples.
    Theses triples are formed as follow :
    - Subject: it is the job name.
    - Predicate: it is the verb which represent activity.
    - Object: it is formed by several words extracted from the sentence to describe activity.

    :param sent: Sentence from which triples are extracted.
    :param jobName: Name of the job which is describe.

    """
    parsedSent = parser.raw_parse(sent)
    triples = []
    concatNoun = ""
    verb = ""
    for line in parsedSent:
        triples, concatNoun, verb = browseTreeV6(jobName, line, triples, concatNoun, verb)
    triples.append((jobName, verb, getLemma(removeStopWords(concatNoun))))
    return triples



def browseTreeV6(jobName, tree, triples, concatNoun, verb):
    """This function browse a dependency tree to extract triple.

    This function is mainly used by `createTripleV6` function of this module.

    """
    triples = triples
    concatNoun = concatNoun
    verb = verb
    for child in tree:
        if type(child) == Tree:
            if child.label() == "VERB":
                if verb == "":
                    verb = child[0]
                else:
                    triples.append((jobName, verb, getLemma(removeStopWords(concatNoun))))
                    concatNoun = ""
                    verb = child[0]
            elif (tree.label() == "NP" and type(child[0]) != Tree) or (
                    tree.label() == "SENT" and child.label() == "NOUN"):
                if concatNoun == "":
                    concatNoun = child[0]
                else:
                    concatNoun += ' ' + child[0]
            elif tree.label() == "NP":
                triples, concatNoun, verb = browseTreeV6GetAll(jobName, child, triples, concatNoun, verb)
            else:
                triples, concatNoun, verb = browseTreeV6(jobName, child, triples, concatNoun, verb)
    return triples, concatNoun, verb


def browseTreeV6GetAll(jobName, tree, triples, concatNoun, verb):
    """This function browse a dependency tree to extract triple.

    This function is mainly used by `browseTreeV6GetAll` function of this module.

    """
    triples = triples
    concatNoun = concatNoun
    verb = verb
    for child in tree:
        if type(child) == Tree:
            if child.label() == "VERB":
                if verb == "":
                    verb = child[0]
                else:
                    concatNoun = ""
                    verb = child[0]
            elif type(child[0]) != Tree:
                if concatNoun == "":
                    concatNoun = child[0]
                else:
                    concatNoun += ' ' + child[0]
            else:
                triples, concatNoun, verb = browseTreeV6GetAll(jobName, child, triples, concatNoun, verb)
    return triples, concatNoun, verb


def createTripleSpacyLefff(sent,jobname):
    parsedSent = parser.raw_parse(sent)
    triples = []
    concatNoun = []
    verb = []
    return triples


def addTriple(graph, subject, predicate, obj):
    """This function format a triple and add it to a graph

    This function add a triple {job, action, complement informations} which desribe a job activity to a graph.
    The subject is declare with the type :Job.
    The predicate is declare with the type :Action.

    :param graph: The graph on which the triple is added.
    :param subject: The triple subject, it represents the job name.
    :param predicate: The triple predicate, it is the verb which represents the job activity.
    :param obj: The triple object, it describes the job activity with the predicate.

    :Example:
    >>>> addTriple(g, "Developper", "code", "software")

    """
    namespaces = graph.namespaces()
    n = [ns for ns in namespaces if ns[0] == ''][0]
    ns = Namespace(URIRef(n[1]))
    graph.add((n[1] + subject, RDF.type, ns.Job))
    graph.add((n[1] + subject, RDFS.label, Literal(subject)))
    graph.add((n[1] + predicate, RDF.type, ns.Action))
    graph.add((n[1] + predicate, RDFS.label, Literal(predicate)))
    objectNode = BNode()
    graph.add((objectNode, RDFS.label, Literal(obj)))
    graph.add((n[1] + subject, n[1] + predicate, objectNode))


def insertTripleV6(graph, filePath, sent, jobName):
    """This function create and insert triples in a graph. Then this graph is saved.

    This function create one or more triples and add them to a rdf graph. These triples describes a job activity.
    Before being add in the graph, triples are format (Upper case first letter in subject and predicate, remove
    specific character).
    This function implements version 6 of BOBI extraction triples.
    Theses triples are formed as follow :
    - Subject: it is the job name.
    - Predicate: it is the verb which represent activity.
    - Object: it is formed by several words extracted from the sentence to describe activity.

    Triples creation is made by `createtripleV6` function from this module.

    After triples are created and added to the graph, it is saved at turtle format.

    :param graph: Rdflib graph on which the triple is added.
    :param filePath: Filepath where the graph will be saved.
    :param sent: Sentence from which triples are extracted.
    :param jobName: Name of the job which is describe.

    """
    triples = createTripleV6(sent, jobName)
    for triple in triples:
        triple = formatTriple(triple)
        addTriple(graph, triple[0], triple[1], triple[2])
    graph.serialize(destination=filePath, format="turtle")


# Les lignes de codes suivantes servent à tester le fonctionnement des méthodes de ce fichier.
# TODO : supprimer les lignes suivantes une fois le service fonctionnel et terminé.

# graphV4 = createGraph("rdf/generatedRdfV4.ttl")
# graphV6 = createGraph("rdf/generatedRdfV6.ttl")
# sentence = "Cadrer les activités avec les équipes agiles et assurer la bonne compréhension des besoins métiers."
# print("Phrase testée : \"" + sentence + "\" \n")
# print("Création de triplet avec la méthode 4 :")
# insertTripleV4(graphV4, sentence, "Product Owner")
# print("\n")
# print("Création de triplet avec la méthode 6 :")
# insertTripleV6(graphV6, sentence, "Product Owner")
# getLemma("Cadrer les activités avec les équipes agiles")


# __________________________________Triples creation V4_______________________________________


def createTripleV4(graph, sent, jobName):
    """This function create triples from a sentence to describe a job activity.

    This function create one or more triples and add them to a rdf graph. These triples describes a job activity.
    This function implements version 4 of BOBI extraction triples.
    Theses triples are formed as follow :
    - Subject: it is the job name.
    - Predicate: it is the verb which represent activity.
    - Object: it is formed by several words extracted from the sentence to describe activity.

    :param graph: Rdflib graph on which the triple is added.
    :param sent: Sentence from which triples are extracted.
    :param jobName: Name of the job which is describe.

    """
    parsedSent = parser.raw_parse(sent)
    triples = []
    concatNoun = ""
    verb = ""
    for line in parsedSent:
        triples, concatNoun, verb = browseTreeV4(graph, jobName, line, triples, concatNoun, verb)
    triples.append("(" + jobName + ", " + verb + ", " + concatNoun + ")")
    addTriple(graph, jobName, verb, concatNoun)


def browseTreeV4(graph, jobName, tree, triples, concatNoun, verb):
    """This function browse a dependency tree to extract triple.

    This function is mainly used by `createTripleV4` function of this module.

    """
    triples = triples
    concatNoun = concatNoun
    verb = verb
    for child in tree:
        if type(child) == Tree:
            if child.label() == "VERB":
                if verb == "":
                    verb = child[0]
                else:
                    addTriple(graph, jobName, verb, concatNoun)
                    triples.append("(" + jobName + ", " + verb + ", " + concatNoun + ")")
                    concatNoun = ""
                    verb = child[0]
            elif tree.label() == "NP" and child.label() == "NOUN":
                if concatNoun == "":
                    concatNoun = child[0]
                else:
                    concatNoun += ' ' + child[0]
            else:
                triples, concatNoun, verb = browseTreeV4(graph, jobName, child, triples, concatNoun, verb)
    return triples, concatNoun, verb


def insertTripleV4(graph, filePath, sent, jobName):
    """This function create and insert triples in a graph. Then this graph is saved.

    This function create one or more triples and add them to a rdf graph. These triples describes a job activity.
    This function implements version 4 of BOBI extraction triples.
    Theses triples are formed as follow :
    - Subject: it is the job name.
    - Predicate: it is the verb which represent activity.
    - Object: it is formed by several words extracted from the sentence to describe activity.

    Triples creation is made by `createtripleV4` function from this module.

    After triples are created and added to the graph, it is saved at turtle format.

    :param graph: Rdflib graph on which the triple is added.
    :param filePath: Filepath where the graph will be saved.
    :param sent: Sentence from which triples are extracted.
    :param jobName: Name of the job which is describe.

    """
    createTripleV4(graph, sent, jobName)
    graph.serialize(destination=filePath, format="turtle")
