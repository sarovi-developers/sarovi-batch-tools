# Sarovi CSV tools

Translate a CSV column or classify support messages with an AI model. Python standard library only. Dry-run first, preview offline, then process a small batch with a durable progress journal.

[فارسی](README.fa.md) · [Create a key](https://api.sarovi.site/developers/start?utm_source=github&utm_medium=organic&utm_campaign=developer_tools_202610&utm_content=sarovi-batch-tools_key) · [Models & pricing](https://api.sarovi.site/developers/pricing?utm_source=github&utm_medium=organic&utm_campaign=developer_tools_202610&utm_content=sarovi-batch-tools_pricing)

## Try it without an API key

Python 3.10+ is required.

```sh
git clone https://github.com/sarovi-developers/sarovi-batch-tools.git
cd sarovi-batch-tools
python3 batch.py translate samples/messages.csv
python3 batch.py translate samples/messages.csv --demo --output demo.results.jsonl
python3 export_csv.py demo.results.jsonl demo.results.csv
```

The first command reports the planned request count with zero network calls. Demo output is synthetic and labeled. The export creates a new CSV and escapes formula-leading output for spreadsheets.

## Translate for real

```sh
export SAROVI_API_KEY="YOUR_SAROVI_API_KEY"
python3 batch.py translate samples/messages.csv   --column text --target Persian --limit 5 --max-tokens 512   --output translation.results.jsonl --run
```

In PowerShell, use `$env:SAROVI_API_KEY="YOUR_SAROVI_API_KEY"`. Set `SAROVI_MODEL` to change models. `SAROVI_BASE_URL` can select either Sarovi domain.

Only the selected text cells are sent to the API. Real runs consume your account credits. Start with the sample file and a small key/project budget; the output-token cap does not guarantee a monetary ceiling.

## Classify support messages

```sh
python3 batch.py classify samples/messages.csv   --labels billing technical other --limit 5   --output labels.results.jsonl --run
```

The tool records the returned label and marks an unexpected label as `valid_label: false`. It does not spend another request trying to repair it. Review AI labels before using them in an automated workflow.

## Resume safely

Run the same command with `--resume`. Completed rows are skipped, and settings/input hashes prevent mixing different jobs. The default is five non-empty rows; increase `--limit` explicitly, up to 100.

A pending or uncertain request stops the run and resume. Keep its journal and inspect its original billing metadata:

```sh
python3 receipt.py --idempotency-key=ORIGINAL_KEY
```

Receipt reads need `usage:read`. Empty lookup results are not proof of no charge. No automatic resubmission or recovery charge is made. Run only one process against a journal at a time.

The journal contains generated output; keep it private. The sample CSV is synthetic. Your original CSV is never overwritten. See [API notes](docs/API-NOTES.md) for provider retention, idempotency limits, and billing details.

## Checks

```sh
python3 -m unittest -v test_batch.py
```

Tests cover zero-network dry-run, offline preview, completed-row deduplication, changed inputs, ambiguous requests, and limits. No paid test calls.

[Complete your first API request](https://api.sarovi.site/developers/start?utm_source=github&utm_medium=organic&utm_campaign=developer_tools_202610&utm_content=sarovi-batch-tools_first_request) · [API cookbook](https://github.com/sarovi-developers/sarovi-api-cookbook)

MIT-licensed code. Sarovi API usage is billed separately.
