import adsk.core
import adsk.fusion
import traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        def pause(message):
            adsk.doEvents()
            ui.messageBox(message)

        def select_only(*entities):
            selections = ui.activeSelections
            selections.clear()
            for entity in entities:
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

        design = app.activeProduct
        if not isinstance(design, adsk.fusion.Design):
            ui.messageBox('No active Fusion design.')
            return

        root = design.rootComponent

        # Washer dimensions in centimeters.
        # Fusion API internal length units are cm.
        outer_diameter = 4.0   # 40 mm
        inner_diameter = 1.5   # 15 mm
        thickness = 0.3        # 3 mm

        sketches = root.sketches
        xy_plane = root.xYConstructionPlane
        sketch = sketches.add(xy_plane)
        sketch.name = 'Washer sketch'
        select_only(sketch)
        pause('Step 1: Created a sketch on the XY plane.')

        center = adsk.core.Point3D.create(0, 0, 0)

        outer_circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            outer_diameter / 2
        )
        select_only(outer_circle)
        pause('Step 2: Created the outer circle.')

        inner_circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            center,
            inner_diameter / 2
        )
        select_only(inner_circle)
        pause('Step 3: Created the inner circle.')

        select_only(outer_circle, inner_circle)
        pause('Step 4: Selected both sketch circles.')

        # Fusion creates one profile for the hole and one for the washer ring.
        # The ring is the larger profile for these dimensions.
        ring_profile = largest_profile(sketch)
        select_only(ring_profile)
        pause('Step 5: Selected the ring profile between the circles.')

        extrudes = root.features.extrudeFeatures
        distance = adsk.core.ValueInput.createByReal(thickness)

        extrude_input = extrudes.createInput(
            ring_profile,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        extrude_input.setDistanceExtent(False, distance)

        extrude = extrudes.add(extrude_input)
        extrude.name = 'Washer extrusion'
        washer_body = extrude.bodies.item(0)
        washer_body.name = 'Simple washer'
        select_only(washer_body)
        pause('Step 6: Extruded the ring profile into a washer body.')

        ui.messageBox('Washer created.')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
