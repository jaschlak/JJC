# Knob Cap Spec

## Purpose

The knob cap is the printed end cap at the handle end of the JJC V1 club. It protects the end of the dowel rod, gives the club a rounded handle end, and provides an impact-tolerant TPU bumper.

Reference diagram:

```text
Resources/Images/4_knob_cap_fit.svg
```

## Part Function

- Fits over the end of the 1/2 inch dowel rod
- Protects the dowel end from impacts
- Creates a rounded, larger knob at the handle end
- Helps keep the club comfortable and safer to catch

## Version 1 Geometry

Basic shape: short cylindrical cap with a blind dowel socket

Suggested starting dimensions:

| Feature | Value | Notes |
| --- | ---: | --- |
| Outer diameter | 34 mm | Larger than the handle sleeve so it acts as a stop/knob |
| Dowel socket diameter | 13.2 mm | 12.7 mm dowel plus 0.5 mm clearance |
| Cap height | 28 mm | Short first-print test |
| Socket depth | 22 mm | Leaves 6 mm of material at the closed end |
| Edge treatment | 1 mm chamfer | Reduces sharp TPU edges |

## Dowel Fit

Use the same dowel clearance as Parts 2 and 3:

```text
1/2 inch dowel = 12.7 mm
clearance = 0.5 mm
socket diameter = 13.2 mm
```

The socket is blind, so the dowel does not pass all the way through the knob cap.

## Print Material

Preferred material:

```text
TPU
```

Reasons:

- absorbs drops and impacts
- feels better in the hand than rigid plastic
- can flex slightly around the dowel

## Print Orientation

Recommended first print orientation:

```text
closed end on the bed, socket opening upward
```

This keeps the solid closed end on the XY plane and leaves the dowel socket opening upward.

## First Test Goals

The first print should answer:

- Does the socket fit the dowel?
- Is the cap too loose, too tight, or about right?
- Is 34 mm a reasonable knob diameter?
- Does the cap feel comfortable at the handle end?
- Does TPU make a good impact bumper for this shape?

## Fusion Script Parameters

Use named variables in the script:

```python
outer_diameter_mm = 34.0
dowel_diameter_mm = 12.7
dowel_clearance_mm = 0.5
cap_height_mm = 28.0
socket_depth_mm = 22.0
edge_chamfer_mm = 1.0
```

Derived value:

```python
socket_diameter_mm = dowel_diameter_mm + dowel_clearance_mm
```

Fusion API note:

```text
Fusion internal length units are centimeters.
Convert mm to cm by dividing by 10.
```

## Open Questions

- Is 34 mm a good knob diameter?
- Should the knob be more rounded in a later version?
- Should the socket be slip fit, snug fit, or glued?
- Should the cap include a mechanical retention feature later?
