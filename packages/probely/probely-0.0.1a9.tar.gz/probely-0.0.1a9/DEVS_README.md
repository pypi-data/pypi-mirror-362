# How to add pydantic schemas

Step 1: generate schema files
```bash
datamodel-codegen  --url https://developers.probely.com/openapi.yaml --input-file-type openapi --output-model-type pydantic_v2.BaseModel  --output deleteme_generated_schema.py --use-annotated --field-constraints --wrap-string-literal --use-double-quotes  --snake-case-field
```
Step 2: extract expected Pydantic models and add to sdk.schemas._schemas.py 
Step 3: delete generated file
