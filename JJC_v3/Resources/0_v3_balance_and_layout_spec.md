# JJC V3 Balance And Layout Spec

## Goal

Create a lighter hollow-body club that does not feel top-heavy in rotation.

V3 keeps the V2 overall length and handle layout, but changes the two body shells to hollow printed shells with an overlapping slip joint.

Reference diagram:

```text
Resources/Images/JJC_v3_hollow_body_concept.svg
```

## Balance Target

There is not a single official center-of-rotation standard for juggling clubs. For this project, use this practical target:

```text
Target balance point: 255-265 mm from knob end
Target balance ratio: 51-53% of total length from knob end
Overall length: 502 mm
```

This keeps the center of rotation slightly above the midpoint, near the body, but not close to the nose.

## V2 Estimate

Using the V2 dimensions and estimated material densities:

```text
Estimated V2 mass: 295.5 g
Estimated V2 balance point: 272.1 mm from knob end
Estimated V2 balance ratio: 54.2% of total length
```

That is higher than the V3 target.

## V3 Estimate

Using hollow body shells, no full-length body dowel sleeves, and the wall thicknesses below:

```text
Part 5 lower body wall thickness: 2.0 mm
Part 6 upper body wall thickness: 1.6 mm
Estimated V3 mass: 266.1 g
Estimated V3 balance point: 260.6 mm from knob end
Estimated V3 balance ratio: 51.9% of total length
```

The estimate assumes:

```text
Hardwood dowel density: 0.70 g/cm^3
TPU/plastic density: 1.20 g/cm^3
Dowel diameter: 12.7 mm
Dowel length: 502 mm
V2 knob, handle, collar, and nose cap dimensions unchanged
Part 5 and Part 6 are hollow shells
Part 5 has a closed bottom plate
Part 6 has a closed top plate
Part 5/6 joint uses a 10 mm overlap
```

## V3 Axial Layout

```text
Part 2 knob cap: 0-28 mm
Part 3 handle sleeve: 28-213 mm
Part 4 handle-to-body collar: 213-233 mm
Part 5 lower hollow body shell: 233-348 mm
Part 6 upper hollow body shell: 348-490 mm
Part 7 nose cap: 490-502 mm
```

## Tuning Rules

After printing one assembled club, balance it on a pencil or round rod and measure from the knob end.

```text
If balance is above 265 mm:
- reduce Part 6 wall thickness by 0.2 mm
- reduce Part 6 top plate thickness by 0.5-1.0 mm
- or add weight near the knob/handle

If balance is below 255 mm:
- increase Part 6 wall thickness by 0.2 mm
- increase Part 6 top plate thickness by 0.5 mm
- or reduce Part 5 wall thickness by 0.2 mm
```

Do not tune balance by making the nose cap heavy unless needed for durability. Nose mass has a large effect on spin feel.
