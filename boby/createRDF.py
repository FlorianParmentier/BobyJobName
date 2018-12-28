from nltk.tree import Tree
from spacy.lang.fr import French
from rdflib import Graph, Literal, RDF, RDFS, Namespace, BNode, URIRef
import pathlib
import os
from unidecode import unidecode
import fr_core_news_md
from spacy_lefff import LefffLemmatizer, POSTagger


nlp = fr_core_news_md.load()
pos = POSTagger()
french_lemmatizer = LefffLemmatizer(after_melt=True)
nlp.add_pipe(pos, name='pos', after='parser')
nlp.add_pipe(french_lemmatizer, name='lefff', after='pos')

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
    predicateFormat = unidecode(upperCaseFirstLetter(triple[1])).replace(" ", "")
    objFormat = unidecode(triple[2])
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


def createTripleSpacyLefff(sent, jobName):
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
    extractedTokens = []
    sentDoc = nlp(sent)
    for token in sentDoc:
        tag = token._.melt_tagger
        if tag == 'V' or tag == 'VINF':
            extractedTokens.append(['verb', token._.lefff_lemma if token._.lefff_lemma is not None else token.lemma_,
                                    tag])
        elif (tag == 'NC' or tag == 'ADJ') and token._.lefff_lemma is not None:
            extractedTokens.append([tag, token._.lefff_lemma])
        elif tag == 'CC':
            extractedTokens.append([tag])

    verbGroup = []
    currentVerbGroup = []
    containsV = False
    containsVINF = False
    nounGroup = []
    currentNounGroup = []
    for token in extractedTokens:
        if token[0] == 'verb':
            if not containsV and token[2] == 'V':
                containsV = True
            if not containsVINF and token[2] == 'VINF':
                containsVINF = True
            currentVerbGroup.append([token[1], token[2]])
            if currentNounGroup:
                nounGroup.append(currentNounGroup)
                currentNounGroup = []
        elif token[0] == 'NC' or token[0] == 'ADJ':
            currentNounGroup.append(token[1])
            if currentVerbGroup:
                verbGroup.append(currentVerbGroup)
                currentVerbGroup = []
        elif token[0] == 'CC' and currentNounGroup:
            currentNounGroup.append('CC')
    if currentNounGroup:
        nounGroup.append(currentNounGroup)
    if currentVerbGroup:
        verbGroup.append(currentVerbGroup)

    triples = []
    for i in range(len(verbGroup)):
        for verb in verbGroup[i]:
            if containsV and containsVINF and verb[1] != 'V' or \
                    (containsVINF and not containsV) or \
                    (containsV and not containsVINF):
                tripleObject = ""
                for noun in nounGroup[i] if len(nounGroup)-1 >= i else nounGroup[len(nounGroup)-1]:
                    if noun == 'CC':
                        triples.append((jobName, verb[0], tripleObject))
                        tripleObject = ""
                    else:
                        tripleObject += noun + " "
                tripleObject = tripleObject[:-1]
                triples.append((jobName, verb[0], tripleObject))

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

    Triples creation is made by `createTripleSpacyLefff` function from this module.

    After triples are created and added to the graph, it is saved at turtle format.

    :param graph: Rdflib graph on which triples are added.
    :param filePath: Filepath where the graph will be saved.
    :param sent: Sentence from which triples are extracted.
    :param jobName: Name of the job which is describe.

    """

    triples, triplesWithoutAdj = createTripleSpacyLefff(sent, jobName)
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


print(createTripleSpacyLefff("Je veux développer des logiciels et des sites web", 'Développeur'))
