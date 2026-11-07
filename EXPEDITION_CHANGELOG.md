# Expedition release 1.2
Built directly on the Greenline source. The original 40 missions remain playable.

- Five-destination star map, saved world positions, return travel and clearly marked Expedition Preview access.
- Sixteen Orion missions covering graphs, BFS/DFS, weighted paths, scheduling, coordinate transforms, tolerances, collision checks, rerouting, heuristic checks, caching and dependencies.
- Route validation in both worker and game. Docking awards XP. Saved deliveries resume. Step replay shows positions and cumulative costs.
- Persistent three-phase convoy recovery. Cargo and a trailing escort follow the validated final path.
- Four Titan missions with offline packet framing, validation, topic routing and delivery policy.
- Four Helix missions with synthetic toy pulses, timestamps, baseline estimates and reproducible noise.
- Four Aurora missions with sample records, cursor interpolation, transforms and quality filtering on a rotating toy chamber.
- Planet surveys, ION dialogue, survey archives and two-axis camera following.
- Schema 3 to 4 migration with a pre-upgrade backup and retained unknown fields.

## Remaining work
84 missions remain. Workshop District, Algorithm Tower and Mission Control Annex each need 16. Titan, Helix and Aurora each need their remaining 12.

Orion's benchmark teaches operation-count models rather than measuring actual runtime. The landslide task uses a supplied updated map. Dynamic terrain changes during a delivery remain future work. The final convoy shares one route with staggered movement.

Advanced signal processing, voltage/LAT interpolation, async/concurrency curricula, richer exploration, scalable text and rebindable controls remain future work. All biomedical-themed data is synthetic and educational.
