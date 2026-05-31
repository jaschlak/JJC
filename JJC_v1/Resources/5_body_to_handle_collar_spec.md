# Body-to-Handle Collar Spec

## Purpose

The body-to-handle collar is the transition piece between the narrow handle sleeve and the wider club body. It helps define the club shape and gives the lower body shell a larger surface to connect to.

Reference diagram:

```text
Resources/Images/5_body_to_handle_collar_fit.svg
```

## Part Function

- Slides over the 1/2 inch dowel rod
- Sits above the handle sleeve
- Flares from handle diameter toward body diameter
- Provides a transition surface for the future lower body shell
- Helps test the feel of the handle-to-body shape

## Version 1 Geometry

Basic shape: tapered collar with a center dowel hole

Suggested starting dimensions:

| Feature | Value | Notes |
| --- | ---: | --- |
| Handle-side outer diameter | 24 mm | Matches the first handle sleeve outer diameter |
| Body-side outer diameter | 42 mm | First estimate for the lower club body transition; starts on the XY plane |
| Inner diameter | 13.2 mm | 12.7 mm dowel plus 0.5 mm clearance |
| Height | 35 mm | Short enough for a fast test print |
| Edge treatment | 0.75 mm chamfer | Reduces sharp TPU edges |

## Dowel Fit

Use the same dowel clearance as Parts 2, 3, and 4:

```text
1/2 inch dowel = 12.7 mm
clearance = 0.5 mm
inner diameter = 13.2 mm
```

## Fit To Nearby Parts

The handle-side diameter should align with the handle sleeve:

```text
handle sleeve outer diameter = 24 mm
collar handle-side outer diameter = 24 mm
```

The body-side diameter is a placeholder for the future lower body shell:

```text
collar body-side outer diameter = 42 mm
```

This can be adjusted after the first body shell dimensions are chosen.

## Print Material

Preferred material:

```text
TPU
```

Reasons:

- impact tolerant
- flexible enough for fitting around the dowel
- consistent with the handle sleeve and knob cap

## Print Orientation

Recommended first print orientation:

```text
standing vertically with the wider 42 mm body side on the bed
```

Benefits:

- wider base improves bed contact
- center hole prints vertically
- no support should be needed for the taper

## First Test Goals

The first print should answer:

- Does the collar slide onto the dowel?
- Does 24 mm line up well with the handle sleeve?
- Does 42 mm feel like a reasonable start for the body transition?
- Does the taper print cleanly in TPU?
- Does the part feel too tall, too short, too steep, or about right?

## Fusion Script Parameters

Use named variables in the script:

```python
handle_side_outer_diameter_mm = 24.0
body_side_outer_diameter_mm = 42.0
dowel_diameter_mm = 12.7
dowel_clearance_mm = 0.5
collar_height_mm = 35.0
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

- Is 42 mm a good starting diameter for the body side?
- Should the taper be straight, curved, or stepped?
- Should this part mechanically lock to the lower body shell?
- Should the collar be bonded to the dowel or remain removable?
