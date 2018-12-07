from createRDF import createGraph, insertTripleV6

graphV6 = createGraph("rdf/generatedRdfV6.ttl")
insertTripleV6(graphV6, "rdf/generatedRdfV6.ttl",
               "Cadrer les activités avec les équipes agiles et assurer la bonne compréhension des besoins métiers.",
               "Product Owner")
insertTripleV6(graphV6, "rdf/generatedRdfV6.ttl",
               "Concevoir l'architecture des logiciels",
               "Développeur")
insertTripleV6(graphV6, "rdf/generatedRdfV6.ttl",
               "Développer des logiciels au sein d'une équipe agile",
               "Développeur")
insertTripleV6(graphV6, "rdf/generatedRdfV6.ttl",
               "Organiser des entretiens d'embauche",
               "Recruteur")
insertTripleV6(graphV6, "rdf/generatedRdfV6.ttl",
               "Prospecter des profils",
               "Recruteur")
insertTripleV6(graphV6, "rdf/generatedRdfV6.ttl",
               "Assurer le suivi de la méthode agile par l'équipe de développement",
               "Scrum Master")
insertTripleV6(graphV6, "rdf/generatedRdfV6.ttl",
               "Définir le contenu des sprints avec l'équipe agile",
               "Scrum Master")
