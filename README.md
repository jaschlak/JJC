# JJC V1

Jordan's Juggle Clubs V1 is a 3D-printing and Fusion scripting project for designing a simple juggling club around a rigid 1/2 inch dowel rod spine.

V2 is started in `JJC_v2/` as a Delphin-style, dowel-core practice club targeting a 502 mm length.

V3 is started in `JJC_v3/` as a hollow-body revision focused on lowering the estimated center of rotation compared with V2.

The current version is intentionally non-electronic. There are no LEDs, microcontrollers, batteries, or diffusers in V1. The goal is to learn the CAD-to-print workflow and build up the club as small, testable parts.

## Design Direction

- Main structure uses a 1/2 inch dowel rod.
- Printed parts fit around or onto the dowel.
- Most printed parts are expected to be TPU.
- The club will be designed in sections because the printer build volume is limited.
- Each part gets a numbered resource spec and, when useful, a matching Fusion script.

## Balance Estimates

Center of rotation is documented as the estimated balance point along the club axis, measured from the knob end.

```text
V1 prototype estimate: 209.1 mm from knob, 50.6% of 413 mm prototype length
V2 estimate: 272.1 mm from knob, 54.2% of 502 mm length
V3 target: 255-265 mm from knob, 51-53% of 502 mm length
V3 estimate: 260.6 mm from knob, 51.9% of 502 mm length
```

These are calculated estimates using documented geometry and material density assumptions. The real value should be checked by balancing the assembled club on a pencil or round rod.

## Printer

Current printer:

```text
Creality Ender 3 V3 SE
Build volume: 220 x 220 x 250 mm
Direct extruder: suitable for TPU
```

TPU should be printed slower than the advertised maximum printer speed.

## Folder Layout

```text
Resources/
  0_parts_list.md
  1_dowel_rod_spec.md
  2_dowel_centering_ring_spec.md
  3_handle_sleeve_spec.md
  4_knob_cap_spec.md
  Images/

Fusion/
  JJCv1_1_dowel_rod/
  JJCv1_2_dowel_centering_ring/
  JJCv1_3_handle_sleeve/
  JJCv1_4_knob cap/
  JJCv1_9_full_club_assembly/
```

## Current Parts

### 1. Dowel Rod

The rigid spine of the club.

```text
1/2 inch = 12.7 mm
```

There is a Fusion script for creating the dowel rod as its own reference part.

Measure the actual dowel before finalizing printed fit dimensions.

### 2. Dowel Centering Ring

A washer-like part that slides over the dowel and helps keep it centered inside the future hollow club body.

### 3. Handle Sleeve

A hollow TPU grip sleeve that slides over the dowel.

### 4. Knob Cap

A TPU end cap with a blind socket for the dowel. This forms the rounded handle-end bumper.

### 9. Full Club Assembly

A Fusion assembly script creates the dowel rod, handle sleeve, knob cap, body-to-handle collar, lower body shell, upper body shell, and nose cap as separate components in one design.

## Fusion Workflow

Fusion scripts must be run from inside Autodesk Fusion, not from normal desktop Python.

To run a script:

1. Open Fusion.
2. Create or open a design.
3. Go to **Utilities > Add-Ins > Scripts and Add-Ins**.
4. Add the relevant script folder if it is not already listed.
5. Select the script.
6. Click **Run**.

Do not run the script with the normal VS Code Python play button. That will fail because regular Python cannot import Fusion's `adsk` module.

## Debugging

Use Fusion's VS Code attach workflow.

The Fusion-generated script folders may include:

```text
.vscode/launch.json
```

Use the attach configuration, usually connecting to:

```text
localhost:9000
```

If VS Code reports connection refused, Fusion's debug listener is not running.

## Units

Fusion's Python API uses centimeters internally.

The scripts use millimeter variables and convert them with:

```python
def mm_to_cm(value_mm):
    return value_mm / 10.0
```

## Notes

- Keep resource specs and Fusion scripts numbered to match the parts list.
- Prefer small test parts before large shell sections.
- Update specs when measurements from real printed parts show the fit needs adjustment.
