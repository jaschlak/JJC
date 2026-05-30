# Dowel Centering Ring Spec

## Purpose

The dowel centering ring keeps the dowel rod aligned with the center axis of the JJC V1 juggling club body. It is the first printed test part for Jordan's Juggle Clubs.

Reference diagram:

```text
Resources/Images/2_dowel_centering_ring_fit.svg
```

## Part Function

- Slides over the dowel rod
- Fits inside a future hollow club body shell
- Holds the dowel near the center of the shell
- Provides a simple test for Fusion scripting, print tolerance, and TPU fit

## Version 1 Geometry

Basic shape: washer-like ring

Suggested starting dimensions:

| Feature | Value | Notes |
| --- | ---: | --- |
| Outer diameter | 35 mm | Placeholder until body shell diameter is chosen |
| Inner diameter | Dowel diameter + clearance | Measure the actual dowel before finalizing |
| Thickness | 6 mm | Tall enough to guide the dowel without taking long to print |
| Edge treatment | Small chamfer or fillet | Helps insertion and reduces sharp TPU edges |

## Dowel Fit

The inner diameter should be larger than the measured dowel diameter.

Suggested starting clearance:

| Material | Clearance |
| --- | ---: |
| TPU flexible slip fit | +0.3 mm to +0.6 mm |
| PETG/PLA slip fit | +0.2 mm to +0.4 mm |

Example:

If the dowel measures 12.7 mm:

```text
inner diameter = 13.2 mm
```

This gives 0.5 mm total clearance.

## Outer Fit

The outer diameter should eventually match the inside diameter of the club body shell.

For the first test print, use:

```text
outer diameter = 35 mm
```

Once the body shell is designed, update this to:

```text
outer diameter = shell inner diameter - clearance
```

Suggested shell clearance:

```text
0.3 mm to 0.8 mm total clearance
```

TPU can tolerate a tighter fit than rigid filament, but too tight may make assembly difficult.

## Print Material

Preferred first material:

```text
TPU
```

Reasons:

- matches the expected club material
- tests flexibility around the dowel
- allows slight compression during assembly

Alternative:

```text
PETG
```

PETG may be useful later if the centering ring needs more stiffness.

## Print Orientation

Print flat on the bed like a washer.

Benefits:

- no supports
- simple circular perimeters
- strongest layer layout for radial compression
- fast print

## First Test Goals

The first print should answer:

- Does the ring slide onto the dowel?
- Is the fit too loose, too tight, or about right?
- Does TPU flex enough to make assembly easy?
- Does the slicer preserve the hole size accurately?
- Does the outer diameter feel reasonable for a future body shell?

## Fusion Script Parameters

Use named variables in the script:

```python
outer_diameter_mm = 35.0
dowel_diameter_mm = 12.7
dowel_clearance_mm = 0.5
ring_thickness_mm = 6.0
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

- What is the actual measured dowel diameter?
- Should the ring be a loose slip fit, snug fit, or press fit?
- What should the first body shell inner diameter be?
- Should the ring eventually include cutouts to save material?
- Should the ring eventually include keyed alignment features?
