# Greenline expansion — version 1.1

The existing Astra engine now includes a 16-mission Hydroponics chapter, for 40 playable missions overall.

- Five rover assignments progress from repeating moves to navigating branching grids with breadth-first search. Python runs in the worker. Both the worker and game validate the returned command list. Mica moves along the displayed rail and delivers a payload before XP and the next bulkhead unlock.
- Deliveries resume after quitting. Replays grant no additional mission XP.
- Added a 192 × 18 tile Hydroponics wing with four sectors, propagation racks, filtration works, reservoir controls and canopy machinery.
- Extended each original deck to 32 × 18 tiles with a connected observation or research alcove and a discoverable field log. Original mission coordinates and IDs are retained.
- Added MARA's contextual dialogue, the Greenline tram, sector travel through J then 7, a local survey with M, and a diagnostic lens reward that marks the grower's archive.
- Learner results select irrigated trays and drive live instrument displays. The valve and final recovery programs animate controller states. A pressure leak recalls the suit to safety, and the pump repair disables it.
- Added a two-stage canopy recovery encounter. The completed relay phase survives a restart.
- Added scrollable lesson briefs with F3/F4 and mouse wheel, camera following, and a chapter ending.
- Schema 2 profiles upgrade to schema 3 with a pre-upgrade backup. Existing XP, completion IDs, drafts, attempts, flags, settings and unknown fields are retained.

# Remaining expansion work

The planned 88-mission campaign has 48 missions remaining. Workshop District, Algorithm Tower and Mission Control Annex have yet to be built. Their OOP, file/database fixtures, advanced algorithm encounters and final Scheduler campaign remain in the attached design backlog.

Further polish includes configurable text-size presets, rebindable controls, music, richer character animation and deeper environmental interactions. The present maps use handcrafted bay layouts and original procedural pixel geometry. The Hydroponics boss has two persistent repair phases. Shield-energy progression and patrol enemies are future systems.

