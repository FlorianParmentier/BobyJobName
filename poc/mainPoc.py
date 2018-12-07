from poc import queryRDFPoc


def trouverMetier():
    score = dict()
    finish = False
    while (not finish):
        print('Que souhaitez vous faire dans votre futur métier?')
        action = input()

        if (action == "exit"):
            finish = True
        else:
            resultArray = queryRDFPoc.trouverMetier(action)
            for result in resultArray:
                if result[0] in score:
                    score[result[0]] += 1
                else:
                    score[result[0]] = 1

    print("\nTableau des resultats :")
    maxScore = 0
    values = []
    for key, value in score.items():
        print(key, ':', value)
        if value > maxScore:
            values = [key]
            maxScore = value
        elif value == maxScore:
            values.append(key)
    print("\n")

    nomsMetier = queryRDFPoc.getLabel(values)
    if len(nomsMetier) == 0:
        print(
            "Il semble que personne n'effectue ces tâches chez Daveo mais c'est peut-être moi qui ai mal compris, " +
            "n'hésitez réessayez d'expliquer autrement ce que vous souhaitez faire dans votre futur metier ;)")
    elif len(nomsMetier) == 1:
        print("Chez nous, c'est le " + nomsMetier[0][0] + " qui effectue ces tâches")
    else:
        reponse = "Chez Daveo, les postes auquels sont associées ces tâches sont : "
        firstElement = True
        for nom in nomsMetier:
            if(firstElement):
                firstElement = False
                reponse += nom[0]
            else:
                reponse += ', ' + nom[0]
        print(reponse)


trouverMetier()
