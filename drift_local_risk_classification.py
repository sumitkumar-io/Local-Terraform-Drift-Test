import json

# ======================
# RISK CLASSIFICATION
# ======================

def classify_risk(actions):
    if "delete" in actions:
        return "HIGH"
    elif "update" in actions:
        return "MEDIUM"
    elif "create" in actions:
        return "LOW"
    return "NONE"

# ======================
# DRIFT ANALYSIS
# ======================

def analyze_drift(plan_file):
    with open(plan_file, 'r') as f:
        data = json.load(f)

    changes = data.get("resource_changes", [])

    print("\n========== DRIFT SUMMARY ==========\n")

    for resource in changes:
        actions = resource["change"]["actions"]

        if actions != ["no-op"]:
            print("Resource:", resource["address"])
            print("Actions:", actions)
            print("Risk Level:", classify_risk(actions))
            print("-----------------------------------")

if __name__ == "__main__":
    analyze_drift("plan.json")
