"""Look up billing metadata for one original logical request. Never resubmits."""
import argparse
import json
import sys
import urllib.parse
from sarovi_http import Sarovi

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--idempotency-key", required=True)
a = p.parse_args()
try:
    data, request_id = Sarovi().request("/requests/lookup?idempotency_key=" + urllib.parse.quote(a.idempotency_key, safe=""))
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print("An empty receipt does not prove the original request was uncharged.", file=sys.stderr)
except (ValueError, RuntimeError, OSError) as error:
    print(str(error), file=sys.stderr); sys.exit(1)
