# Contributing

ProofFlow Schema Sandbox is an experimental research environment, not a guaranteed solver. Contributions should preserve these boundaries:

1. do not force every project toward a complete answer;
2. do not delete or overwrite original research artifacts;
3. make objections easy but route closure difficult;
4. do not treat same-model agreement as independent review;
5. do not add an automatic `SOLVED` state;
6. require human confirmation before imported model text changes the research graph;
7. keep optional tools behind explicit project-level enablement;
8. record failed tool runs and route replacements rather than hiding them.

Before opening a pull request:

```bash
./scripts/test.sh
python -m compileall -q apps/api scripts tests
node --check prototype/app.js
npm run build --prefix apps/web
```

Feature proposals should describe which research state they create, preserve, invalidate, or make recoverable—not only the user-interface element they add.
