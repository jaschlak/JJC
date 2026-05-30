# Handle Sleeve Spec

## Purpose

The handle sleeve is the printed grip section that slides over the dowel rod. It gives the club a larger, more comfortable handle while using the dowel as the rigid center spine.

Reference diagram:

```text
Resources/Images/3_handle_sleeve_fit.svg
```

## Part Function

- Slides over the 1/2 inch dowel rod
- Provides the main hand grip area
- Adds diameter around the dowel without needing a solid printed handle
- Tests a longer TPU sleeve fit before designing the full club body

## Version 1 Geometry

Basic shape: hollow tube

Suggested starting dimensions:

| Feature | Value | Notes |
| --- | ---: | --- |
| Outer diameter | 24 mm | First grip-size test |
| Inner diameter | Dowel diameter + clearance | Matches the dowel centering ring hole |
| Length | 80 mm | Short enough for a first print, long enough to test grip feel |
| Edge treatment | Small chamfer | Helps the sleeve slide onto the dowel |

## Dowel Fit

Use the same starting clearance as the dowel centering ring:

```text
1/2 inch dowel = 12.7 mm
clearance = 0.5 mm
inner diameter = 13.2 mm
```

This should be a slip fit for TPU. If the sleeve is too loose, reduce clearance. If it is too tight, increase clearance.

## Print Material

Preferred material:

```text
TPU
```

Reasons:

- comfortable grip feel
- impact tolerant
- can flex slightly over the dowel

## Print Orientation

Recommended first print orientation:

```text
standing vertically on one end
```

Benefits:

- cleaner circular hole
- no support needed for a straight tube
- tests whether the printer handles a taller TPU sleeve well

If vertical TPU printing is unstable, test a shorter sleeve length before changing the part design.

## First Test Goals

The first print should answer:

- Does the sleeve slide onto the dowel?
- Is the grip diameter comfortable?
- Is 80 mm a useful test length?
- Does TPU print cleanly as a vertical tube?
- Does the sleeve twist or wobble on the dowel?

## Fusion Script Parameters

Use named variables in the script:

```python
outer_diameter_mm = 24.0
dowel_diameter_mm = 12.7
dowel_clearance_mm = 0.5
sleeve_length_mm = 80.0
edge_chamfer_mm = 0.75
```

Derived value:

```python
inner_diameter_mm = dowel_diameter_mm + dowel_clearance_mm
```

Fusion API note:

```text
Fusion internal length units are centimeters.
Convert mm to cm by dividing by 10.
```

## Open Questions

- Is 24 mm a comfortable grip diameter?
- Should the handle sleeve be one long piece or several shorter grip sections?
- Should the outside eventually have grooves, ribs, or a textured grip?
- Should the sleeve be removable or bonded to the dowel?
