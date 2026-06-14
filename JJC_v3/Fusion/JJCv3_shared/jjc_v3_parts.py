"""Shared JJC V3 Fusion geometry builders."""

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

LOWER_BODY_WALL_MM = 2.0
UPPER_BODY_WALL_MM = 1.6
LOWER_BODY_BOTTOM_PLATE_MM = 4.0
UPPER_BODY_TOP_PLATE_MM = 3.0
SLIP_JOINT_DEPTH_MM = 10.0
LOWER_MALE_LIP_OD_MM = 74.0
LOWER_MALE_LIP_ID_MM = 70.0
UPPER_SOCKET_ID_MM = 74.4
UPPER_SOCKET_OD_MM = 76.4
UPPER_INSERT_HUB_HEIGHT_MM = 2.0
UPPER_TO_LOWER_INSERT_DEPTH_MM = 10.0
UPPER_TO_LOWER_INSERT_OD_MM = 69.4
UPPER_TO_LOWER_INSERT_ID_MM = 64.4
UPPER_INSERT_FLARE_HEIGHT_MM = 7.0
UPPER_INSERT_WALL_BLEND_HEIGHT_MM = 10.0

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
    sketch.sketchCurves.sketchCircles.addByCenterRadius(center, mm_to_cm(outer_mm / 2.0))
    sketch.sketchCurves.sketchCircles.addByCenterRadius(center, mm_to_cm(inner_mm / 2.0))

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


def fillet_edges_by_radius(component, body, radius_mm, z_target_mm=None):
    """Apply a fillet to interior edges near a target Z height."""
    fillets = component.features.filletFeatures

    edges_to_fillet = []
    tolerance_mm = 2.0

    # Find circular edges near the target Z
    for edge in body.edges:
        edge_curve = edge.geometry
        if not isinstance(edge_curve, adsk.core.Circle3D):
            continue

        # Check if edge is near target Z
        center = edge_curve.center
        z_cm = center.z
        z_mm = z_cm * 10.0

        if z_target_mm is not None:
            if abs(z_mm - z_target_mm) > tolerance_mm:
                continue

        edges_to_fillet.append(edge)

    # Add edges to fillet input
    if len(edges_to_fillet) > 0:
        edge_collection = adsk.core.ObjectCollection.create()
        for edge in edges_to_fillet:
            edge_collection.add(edge)

        fillet_input = fillets.createInput()
        fillet_input.edgeSetInputs.addConstantRadiusEdgeSet(
            edge_collection,
            adsk.core.ValueInput.createByReal(mm_to_cm(radius_mm)),
            False
        )

        feature = fillets.add(fillet_input)
        feature.name = f'Fillet {radius_mm}mm'
        return feature

    return None


def loft_body(component, profiles, name):
    lofts = component.features.loftFeatures
    loft_input = lofts.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    for profile in profiles:
        loft_input.loftSections.add(profile)
    feature = lofts.add(loft_input)
    feature.name = f'{name} feature'
    body = feature.bodies.item(0)
    body.name = name
    return body


def loft_join(component, profiles, name):
    lofts = component.features.loftFeatures
    loft_input = lofts.createInput(adsk.fusion.FeatureOperations.JoinFeatureOperation)
    for profile in profiles:
        loft_input.loftSections.add(profile)
    feature = lofts.add(loft_input)
    feature.name = f'{name} feature'
    return feature


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
        circle_profile(component, z_offset_mm, DOWEL_DIAMETER_MM, 'V3 dowel rod profile'),
        TOTAL_LENGTH_MM,
        'V3 Item 1 - Dowel rod'
    )

    if include_pilot_holes:
        cut_body(
            component,
            circle_profile(component, z_offset_mm, DOWEL_PILOT_HOLE_DIAMETER_MM, 'Bottom dowel screw pilot profile'),
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
            circle_profile(component, z_offset_mm, cap_screw_side_face_diameter(outer_diameter_mm), 'Knob cap screw-side softened face profile'),
            circle_profile(component, z_offset_mm + (SOCKET_SIDE_FILLET_OFFSET_TWO_MM * 0.45), outer_diameter_mm - 6.0, 'Knob cap screw-side blend profile'),
            circle_profile(component, z_offset_mm + SOCKET_SIDE_FILLET_OFFSET_TWO_MM, outer_diameter_mm, 'Knob cap full outside profile near screw side'),
            circle_profile(component, z_offset_mm + KNOB_HEIGHT_MM - SCREW_SIDE_FILLET_OFFSET_TWO_MM, outer_diameter_mm, 'Knob cap full outside profile near socket side'),
            circle_profile(component, z_offset_mm + KNOB_HEIGHT_MM - (SCREW_SIDE_FILLET_OFFSET_TWO_MM * 0.45), outer_diameter_mm - 6.0, 'Knob cap socket-side blend profile'),
            circle_profile(component, z_offset_mm + KNOB_HEIGHT_MM, cap_socket_side_face_diameter(outer_diameter_mm), 'Knob cap socket-side softened face profile'),
        ],
        'V3 Item 2 - Knob cap'
    )

    cut_body(component, circle_profile(component, z_offset_mm + closed_end_mm, DOWEL_HOLE_DIAMETER_MM, 'Knob cap dowel socket profile'), socket_depth_mm, 'V3 Item 2 - Dowel socket cut')
    cut_body(component, circle_profile(component, z_offset_mm, KNOB_SCREW_PILOT_DIAMETER_MM, 'Knob cap screw pilot profile'), closed_end_mm, 'V3 Item 2 - Screw pilot cut')
    loft_cut(
        component,
        [
            circle_profile(component, z_offset_mm, KNOB_SCREW_OUTER_CLEARANCE_DIAMETER_MM, 'Knob cap screw outer clearance profile'),
            circle_profile(component, z_offset_mm + KNOB_SCREW_CHAMFER_DEPTH_MM, KNOB_SCREW_PILOT_DIAMETER_MM, 'Knob cap screw pilot chamfer endpoint profile'),
        ],
        'V3 Item 2 - Screw opening chamfer cut'
    )
    return body


def create_handle_sleeve(component, z_offset_mm=0.0):
    knob_end_outer_mm = cap_socket_side_face_diameter(33.0)

    sketch = component.sketches.add(component.xZConstructionPlane)
    sketch.name = 'V3 handle sleeve straight taper profile'

    inner_radius_cm = mm_to_cm(DOWEL_HOLE_DIAMETER_MM / 2.0)
    knob_outer_radius_cm = mm_to_cm(knob_end_outer_mm / 2.0)
    grip_outer_radius_cm = mm_to_cm(HANDLE_OUTER_DIAMETER_MM / 2.0)
    start_z_cm = -mm_to_cm(z_offset_mm)
    end_z_cm = -mm_to_cm(z_offset_mm + HANDLE_LENGTH_MM)

    lines = sketch.sketchCurves.sketchLines
    axis = lines.addByTwoPoints(adsk.core.Point3D.create(0, start_z_cm, 0), adsk.core.Point3D.create(0, end_z_cm, 0))
    axis.isConstruction = True

    points = [
        adsk.core.Point3D.create(inner_radius_cm, start_z_cm, 0),
        adsk.core.Point3D.create(knob_outer_radius_cm, start_z_cm, 0),
        adsk.core.Point3D.create(grip_outer_radius_cm, end_z_cm, 0),
        adsk.core.Point3D.create(inner_radius_cm, end_z_cm, 0),
    ]
    for index in range(len(points)):
        lines.addByTwoPoints(points[index], points[(index + 1) % len(points)])

    return revolve_body(component, sketch.profiles.item(0), axis, 'V3 Item 3 - Handle sleeve')


def create_handle_to_body_collar(component, z_offset_mm=0.0):
    sketch = component.sketches.add(component.xZConstructionPlane)
    sketch.name = 'V3 handle-to-body collar straight taper profile'

    inner_radius_cm = mm_to_cm(DOWEL_HOLE_DIAMETER_MM / 2.0)
    handle_outer_radius_cm = mm_to_cm(HANDLE_OUTER_DIAMETER_MM / 2.0)
    body_outer_radius_cm = mm_to_cm(42.0 / 2.0)
    start_z_cm = -mm_to_cm(z_offset_mm)
    end_z_cm = -mm_to_cm(z_offset_mm + COLLAR_HEIGHT_MM)

    lines = sketch.sketchCurves.sketchLines
    axis = lines.addByTwoPoints(adsk.core.Point3D.create(0, start_z_cm, 0), adsk.core.Point3D.create(0, end_z_cm, 0))
    axis.isConstruction = True

    points = [
        adsk.core.Point3D.create(inner_radius_cm, start_z_cm, 0),
        adsk.core.Point3D.create(handle_outer_radius_cm, start_z_cm, 0),
        adsk.core.Point3D.create(body_outer_radius_cm, end_z_cm, 0),
        adsk.core.Point3D.create(inner_radius_cm, end_z_cm, 0),
    ]
    for index in range(len(points)):
        lines.addByTwoPoints(points[index], points[(index + 1) % len(points)])

    return revolve_body(component, sketch.profiles.item(0), axis, 'V3 Item 4 - Handle-to-body collar')


def shell_inner_diameter(outer_mm, wall_mm):
    return outer_mm - (wall_mm * 2.0)


def create_lower_body_shell(component, z_offset_mm=0.0):
    mid_z_mm = z_offset_mm + (LOWER_BODY_HEIGHT_MM * 0.5)
    end_z_mm = z_offset_mm + LOWER_BODY_HEIGHT_MM
    shell = loft_body(
        component,
        [
            circle_profile(component, z_offset_mm, 42.0, 'Lower body start outer profile'),
            circle_profile(component, mid_z_mm, 70.0, 'Lower body belly outer profile'),
            circle_profile(component, end_z_mm, 78.0, 'Lower body top outer profile'),
        ],
        'V3 Item 5 - Lower hollow body shell'
    )

    loft_cut(
        component,
        [
            circle_profile(
                component,
                z_offset_mm + LOWER_BODY_BOTTOM_PLATE_MM,
                shell_inner_diameter(42.0, LOWER_BODY_WALL_MM),
                'Lower body cavity start profile'
            ),
            circle_profile(
                component,
                mid_z_mm,
                shell_inner_diameter(70.0, LOWER_BODY_WALL_MM),
                'Lower body cavity belly profile'
            ),
            circle_profile(
                component,
                end_z_mm,
                shell_inner_diameter(78.0, LOWER_BODY_WALL_MM),
                'Lower body cavity open top profile'
            ),
        ],
        'V3 Item 5 - Explicit hollow cavity cut'
    )
    cut_body(
        component,
        circle_profile(component, z_offset_mm, DOWEL_HOLE_DIAMETER_MM, 'Lower body bottom dowel clearance profile'),
        LOWER_BODY_BOTTOM_PLATE_MM,
        'V3 Item 5 - Bottom dowel clearance cut'
    )
    join_extrude(
        component,
        annular_profile(component, end_z_mm - SLIP_JOINT_DEPTH_MM, LOWER_MALE_LIP_OD_MM, LOWER_MALE_LIP_ID_MM, 'Lower body male slip lip profile'),
        SLIP_JOINT_DEPTH_MM,
        'V3 Item 5 - Male slip lip'
    )
    return shell


def create_upper_body_shell(component, z_offset_mm=0.0):
    mid_z_mm = z_offset_mm + (UPPER_BODY_HEIGHT_MM * 0.5)
    end_z_mm = z_offset_mm + UPPER_BODY_HEIGHT_MM
    insert_start_z_mm = z_offset_mm - UPPER_TO_LOWER_INSERT_DEPTH_MM
    shell = loft_body(
        component,
        [
            circle_profile(component, z_offset_mm, 78.0, 'Upper body bottom outer profile'),
            circle_profile(component, mid_z_mm, 66.0, 'Upper body belly outer profile'),
            circle_profile(component, end_z_mm, 40.0, 'Upper body top outer profile'),
        ],
        'V3 Item 6 - Upper hollow body shell'
    )

    loft_cut(
        component,
        [
            circle_profile(
                component,
                z_offset_mm,
                shell_inner_diameter(78.0, UPPER_BODY_WALL_MM),
                'Upper body cavity open around insert profile'
            ),
            circle_profile(
                component,
                mid_z_mm,
                shell_inner_diameter(66.0, UPPER_BODY_WALL_MM),
                'Upper body cavity belly profile'
            ),
            circle_profile(
                component,
                end_z_mm - UPPER_BODY_TOP_PLATE_MM,
                shell_inner_diameter(40.0, UPPER_BODY_WALL_MM),
                'Upper body cavity top stop profile'
            ),
        ],
        'V3 Item 6 - Explicit hollow cavity cut'
    )
    join_extrude(
        component,
        annular_profile(
            component,
            insert_start_z_mm,
            UPPER_TO_LOWER_INSERT_OD_MM,
            UPPER_TO_LOWER_INSERT_ID_MM,
            'Upper body lower insert profile'
        ),
        UPPER_TO_LOWER_INSERT_DEPTH_MM + UPPER_INSERT_HUB_HEIGHT_MM,
        'V3 Item 6 - Insert into Part 5'
    )
    loft_join(
        component,
        [
            annular_profile(
                component,
                z_offset_mm + UPPER_INSERT_HUB_HEIGHT_MM,
                UPPER_TO_LOWER_INSERT_OD_MM,
                UPPER_TO_LOWER_INSERT_ID_MM,
                'Upper body wall connector ramp base profile'
            ),
            annular_profile(
                component,
                z_offset_mm + UPPER_INSERT_FLARE_HEIGHT_MM,
                73.6,
                70.6,
                'Upper body internal ramp shoulder profile'
            ),
            annular_profile(
                component,
                z_offset_mm + UPPER_INSERT_WALL_BLEND_HEIGHT_MM,
                shell_inner_diameter(78.0, UPPER_BODY_WALL_MM),
                shell_inner_diameter(78.0, UPPER_BODY_WALL_MM) - 2.0,
                'Upper body internal ramp wall blend profile'
            ),
        ],
        'V3 Item 6 - Thin flared sleeve from insert into shell'
    )
    cavity_inner_diameter_mm = shell_inner_diameter(40.0, UPPER_BODY_WALL_MM)
    
    cut_body(
        component,
        circle_profile(
            component,
            end_z_mm - UPPER_BODY_TOP_PLATE_MM,
            DOWEL_HOLE_DIAMETER_MM,
            'Upper body top dowel clearance profile'
        ),
        UPPER_BODY_TOP_PLATE_MM,
        'V3 Item 6 - Top dowel clearance cut'
    )
    
    loft_join(
        component,
        [
            annular_profile(
                component,
                end_z_mm - UPPER_BODY_TOP_PLATE_MM,
                40.0,
                cavity_inner_diameter_mm,
                'Upper body top ramp base profile'
            ),
            annular_profile(
                component,
                end_z_mm - 2.0,
                40.0,
                cavity_inner_diameter_mm + 0.8,
                'Upper body top ramp middle profile'
            ),
            annular_profile(
                component,
                end_z_mm - 0.5,
                40.0,
                cavity_inner_diameter_mm + 1.6,
                'Upper body top ramp blend profile'
            ),
            annular_profile(
                component,
                end_z_mm - 0.1,
                40.0,
                39.9,
                'Upper body top ramp near-surface profile'
            ),
        ],
        'V3 Item 6 - Top disk annular support ramp'
    )
    loft_join(
        component,
        [
            annular_profile(
                component,
                z_offset_mm,
                UPPER_SOCKET_OD_MM,
                UPPER_SOCKET_ID_MM,
                'Upper body receiving socket wall bottom profile'
            ),
            annular_profile(
                component,
                z_offset_mm + SLIP_JOINT_DEPTH_MM,
                UPPER_SOCKET_OD_MM,
                UPPER_SOCKET_ID_MM,
                'Upper body receiving socket wall top profile'
            ),
        ],
        'V3 Item 6 - Receiving socket wall'
    )

    return shell


def create_nose_cap(component, z_offset_mm=0.0):
    outer_diameter_mm = 40.0
    screw_face_diameter_mm = 22.0
    socket_depth_mm = 7.0
    closed_end_mm = NOSE_HEIGHT_MM - socket_depth_mm

    body = loft_body(
        component,
        [
            circle_profile(component, z_offset_mm, outer_diameter_mm, 'Nose cap socket-side 40 mm face profile'),
            circle_profile(component, z_offset_mm + 2.0, outer_diameter_mm, 'Nose cap full-width socket-side shoulder profile'),
            circle_profile(component, z_offset_mm + 7.0, outer_diameter_mm - 4.0, 'Nose cap short taper profile'),
            circle_profile(component, z_offset_mm + NOSE_HEIGHT_MM, screw_face_diameter_mm, 'Nose cap screw-side compact face profile'),
        ],
        'V3 Item 7 - Nose cap'
    )

    cut_body(component, circle_profile(component, z_offset_mm, DOWEL_HOLE_DIAMETER_MM, 'Nose cap dowel socket profile'), socket_depth_mm, 'V3 Item 7 - Dowel socket cut')
    cut_body(component, circle_profile(component, z_offset_mm + socket_depth_mm, NOSE_SCREW_CLEARANCE_DIAMETER_MM, 'Nose cap screw clearance profile'), closed_end_mm, 'V3 Item 7 - Screw clearance cut')
    loft_cut(
        component,
        [
            circle_profile(component, z_offset_mm + NOSE_HEIGHT_MM - NOSE_SCREW_HEAD_CHAMFER_DEPTH_MM, NOSE_SCREW_CLEARANCE_DIAMETER_MM, 'Nose cap inner screw clearance profile'),
            circle_profile(component, z_offset_mm + NOSE_HEIGHT_MM, NOSE_SCREW_HEAD_CHAMFER_DIAMETER_MM, 'Nose cap outer screw chamfer profile'),
        ],
        'V3 Item 7 - Nose cap screw head chamfer cut'
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
