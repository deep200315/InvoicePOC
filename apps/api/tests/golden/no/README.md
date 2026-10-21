# Golden set · Norway

Put the real invoices here, each with an `expected.json` written by hand (task T-106, owner Kuhu):

- `<invoice file>` (PDF or XLSX, exactly as issued, never edited)
- `<invoice file>.expected.json` with the mapped field id -> value, the expected requirements and the expected score

The golden test (`tests/golden/test_golden.py`) fails if the pipeline output differs from it.
