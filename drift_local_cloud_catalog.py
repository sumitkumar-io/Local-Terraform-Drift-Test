import json

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

CATALOG_FILE = "cloud_catalog.json"

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

def analyze(plan_file):
    with open(plan_file, "r") as f:
        data = json.load(f)

    print("\n========== DRIFT ANALYSIS ==========\n")

    drift_found = False

    for resource in data.get("resource_changes", []):
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

def compare_with_catalog(plan_file):
    try:
        with open(CATALOG_FILE, "r") as f:
            catalog = json.load(f)
    except FileNotFoundError:
        print("\nCloud catalog file not found. Skipping catalog comparison.")
        return

    with open(plan_file, "r") as f:
        plan_data = json.load(f)

    print("\n========== CATALOG COMPARISON ==========\n")

    for resource in plan_data.get("resource_changes", []):
        address = resource["address"]
        after = resource["change"].get("after") or {}

        if address in catalog:
            print("Comparing Resource:", address)

            catalog_fields = catalog[address]

            for key in catalog_fields:
                if after.get(key) != catalog_fields.get(key):
                    print(f" - Drift from Catalog in field: {key}")

            print("-----------------------------------")

# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":

    plan_file = input("Enter plan JSON file path (example: plan.json): ").strip()

    try:
        analyze(plan_file)
        compare_with_catalog(plan_file)
    except FileNotFoundError:
        print("Plan file not found. Please check the path.")
