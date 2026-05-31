# Lower Body Shell Spec

## Purpose

The lower body shell is the first hollow club-body section above the body-to-handle collar. It begins defining the larger club body shape while keeping the dowel rod as the rigid center spine.

Reference diagram:

```text
Resources/Images/6_lower_body_shell_fit.svg
```

## Part Function

- Forms the lower hollow body of the club
- Fits around the dowel rod with internal space for centering rings
- Connects conceptually to the body-to-handle collar
- Tests TPU printing of a larger hollow tapered shell

## Version 1 Geometry

Basic shape: hollow tapered tube

Suggested starting dimensions:

| Feature | Value | Notes |
| --- | ---: | --- |
| Wide outer diameter | 58 mm | Starts on the XY plane for better printing |
| Collar-side outer diameter | 42 mm | Matches the body side of Part 5 |
| Wall thickness | 2 mm | First TPU shell test |
| Height | 120 mm | Fits comfortably in the printer height |
| Dowel sleeve inner diameter | 13.2 mm | 12.7 mm dowel plus 0.5 mm clearance |
| Dowel sleeve outer diameter | 20 mm | Structural tube bonded around dowel |
| Bulkhead height | 5 mm each | Internal disks connecting sleeve to shell |
| Edge treatment | 0.5 mm chamfer | Reduces sharp TPU edges |

## Orientation

The wide 58 mm side should start on the XY plane:

```text
wide body side = Z 0 / XY plane
collar-side 42 mm opening = top
```

This prints the part wide-side down for better bed contact.

## Fit To Nearby Parts

The collar-side opening should match Part 5:

```text
Part 5 body-side outer diameter = 42 mm
Part 6 collar-side outer diameter = 42 mm
```

This version includes an integrated dowel sleeve and two internal bulkheads, so it is more than a loose outer shell.

## Structural Features

Part 6 now has:

- a center sleeve around the dowel
- a lower bulkhead near the XY plane
- an upper bulkhead near the collar-side opening

These features create a force path:

```text
outer shell -> bulkheads -> dowel sleeve -> dowel rod
```

This should make the part more useful for a practice club than a plain hollow shell.

## Print Material

Preferred material:

```text
TPU
```

Reasons:

- impact tolerant
- flexible body feel
- suitable for dropped juggling props

## Print Orientation

Recommended first print orientation:

```text
standing vertically with the wide 58 mm side on the bed
```

This gives the shell its largest bed contact area.

## First Test Goals

The first print should answer:

- Does the hollow shell print cleanly in TPU?
- Is 2 mm wall thickness enough?
- Does 120 mm height print reliably?
- Does the taper feel reasonable for a club body?
- Does the 42 mm collar-side opening align visually with Part 5?

## Fusion Script Parameters

Use named variables in the script:

```python
wide_outer_diameter_mm = 58.0
collar_side_outer_diameter_mm = 42.0
wall_thickness_mm = 2.0
shell_height_mm = 120.0
dowel_diameter_mm = 12.7
dowel_clearance_mm = 0.5
dowel_sleeve_outer_diameter_mm = 20.0
lower_bulkhead_height_mm = 5.0
upper_bulkhead_height_mm = 5.0
edge_chamfer_mm = 0.5
```

Derived values:

```python
wide_inner_diameter_mm = wide_outer_diameter_mm - (wall_thickness_mm * 2)
collar_side_inner_diameter_mm = collar_side_outer_diameter_mm - (wall_thickness_mm * 2)
```

Fusion API note:

```text
Fusion internal length units are centimeters.
Convert mm to cm by dividing by 10.
```

## Open Questions

- Is 58 mm wide enough for the lower body?
- Is 120 mm a good first section height?
- Should wall thickness stay at 2 mm or increase for TPU?
- Should this part eventually include a socket, lip, or keyed joint for Part 5?
- Should centering ring stops be added inside the shell later?
