import random

from heuristique import (
    affecterVillesAuxStations,
    coutTotal,
    cycleVoisinPlusProche,
)


def descenteStochastique(
    solution,
    matriceDist,
    alpha,
    station1,
    k,
    graineAleatoire,
):
    generateurAleatoire = random.Random(graineAleatoire)
    n = matriceDist.shape[0]

    stations = list(solution["stations"])
    ensembleStations = set(stations)
    villesNonStations = [
        indiceVille for indiceVille in range(n)
        if indiceVille not in ensembleStations
    ]

    meilleureSolution = solution

    for _ in range(k):
        stationsSansStation1 = [station for station in stations if station != station1]
        if not stationsSansStation1 or not villesNonStations:
            break

        stationRetiree = generateurAleatoire.choice(stationsSansStation1)
        villeAjoutee = generateurAleatoire.choice(villesNonStations)

        stationsTemporaires = [
            villeAjoutee if station == stationRetiree else station
            for station in stations
        ]

        affectationTemporaire = affecterVillesAuxStations(stationsTemporaires, matriceDist)
        cycleTemporaire = cycleVoisinPlusProche(stationsTemporaires, matriceDist, station1)
        coutTemporaire, coutMetroTemporaire, coutMarcheTemporaire = coutTotal(
            stationsTemporaires,
            cycleTemporaire,
            affectationTemporaire,
            matriceDist,
            alpha,
        )

        if coutTemporaire < meilleureSolution["coutTotal"]:
            stations = stationsTemporaires
            ensembleStations = set(stations)
            villesNonStations = [
                indiceVille for indiceVille in range(n)
                if indiceVille not in ensembleStations
            ]
            meilleureSolution = {
                "stations": stations,
                "affectation": affectationTemporaire,
                "cycleStations": cycleTemporaire,
                "coutTotal": coutTemporaire,
                "coutMetro": coutMetroTemporaire,
                "coutMarche": coutMarcheTemporaire,
            }

    return meilleureSolution
