"""Create the JJC V2 Delphin-style club as a true Fusion assembly."""

import os
import sys
import traceback
import importlib
import adsk.core
import adsk.fusion


SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'JJCv2_shared')
if SHARED_DIR not in sys.path:
    sys.path.insert(0, SHARED_DIR)

import jjc_v2_parts  # noqa: E402

jjc_v2_parts = importlib.reload(jjc_v2_parts)


def run(_context):
    global jjc_v2_parts
    ui = None
    try:
        jjc_v2_parts = importlib.reload(jjc_v2_parts)
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        if not isinstance(design, adsk.fusion.Design):
            ui.messageBox('No active Fusion design.')
            return

        root = design.rootComponent

        def add_part_component(name, z_offset_mm, builder):
            transform = adsk.core.Matrix3D.create()
            transform.translation = adsk.core.Vector3D.create(
                0,
                0,
                jjc_v2_parts.mm_to_cm(z_offset_mm)
            )
            occurrence = root.occurrences.addNewComponent(transform)
            occurrence.component.name = name
            body = builder(occurrence.component, 0.0)
            return occurrence, body

        parts = [
            ('Item 1 - Dowel rod', 0.0, lambda component, z: jjc_v2_parts.create_dowel_rod(component, z, True)),
            ('Item 2 - Knob cap', jjc_v2_parts.Z_KNOB_MM, jjc_v2_parts.create_knob_cap),
            ('Item 3 - Handle sleeve', jjc_v2_parts.Z_HANDLE_MM, jjc_v2_parts.create_handle_sleeve),
            ('Item 4 - Handle-to-body collar', jjc_v2_parts.Z_COLLAR_MM, jjc_v2_parts.create_handle_to_body_collar),
            ('Item 5 - Lower slim body shell', jjc_v2_parts.Z_LOWER_BODY_MM, jjc_v2_parts.create_lower_body_shell),
            ('Item 6 - Upper slim body shell', jjc_v2_parts.Z_UPPER_BODY_MM, jjc_v2_parts.create_upper_body_shell),
            ('Item 7 - Nose cap', jjc_v2_parts.Z_NOSE_MM, jjc_v2_parts.create_nose_cap),
        ]

        occurrences = []
        for name, z_offset_mm, builder in parts:
            occurrence, _body = add_part_component(name, z_offset_mm, builder)
            occurrences.append(occurrence)

        ui.activeSelections.clear()
        if occurrences:
            ui.activeSelections.add(occurrences[0])

        ui.messageBox(
            'JJC V2 assembly created.\n\n'
            'Each club part is now a separate Fusion component created from '
            'the shared V2 part builders.\n\n'
            f'Overall length: {jjc_v2_parts.TOTAL_LENGTH_MM} mm'
        )

    except RuntimeError as error:
        if ui:
            ui.messageBox(
                'Failed to create a multi-component assembly.\n\n'
                'Fusion is probably in a Part Design document. Create a new '
                'Hybrid Design or Assembly Design, then run this script again.\n\n'
                f'Details:\n{error}'
            )
    except:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')
