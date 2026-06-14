# V3 Lower Hollow Body Shell Spec

## Purpose

The lower body shell forms the lower half of the hollow club body. It starts at the handle-to-body collar and expands to the widest body section.

It has a closed bottom, an open top, and a male slip-joint lip that slides into Part 6.

Reference diagram:

```text
Resources/Images/5_lower_body_shell_fit.svg
```

## Geometry

```text
Start Z: 233 mm
End Z: 348 mm
Height: 115 mm
Start outer diameter: 42 mm
Belly outer diameter: 70 mm
Top outer diameter: 78 mm
Wall thickness: 2.0 mm
Internal cavity diameter at bottom: 38.0 mm
Internal cavity diameter at belly: 66.0 mm
Internal cavity diameter at top before slip lip: 74.0 mm
Bottom plate thickness: 4 mm
Bottom dowel clearance hole: 13.2 mm
Top: open
Male slip lip height: 10 mm
Male slip lip outer diameter: 74.0 mm
Male slip lip wall thickness: 2.0 mm
Male slip lip inner diameter: 70.0 mm
Top edge chamfer: 0.6 mm
```

The lower wall is intentionally thicker than the upper wall. It moves mass downward relative to the upper shell and helps keep the finished club balance near the V3 target.

## Hollow Interior

This part is a hollow shell, not a solid body.

```text
Main body wall: annular 2.0 mm shell
Interior cavity: open above the 4 mm bottom plate
Bottom closure: 4 mm plate with only the 13.2 mm dowel clearance hole
Top opening through slip lip: 70.0 mm ID
Full-length center sleeve: none
Infill inside body cavity: none intended
```

In Fusion, the main body should be made as an outer solid loft followed by an explicit internal cavity loft cut. This avoids export/import ambiguity where another CAD program may interpret an annular loft as filled.

## Joint To Part 6

```text
Part 5 male lip OD: 74.0 mm
Part 6 receiving socket ID: 74.4 mm
Diametral clearance: 0.4 mm
Radial clearance: 0.2 mm per side
Overlap depth: 10 mm
Part 5 male lip ID: 70.0 mm
Part 6 stabilizing insert OD: 69.4 mm
Part 6 stabilizing insert ID: 64.4 mm
Insert diametral clearance inside Part 5 lip: 0.6 mm
```

This should be a slide fit, not a press fit. Part 6 now stabilizes the joint with a straight thickened hollow insert that slides into the open center of the Part 5 lip. If the printer makes TPU oversized, reduce the Part 6 insert OD slightly.

## Balance Role

Estimated contribution:

```text
Lower shell walls: 44.0 g combined
Lower bottom plate: 5.0 g
Lower male slip lip: 5.4 g
```

The 2.0 mm wall is part of the balance plan. Do not reduce it until a printed club has been weighed and balanced.

## Print Orientation

Print bottom down.

```text
Closed bottom on the bed
Open top upward
Slip lip printed at the top
```
