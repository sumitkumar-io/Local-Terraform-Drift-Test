import json
import os

# ==========================================
# CONFIGURATION
# ==========================================

IGNORE_FIELDS = [
    "id",
    "arn",
    "provider",
    "timeouts",
    "directory_permission",
    "file_permission",
    "lifecycle"
]

# ==========================================
# RISK CLASSIFICATION
# ==========================================

def classify_risk(actions):
    if "delete" in actions:
        return "HIGH"
    elif "update" in actions:
        return "MEDIUM"
    elif "create" in actions:
        return "LOW"
    return "NONE"

# ==========================================
# DRIFT ANALYSIS
# ==========================================

def analyze_drift(plan_data):
    print("\n========== DRIFT ANALYSIS ==========\n")

    drift_found = False

    for resource in plan_data.get("resource_changes", []):
        actions = resource["change"]["actions"]

        if actions != ["no-op"]:
            drift_found = True

            print("Resource:", resource["address"])
            print("Actions:", actions)
            print("Risk Level:", classify_risk(actions))

            before = resource["change"].get("before") or {}
            after = resource["change"].get("after") or {}

            print("Real Drifted Fields:")

            for key in after:
                if key in IGNORE_FIELDS:
                    continue
                if before.get(key) != after.get(key):
                    print(" -", key)

            print("-----------------------------------")

    if not drift_found:
        print("No drift detected. Infrastructure is aligned.")

# ==========================================
# CLOUD CATALOG COMPARISON
# ==========================================

def compare_with_catalog(plan_data, catalog_data):
    print("\n========== CATALOG COMPARISON ==========\n")

    catalog_matched = False

    for resource in plan_data.get("resource_changes", []):
        address = resource["address"]
        after = resource["change"].get("after") or {}

        if address in catalog_data:
            catalog_matched = True
            print("Comparing Resource:", address)

            catalog_fields = catalog_data[address]
            mismatch_found = False

            for key in catalog_fields:
                if after.get(key) != catalog_fields.get(key):
                    mismatch_found = True
                    print(f" - Drift from Catalog in field: {key}")

            if not mismatch_found:
                print(" No differences from catalog.")

            print("-----------------------------------")

    if not catalog_matched:
        print("No matching resources found in catalog.")

# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":

    plan_file = input("Enter plan JSON file path (example: plan.json): ").strip()
    catalog_file = input("Enter catalog JSON file path (example: cloud_catalog.json): ").strip()

    if not os.path.exists(plan_file):
        print("Plan file not found.")
        exit()

    if not os.path.exists(catalog_file):
        print("Catalog file not found.")
        exit()

    with open(plan_file, "r") as f:
        plan_data = json.load(f)

    with open(catalog_file, "r") as f:
        catalog_data = json.load(f)

    analyze_drift(plan_data)
    compare_with_catalog(plan_data, catalog_data)
