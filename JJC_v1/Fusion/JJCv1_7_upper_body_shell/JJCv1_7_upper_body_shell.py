"""Create the JJC V1 upper body shell."""

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

        # Parameters from Resources/7_upper_body_shell_spec.md.
        wide_outer_diameter_mm = 58.0
        nose_side_outer_diameter_mm = 32.0
        wall_thickness_mm = 2.0
        shell_height_mm = 120.0
        dowel_diameter_mm = 12.7
        dowel_clearance_mm = 0.5
        dowel_sleeve_outer_diameter_mm = 20.0
        lower_bulkhead_height_mm = 5.0
        upper_bulkhead_height_mm = 5.0
        wide_inner_diameter_mm = wide_outer_diameter_mm - (wall_thickness_mm * 2.0)
        nose_side_inner_diameter_mm = nose_side_outer_diameter_mm - (wall_thickness_mm * 2.0)
        dowel_hole_diameter_mm = dowel_diameter_mm + dowel_clearance_mm

        def select_only(*entities):
            selections = ui.activeSelections
            selections.clear()
            for entity in entities:
                if entity:
                    selections.add(entity)
            adsk.doEvents()

        def largest_profile(sketch):
            largest = None
            largest_area = -1
            for index in range(sketch.profiles.count):
                profile = sketch.profiles.item(index)
                area = profile.areaProperties().area
                if area > largest_area:
                    largest = profile
                    largest_area = area
            return largest

        def circle_profile(sketch, diameter_mm):
            center = adsk.core.Point3D.create(0, 0, 0)
            sketch.sketchCurves.sketchCircles.addByCenterRadius(
                center,
                mm_to_cm(diameter_mm / 2.0)
            )
            return sketch.profiles.item(0)

        def add_joined_extrude(profile, distance_mm, name):
            extrudes = component.features.extrudeFeatures
            extrude_input = extrudes.createInput(
                profile,
                adsk.fusion.FeatureOperations.JoinFeatureOperation
            )
            extrude_input.setDistanceExtent(
                False,
                adsk.core.ValueInput.createByReal(mm_to_cm(distance_mm))
            )
            extrude = extrudes.add(extrude_input)
            extrude.name = name
            return extrude

        def add_cut_extrude(profile, distance_mm, name):
            extrudes = component.features.extrudeFeatures
            extrude_input = extrudes.createInput(
                profile,
                adsk.fusion.FeatureOperations.CutFeatureOperation
            )
            extrude_input.setDistanceExtent(
                False,
                adsk.core.ValueInput.createByReal(mm_to_cm(distance_mm))
            )
            extrude = extrudes.add(extrude_input)
            extrude.name = name
            return extrude

        center = adsk.core.Point3D.create(0, 0, 0)

        bottom_sketch = component.sketches.add(component.xYConstructionPlane)
        bottom_sketch.name = 'Wide body-side upper shell profile on XY plane'
        bottom_sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(wide_outer_diameter_mm / 2.0)
        )
        bottom_sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(wide_inner_diameter_mm / 2.0)
        )
        bottom_profile = largest_profile(bottom_sketch)

        plane_input = component.constructionPlanes.createInput()
        plane_input.setByOffset(
            component.xYConstructionPlane,
            adsk.core.ValueInput.createByReal(mm_to_cm(shell_height_mm))
        )
        top_plane = component.constructionPlanes.add(plane_input)
        top_plane.name = 'Nose-side upper shell plane'

        top_sketch = component.sketches.add(top_plane)
        top_sketch.name = 'Nose-side upper shell profile'
        top_sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(nose_side_outer_diameter_mm / 2.0)
        )
        top_sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(nose_side_inner_diameter_mm / 2.0)
        )
        top_profile = largest_profile(top_sketch)

        lofts = component.features.loftFeatures
        loft_input = lofts.createInput(
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        loft_input.loftSections.add(bottom_profile)
        loft_input.loftSections.add(top_profile)

        loft = lofts.add(loft_input)
        loft.name = 'Upper body shell loft'

        body = loft.bodies.item(0)
        body.name = 'Upper body shell'

        sleeve_sketch = component.sketches.add(component.xYConstructionPlane)
        sleeve_sketch.name = 'Integrated dowel sleeve sketch'
        sleeve_profile = circle_profile(
            sleeve_sketch,
            dowel_sleeve_outer_diameter_mm
        )
        add_joined_extrude(
            sleeve_profile,
            shell_height_mm,
            'Integrated dowel sleeve'
        )

        lower_bulkhead_sketch = component.sketches.add(component.xYConstructionPlane)
        lower_bulkhead_sketch.name = 'Lower structural bulkhead sketch'
        lower_bulkhead_profile = circle_profile(
            lower_bulkhead_sketch,
            wide_inner_diameter_mm
        )
        add_joined_extrude(
            lower_bulkhead_profile,
            lower_bulkhead_height_mm,
            'Lower structural bulkhead'
        )

        upper_plane_input = component.constructionPlanes.createInput()
        upper_plane_input.setByOffset(
            component.xYConstructionPlane,
            adsk.core.ValueInput.createByReal(mm_to_cm(shell_height_mm - upper_bulkhead_height_mm))
        )
        upper_bulkhead_plane = component.constructionPlanes.add(upper_plane_input)
        upper_bulkhead_plane.name = 'Upper bulkhead start plane'

        upper_bulkhead_sketch = component.sketches.add(upper_bulkhead_plane)
        upper_bulkhead_sketch.name = 'Upper structural bulkhead sketch'
        upper_bulkhead_profile = circle_profile(
            upper_bulkhead_sketch,
            nose_side_inner_diameter_mm
        )
        add_joined_extrude(
            upper_bulkhead_profile,
            upper_bulkhead_height_mm,
            'Upper structural bulkhead'
        )

        dowel_hole_sketch = component.sketches.add(component.xYConstructionPlane)
        dowel_hole_sketch.name = 'Full-length dowel hole cut sketch'
        dowel_hole_profile = circle_profile(
            dowel_hole_sketch,
            dowel_hole_diameter_mm
        )
        add_cut_extrude(
            dowel_hole_profile,
            shell_height_mm,
            '13.2 mm full-length dowel hole cut'
        )

        select_only(body)
        ui.messageBox(
            'Upper body shell created.\n\n'
            'The wide 58 mm side starts on the XY plane.\n\n'
            f'Wide outer diameter: {wide_outer_diameter_mm} mm\n'
            f'Nose-side outer diameter: {nose_side_outer_diameter_mm} mm\n'
            f'Wall thickness: {wall_thickness_mm} mm\n'
            f'Dowel sleeve: {dowel_hole_diameter_mm} mm ID, {dowel_sleeve_outer_diameter_mm} mm OD\n'
            f'Height: {shell_height_mm} mm'
        )

    except:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')
