# Dowel Rod Spec

## Purpose

The dowel rod is the rigid center spine of the JJC V1 juggling club. Printed parts are designed to slide over, grip, or align around this rod.

## Recommended V1 Size

Use a 1/2 inch dowel rod for the first prototype.

```text
1/2 inch = 12.7 mm
```

Recommended design value:

```text
dowel diameter = 12.7 mm
```

## Why 1/2 Inch

A 1/2 inch dowel is a good first choice because it is:

- easy to find
- stiff enough for a first club prototype
- not excessively heavy
- large enough to design printed sleeves and rings around
- simple to measure and replace

## Material

Recommended first material:

```text
hardwood dowel
```

Possible later alternatives:

- fiberglass rod
- carbon fiber tube or rod
- aluminum tube

For V1, use a simple hardwood dowel unless there is a clear reason to change.

## Measurement Requirement

Measure the actual dowel with calipers before finalizing printed parts.

Even if the dowel is sold as 1/2 inch, the actual diameter may vary slightly.

Record:

```text
measured dowel diameter = ____ mm
```

Use the measured value in Fusion scripts instead of assuming exactly 12.7 mm.

## Printed-Part Clearance

For parts that slide over the dowel, use:

```text
hole diameter = measured dowel diameter + clearance
```

Suggested first clearance for TPU:

```text
0.5 mm total clearance
```

Example using nominal 1/2 inch dowel:

```text
12.7 mm dowel + 0.5 mm clearance = 13.2 mm hole
```

## Length

The final dowel length depends on the final club length.

For the first design phase, model the dowel as a reference cylinder running through:

- knob cap
- handle sleeve
- body-to-handle collar
- body shell
- nose cap

Leave final length open until the overall club proportions are chosen.

## Open Questions

- What is the actual measured dowel diameter?
- What total club length should V1 target?
- Should the dowel run all the way into the nose cap?
- Should printed parts be removable from the dowel or permanently bonded?
- Should the dowel be wood for V1 or should we move to a tube/rod material later?
