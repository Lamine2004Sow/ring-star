import math

import numpy as np
import tsplib95


def chargerInstanceTsplib(cheminTsp):
    probleme = tsplib95.load(cheminTsp)
    coordonnees = probleme.node_coords
    if coordonnees is None:
        raise ValueError("Instance TSPLIB sans coordonnées (node_coords manquant).")

    identifiants = sorted(coordonnees.keys())
    idVersIndice = {
        identifiantNoeud: indice
        for indice, identifiantNoeud in enumerate(identifiants)
    }
    indiceVersId = {
        indice: identifiantNoeud
        for identifiantNoeud, indice in idVersIndice.items()
    }

    points = np.zeros((len(identifiants), 2), dtype=float)
    for identifiantNoeud in identifiants:
        i = idVersIndice[identifiantNoeud]
        x, y = coordonnees[identifiantNoeud]
        points[i, 0] = float(x)
        points[i, 1] = float(y)

    return points, idVersIndice, indiceVersId


def construireMatriceDistances(points):
    difference = points[:, None, :] - points[None, :, :]
    matriceDist = np.sqrt(np.sum(difference * difference, axis=2))
    return matriceDist


def coutCycle(cycleStations, matriceDist):
    if len(cycleStations) <= 1:
        return 0.0

    cout = 0.0
    for stationA, stationB in zip(cycleStations, cycleStations[1:]):
        cout += float(matriceDist[stationA, stationB])
    cout += float(matriceDist[cycleStations[-1], cycleStations[0]])

    return cout


def coutTotal(stations, cycleStations, affectation, matriceDist, alpha):
    coutMetro = coutCycle(cycleStations, matriceDist)

    coutMarche = 0.0
    for indiceVille, stationAffectee in enumerate(affectation):
        if indiceVille == stationAffectee:
            continue
        coutMarche += float(matriceDist[indiceVille, stationAffectee])

    cout = alpha * coutMetro + coutMarche
    return cout, alpha * coutMetro, coutMarche


def cycleVoisinPlusProche(stations, matriceDist, station1):
    if station1 not in stations:
        raise ValueError("station1 doit appartenir à la liste des stations.")

    stationsNonVisitees = set(stations)
    stationsNonVisitees.remove(station1)

    cycleStations = [station1]
    stationCourante = station1

    while stationsNonVisitees:
        prochaineStation = min(
            stationsNonVisitees,
            key=lambda j: matriceDist[stationCourante, j],
        )
        cycleStations.append(prochaineStation)
        stationsNonVisitees.remove(prochaineStation)
        stationCourante = prochaineStation

    return cycleStations


def affecterVillesAuxStations(stations, matriceDist):
    n = matriceDist.shape[0]
    ensembleStations = set(stations)
    affectation = [stations[0]] * n

    for indiceVille in range(n):
        if indiceVille in ensembleStations:
            affectation[indiceVille] = indiceVille
            continue

        affectation[indiceVille] = min(
            stations,
            key=lambda station: matriceDist[indiceVille, station],
        )

    return affectation


def selectionStationsGrille(points, p, station1, matriceDist):
    n = points.shape[0]
    if p < 3 or p > n:
        raise ValueError("Il faut n >= p >= 3.")

    xmin, ymin = float(points[:, 0].min()), float(points[:, 1].min())
    xmax, ymax = float(points[:, 0].max()), float(points[:, 1].max())

    q = int(math.ceil(math.sqrt(p)))
    q = max(q, 1)

    pasX = (xmax - xmin) / q if (xmax - xmin) > 0 else 1.0
    pasY = (ymax - ymin) / q if (ymax - ymin) > 0 else 1.0

    candidats = []
    for indiceX in range(q):
        for indiceY in range(q):
            centreX = xmin + (indiceX + 0.5) * pasX
            centreY = ymin + (indiceY + 0.5) * pasY

            borneXMin, borneXMax = (
                xmin + indiceX * pasX,
                xmin + (indiceX + 1) * pasX,
            )
            borneYMin, borneYMax = (
                ymin + indiceY * pasY,
                ymin + (indiceY + 1) * pasY,
            )

            indicesDansCase = np.where(
                (points[:, 0] >= borneXMin)
                & (points[:, 0] < borneXMax)
                & (points[:, 1] >= borneYMin)
                & (points[:, 1] < borneYMax)
            )[0]
            if len(indicesDansCase) == 0:
                continue

            distanceAuCentre = (points[indicesDansCase, 0] - centreX) ** 2 + (
                points[indicesDansCase, 1] - centreY
            ) ** 2
            ville = int(indicesDansCase[int(np.argmin(distanceAuCentre))])
            candidats.append(ville)

    stations = [station1]
    for candidat in candidats:
        if candidat != station1 and candidat not in stations:
            stations.append(candidat)

    villesNonStations = [
        indiceVille for indiceVille in range(n)
        if indiceVille not in stations
    ]

    if len(stations) < p:
        while len(stations) < p and villesNonStations:
            prochaineVille = max(
                villesNonStations,
                key=lambda indiceVille: min(matriceDist[indiceVille, station] for station in stations),
            )
            stations.append(prochaineVille)
            villesNonStations.remove(prochaineVille)
    elif len(stations) > p:
        while len(stations) > p:
            candidatsASupprimer = [station for station in stations if station != station1]
            if not candidatsASupprimer:
                break

            mesureRedondance = []
            for station in candidatsASupprimer:
                autresStations = [autre for autre in stations if autre != station]
                mesureRedondance.append(
                    (min(matriceDist[station, autre] for autre in autresStations), station)
                )
            _, stationASupprimer = min(mesureRedondance)
            stations.remove(stationASupprimer)

    return stations


def construireSolutionGloutonne(points, matriceDist, p, alpha, station1):
    stations = selectionStationsGrille(points, p, station1, matriceDist)
    affectation = affecterVillesAuxStations(stations, matriceDist)
    cycleStations = cycleVoisinPlusProche(stations, matriceDist, station1)

    cout, coutMetro, coutMarche = coutTotal(
        stations,
        cycleStations,
        affectation,
        matriceDist,
        alpha,
    )

    return {
        "stations": stations,
        "affectation": affectation,
        "cycleStations": cycleStations,
        "coutTotal": cout,
        "coutMetro": coutMetro,
        "coutMarche": coutMarche,
    }
