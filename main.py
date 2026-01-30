import sys
import time

from heuristique import (
    chargerInstanceTsplib,
    construireMatriceDistances,
    construireSolutionGloutonne,
)
from metaheuristique import descenteStochastique
from plne import resoudrePlneCompacte
from visualisation import afficherSolution, nuageDePoints


def main():
    cheminTsp = "data/" + sys.argv[1]
    p = int(sys.argv[2])

    alpha = 1.0
    graineAleatoire = 0

    points, _, _ = chargerInstanceTsplib(cheminTsp)
    matriceDist = construireMatriceDistances(points)

    nuageDePoints(
        points,
        f"Instance {sys.argv[1]}",
        f"img/{sys.argv[1]}_instance.png",
    )

    station1 = 0
    n = matriceDist.shape[0]

    k = max(500, 10 * n)

    t0 = time.time()
    solutionGloutonne = construireSolutionGloutonne(points, matriceDist, p, alpha, station1)
    t1 = time.time()

    t2 = time.time()
    solutionDescente = descenteStochastique(
        solutionGloutonne,
        matriceDist,
        alpha,
        station1,
        k,
        graineAleatoire,
    )
    t3 = time.time()

    print("=== Heuristique ===")
    print(
        f"Glouton: cout={solutionGloutonne['coutTotal']:.3f} "
        f"(metro={solutionGloutonne['coutMetro']:.3f}, marche={solutionGloutonne['coutMarche']:.3f}) "
        f"temps={t1 - t0:.3f}s"
    )
    print(f"Solution gloutonne: {solutionGloutonne['stations']}")

    afficherSolution(
        points,
        solutionGloutonne,
        "Solution gloutonne",
        f"img/{sys.argv[1]}_gloutonne_p{p}.png",
    )

    print("=== Métaheuristique ===")
    print(
        f"Descente: cout={solutionDescente['coutTotal']:.3f} "
        f"(metro={solutionDescente['coutMetro']:.3f}, marche={solutionDescente['coutMarche']:.3f}) "
        f"temps={t3 - t2:.3f}s"
    )
    print(f"Solution descente: {solutionDescente['stations']}")

    afficherSolution(
        points,
        solutionDescente,
        "Solution descente stochastique",
        f"img/{sys.argv[1]}_descente_p{p}.png",
    )

    solutionPlne = None
    statutPlne = None
    t4 = t5 = None
    if n <= 100:
        t4 = time.time()
        statutPlne, solutionPlne = resoudrePlneCompacte(matriceDist, p, alpha, station1)
        t5 = time.time()

        print("=== PuLP (formulation compacte) ===")
        print(f"Statut: {statutPlne}")
        print(
            f"PuLP: cout={solutionPlne['coutTotal']:.3f} "
            f"(metro={solutionPlne['coutMetro']:.3f}, marche={solutionPlne['coutMarche']:.3f}) "
            f"temps={t5 - t4:.3f}s"
        )
        print(f"Solution PuLP: {solutionPlne['stations']}")

        afficherSolution(
            points,
            solutionPlne,
            f"Solution PuLP ({statutPlne})",
            f"img/{sys.argv[1]}_pulp_p{p}.png",
        )

    else:
        print("=== PuLP (formulation compacte) ===")
        print(f"Instance trop grande (n={n}) => PuLP ignoré (très lent au-delà de ~100 points).")


if __name__ == "__main__":
    main()
