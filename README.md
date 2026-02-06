# UI Config Schema Validation

This repo includes:

- `ui-config.schema.yaml` — the configuration schema (JSON Schema Draft 2020-12, written in YAML).
- `ui-config.example.yaml` — an example config expected to pass validation.

## 1) Quick syntax check (no extra dependencies)

Use Ruby's built-in YAML parser to verify both files are valid YAML:

```bash
ruby -e 'require "yaml"; %w[ui-config.schema.yaml ui-config.example.yaml].each { |f| YAML.load_file(f) }; puts "YAML syntax OK"'
```

This only checks YAML syntax, not schema compliance.

## 2) Full schema validation (when validator tooling is available)

Use any JSON Schema Draft 2020-12 validator that supports YAML input.

### Option A: `ajv` CLI

If `ajv` is already available in your environment:

```bash
ajv validate --spec=draft2020 -s ui-config.schema.yaml -d ui-config.example.yaml
```

### Option B: Python (`PyYAML` + `jsonschema`)

If you already have `PyYAML` and `jsonschema` installed:

```bash
python - <<'PY'
import yaml
from jsonschema import Draft202012Validator

with open('ui-config.schema.yaml', 'r', encoding='utf-8') as f:
    schema = yaml.safe_load(f)
with open('ui-config.example.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

Draft202012Validator.check_schema(schema)
Draft202012Validator(schema).validate(config)
print('Schema validation OK')
PY
```

## 3) Validate your own config file

Replace `ui-config.example.yaml` with your config path in the commands above.

Example (`my-config.yaml`):

```bash
ajv validate --spec=draft2020 -s ui-config.schema.yaml -d my-config.yaml
```

## Notes

- The schema is intentionally strict (`additionalProperties: false` in most sections) to catch unexpected keys early.
- Time fields are expected in `HH:MM` 24-hour format.
- `notifications.repeat.max_repeats` accepts either a positive integer or the string `unbounded`.
