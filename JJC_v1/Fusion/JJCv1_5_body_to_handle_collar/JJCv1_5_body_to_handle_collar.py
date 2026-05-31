"""Create the JJC V1 body-to-handle collar."""

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

        # Parameters from Resources/5_body_to_handle_collar_spec.md.
        lower_outer_diameter_mm = 24.0
        upper_outer_diameter_mm = 42.0
        dowel_diameter_mm = 12.7
        dowel_clearance_mm = 0.5
        collar_height_mm = 35.0
        edge_chamfer_mm = 0.75

        inner_diameter_mm = dowel_diameter_mm + dowel_clearance_mm

        def select_only(*entities):
            selections = ui.activeSelections
            selections.clear()
            for entity in entities:
                if entity:
                    selections.add(entity)
            adsk.doEvents()

        center = adsk.core.Point3D.create(0, 0, 0)

        # The larger 42 mm body-side face is created directly on the XY plane.
        bottom_sketch = component.sketches.add(component.xYConstructionPlane)
        bottom_sketch.name = 'Body-side collar profile on XY plane'
        bottom_sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(upper_outer_diameter_mm / 2.0)
        )
        bottom_profile = bottom_sketch.profiles.item(0)

        plane_input = component.constructionPlanes.createInput()
        plane_input.setByOffset(
            component.xYConstructionPlane,
            adsk.core.ValueInput.createByReal(mm_to_cm(collar_height_mm))
        )
        top_plane = component.constructionPlanes.add(plane_input)
        top_plane.name = 'Handle-side collar plane'

        top_sketch = component.sketches.add(top_plane)
        top_sketch.name = 'Handle-side collar profile'
        top_sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(lower_outer_diameter_mm / 2.0)
        )
        top_profile = top_sketch.profiles.item(0)

        lofts = component.features.loftFeatures
        loft_input = lofts.createInput(
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        loft_input.loftSections.add(bottom_profile)
        loft_input.loftSections.add(top_profile)

        loft = lofts.add(loft_input)
        loft.name = 'Body-to-handle collar loft'

        body = loft.bodies.item(0)
        body.name = 'Body-to-handle collar'

        hole_sketch = component.sketches.add(component.xYConstructionPlane)
        hole_sketch.name = 'Dowel hole cut sketch'
        hole_sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(inner_diameter_mm / 2.0)
        )
        hole_profile = hole_sketch.profiles.item(0)

        extrudes = component.features.extrudeFeatures
        cut_input = extrudes.createInput(
            hole_profile,
            adsk.fusion.FeatureOperations.CutFeatureOperation
        )
        cut_input.setDistanceExtent(
            False,
            adsk.core.ValueInput.createByReal(mm_to_cm(collar_height_mm))
        )
        hole_cut = extrudes.add(cut_input)
        hole_cut.name = '13.2 mm dowel hole cut'

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
            chamfer.name = '0.75 mm edge chamfer'

        select_only(body)
        ui.messageBox(
            'Body-to-handle collar created.\n\n'
            'The larger body-side face starts on the XY plane.\n\n'
            f'Body-side outer diameter: {upper_outer_diameter_mm} mm\n'
            f'Handle-side outer diameter: {lower_outer_diameter_mm} mm\n'
            f'Inner diameter: {inner_diameter_mm} mm\n'
            f'Height: {collar_height_mm} mm'
        )

    except:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')
