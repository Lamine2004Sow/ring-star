import networkx as nx
import pulp

from heuristique import coutTotal


def resoudrePlneCompacte(
    matriceDist,
    p,
    alpha,
    station1,
):
    n = matriceDist.shape[0]
    sommets = list(range(n))
    aretes = [(i, j) for i in range(n) for j in range(i + 1, n)]

    modele = pulp.LpProblem("Anneau_Etoile", pulp.LpMinimize)

    y = pulp.LpVariable.dicts(
        "y",
        (sommets, sommets),
        lowBound=0,
        upBound=1,
        cat=pulp.LpBinary,
    )

    x = pulp.LpVariable.dicts(
        "x",
        aretes,
        lowBound=0,
        upBound=1,
        cat=pulp.LpBinary,
    )

    z = pulp.LpVariable.dicts(
        "z",
        (sommets, sommets),
        lowBound=0,
        upBound=p - 1,
        cat=pulp.LpContinuous,
    )

    coutMetroLineaire = pulp.lpSum(
        float(matriceDist[i, j]) * x[(i, j)]
        for (i, j) in aretes
    )
    coutMarcheLineaire = pulp.lpSum(
        float(matriceDist[i, j]) * y[i][j]
        for i in sommets
        for j in sommets
    )
    modele += alpha * coutMetroLineaire + coutMarcheLineaire

    modele += pulp.lpSum(y[i][i] for i in sommets) == p

    for i in sommets:
        modele += pulp.lpSum(y[i][j] for j in sommets) == 1

    for i in sommets:
        for j in sommets:
            if i == j:
                continue
            modele += y[i][j] <= y[j][j]

    modele += y[station1][station1] == 1
    for j in sommets:
        if j == station1:
            continue
        modele += y[station1][j] == 0

    for i in sommets:
        aretesIncidentes = []
        for j in sommets:
            if i == j:
                continue
            a, b = (i, j) if i < j else (j, i)
            aretesIncidentes.append(x[(a, b)])

        modele += pulp.lpSum(aretesIncidentes) == 2 * y[i][i]

    modele += pulp.lpSum(z[station1][j] for j in sommets if j != station1) == p - 1

    for i in sommets:
        if i == station1:
            continue
        flotEntrant = pulp.lpSum(z[j][i] for j in sommets if j != i)
        flotSortant = pulp.lpSum(
            z[i][j]
            for j in sommets
            if j != i and j != station1
        )
        modele += flotEntrant == flotSortant + y[i][i]

    for i, j in aretes:
        modele += z[i][j] + z[j][i] <= (p - 1) * x[(i, j)]

    solveur = pulp.PULP_CBC_CMD(msg=False)
    statut = modele.solve(solveur)
    chaineStatut = pulp.LpStatus.get(statut, str(statut))

    stations = [i for i in sommets if (pulp.value(y[i][i]) or 0.0) > 0.5]
    stations = sorted(set(stations))

    affectation = []
    for i in sommets:
        stationAssociee = max(sommets, key=lambda j: pulp.value(y[i][j]) or 0.0)
        affectation.append(int(stationAssociee))

    aretesCycle = []
    for i, j in aretes:
        if (pulp.value(x[(i, j)]) or 0.0) > 0.5:
            aretesCycle.append((i, j))

    graphe = nx.Graph()
    graphe.add_nodes_from(stations)
    graphe.add_edges_from(aretesCycle)

    cycleStations = [station1]
    if len(stations) > 1 and graphe.has_node(station1):
        stationPrecedente = None
        stationCourante = station1
        for _ in range(len(stations) - 1):
            voisins = list(graphe.neighbors(stationCourante))
            if len(voisins) < 2 and stationPrecedente is None:
                break

            if stationPrecedente is None or voisins[0] != stationPrecedente:
                stationSuivante = voisins[0]
            else:
                stationSuivante = voisins[1]

            cycleStations.append(int(stationSuivante))
            stationPrecedente, stationCourante = stationCourante, stationSuivante

    cout, coutMetro, coutMarche = coutTotal(stations, cycleStations, affectation, matriceDist, alpha)
    return chaineStatut, {
        "stations": stations,
        "affectation": affectation,
        "cycleStations": cycleStations,
        "coutTotal": cout,
        "coutMetro": coutMetro,
        "coutMarche": coutMarche,
    }
