import matplotlib.pyplot as plt
import numpy as np


def nuageDePoints(points, titre="Instance du problème", cheminPng="instance.png"):
    fig, axe = plt.subplots(figsize=(9, 7))

    axe.scatter(
        points[:, 0],
        points[:, 1],
        s=18,
        c="tab:blue",
        alpha=0.7,
        label="Villes",
    )

    axe.set_title(titre)
    axe.legend()
    axe.axis("equal")
    axe.grid(True, linewidth=0.3, alpha=0.3)

    fig.savefig(cheminPng, dpi=200, bbox_inches="tight")
    plt.close(fig)

    return fig, axe


def afficherSolution(
    points,
    solution,
    titre,
    cheminPng,
):
    n = points.shape[0]
    ensembleStations = set(solution["stations"])

    fig, axe = plt.subplots(figsize=(9, 7))
    axe.scatter(
        points[:, 0],
        points[:, 1],
        s=18,
        c="tab:blue",
        alpha=0.7,
        label="Villes",
    )
    axe.scatter(
        points[list(ensembleStations), 0],
        points[list(ensembleStations), 1],
        s=55,
        c="tab:red",
        label="Stations",
    )

    cycleStations = solution["cycleStations"]
    if len(cycleStations) >= 2:
        for stationA, stationB in zip(
            cycleStations,
            cycleStations[1:] + [cycleStations[0]],
        ):
            axe.plot(
                [points[stationA, 0], points[stationB, 0]],
                [points[stationA, 1], points[stationB, 1]],
                color="black",
                linewidth=2.2,
            )

    for indiceVille in range(n):
        stationAffectee = solution["affectation"][indiceVille]
        if indiceVille == stationAffectee:
            continue
        axe.plot(
            [points[indiceVille, 0], points[stationAffectee, 0]],
            [points[indiceVille, 1], points[stationAffectee, 1]],
            color="gray",
            linestyle="--",
            linewidth=0.8,
            alpha=0.5,
        )

    axe.set_title(titre)
    axe.legend()
    axe.axis("equal")
    axe.grid(True, linewidth=0.3, alpha=0.3)

    fig.savefig(cheminPng, dpi=200, bbox_inches="tight")
    return fig, axe
