"""Create a JJC V1 full club layout in the active Fusion design."""

import math
import traceback
import adsk.core
import adsk.fusion


def mm_to_cm(value_mm):
    """Fusion API length values are centimeters."""
    return value_mm / 10.0


def run(_context):
    """This function is called by Fusion when the script is run."""
    ui = None

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        design = app.activeProduct
        if not isinstance(design, adsk.fusion.Design):
            ui.messageBox('No active Fusion design.')
            return

        component = design.rootComponent

        dowel_diameter_mm = 12.7
        dowel_clearance_mm = 0.5
        dowel_hole_diameter_mm = dowel_diameter_mm + dowel_clearance_mm

        knob_height_mm = 28.0
        handle_length_mm = 80.0
        collar_height_mm = 35.0
        lower_shell_height_mm = 120.0
        upper_shell_height_mm = 120.0
        nose_cap_height_mm = 30.0
        total_length_mm = (
            knob_height_mm
            + handle_length_mm
            + collar_height_mm
            + lower_shell_height_mm
            + upper_shell_height_mm
            + nose_cap_height_mm
        )

        z_knob = 0.0
        z_handle = z_knob + knob_height_mm
        z_collar = z_handle + handle_length_mm
        z_lower_shell = z_collar + collar_height_mm
        z_upper_shell = z_lower_shell + lower_shell_height_mm
        z_nose_cap = z_upper_shell + upper_shell_height_mm

        def select_only(*entities):
            selections = ui.activeSelections
            selections.clear()
            for entity in entities:
                if entity:
                    selections.add(entity)
            adsk.doEvents()

        def offset_plane(z_offset_mm, name):
            if z_offset_mm == 0:
                return component.xYConstructionPlane

            plane_input = component.constructionPlanes.createInput()
            plane_input.setByOffset(
                component.xYConstructionPlane,
                adsk.core.ValueInput.createByReal(mm_to_cm(z_offset_mm))
            )
            plane = component.constructionPlanes.add(plane_input)
            plane.name = name
            return plane

        def circle_profile(z_offset_mm, diameter_mm, name):
            sketch = component.sketches.add(offset_plane(z_offset_mm, f'{name} plane'))
            sketch.name = name
            sketch.sketchCurves.sketchCircles.addByCenterRadius(
                adsk.core.Point3D.create(0, 0, 0),
                mm_to_cm(diameter_mm / 2.0)
            )
            return sketch.profiles.item(0)

        def annular_profile(z_offset_mm, outer_diameter_mm, inner_diameter_mm, name):
            sketch = component.sketches.add(offset_plane(z_offset_mm, f'{name} plane'))
            sketch.name = name
            center = adsk.core.Point3D.create(0, 0, 0)
            sketch.sketchCurves.sketchCircles.addByCenterRadius(
                center,
                mm_to_cm(outer_diameter_mm / 2.0)
            )
            sketch.sketchCurves.sketchCircles.addByCenterRadius(
                center,
                mm_to_cm(inner_diameter_mm / 2.0)
            )

            outer_radius_cm = mm_to_cm(outer_diameter_mm / 2.0)
            inner_radius_cm = mm_to_cm(inner_diameter_mm / 2.0)
            expected_area = math.pi * (
                outer_radius_cm * outer_radius_cm
                - inner_radius_cm * inner_radius_cm
            )

            best_profile = None
            best_delta = None
            for index in range(sketch.profiles.count):
                profile = sketch.profiles.item(index)
                delta = abs(profile.areaProperties().area - expected_area)
                if best_delta is None or delta < best_delta:
                    best_delta = delta
                    best_profile = profile
            return best_profile

        def extrude_body(profile, distance_mm, name):
            extrudes = component.features.extrudeFeatures
            extrude_input = extrudes.createInput(
                profile,
                adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            extrude_input.setDistanceExtent(
                False,
                adsk.core.ValueInput.createByReal(mm_to_cm(distance_mm))
            )
            extrude = extrudes.add(extrude_input)
            extrude.name = f'{name} feature'
            body = extrude.bodies.item(0)
            body.name = name
            return body

        def loft_body(bottom_profile, top_profile, name):
            lofts = component.features.loftFeatures
            loft_input = lofts.createInput(
                adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            loft_input.loftSections.add(bottom_profile)
            loft_input.loftSections.add(top_profile)
            loft = lofts.add(loft_input)
            loft.name = f'{name} feature'
            body = loft.bodies.item(0)
            body.name = name
            return body

        def create_cylinder(name, diameter_mm, height_mm, z_offset_mm):
            profile = circle_profile(z_offset_mm, diameter_mm, f'{name} profile')
            return extrude_body(profile, height_mm, name)

        def create_tube(name, outer_diameter_mm, inner_diameter_mm, height_mm, z_offset_mm):
            profile = annular_profile(
                z_offset_mm,
                outer_diameter_mm,
                inner_diameter_mm,
                f'{name} annular profile'
            )
            return extrude_body(profile, height_mm, name)

        def create_tapered_tube(name, bottom_outer_mm, bottom_inner_mm,
                                top_outer_mm, top_inner_mm, height_mm, z_offset_mm):
            bottom_profile = annular_profile(
                z_offset_mm,
                bottom_outer_mm,
                bottom_inner_mm,
                f'{name} lower annular profile'
            )
            top_profile = annular_profile(
                z_offset_mm + height_mm,
                top_outer_mm,
                top_inner_mm,
                f'{name} upper annular profile'
            )
            return loft_body(bottom_profile, top_profile, name)

        def create_cap(name, outer_diameter_mm, height_mm, socket_depth_mm, z_offset_mm):
            closed_end_thickness_mm = height_mm - socket_depth_mm
            closed_profile = circle_profile(
                z_offset_mm,
                outer_diameter_mm,
                f'{name} closed end profile'
            )
            closed_body = extrude_body(
                closed_profile,
                closed_end_thickness_mm,
                f'{name} closed end'
            )

            wall_profile = annular_profile(
                z_offset_mm + closed_end_thickness_mm,
                outer_diameter_mm,
                dowel_hole_diameter_mm,
                f'{name} socket wall profile'
            )
            extrude_body(wall_profile, socket_depth_mm, f'{name} socket wall')
            return closed_body

        def create_shell_section(name, bottom_outer_mm, top_outer_mm, height_mm, z_offset_mm):
            wall_thickness_mm = 2.0
            sleeve_outer_diameter_mm = 20.0
            bulkhead_height_mm = 5.0
            bottom_inner_mm = bottom_outer_mm - (wall_thickness_mm * 2.0)
            top_inner_mm = top_outer_mm - (wall_thickness_mm * 2.0)

            shell = create_tapered_tube(
                name,
                bottom_outer_mm,
                bottom_inner_mm,
                top_outer_mm,
                top_inner_mm,
                height_mm,
                z_offset_mm
            )
            create_tube(
                f'{name} integrated dowel sleeve',
                sleeve_outer_diameter_mm,
                dowel_hole_diameter_mm,
                height_mm,
                z_offset_mm
            )
            create_tube(
                f'{name} lower bulkhead',
                bottom_inner_mm,
                dowel_hole_diameter_mm,
                bulkhead_height_mm,
                z_offset_mm
            )
            create_tube(
                f'{name} upper bulkhead',
                top_inner_mm,
                dowel_hole_diameter_mm,
                bulkhead_height_mm,
                z_offset_mm + height_mm - bulkhead_height_mm
            )
            return shell

        dowel = create_cylinder('Item 1 - Dowel rod', dowel_diameter_mm, total_length_mm, 0.0)
        create_cap('Item 4 - Knob cap', 34.0, knob_height_mm, 22.0, z_knob)
        create_tube('Item 3 - Handle sleeve', 24.0, dowel_hole_diameter_mm, handle_length_mm, z_handle)
        create_tapered_tube(
            'Item 5 - Body-to-handle collar',
            42.0,
            dowel_hole_diameter_mm,
            24.0,
            dowel_hole_diameter_mm,
            collar_height_mm,
            z_collar
        )
        create_shell_section(
            'Item 6 - Lower body shell',
            42.0,
            58.0,
            lower_shell_height_mm,
            z_lower_shell
        )
        create_shell_section(
            'Item 7 - Upper body shell',
            58.0,
            32.0,
            upper_shell_height_mm,
            z_upper_shell
        )
        create_cap('Item 8 - Nose cap', 32.0, nose_cap_height_mm, 22.0, z_nose_cap)

        select_only(dowel)
        ui.messageBox(
            'JJC V1 full club layout created.\n\n'
            'Fusion is currently in a Part Design document, so the script '
            'created separate named bodies instead of separate components.\n\n'
            f'Assembly length: {total_length_mm} mm'
        )

    except:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')
