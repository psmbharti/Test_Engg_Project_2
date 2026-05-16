import pandas as pd
from pathlib import Path
from lxml import etree

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "hardware_asset_registry_50000.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_data():
    return pd.read_csv(DATA_FILE)

def build_xml(df, max_assets=1000):
    root = etree.Element("AssetInventory")
    meta = etree.SubElement(root, "Metadata")
    etree.SubElement(meta, "SourceFile").text = DATA_FILE.name
    etree.SubElement(meta, "TotalAssets").text = str(len(df))

    assets_node = etree.SubElement(root, "Assets")

    for _, row in df.head(max_assets).iterrows():
        asset = etree.SubElement(assets_node, "Asset")
        etree.SubElement(asset, "AssetID").text = str(row.get("asset_id", ""))
        etree.SubElement(asset, "AssetTag").text = str(row.get("asset_tag", ""))
        etree.SubElement(asset, "Category").text = str(row.get("device_category", ""))
        etree.SubElement(asset, "Subcategory").text = str(row.get("device_subcategory", ""))
        etree.SubElement(asset, "Manufacturer").text = str(row.get("manufacturer", ""))
        etree.SubElement(asset, "Model").text = str(row.get("model_name", ""))
        etree.SubElement(asset, "SerialNumber").text = str(row.get("serial_number", ""))
        etree.SubElement(asset, "Location").text = str(row.get("physical_location", ""))
        etree.SubElement(asset, "LocationCriticality").text = str(row.get("location_criticality", ""))
        etree.SubElement(asset, "Owner").text = str(row.get("current_owner", ""))
        etree.SubElement(asset, "Status").text = str(row.get("asset_status", ""))
        etree.SubElement(asset, "BusinessFunction").text = str(row.get("business_function", ""))
        etree.SubElement(asset, "OS").text = str(row.get("operating_system", ""))
        etree.SubElement(asset, "OSVersion").text = str(row.get("os_version", ""))
        etree.SubElement(asset, "RiskScore").text = str(row.get("risk_score", ""))
        etree.SubElement(asset, "DataClassification").text = str(row.get("data_classification", ""))
        etree.SubElement(asset, "EncryptionEnabled").text = str(row.get("encryption_enabled", ""))
        etree.SubElement(asset, "UptimePercentage").text = str(row.get("uptime_percentage", ""))

    return root

def main():
    df = load_data()
    root = build_xml(df)
    tree = etree.ElementTree(root)
    out_file = OUTPUT_DIR / "asset_inventory_config.xml"
    tree.write(str(out_file), pretty_print=True, xml_declaration=True, encoding="UTF-8")
    print(f"XML configuration generated: {out_file}")

if __name__ == "__main__":
    main()
