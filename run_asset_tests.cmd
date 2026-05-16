@echo off
cd /d C:\QA_Projects\HardwareAssetRegistry
call venv\Scripts\activate

echo Running asset validation...
python scripts\validate_assets.py

echo Generating XML configuration...
python scripts\generate_asset_xml.py

echo Test run complete. Check the 'output' folder.
pause
