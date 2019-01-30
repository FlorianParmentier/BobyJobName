from boby.createRDF import createGraph, insertTripleV6

graph = createGraph("rdf/generatedRdf.ttl")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Développer des logiciels et des sites web",
               "Développeur")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Tester des logiciels et des sites web",
               "Développeur")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Travailler en équipe",
               "Développeur")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Travailler en mode agile",
               "Développeur")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Concevoir l'architecture de logiciels et de sites web",
               "Développeur")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Organiser des entretiens d'embauche",
               "Recruteur")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Prospecter des profils",
               "Recruteur")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Travailler en équipe",
               "Recruteur")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Rencontrer des candidats en salon",
               "Recruteur")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Choisir les meilleurs profils",
               "Recruteur")
