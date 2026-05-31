# Upper Body Shell Spec

## Purpose

The upper body shell is the second hollow club-body section. It continues from the lower body shell toward the nose cap and helps complete the main club body volume.

Reference diagram:

```text
Resources/Images/7_upper_body_shell_fit.svg
```

## Part Function

- Forms the upper hollow body of the club
- Continues the body shape from Part 6
- Narrows toward the future nose cap
- Leaves internal room around the dowel and centering rings
- Tests a second tapered TPU shell section

## Version 1 Geometry

Basic shape: hollow tapered tube

Suggested starting dimensions:

| Feature | Value | Notes |
| --- | ---: | --- |
| Lower/wide outer diameter | 58 mm | Starts on the XY plane for better printing |
| Nose-side outer diameter | 32 mm | First estimate for transition toward the nose cap |
| Wall thickness | 2 mm | Matches Part 6 |
| Height | 120 mm | Same first-test height as Part 6 |
| Dowel sleeve inner diameter | 13.2 mm | 12.7 mm dowel plus 0.5 mm clearance |
| Dowel sleeve outer diameter | 20 mm | Structural tube bonded around dowel |
| Bulkhead height | 5 mm each | Internal disks connecting sleeve to shell |
| Edge treatment | 0.5 mm chamfer | Reduces sharp TPU edges |

## Orientation

The wide 58 mm side should start on the XY plane:

```text
wide body side = Z 0 / XY plane
nose-side 32 mm opening = top
```

This prints the part wide-side down for better bed contact.

## Fit To Nearby Parts

The lower/wide side should align with Part 6:

```text
Part 6 wide outer diameter = 58 mm
Part 7 lower/wide outer diameter = 58 mm
```

The nose-side opening is a placeholder for Part 8:

```text
Part 7 nose-side outer diameter = 32 mm
```

This version includes an integrated dowel sleeve and two internal bulkheads, so it is more than a loose outer shell.

## Structural Features

Part 7 now has:

- a center sleeve around the dowel
- a lower bulkhead near the wide body side
- an upper bulkhead near the nose-side opening

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
- consistent with the lower body shell

## Print Orientation

Recommended first print orientation:

```text
standing vertically with the wide 58 mm side on the bed
```

This gives the shell its largest bed contact area.

## First Test Goals

The first print should answer:

- Does the upper shell print cleanly in TPU?
- Does 2 mm wall thickness work for a taller tapered shell?
- Does the 32 mm nose-side opening look reasonable?
- Does the body shape pair well with Part 6?
- Is the combined body length moving toward a usable club shape?

## Fusion Script Parameters

Use named variables in the script:

```python
wide_outer_diameter_mm = 58.0
nose_side_outer_diameter_mm = 32.0
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
nose_side_inner_diameter_mm = nose_side_outer_diameter_mm - (wall_thickness_mm * 2)
```

Fusion API note:

```text
Fusion internal length units are centimeters.
Convert mm to cm by dividing by 10.
```

## Open Questions

- Is 32 mm a good starting diameter for the nose side?
- Should the upper shell be longer or shorter than Part 6?
- Should Part 6 and Part 7 eventually overlap or use a coupler?
- Should centering ring stops be added inside the shell later?
