# V3 Upper Hollow Body Shell Spec

## Purpose

The upper body shell forms the upper half of the hollow club body. It receives the Part 5 slip lip at the bottom and closes the body near the nose.

It has a receiving slip socket, an insert that slides into Part 5, a minimal wall-supported connector ramp, and a closed top with a dowel clearance hole.

Reference diagram:

```text
Resources/Images/6_upper_body_shell_fit.svg
```

## Geometry

```text
Start Z: 348 mm
End Z: 490 mm
Height: 142 mm
Start outer diameter: 78 mm
Belly outer diameter: 66 mm
Top outer diameter: 40 mm
Wall thickness: 1.6 mm
Internal cavity diameter at bottom before socket: 74.8 mm
Internal cavity diameter at belly: 62.8 mm
Internal cavity diameter near top: 36.8 mm
Bottom: mostly open around the Part 5 insert
Insert hub height inside Part 6: 2 mm
Part 5 insert depth: 10 mm
Part 5 insert outer diameter: 69.4 mm
Part 5 insert inner diameter: 64.4 mm
Thickened insert wall thickness: 2.5 mm
Insert-to-shell main flare height: 7 mm
Insert-to-shell wall blend height: 10 mm
Receiving socket depth: 10 mm
Receiving socket inner diameter: 74.4 mm
Receiving socket outer diameter: 76.4 mm
Receiving socket wall thickness: 1.0 mm minimum
Top plate thickness: 3 mm
Top dowel clearance hole: 13.2 mm
Bottom edge chamfer: 0.6 mm
```

The upper wall is thinner than the lower wall to reduce top mass and keep the balance point out of the nose-heavy range.

## Hollow Interior

This part is a hollow shell, not a solid body.

```text
Main body wall: annular 1.6 mm shell
Interior cavity: open around the lower insert until the 3 mm top plate
Bottom receiving opening: 74.4 mm ID at the socket around the insert
Lower closure: none across the full body diameter
Part 5 stabilizing insert: straight thickened hollow sleeve, 69.4 mm OD x 64.4 mm ID x 10 mm deep, continuing 2 mm into Part 6 as a hub
Insert-to-shell flare: short conical sleeve from the insert hub toward the normal Part 6 shell wall, followed by a small outer-wall blend profile so the sleeve does not end as a blunt flat ring
Bottom receiving socket: reinforced by a full annular wall from 76.4 mm OD to 74.4 mm ID for improved shell rigidity and better fit to Part 5
Top closure: 3 mm plate with only the 13.2 mm dowel clearance hole; interior top edge includes a 1 mm sloped transition between the top disk and outer wall for printability
Full-length center sleeve: none
Infill inside body cavity: none intended
```

In Fusion, the main body should be made as an outer solid loft followed by an explicit internal cavity loft cut. This avoids export/import ambiguity where another CAD program may interpret an annular loft as filled.

## Joint To Part 5

```text
Part 5 male lip OD: 74.0 mm
Part 6 receiving socket ID: 74.4 mm
Diametral clearance: 0.4 mm
Radial clearance: 0.2 mm per side
Overlap depth: 10 mm
Part 6 stabilizing insert OD: 69.4 mm
Part 6 stabilizing insert ID: 64.4 mm
Part 5 male lip ID: 70.0 mm
Insert diametral clearance: 0.6 mm
```

The joint is meant to locate the shells and resist side movement. Part 6's straight 69.4 mm hollow insert reaches into Part 5's 70.0 mm lip opening. The thickened insert and shorter flared sleeve hub add joint stiffness without filling the lower end of Part 6 with a broad disk. Bond the overlap with flexible adhesive if the shell should be permanent.

## Balance Role

Estimated contribution:

```text
Upper shell walls: 33.8 g combined
Upper top plate: 3.6 g
Upper receiving socket wall: 2.3 g
Lower insert and flared sleeve: adds joint stiffness with much less mass than a full stabilizing disk
```

The 1.6 mm wall is the main V3 balance change. Increasing this wall moves the center of rotation upward; decreasing it moves the center downward.

## Print Orientation

Print top down.

```text
Closed top on the bed
Straight thickened hollow insert printed near the top of the print
The main flare reaches its shoulder 5 mm above the insert hub, then blends into the wall over the next 3 mm to reduce the abrupt shelf at the shell wall
```
