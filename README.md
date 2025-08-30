# FSA → RegExp (CLI)

Validate an FSA and translate it to a regular expression. Input is taken from `input.txt`; output is the regex (or `E#` error) to stdout.

## Run
```bash
python3 fsa2regex.py
```

## Input format (input.txt)

- type=[deterministic|non-deterministic]
- states=[q0,q1,...]
- alphabet=[a,b,_]
- initial=[q0]
- accepting=[q1,q2]
- transitions=[q0>a>q1,q1>b>q2,...]

## Notes
- Errors: E1–E7 (malformed, missing initial/accepting, unknown states/alphabet, disjoint states, non-determinism).
- Uses state-elimination with eps for ε.

