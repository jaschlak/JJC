"""Create the JJC V3 knob cap."""

import os
import sys
import traceback
import importlib
import adsk.core
import adsk.fusion


SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'JJCv3_shared')
if SHARED_DIR not in sys.path:
    sys.path.insert(0, SHARED_DIR)

import jjc_v3_parts  # noqa: E402

jjc_v3_parts = importlib.reload(jjc_v3_parts)


def run(_context):
    global jjc_v3_parts
    ui = None
    try:
        jjc_v3_parts = importlib.reload(jjc_v3_parts)
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        if not isinstance(design, adsk.fusion.Design):
            ui.messageBox('No active Fusion design.')
            return
        body = jjc_v3_parts.create_knob_cap(design.rootComponent)
        ui.activeSelections.clear()
        ui.activeSelections.add(body)
        ui.messageBox('V3 knob cap created.')
    except:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')
