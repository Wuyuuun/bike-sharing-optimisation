# Bike-Sharing Deployment and Rebalancing

A two-stage optimisation model for a shared-bicycle system: where to put the stations and how
many bikes to seed them with, and then how to move bikes between them during the day so that
riders do not arrive at an empty rack.

**Team:** Turing Team — regional mathematical modelling project, 2025
**Area studied:** Taipa, Macau

## The two problems

**Stage 1 — deployment.** Choose station locations and initial bike counts. Service quality is
not uniform across a city: a rack beside a residential block empties in the morning and fills in
the evening, while one in a tourist area does the opposite. The model partitions the district
into residential, tourist and transport-hub zones and treats those demand patterns as different
rather than averaging them away. The objective is to minimise the service gap — the expected
demand that cannot be served — subject to a fixed budget of stations and bikes.

**Stage 2 — rebalancing.** Once the stations are seeded, bikes still drift out of balance during
the day. The rebalancing model routes a fleet of trucks between stations to correct this,
balancing transport cost against a penalty for stations left unserved, and allowing more than
one truck so that the routes have to be coordinated.

## What is in this repository

| Path | What it is |
|---|---|
| `paper/paper.pdf` | The full written report |
| `code/allocation_gurobi.py` | The deployment model: a `BikeAllocationSolver` class building the mixed-integer programme in Gurobi |
| `code/rebalancing_pulp.py` | The rebalancing model: station coordinates, demand, and the multi-truck routing model in PuLP |
| `source/` | Complete LaTeX source (`main.tex`, `sections/`, `myClass.cls`, `ref.bib`) |

The code in `code/` is the same code that appears as listings in the paper, extracted here so it
can be read and run directly rather than through the document.

## Method

- **Mixed-integer programming** for station siting and initial allocation, with the service gap
  as the objective.
- **Directed graph / vehicle routing** for the rebalancing stage, with transport cost and
  unserved-station penalty combined into a single objective.
- **Sensitivity analysis** on the budget and demand parameters, to check which assumptions the
  result actually depends on.

## Tools

Python (Gurobi, PuLP, NumPy), LaTeX.

## Note on language

The report and the code comments are in Chinese. The model structure, the code and the figures
are readable without it; an English summary is available on request.
