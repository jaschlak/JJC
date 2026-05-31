"""Create the JJC V1 dowel centering ring."""

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

        root = design.rootComponent

        # Parameters from Resources/2_dowel_centering_ring_spec.md.
        outer_diameter_mm = 35.0
        dowel_diameter_mm = 12.7
        dowel_clearance_mm = 0.5
        ring_thickness_mm = 6.0
        edge_chamfer_mm = 0.5

        inner_diameter_mm = dowel_diameter_mm + dowel_clearance_mm

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

        component = root

        sketch = component.sketches.add(component.xYConstructionPlane)
        sketch.name = 'Ring profile sketch'

        center = adsk.core.Point3D.create(0, 0, 0)
        outer_circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(outer_diameter_mm / 2.0)
        )

        inner_circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(inner_diameter_mm / 2.0)
        )

        ring_profile = largest_profile(sketch)

        extrudes = component.features.extrudeFeatures
        extrude_input = extrudes.createInput(
            ring_profile,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        extrude_input.setDistanceExtent(
            False,
            adsk.core.ValueInput.createByReal(mm_to_cm(ring_thickness_mm))
        )

        extrude = extrudes.add(extrude_input)
        extrude.name = '6 mm ring extrusion'

        body = extrude.bodies.item(0)
        body.name = 'Dowel centering ring'

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
            chamfer.name = '0.5 mm edge chamfer'

        select_only(body)
        ui.messageBox(
            'Dowel centering ring created.\n\n'
            f'Outer diameter: {outer_diameter_mm} mm\n'
            f'Inner diameter: {inner_diameter_mm} mm\n'
            f'Thickness: {ring_thickness_mm} mm'
        )

    except:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')
