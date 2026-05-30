# Simple Washer Fusion Script

This folder contains a small Autodesk Fusion Python script that creates a simple washer from two sketch circles and an extrusion.

## Run The Script

1. Open Autodesk Fusion.
2. Create a new design.
3. Switch to the **Utilities** tab.
4. Open **Add-Ins > Scripts and Add-Ins**.
5. Select the **Scripts** tab.
6. If `make_simple_washer` is listed, select it.
7. If it is not listed, click the green **+** button and add this folder:

   ```text
   test/make_simple_washer
   ```

8. Click **Run**.

The script pauses with message boxes after each major step so you can inspect Fusion before continuing.

## Debug In VS Code

1. In Fusion, open **Utilities > Add-Ins > Scripts and Add-Ins**.
2. Select `make_simple_washer`.
3. Click **Edit** to let Fusion open the script in VS Code.
4. In VS Code, set breakpoints in `make_simple_washer.py`.
5. Start the **Python: Attach** debug configuration.
6. Run the script from Fusion.

If VS Code says **connection refused**, Fusion's debug listener is probably not running. Reopen the script from Fusion with **Edit**, then try attaching again.

To check whether anything is listening on port `9000`:

```powershell
Get-NetTCPConnection -LocalPort 9000 -ErrorAction SilentlyContinue |
  Select-Object LocalAddress,LocalPort,State,OwningProcess
```

If no row appears, Fusion is not listening on that port.

## Browser Notes

Fusion does not provide a scriptable API or preference to auto-expand the main Browser tree folders like **Sketches** and **Bodies**.

For this learning script:

1. When the script pauses after creating the sketch, manually expand **Sketches** in the Browser.
2. After the extrusion creates the washer, manually expand **Bodies** if Fusion leaves it collapsed.
3. Watch the canvas selection as well as the Browser. The script selects each object as it creates it.

## Units

Fusion API length values are in centimeters.

```python
outer_diameter = 4.0   # 40 mm
inner_diameter = 1.5   # 15 mm
thickness = 0.3        # 3 mm
```

Change those values to resize the washer.

## Common Debugger Quirk

After the script finishes, VS Code may open a tab named `<string>` with a message like:

```text
Could not load source '<string>'
```

That usually means the debugger tried to step into Fusion's internal script wrapper after your script returned. If the washer was created and Fusion did not show a traceback from the script, this is just debugger noise. Press **Continue** or stop debugging.
