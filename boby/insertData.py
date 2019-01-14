from boby.createRDF import createGraph, insertTripleV6

graph = createGraph("rdf/generatedRdf.ttl")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Cadrer les activités avec les équipes agiles et assurer la bonne compréhension des besoins métiers.",
               "Product Owner")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Concevoir l'architecture des logiciels",
               "Développeur")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Développer des logiciels au sein d'une équipe agile",
               "Développeur")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Organiser des entretiens d'embauche",
               "Recruteur")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Prospecter des profils",
               "Recruteur")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Assurer le suivi de la méthode agile par l'équipe de développement",
               "Scrum Master")
insertTripleV6(graph, "rdf/generatedRdf.ttl",
               "Définir le contenu des sprints avec l'équipe agile",
               "Scrum Master")
