"""Create the JJC V1 dowel rod reference part."""

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

        # Parameters from Resources/1_dowel_rod_spec.md.
        dowel_diameter_mm = 12.7
        dowel_length_mm = 413.0

        def select_only(*entities):
            selections = ui.activeSelections
            selections.clear()
            for entity in entities:
                if entity:
                    selections.add(entity)
            adsk.doEvents()

        sketch = component.sketches.add(component.xYConstructionPlane)
        sketch.name = 'Dowel rod end profile'

        center = adsk.core.Point3D.create(0, 0, 0)
        sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            mm_to_cm(dowel_diameter_mm / 2.0)
        )

        extrudes = component.features.extrudeFeatures
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        extrude_input.setDistanceExtent(
            False,
            adsk.core.ValueInput.createByReal(mm_to_cm(dowel_length_mm))
        )

        extrude = extrudes.add(extrude_input)
        extrude.name = '413 mm dowel rod extrusion'

        body = extrude.bodies.item(0)
        body.name = 'Dowel rod'

        select_only(body)
        ui.messageBox(
            'Dowel rod created.\n\n'
            f'Diameter: {dowel_diameter_mm} mm\n'
            f'Length: {dowel_length_mm} mm'
        )

    except:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')
