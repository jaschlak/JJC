# JJC V2

JJC V2 is a Delphin-style juggling club prototype: a long, light, dowel-core club intended to be good enough for actual juggling practice.

This is not a copy of Henry's geometry or branding. It uses the same broad category: a light composite club with a rigid center dowel, long handle, slim body, and replaceable printed end parts.

## Design Targets

| Feature | Target |
| --- | ---: |
| Overall length | 520 mm |
| Target finished weight | 200-220 g |
| Core | 12.7 mm hardwood dowel |
| Handle outside diameter | 24 mm |
| Maximum body outside diameter | 78 mm |
| Material | TPU printed parts around wood dowel |
| Printer | Creality Ender 3 V3 SE |

## Parts

| Item | Part | Length |
| ---: | --- | ---: |
| 1 | Dowel rod | 520 mm |
| 2 | Knob cap | 28 mm |
| 3 | Handle sleeve | 185 mm |
| 4 | Handle-to-body collar | 20 mm |
| 5 | Lower body shell | 115 mm |
| 6 | Upper body shell | 142 mm |
| 7 | Nose cap | 30 mm |

## Folder Layout

```text
Resources/
  0_v2_delphin_style_spec.md
  1_dowel_rod_spec.md
  2_knob_cap_spec.md
  3_handle_sleeve_spec.md
  4_handle_to_body_collar_spec.md
  5_lower_body_shell_spec.md
  6_upper_body_shell_spec.md
  7_nose_cap_spec.md
  Images/

Fusion/
  JJCv2_shared/
  JJCv2_0_delphin_style_club/
  JJCv2_1_dowel_rod/
  JJCv2_2_knob_cap/
  JJCv2_3_handle_sleeve/
  JJCv2_4_handle_to_body_collar/
  JJCv2_5_lower_body_shell/
  JJCv2_6_upper_body_shell/
  JJCv2_7_nose_cap/
```

## Fusion Scripts

The individual scripts and the full assembly script all import their geometry from:

```text
JJC_v2/Fusion/JJCv2_shared/jjc_v2_parts.py
```

Change dimensions and part geometry there first. The standalone scripts and assembly script will then use the same source.

Run the full assembly script from inside Autodesk Fusion:

```text
JJC_v2/Fusion/JJCv2_0_delphin_style_club
```

The full assembly script creates each club part as a separate Fusion component. Run it in a Hybrid Design or Assembly Design. A normal Part Design document only allows one component and will reject the assembly.

Run individual part scripts when preparing printable part files:

```text
JJC_v2/Fusion/JJCv2_1_dowel_rod
JJC_v2/Fusion/JJCv2_2_knob_cap
JJC_v2/Fusion/JJCv2_3_handle_sleeve
JJC_v2/Fusion/JJCv2_4_handle_to_body_collar
JJC_v2/Fusion/JJCv2_5_lower_body_shell
JJC_v2/Fusion/JJCv2_6_upper_body_shell
JJC_v2/Fusion/JJCv2_7_nose_cap
```

If you later want true Fusion components and joints, create a Hybrid Design or Assembly Design first and the scripts can be adapted for that workflow.

## Print Strategy

The full club is too long to print as one object. Print the TPU parts separately and assemble them onto the dowel:

1. Print a short fit test for the dowel hole before printing full parts.
2. Print the handle sleeve upright if the TPU is stable.
3. Print the body shells wide side down.
4. Use low infill where there is actual internal volume, but expect thin walls to print mostly as perimeters.
5. Weigh the finished club and tune shell wall thickness or cap thickness before printing a matched set.
