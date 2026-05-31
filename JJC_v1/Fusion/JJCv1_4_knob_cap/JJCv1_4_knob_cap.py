"""Create the JJC V1 knob cap."""

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

        # Parameters from Resources/4_knob_cap_spec.md.
        outer_diameter_mm = 34.0
        dowel_diameter_mm = 12.7
        dowel_clearance_mm = 0.5
        cap_height_mm = 28.0
        socket_depth_mm = 22.0
        edge_chamfer_mm = 1.0

        socket_diameter_mm = dowel_diameter_mm + dowel_clearance_mm
        bottom_thickness_mm = cap_height_mm - socket_depth_mm

        def select_only(*entities):
            selections = ui.activeSelections
            selections.clear()
            for entity in entities:
                if entity:
                    selections.add(entity)
            adsk.doEvents()

        bottom_sketch = component.sketches.add(component.xYConstructionPlane)
        bottom_sketch.name = 'Knob cap closed bottom sketch'

        center = adsk.core.Point3D.create(0, 0, 0)
        bottom_sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(outer_diameter_mm / 2.0)
        )

        bottom_profile = bottom_sketch.profiles.item(0)

        extrudes = component.features.extrudeFeatures
        cap_input = extrudes.createInput(
            bottom_profile,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        cap_input.setDistanceExtent(
            False,
            adsk.core.ValueInput.createByReal(mm_to_cm(bottom_thickness_mm))
        )

        bottom_extrude = extrudes.add(cap_input)
        bottom_extrude.name = '6 mm closed bottom extrusion'

        body = bottom_extrude.bodies.item(0)
        body.name = 'Knob cap'

        plane_input = component.constructionPlanes.createInput()
        plane_input.setByOffset(
            component.xYConstructionPlane,
            adsk.core.ValueInput.createByReal(mm_to_cm(bottom_thickness_mm))
        )
        socket_plane = component.constructionPlanes.add(plane_input)
        socket_plane.name = 'Socket opening plane'

        wall_sketch = component.sketches.add(socket_plane)
        wall_sketch.name = 'Knob cap socket wall sketch'
        wall_sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(outer_diameter_mm / 2.0)
        )
        wall_sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(socket_diameter_mm / 2.0)
        )

        wall_profile = None
        largest_area = -1
        for index in range(wall_sketch.profiles.count):
            profile = wall_sketch.profiles.item(index)
            area = profile.areaProperties().area
            if area > largest_area:
                largest_area = area
                wall_profile = profile

        wall_input = extrudes.createInput(
            wall_profile,
            adsk.fusion.FeatureOperations.JoinFeatureOperation
        )
        wall_input.setDistanceExtent(
            False,
            adsk.core.ValueInput.createByReal(mm_to_cm(socket_depth_mm))
        )
        wall_extrude = extrudes.add(wall_input)
        wall_extrude.name = '22 mm socket wall extrusion'

        edge_collection = adsk.core.ObjectCollection.create()
        for index in range(body.edges.count):
            edge_collection.add(body.edges.item(index))

        if edge_collection.count > 0:
            chamfers = component.features.chamferFeatures
            chamfer_input = chamfers.createInput(edge_collection, True)
            chamfer_input.setToEqualDistance(
                adsk.core.ValueInput.createByReal(mm_to_cm(edge_chamfer_mm))
            )
            chamfer = chamfers.add(chamfer_input)
            chamfer.name = '1 mm edge chamfer'

        select_only(body)
        ui.messageBox(
            'Knob cap created.\n\n'
            f'Outer diameter: {outer_diameter_mm} mm\n'
            f'Socket diameter: {socket_diameter_mm} mm\n'
            f'Cap height: {cap_height_mm} mm\n'
            f'Socket depth: {socket_depth_mm} mm'
        )

    except:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')
