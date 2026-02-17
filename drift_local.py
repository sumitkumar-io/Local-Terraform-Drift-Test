import json

def analyze_drift(plan_file):
    with open(plan_file, 'r') as f:
        data = json.load(f)

    changes = data.get("resource_changes", [])

    print("\n====== DRIFT SUMMARY ======\n")

    drift_found = False

    for resource in changes:
        actions = resource["change"]["actions"]

        if actions != ["no-op"]:
            drift_found = True
            print("Resource:", resource["address"])
            print("Actions:", actions)

            before = resource["change"].get("before") or {}
            after = resource["change"].get("after") or {}

            print("Changed Fields:")

            for key in after:
                if before.get(key) != after.get(key):
                    print(" -", key)

            print("--------------------------------")

    if not drift_found:
        print("No drift detected.")

if __name__ == "__main__":
    analyze_drift("plan.json")
