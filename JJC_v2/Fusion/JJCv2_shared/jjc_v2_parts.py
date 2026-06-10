"""Shared JJC V2 Fusion geometry builders."""

import math
import adsk.core
import adsk.fusion


DOWEL_DIAMETER_MM = 12.7
DOWEL_HOLE_DIAMETER_MM = 13.2

KNOB_HEIGHT_MM = 28.0
HANDLE_LENGTH_MM = 185.0
HANDLE_OUTER_DIAMETER_MM = 24.0
COLLAR_HEIGHT_MM = 20.0
LOWER_BODY_HEIGHT_MM = 115.0
UPPER_BODY_HEIGHT_MM = 142.0
NOSE_HEIGHT_MM = 12.0

Z_KNOB_MM = 0.0
Z_HANDLE_MM = Z_KNOB_MM + KNOB_HEIGHT_MM
Z_COLLAR_MM = Z_HANDLE_MM + HANDLE_LENGTH_MM
Z_LOWER_BODY_MM = Z_COLLAR_MM + COLLAR_HEIGHT_MM
Z_UPPER_BODY_MM = Z_LOWER_BODY_MM + LOWER_BODY_HEIGHT_MM
Z_NOSE_MM = Z_UPPER_BODY_MM + UPPER_BODY_HEIGHT_MM
TOTAL_LENGTH_MM = Z_NOSE_MM + NOSE_HEIGHT_MM

BODY_WALL_MM = 1.2
BODY_SLEEVE_OUTER_DIAMETER_MM = 17.0
BODY_BULKHEAD_HEIGHT_MM = 4.0

KNOB_SCREW_PILOT_DIAMETER_MM = 2.9
KNOB_SCREW_OUTER_CLEARANCE_DIAMETER_MM = 10.0
KNOB_SCREW_CHAMFER_DEPTH_MM = 4.0

NOSE_SCREW_CLEARANCE_DIAMETER_MM = 3.2
NOSE_SCREW_HEAD_CHAMFER_DIAMETER_MM = 10.0
NOSE_SCREW_HEAD_CHAMFER_DEPTH_MM = 2.0
SCREW_SIDE_FILLET_OFFSET_ONE_MM = 9.0
SCREW_SIDE_FILLET_OFFSET_TWO_MM = 10.0
SOCKET_SIDE_FILLET_OFFSET_ONE_MM = 18.0
SOCKET_SIDE_FILLET_OFFSET_TWO_MM = 3.0

DOWEL_PILOT_HOLE_DIAMETER_MM = 2.9
DOWEL_PILOT_HOLE_DEPTH_MM = 18.0


def mm_to_cm(value_mm):
    return value_mm / 10.0


def offset_plane(component, z_mm, name):
    if abs(z_mm) < 0.0001:
        return component.xYConstructionPlane

    plane_input = component.constructionPlanes.createInput()
    plane_input.setByOffset(
        component.xYConstructionPlane,
        adsk.core.ValueInput.createByReal(mm_to_cm(z_mm))
    )
    plane = component.constructionPlanes.add(plane_input)
    plane.name = name
    return plane


def circle_profile(component, z_mm, diameter_mm, name):
    sketch = component.sketches.add(offset_plane(component, z_mm, f'{name} plane'))
    sketch.name = name
    sketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0),
        mm_to_cm(diameter_mm / 2.0)
    )
    return sketch.profiles.item(0)


def annular_profile(component, z_mm, outer_mm, inner_mm, name):
    sketch = component.sketches.add(offset_plane(component, z_mm, f'{name} plane'))
    sketch.name = name
    center = adsk.core.Point3D.create(0, 0, 0)
    sketch.sketchCurves.sketchCircles.addByCenterRadius(
        center,
        mm_to_cm(outer_mm / 2.0)
    )
    sketch.sketchCurves.sketchCircles.addByCenterRadius(
        center,
        mm_to_cm(inner_mm / 2.0)
    )

    expected = math.pi * (
        mm_to_cm(outer_mm / 2.0) ** 2
        - mm_to_cm(inner_mm / 2.0) ** 2
    )
    return min(
        (sketch.profiles.item(index) for index in range(sketch.profiles.count)),
        key=lambda candidate: abs(candidate.areaProperties().area - expected)
    )


def extrude_body(component, profile, distance_mm, name):
    extrudes = component.features.extrudeFeatures
    extrude_input = extrudes.createInput(
        profile,
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    extrude_input.setDistanceExtent(
        False,
        adsk.core.ValueInput.createByReal(mm_to_cm(distance_mm))
    )
    feature = extrudes.add(extrude_input)
    feature.name = f'{name} feature'
    body = feature.bodies.item(0)
    body.name = name
    return body


def join_extrude(component, profile, distance_mm, name):
    extrudes = component.features.extrudeFeatures
    extrude_input = extrudes.createInput(
        profile,
        adsk.fusion.FeatureOperations.JoinFeatureOperation
    )
    extrude_input.setDistanceExtent(
        False,
        adsk.core.ValueInput.createByReal(mm_to_cm(distance_mm))
    )
    feature = extrudes.add(extrude_input)
    feature.name = f'{name} feature'
    return feature


def cut_body(component, profile, distance_mm, name):
    extrudes = component.features.extrudeFeatures
    extrude_input = extrudes.createInput(
        profile,
        adsk.fusion.FeatureOperations.CutFeatureOperation
    )
    extrude_input.setDistanceExtent(
        False,
        adsk.core.ValueInput.createByReal(mm_to_cm(distance_mm))
    )
    feature = extrudes.add(extrude_input)
    feature.name = f'{name} feature'
    return feature


def loft_body(component, profiles, name):
    lofts = component.features.loftFeatures
    loft_input = lofts.createInput(
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    for profile in profiles:
        loft_input.loftSections.add(profile)
    feature = lofts.add(loft_input)
    feature.name = f'{name} feature'
    body = feature.bodies.item(0)
    body.name = name
    return body


def loft_cut(component, profiles, name):
    lofts = component.features.loftFeatures
    loft_input = lofts.createInput(adsk.fusion.FeatureOperations.CutFeatureOperation)
    for profile in profiles:
        loft_input.loftSections.add(profile)
    feature = lofts.add(loft_input)
    feature.name = f'{name} feature'
    return feature


def revolve_body(component, profile, axis, name):
    revolves = component.features.revolveFeatures
    revolve_input = revolves.createInput(
        profile,
        axis,
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    revolve_input.setAngleExtent(
        False,
        adsk.core.ValueInput.createByReal(math.pi * 2.0)
    )
    feature = revolves.add(revolve_input)
    feature.name = f'{name} feature'
    body = feature.bodies.item(0)
    body.name = name
    return body


def shell_inner_diameter(outer_mm):
    return outer_mm - (BODY_WALL_MM * 2.0)


def cap_screw_side_face_diameter(outer_diameter_mm):
    return max(
        KNOB_SCREW_OUTER_CLEARANCE_DIAMETER_MM + 5.0,
        outer_diameter_mm - (SOCKET_SIDE_FILLET_OFFSET_ONE_MM * 2.0)
    )


def cap_socket_side_face_diameter(outer_diameter_mm):
    return max(
        DOWEL_HOLE_DIAMETER_MM + 5.0,
        outer_diameter_mm - (SCREW_SIDE_FILLET_OFFSET_ONE_MM * 2.0)
    )


def create_dowel_rod(component, z_offset_mm=0.0, include_pilot_holes=False):
    body = extrude_body(
        component,
        circle_profile(component, z_offset_mm, DOWEL_DIAMETER_MM, 'V2 dowel rod profile'),
        TOTAL_LENGTH_MM,
        'V2 Item 1 - Dowel rod'
    )

    if include_pilot_holes:
        cut_body(
            component,
            circle_profile(
                component,
                z_offset_mm,
                DOWEL_PILOT_HOLE_DIAMETER_MM,
                'Bottom dowel screw pilot profile'
            ),
            DOWEL_PILOT_HOLE_DEPTH_MM,
            'Bottom dowel screw pilot hole'
        )
        cut_body(
            component,
            circle_profile(
                component,
                z_offset_mm + TOTAL_LENGTH_MM - DOWEL_PILOT_HOLE_DEPTH_MM,
                DOWEL_PILOT_HOLE_DIAMETER_MM,
                'Top dowel screw pilot profile'
            ),
            DOWEL_PILOT_HOLE_DEPTH_MM,
            'Top dowel screw pilot hole'
        )

    return body


def create_knob_cap(component, z_offset_mm=0.0):
    outer_diameter_mm = 33.0
    socket_depth_mm = 22.0
    closed_end_mm = KNOB_HEIGHT_MM - socket_depth_mm

    body = loft_body(
        component,
        [
            circle_profile(
                component,
                z_offset_mm,
                cap_screw_side_face_diameter(outer_diameter_mm),
                'Knob cap screw-side softened face profile'
            ),
            circle_profile(
                component,
                z_offset_mm + (SOCKET_SIDE_FILLET_OFFSET_TWO_MM * 0.45),
                outer_diameter_mm - 6.0,
                'Knob cap screw-side blend profile'
            ),
            circle_profile(
                component,
                z_offset_mm + SOCKET_SIDE_FILLET_OFFSET_TWO_MM,
                outer_diameter_mm,
                'Knob cap full outside profile near screw side'
            ),
            circle_profile(
                component,
                z_offset_mm + KNOB_HEIGHT_MM - SCREW_SIDE_FILLET_OFFSET_TWO_MM,
                outer_diameter_mm,
                'Knob cap full outside profile near socket side'
            ),
            circle_profile(
                component,
                z_offset_mm + KNOB_HEIGHT_MM - (SCREW_SIDE_FILLET_OFFSET_TWO_MM * 0.45),
                outer_diameter_mm - 6.0,
                'Knob cap socket-side blend profile'
            ),
            circle_profile(
                component,
                z_offset_mm + KNOB_HEIGHT_MM,
                cap_socket_side_face_diameter(outer_diameter_mm),
                'Knob cap socket-side softened face profile'
            ),
        ],
        'V2 Item 2 - Knob cap'
    )

    cut_body(
        component,
        circle_profile(
            component,
            z_offset_mm + closed_end_mm,
            DOWEL_HOLE_DIAMETER_MM,
            'Knob cap dowel socket profile'
        ),
        socket_depth_mm,
        'V2 Item 2 - Dowel socket cut'
    )
    cut_body(
        component,
        circle_profile(
            component,
            z_offset_mm,
            KNOB_SCREW_PILOT_DIAMETER_MM,
            'Knob cap screw pilot profile'
        ),
        closed_end_mm,
        'V2 Item 2 - Screw pilot cut'
    )
    loft_cut(
        component,
        [
            circle_profile(
                component,
                z_offset_mm,
                KNOB_SCREW_OUTER_CLEARANCE_DIAMETER_MM,
                'Knob cap screw outer clearance profile'
            ),
            circle_profile(
                component,
                z_offset_mm + KNOB_SCREW_CHAMFER_DEPTH_MM,
                KNOB_SCREW_PILOT_DIAMETER_MM,
                'Knob cap screw pilot chamfer endpoint profile'
            ),
        ],
        'V2 Item 2 - Screw opening chamfer cut'
    )

    return body


def _extrude_input(component, profile, distance_mm, operation):
    extrudes = component.features.extrudeFeatures
    extrude_input = extrudes.createInput(profile, operation)
    extrude_input.setDistanceExtent(
        False,
        adsk.core.ValueInput.createByReal(mm_to_cm(distance_mm))
    )
    return extrude_input


def create_handle_sleeve(component, z_offset_mm=0.0):
    knob_end_outer_mm = cap_socket_side_face_diameter(33.0)

    sketch = component.sketches.add(component.xZConstructionPlane)
    sketch.name = 'V2 handle sleeve straight taper profile'

    inner_radius_cm = mm_to_cm(DOWEL_HOLE_DIAMETER_MM / 2.0)
    knob_outer_radius_cm = mm_to_cm(knob_end_outer_mm / 2.0)
    grip_outer_radius_cm = mm_to_cm(HANDLE_OUTER_DIAMETER_MM / 2.0)
    start_z_cm = -mm_to_cm(z_offset_mm)
    end_z_cm = -mm_to_cm(z_offset_mm + HANDLE_LENGTH_MM)

    lines = sketch.sketchCurves.sketchLines
    axis = lines.addByTwoPoints(
        adsk.core.Point3D.create(0, start_z_cm, 0),
        adsk.core.Point3D.create(0, end_z_cm, 0)
    )
    axis.isConstruction = True

    points = [
        adsk.core.Point3D.create(inner_radius_cm, start_z_cm, 0),
        adsk.core.Point3D.create(knob_outer_radius_cm, start_z_cm, 0),
        adsk.core.Point3D.create(grip_outer_radius_cm, end_z_cm, 0),
        adsk.core.Point3D.create(inner_radius_cm, end_z_cm, 0),
    ]
    for index in range(len(points)):
        lines.addByTwoPoints(points[index], points[(index + 1) % len(points)])

    return revolve_body(
        component,
        sketch.profiles.item(0),
        axis,
        'V2 Item 3 - Handle sleeve'
    )


def create_handle_to_body_collar(component, z_offset_mm=0.0):
    sketch = component.sketches.add(component.xZConstructionPlane)
    sketch.name = 'V2 handle-to-body collar straight taper profile'

    inner_radius_cm = mm_to_cm(DOWEL_HOLE_DIAMETER_MM / 2.0)
    handle_outer_radius_cm = mm_to_cm(HANDLE_OUTER_DIAMETER_MM / 2.0)
    body_outer_radius_cm = mm_to_cm(42.0 / 2.0)
    start_z_cm = -mm_to_cm(z_offset_mm)
    end_z_cm = -mm_to_cm(z_offset_mm + COLLAR_HEIGHT_MM)

    lines = sketch.sketchCurves.sketchLines
    axis = lines.addByTwoPoints(
        adsk.core.Point3D.create(0, start_z_cm, 0),
        adsk.core.Point3D.create(0, end_z_cm, 0)
    )
    axis.isConstruction = True

    points = [
        adsk.core.Point3D.create(inner_radius_cm, start_z_cm, 0),
        adsk.core.Point3D.create(handle_outer_radius_cm, start_z_cm, 0),
        adsk.core.Point3D.create(body_outer_radius_cm, end_z_cm, 0),
        adsk.core.Point3D.create(inner_radius_cm, end_z_cm, 0),
    ]
    for index in range(len(points)):
        lines.addByTwoPoints(points[index], points[(index + 1) % len(points)])

    return revolve_body(
        component,
        sketch.profiles.item(0),
        axis,
        'V2 Item 4 - Handle-to-body collar'
    )


def create_body_shell(component, name, z_offset_mm, height_mm,
                      start_outer_mm, mid_outer_mm, end_outer_mm):
    mid_z_mm = z_offset_mm + (height_mm * 0.45)
    end_z_mm = z_offset_mm + height_mm
    shell = loft_body(
        component,
        [
            annular_profile(
                component,
                z_offset_mm,
                start_outer_mm,
                shell_inner_diameter(start_outer_mm),
                f'{name} start profile'
            ),
            annular_profile(
                component,
                mid_z_mm,
                mid_outer_mm,
                shell_inner_diameter(mid_outer_mm),
                f'{name} belly profile'
            ),
            annular_profile(
                component,
                end_z_mm,
                end_outer_mm,
                shell_inner_diameter(end_outer_mm),
                f'{name} end profile'
            ),
        ],
        name
    )
    join_extrude(
        component,
        annular_profile(
            component,
            z_offset_mm,
            start_outer_mm,
            DOWEL_HOLE_DIAMETER_MM,
            f'{name} lower bulkhead profile'
        ),
        BODY_BULKHEAD_HEIGHT_MM,
        f'{name} lower bulkhead'
    )
    join_extrude(
        component,
        annular_profile(
            component,
            end_z_mm - BODY_BULKHEAD_HEIGHT_MM,
            end_outer_mm,
            DOWEL_HOLE_DIAMETER_MM,
            f'{name} upper bulkhead profile'
        ),
        BODY_BULKHEAD_HEIGHT_MM,
        f'{name} upper bulkhead'
    )
    join_extrude(
        component,
        annular_profile(
            component,
            z_offset_mm,
            BODY_SLEEVE_OUTER_DIAMETER_MM,
            DOWEL_HOLE_DIAMETER_MM,
            f'{name} sleeve profile'
        ),
        height_mm,
        f'{name} integrated dowel sleeve'
    )
    cut_body(
        component,
        circle_profile(
            component,
            z_offset_mm,
            DOWEL_HOLE_DIAMETER_MM,
            f'{name} final dowel through-bore profile'
        ),
        height_mm,
        f'{name} final 13.2 mm dowel through-bore cut'
    )
    return shell


def create_lower_body_shell(component, z_offset_mm=0.0):
    return create_body_shell(
        component,
        'V2 Item 5 - Lower slim body shell',
        z_offset_mm,
        LOWER_BODY_HEIGHT_MM,
        42.0,
        70.0,
        78.0
    )


def create_upper_body_shell(component, z_offset_mm=0.0):
    return create_body_shell(
        component,
        'V2 Item 6 - Upper slim body shell',
        z_offset_mm,
        UPPER_BODY_HEIGHT_MM,
        78.0,
        66.0,
        40.0
    )


def create_nose_cap(component, z_offset_mm=0.0):
    outer_diameter_mm = 40.0
    screw_face_diameter_mm = 22.0
    socket_depth_mm = 7.0
    closed_end_mm = NOSE_HEIGHT_MM - socket_depth_mm

    body = loft_body(
        component,
        [
            circle_profile(
                component,
                z_offset_mm,
                outer_diameter_mm,
                'Nose cap socket-side 40 mm face profile'
            ),
            circle_profile(
                component,
                z_offset_mm + 2.0,
                outer_diameter_mm,
                'Nose cap full-width socket-side shoulder profile'
            ),
            circle_profile(
                component,
                z_offset_mm + 7.0,
                outer_diameter_mm - 4.0,
                'Nose cap short taper profile'
            ),
            circle_profile(
                component,
                z_offset_mm + NOSE_HEIGHT_MM,
                screw_face_diameter_mm,
                'Nose cap screw-side compact face profile'
            ),
        ],
        'V2 Item 7 - Nose cap'
    )

    cut_body(
        component,
        circle_profile(
            component,
            z_offset_mm,
            DOWEL_HOLE_DIAMETER_MM,
            'Nose cap dowel socket profile'
        ),
        socket_depth_mm,
        'V2 Item 7 - Dowel socket cut'
    )

    cut_body(
        component,
        circle_profile(
            component,
            z_offset_mm + socket_depth_mm,
            NOSE_SCREW_CLEARANCE_DIAMETER_MM,
            'Nose cap screw clearance profile'
        ),
        closed_end_mm,
        'V2 Item 7 - Screw clearance cut'
    )

    loft_cut(
        component,
        [
            circle_profile(
                component,
                z_offset_mm + NOSE_HEIGHT_MM - NOSE_SCREW_HEAD_CHAMFER_DEPTH_MM,
                NOSE_SCREW_CLEARANCE_DIAMETER_MM,
                'Nose cap inner screw clearance profile'
            ),
            circle_profile(
                component,
                z_offset_mm + NOSE_HEIGHT_MM,
                NOSE_SCREW_HEAD_CHAMFER_DIAMETER_MM,
                'Nose cap outer screw chamfer profile'
            ),
        ],
        'V2 Item 7 - Nose cap screw head chamfer cut'
    )
    return body


def create_full_club(component):
    dowel = create_dowel_rod(component, 0.0, include_pilot_holes=True)
    create_knob_cap(component, Z_KNOB_MM)
    create_handle_sleeve(component, Z_HANDLE_MM)
    create_handle_to_body_collar(component, Z_COLLAR_MM)
    create_lower_body_shell(component, Z_LOWER_BODY_MM)
    create_upper_body_shell(component, Z_UPPER_BODY_MM)
    create_nose_cap(component, Z_NOSE_MM)
    return dowel
