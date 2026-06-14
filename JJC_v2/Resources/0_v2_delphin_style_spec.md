# JJC V2 Delphin-Style Club Spec

## Goal

Create a light, juggleable, Delphin-style club around a 1/2 inch hardwood dowel.

The target is not to copy Henry's Delphin dimensions exactly. The useful reference points are:

- long training club length around 51 cm
- finished weight around 205 g
- rigid wood spine
- long handle
- slim, rounded body

## Target Geometry

```text
Overall length: 502 mm
Dowel diameter: 12.7 mm
Dowel clearance holes: 13.2 mm
Handle OD: 24 mm
Max body OD: 78 mm
Nose OD: 40 mm
Knob cap #6 screw pilot: 2.9 mm
Knob cap screw outer-clearance chamfer: 10.0 mm outside diameter to 2.9 mm pilot diameter
Nose cap screw clearance: 3.2 mm
Nose cap socket-side OD: 40 mm to match Part 6
Nose cap screw-side face diameter: 22 mm
Nose cap height: 12 mm
Nose cap screw head chamfer: 10.0 mm diameter x 2.0 mm deep
```

## Axial Layout

| Item | Part | Start Z | Length | End Z |
| ---: | --- | ---: | ---: | ---: |
| 2 | Knob cap | 0 mm | 28 mm | 28 mm |
| 3 | Handle sleeve | 28 mm | 185 mm | 213 mm |
| 4 | Handle-to-body collar | 213 mm | 20 mm | 233 mm |
| 5 | Lower body shell | 233 mm | 115 mm | 348 mm |
| 6 | Upper body shell | 348 mm | 142 mm | 490 mm |
| 7 | Nose cap | 490 mm | 12 mm | 502 mm |

The printed parts stack to 502 mm. The caps have blind sockets, so the dowel does not need to run through every last millimeter of printed bumper material.

## Estimated Balance

Using the documented V2 dimensions and estimated material densities:

```text
Hardwood dowel density assumption: 0.70 g/cm^3
TPU/plastic density assumption: 1.20 g/cm^3
Estimated V2 mass: 295.5 g
Estimated V2 balance point: 272.1 mm from knob end
Estimated V2 balance ratio: 54.2% of total length
```

This estimate is the club's center of mass along the dowel axis. It should be checked by balancing a printed assembly on a pencil or round rod.

## Body Shape

The V2 body uses a long slim Delphin-style profile:

```text
Collar end: 42 mm OD
Widest point: 78 mm OD
Nose end: 40 mm OD
Body shell wall: 1.2 mm
Internal sleeve OD: 17 mm
Internal sleeve ID: 13.2 mm
Bulkheads: 4 mm at shell ends
```

## Weight Tuning

The first prototype should be weighed after assembly. To reduce weight:

- reduce body shell wall from 1.2 mm to 1.0 mm
- reduce sleeve OD from 17 mm to 16 mm
- reduce cap closed-end thickness

To increase durability:

- increase body shell wall to 1.6 mm
- use 3 perimeters in the slicer
- increase bulkhead height from 4 mm to 6 mm

## Slicer Starting Point

Recommended Simplify3D starting profile:

```text
Layer height: 0.24-0.30 mm
Perimeters: 3
Infill: 10-15%
Top/bottom layers: 3
TPU speed: 25-35 mm/s if feeding reliably
```

Thin walls and rings may still print mostly as perimeters/gap fill. That is expected.
