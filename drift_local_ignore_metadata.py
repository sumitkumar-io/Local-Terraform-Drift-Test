import json

IGNORE_FIELDS = [
    "id",
    "arn",
    "provider",
    "timeouts",
    "directory_permission",
    "file_permission"
]

def classify_risk(actions):
    if "delete" in actions:
        return "HIGH"
    elif "update" in actions:
        return "MEDIUM"
    elif "create" in actions:
        return "LOW"
    return "NONE"

def analyze_drift(plan_file):
    with open(plan_file, 'r') as f:
        data = json.load(f)

    changes = data.get("resource_changes", [])

    print("\n========== CLEAN DRIFT SUMMARY ==========\n")

    for resource in changes:
        actions = resource["change"]["actions"]

        if actions != ["no-op"]:
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

if __name__ == "__main__":
    analyze_drift("plan.json")
