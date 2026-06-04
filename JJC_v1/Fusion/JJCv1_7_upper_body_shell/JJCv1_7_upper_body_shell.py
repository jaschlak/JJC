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
        dowel_hole_diameter_mm = dowel_diameter_mm + dowel_clearance_mm

        def select_only(*entities):
            selections = ui.activeSelections
            selections.clear()
            for entity in entities:
                if entity:
                    selections.add(entity)
            adsk.doEvents()

        def circle_profile(sketch, diameter_mm):
            center = adsk.core.Point3D.create(0, 0, 0)
            sketch.sketchCurves.sketchCircles.addByCenterRadius(
                center,
                mm_to_cm(diameter_mm / 2.0)
            )
            return sketch.profiles.item(0)

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
        bottom_profile = bottom_sketch.profiles.item(0)

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
        top_profile = top_sketch.profiles.item(0)

        lofts = component.features.loftFeatures
        loft_input = lofts.createInput(
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        loft_input.loftSections.add(bottom_profile)
        loft_input.loftSections.add(top_profile)

        loft = lofts.add(loft_input)
        loft.name = 'Upper body infill-ready solid loft'

        body = loft.bodies.item(0)
        body.name = 'Upper body infill-ready shell'

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
            f'Slicer wall target: {wall_thickness_mm} mm\n'
            f'Dowel hole: {dowel_hole_diameter_mm} mm through-hole\n'
            f'Solid body around dowel hole is ready for slicer infill.\n'
            f'Height: {shell_height_mm} mm'
        )

    except:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')
