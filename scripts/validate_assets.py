import pandas as pd
from pathlib import Path
import datetime as dt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "hardware_asset_registry_50000.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

ALLOWED_STATUS = ["In Use", "In Repair", "Retired", "Decommissioned", "In Storage"]
SENSITIVE_CLASSES = ["Confidential", "Restricted"]
MAX_PATCH_AGE_DAYS = 30

def load_data():
    df = pd.read_csv(DATA_FILE)
    return df

def parse_dates(df):
    date_cols = [
        "purchase_date", "warranty_end_date", "eol_date",
        "eos_date", "last_security_patch", "last_scan_date"
    ]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

def check_uniqueness(df):
    issues = {}
    for col in ["asset_id", "asset_tag", "serial_number"]:
        if col in df.columns and df[col].duplicated().any():
            issues[f"duplicate_{col}"] = df[df[col].duplicated(keep=False)]
    return issues

def check_completeness(df):
    issues = {}
    critical_cols = [
        "asset_id", "asset_tag", "device_category", "manufacturer",
        "serial_number", "physical_location", "current_owner", "asset_status"
    ]
    for col in critical_cols:
        if col in df.columns:
            null_rows = df[df[col].isna() | (df[col] == "")]
            if not null_rows.empty:
                issues[f"missing_{col}"] = null_rows
    return issues

def check_status_validity(df):
    issues = {}
    if "asset_status" in df.columns:
        invalid = df[~df["asset_status"].isin(ALLOWED_STATUS)]
        if not invalid.empty:
            issues["invalid_asset_status"] = invalid
    return issues

def check_lifecycle(df):
    issues = {}
    if {"purchase_date", "warranty_end_date"}.issubset(df.columns):
        bad_order = df[df["warranty_end_date"] < df["purchase_date"]]
        if not bad_order.empty:
            issues["warranty_before_purchase"] = bad_order

    if {"warranty_end_date", "eol_date"}.issubset(df.columns):
        warranty_after_eol = df[df["warranty_end_date"] > df["eol_date"]]
        if not warranty_after_eol.empty:
            issues["warranty_after_eol"] = warranty_after_eol

    if {"eol_date", "eos_date"}.issubset(df.columns):
        eos_before_eol = df[df["eos_date"] < df["eol_date"]]
        if not eos_before_eol.empty:
            issues["eos_before_eol"] = eos_before_eol

    return issues

def check_security_policy(df):
    issues = {}
    if "data_classification" in df.columns:
        sensitive = df[df["data_classification"].isin(SENSITIVE_CLASSES)]
        # Encryption
        if "encryption_enabled" in df.columns:
            not_encrypted = sensitive[sensitive["encryption_enabled"] == False]
            if not not_encrypted.empty:
                issues["sensitive_not_encrypted"] = not_encrypted
        # AV & firewall
        if {"antivirus_installed", "firewall_enabled"}.issubset(df.columns):
            no_av_fw = sensitive[
                (sensitive["antivirus_installed"] == False) |
                (sensitive["firewall_enabled"] == False)
            ]
            if not no_av_fw.empty:
                issues["sensitive_missing_protection"] = no_av_fw
    return issues

def check_patch_compliance(df):
    issues = {}
    if "patch_compliance_days" in df.columns:
        non_compliant = df[df["patch_compliance_days"] > MAX_PATCH_AGE_DAYS]
        if not non_compliant.empty:
            issues["patch_non_compliant"] = non_compliant
    return issues

def check_risk_consistency(df):
    issues = {}
    if {"risk_score", "vulnerability_count"}.issubset(df.columns):
        # Example: high risk but zero vulnerabilities or vice versa
        suspicious = df[
            ((df["risk_score"] >= 80) & (df["vulnerability_count"] == 0)) |
            ((df["risk_score"] <= 20) & (df["vulnerability_count"] > 50))
        ]
        if not suspicious.empty:
            issues["risk_inconsistent_with_vulns"] = suspicious
    return issues

def check_financials(df):
    issues = {}
    today = pd.Timestamp.today()
    if {"purchase_price_usd", "depreciation_rate", "residual_value", "purchase_date"}.issubset(df.columns):
        age_years = (today - df["purchase_date"]).dt.days / 365.25
        expected_residual = df["purchase_price_usd"] * (1 - df["depreciation_rate"]) ** age_years
        diff = (df["residual_value"] - expected_residual).abs()
        out_of_range = df[diff > (0.2 * df["purchase_price_usd"])]
        if not out_of_range.empty:
            issues["residual_value_out_of_range"] = out_of_range
    return issues

def save_issue_frames(issue_dict, prefix):
    for name, frame in issue_dict.items():
        out_path = OUTPUT_DIR / f"{prefix}_{name}.xlsx"
        frame.to_excel(out_path, index=False)

def build_summary(df, all_issues):
    summary = {
        "total_assets": len(df),
        "unique_asset_id": df["asset_id"].nunique() if "asset_id" in df.columns else None,
        "unique_serial_number": df["serial_number"].nunique() if "serial_number" in df.columns else None,
        "issue_counts": {k: len(v) for k, v in all_issues.items()}
    }
    if "asset_status" in df.columns:
        summary["status_distribution"] = df["asset_status"].value_counts().to_dict()
    if "data_classification" in df.columns:
        summary["classification_distribution"] = df["data_classification"].value_counts().to_dict()
    if "risk_score" in df.columns:
        summary["avg_risk_score"] = df["risk_score"].mean()
    return summary

def export_summary(summary):
    rows = [
        {"Metric": "Total Assets", "Value": summary["total_assets"]},
        {"Metric": "Unique Asset IDs", "Value": summary["unique_asset_id"]},
        {"Metric": "Unique Serial Numbers", "Value": summary["unique_serial_number"]},
        {"Metric": "Average Risk Score", "Value": summary.get("avg_risk_score")}
    ]
    pd.DataFrame(rows).to_excel(OUTPUT_DIR / "summary_metrics.xlsx", index=False)

    if "status_distribution" in summary:
        pd.DataFrame(
            [{"asset_status": k, "count": v} for k, v in summary["status_distribution"].items()]
        ).to_excel(OUTPUT_DIR / "status_distribution.xlsx", index=False)

    if "classification_distribution" in summary:
        pd.DataFrame(
            [{"data_classification": k, "count": v} for k, v in summary["classification_distribution"].items()]
        ).to_excel(OUTPUT_DIR / "classification_distribution.xlsx", index=False)

def main():
    df = load_data()
    df = parse_dates(df)

    issues = {}
    issues.update(check_uniqueness(df))
    issues.update(check_completeness(df))
    issues.update(check_status_validity(df))
    issues.update(check_lifecycle(df))
    issues.update(check_security_policy(df))
    issues.update(check_patch_compliance(df))
    issues.update(check_risk_consistency(df))
    issues.update(check_financials(df))

    save_issue_frames(issues, "issues")

    summary = build_summary(df, issues)
    export_summary(summary)

    print("Validation complete. Issues and summary exported to 'output'.")

if __name__ == "__main__":
    main()
