"""Create the JJC V1 nose cap."""

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

        # Parameters from Resources/8_nose_cap_spec.md.
        outer_diameter_mm = 32.0
        dowel_diameter_mm = 12.7
        dowel_clearance_mm = 0.5
        cap_height_mm = 30.0
        socket_depth_mm = 22.0

        socket_diameter_mm = dowel_diameter_mm + dowel_clearance_mm
        closed_end_thickness_mm = cap_height_mm - socket_depth_mm

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

        center = adsk.core.Point3D.create(0, 0, 0)

        bottom_sketch = component.sketches.add(component.xYConstructionPlane)
        bottom_sketch.name = 'Nose cap closed end sketch'
        bottom_sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(outer_diameter_mm / 2.0)
        )
        bottom_profile = bottom_sketch.profiles.item(0)

        extrudes = component.features.extrudeFeatures
        bottom_input = extrudes.createInput(
            bottom_profile,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        bottom_input.setDistanceExtent(
            False,
            adsk.core.ValueInput.createByReal(mm_to_cm(closed_end_thickness_mm))
        )
        bottom_extrude = extrudes.add(bottom_input)
        bottom_extrude.name = '8 mm closed nose end extrusion'

        body = bottom_extrude.bodies.item(0)
        body.name = 'Nose cap'

        plane_input = component.constructionPlanes.createInput()
        plane_input.setByOffset(
            component.xYConstructionPlane,
            adsk.core.ValueInput.createByReal(mm_to_cm(closed_end_thickness_mm))
        )
        socket_plane = component.constructionPlanes.add(plane_input)
        socket_plane.name = 'Nose cap socket opening plane'

        wall_sketch = component.sketches.add(socket_plane)
        wall_sketch.name = 'Nose cap socket wall sketch'
        wall_sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(outer_diameter_mm / 2.0)
        )
        wall_sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(socket_diameter_mm / 2.0)
        )

        wall_profile = largest_profile(wall_sketch)
        wall_input = extrudes.createInput(
            wall_profile,
            adsk.fusion.FeatureOperations.JoinFeatureOperation
        )
        wall_input.setDistanceExtent(
            False,
            adsk.core.ValueInput.createByReal(mm_to_cm(socket_depth_mm))
        )
        wall_extrude = extrudes.add(wall_input)
        wall_extrude.name = '22 mm nose cap socket wall extrusion'

        select_only(body)
        ui.messageBox(
            'Nose cap created.\n\n'
            f'Outer diameter: {outer_diameter_mm} mm\n'
            f'Socket diameter: {socket_diameter_mm} mm\n'
            f'Cap height: {cap_height_mm} mm\n'
            f'Socket depth: {socket_depth_mm} mm'
        )

    except:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')
