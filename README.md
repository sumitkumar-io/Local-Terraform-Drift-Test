README - local-terraform-drift-test
📌 Project Overview
local-terraform-drift-test is a lightweight local Terraform drift detection toolkit that analyzes Terraform plan/state JSON output and compares it with expected definitions (cloud_catalog) for drift validation.

Detects resource changes (create, update, delete) vs no-op
Classifies risk levels: LOW, MEDIUM, HIGH
Ignored common volatile fields (id, arn, provider, etc.)
Supports “catalog” (expected configuration) comparison
Includes progressively advanced engines:
drift_local.py (basic drift report)
drift_engine_dynamic.py (drift + risk + catalog compare)
drift_engine_enterprise.py (deep recursive diff + catalog compare)
📁 Repository files
main.tf - Terraform config for sample infra (or existing test context)
terraform.tfstate, plan.json, tfplan.binary - sample Terraform outputs
cloud_catalog.json, cloud_catalog2.json - expected resource content references
drift_local.py - minimal plan change reporter
drift_engine_dynamic.py - dynamic risk class + catalog match
drift_engine_enterprise.py - enterprise-style deep diff and catalog sync
drift_local_* - additional helper modules (ignore metadata, risk classification, cloud catalog logic)
⚙️ Prerequisites
Python 3.x
Terraform plan JSON (e.g., terraform show -json [tfplan.binary](http://_vscodecontentref_/12) > plan.json)
Optional: cloud catalog JSON map (address -> expected attributes)
▶️ Run examples
1. Basic drift check
reads plan.json
prints changed resources (includes fields changed)
2. Dynamic drift + risk + catalog compare
prompts for plan file and catalog file
prints:
drift resources
risk level
real drifted fields (ignores IGNORE_FIELDS)
catalog mismatches
3. Enterprise deep diff + catalog
prompts for plan + catalog
prints:
deep recursive diff with path/type/before-after
catalog expected vs actual differences
🛠️ How to prepare input
Generate plan JSON:

terraform plan -out=tfplan.binary
terraform show -json [tfplan.binary](http://_vscodecontentref_/16) > plan.json
Build cloud_catalog.json mapping:
{
  "aws_s3_bucket.example": {
    "bucket": "my-bucket",
    "acl": "private"
  }
}

Put plan file + catalog in repo root and run script.
✅ Expected behavior
If no drift: script prints No drift detected.
If drift exists: lists resource address, actions, risk, fields
If catalog mismatch: highlights fields where plan differs from catalog
If catalog has no resource: reports not found
💡 Tips
Use drift_engine_enterprise.py for the most detailed differences and evidence for non-idempotent TF drift.
For custom logic, adjust IGNORE_FIELDS list in engine files.
This is a local (offline) validation pattern; integrate with CI by using generated plan.json.
🧹 Next steps (suggested)
Add CLI argument parser (argparse) for automation.
Add output formats: JSON/CSV.
Add unit tests around deep_diff/classify_risk.
Add logging and "drift threshold" rules for alerting.
