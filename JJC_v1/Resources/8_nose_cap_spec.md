# Nose Cap Spec

## Purpose

The nose cap is the printed impact cap at the top end of the JJC V1 club. It protects the dowel end, closes the upper body shell, and gives the club a finished nose.

Reference diagram:

```text
Resources/Images/8_nose_cap_fit.svg
```

## Part Function

- Fits over the end of the 1/2 inch dowel rod
- Connects conceptually to the nose-side end of Part 7
- Protects the dowel end from impacts
- Finishes the top end of the club body

## Version 1 Geometry

Basic shape: short cylindrical TPU cap with a blind dowel socket

Suggested starting dimensions:

| Feature | Value | Notes |
| --- | ---: | --- |
| Outer diameter | 32 mm | Matches the nose-side outer diameter of Part 7 |
| Dowel socket diameter | 13.2 mm | 12.7 mm dowel plus 0.5 mm clearance |
| Cap height | 30 mm | First impact-cap test |
| Socket depth | 22 mm | Leaves 8 mm of solid TPU at the closed end |
| Closed end thickness | 8 mm | Impact material at nose tip |

## Dowel Fit

Use the same dowel clearance as the other dowel-fitting parts:

```text
1/2 inch dowel = 12.7 mm
clearance = 0.5 mm
socket diameter = 13.2 mm
```

The socket is blind, so the dowel does not pass all the way through the cap.

## Fit To Nearby Parts

The outer diameter should align with Part 7:

```text
Part 7 nose-side outer diameter = 32 mm
Part 8 outer diameter = 32 mm
```

This version does not include a locking joint yet.

## Print Material

Preferred material:

```text
TPU
```

Reasons:

- absorbs impacts
- protects the dowel end
- consistent with the body and handle parts

## Print Orientation

Recommended first print orientation:

```text
closed nose end on the XY plane, socket opening upward
```

This gives the cap a solid base on the print bed and avoids support inside the dowel socket.

## First Test Goals

The first print should answer:

- Does the socket fit the dowel?
- Does the 32 mm diameter align visually with Part 7?
- Is 8 mm enough closed-end material for impact protection?
- Does the cap feel too small, too large, or about right?

## Fusion Script Parameters

Use named variables in the script:

```python
outer_diameter_mm = 32.0
dowel_diameter_mm = 12.7
dowel_clearance_mm = 0.5
cap_height_mm = 30.0
socket_depth_mm = 22.0
```

Derived values:

```python
socket_diameter_mm = dowel_diameter_mm + dowel_clearance_mm
closed_end_thickness_mm = cap_height_mm - socket_depth_mm
```

Fusion API note:

```text
Fusion internal length units are centimeters.
Convert mm to cm by dividing by 10.
```

## Open Questions

- Should the nose cap become more rounded in a later version?
- Should the nose cap overlap Part 7 instead of just matching its diameter?
- Should the socket be glued to the dowel or remain removable?
- Is 30 mm a good cap height for practice juggling?
