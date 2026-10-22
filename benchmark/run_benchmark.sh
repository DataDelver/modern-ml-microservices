#!/usr/bin/env bash
# Benchmarks the housing-price orchestrator pre- and post- async conversion.
#   pre  : commit bba5b4d ("Part ten")      -> sync endpoints + httpx.Client
#   post : current HEAD (part-twelve)       -> async endpoints + httpx.AsyncClient
# Both run in the same venv, single uvicorn process each, against one mock
# model server (simulated inference delay = $MODEL_DELAY_MS, default 50 ms).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$REPO_ROOT/.venv/bin/python"
PRE_COMMIT="${PRE_COMMIT:-bba5b4d}"
WORK="$(mktemp -d /tmp/orch-bench.XXXXXX)"
RESULTS="$WORK/results"
mkdir -p "$RESULTS"

MODEL_PORT=18099
PRE_PORT=18080
POST_PORT=18081
PIDS=()

cleanup() {
  for pid in "${PIDS[@]:-}"; do kill "$pid" 2>/dev/null || true; done
  wait 2>/dev/null || true
  git -C "$REPO_ROOT" worktree remove --force "$WORK/pre-async" 2>/dev/null || true
  rm -rf "$WORK"
}
trap cleanup EXIT

echo "==> Checking out pre-async version ($PRE_COMMIT) into temp worktree"
git -C "$REPO_ROOT" worktree add --detach --force "$WORK/pre-async" "$PRE_COMMIT"

echo "==> Starting mock model server on :$MODEL_PORT (delay ${MODEL_DELAY_MS:-50} ms)"
MODEL_DELAY_MS="${MODEL_DELAY_MS:-50}" PORT="$MODEL_PORT" "$PY" "$REPO_ROOT/benchmark/mock_model_server.py" &
PIDS+=($!)

echo "==> Starting PRE-async orchestrator on :$PRE_PORT"
cd "$WORK/pre-async/housing-price-orchestrator/src"
MODEL_URL="http://127.0.0.1:$MODEL_PORT" ENV=dev "$PY" -m uvicorn main:app --port "$PRE_PORT" --log-level warning &
PIDS+=($!)
cd "$REPO_ROOT"

echo "==> Starting POST-async orchestrator on :$POST_PORT"
cd "$REPO_ROOT/housing-price-orchestrator/src"
MODEL_URL="http://127.0.0.1:$MODEL_PORT" ENV=dev "$PY" -m uvicorn main:app --port "$POST_PORT" --log-level warning &
PIDS+=($!)
cd "$REPO_ROOT"

echo "==> Waiting for readiness"
for port in "$PRE_PORT" "$POST_PORT"; do
  for _ in $(seq 1 100); do
    code=$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$port/api/v1/price/predict" -X POST \
        -H 'Content-Type: application/json' -d '{}' || true)
    # 422 (validation) or 200 means the app is serving; 000/5xx means not ready yet
    { [ "$code" = "422" ] || [ "$code" = "200" ]; } && break
    sleep 0.2
  done
done
echo "    both orchestrators are up"

echo "==> Running workload against PRE-async (:$PRE_PORT)"
"$PY" "$REPO_ROOT/benchmark/bench.py" --base-url "http://127.0.0.1:$PRE_PORT" --out "$RESULTS/pre.json" >/dev/null

echo "==> Running workload against POST-async (:$POST_PORT)"
"$PY" "$REPO_ROOT/benchmark/bench.py" --base-url "http://127.0.0.1:$POST_PORT" --out "$RESULTS/post.json" >/dev/null

cp "$RESULTS/pre.json" "$RESULTS/post.json" "$REPO_ROOT/benchmark/"
echo
echo "================= COMPARISON (v = better) ================="
"$PY" "$REPO_ROOT/benchmark/compare.py" "$RESULTS/pre.json" "$RESULTS/post.json"
echo "============================================================"
echo "Raw JSON reports saved to: $REPO_ROOT/benchmark/pre.json, $REPO_ROOT/benchmark/post.json"
