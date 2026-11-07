# v1.4 verification — 2026-11-06

## Gameplay and compatibility
- 21 unittest methods passed (17.11 seconds in the final recorded full run). The campaign suites exercise all 76 missions: original 24, Greenline 16, expedition 28, Workshop first four and second four.
- Preserved legacy-save migration, damaged-save recovery, editor controls, route validation, rover delivery/replay, physical gates and repeat-XP checks.
- New tests walk to the actual Astra Workshop entrance and traverse the second wing, verify gates, reject starter/incorrect programs, reopen diagnostics and reload after every new mission. Earlier drafts and XP survive.
- Exact custom exception type, inheritance, delegated battery consumption and unclosed file handles are checked. All file fixtures are temporary.
- Tests verify that a legacy position inside a new prop can escape without resetting the profile.

## Native Windows
- Eight Workshop missions executed through the editor on the Windows display driver. Machine rendering, world arrivals, resize, saved return and quit passed.
- Measured 360-frame update/render average: 6.00 ms; maximum: 7.44 ms. This measures the scripted test on this machine, not guaranteed end-user performance.
- Native restored-Workshop and service-log diagnostics screenshots were captured at 1280×720, 1600×900 and 1920×1080.

## Visual evidence
- 36 AFTER screenshots: six locations × three requested resolutions × two collision-free player/camera positions. All use the actual native Pygame window, not mockups.
- 36 BEFORE screenshots captured from the retained v1.3 source using the same camera-test procedure. Camera/player coordinates and output dimensions are recorded in each manifest. The Workshop's camera behavior intentionally differs in v1.4.
- Reviewed all current captures through six contact sheets, plus full-size Orion, Workshop, Astra and other-world images. Before/after comparison shows the removed Orion overlays. The image archive includes originals, contact sheets and the separate restored-machine/interface captures.
- Inspection led to fixes for craters covering rock walls, oversized dark Workshop floor blocks, blocked legacy positions, and Workshop consoles being cut off while walking the service route.
- HUD and controls remain within letterboxed bounds at all three resolutions. Offscreen scenery is intentionally cropped at the viewport; screenshots do not establish coverage of every possible camera position or dynamic state.
- The matrix uses disposable fresh visual profiles positioned for inspection; it is not presented as a manual human campaign playthrough. Restored Workshop captures come from the native scripted completion of all eight missions.

## Reproduce
```
runtime\python.exe -m unittest discover -s tests -v
runtime\python.exe tools\check_content.py
runtime\python.exe tools\native_visual_revision.py
runtime\python.exe tools\visual_matrix.py --output visual-captures
```

## Packaging
Windows and source archive integrity checks passed. The extracted Windows package passed all three new regression methods. Its actual batch launcher opened a native window, exited normally and wrote the disposable save. The independent original-content validator also passed all 24 reference solutions and six map schemas.

The biomedical examples remain synthetic educational models. The code worker is a separate process with a timeout, not a hardened security sandbox. No live player save was changed by these tests.

