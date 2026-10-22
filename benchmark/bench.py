"""Load-testing client for the housing-price orchestrator.

Runs a fixed scenario set against one running orchestrator instance and
writes a JSON metrics report. Scenarios:
  - sequential   : 50 single predictions, 1 at a time (raw latency)
  - concurrent   : 300 single predictions at concurrency 10 / 50 / 100
  - batch        : 150 batch predictions (batch size 20) at concurrency 10 / 50
"""

import argparse
import asyncio
import json
import math
import time

import httpx

SINGLE_PAYLOAD = {
    'id': 1,
    'ms_sub_class': 20,
    'ms_zoning': 'RL',
    'lot_area': 8450,
    'street': 'Pave',
    'lot_shape': 'Reg',
    'land_contour': 'Lvl',
    'utilities': 'AllPub',
    'lot_config': 'Inside',
    'land_slope': 'Gtl',
    'neighborhood': 'CollgCr',
    'condition_1': 'Norm',
    'condition_2': 'Norm',
    'bldg_type': '1Fam',
    'house_style': '2Story',
    'overall_qual': 7,
    'overall_cond': 5,
    'year_built': 2003,
    'year_remod_add': 2003,
    'roof_style': 'Gable',
    'roof_matl': 'CompShg',
    'exterior_1st': 'VinylSd',
    'exterior_2nd': 'VinylSd',
    'exter_qual': 'Gd',
    'exter_cond': 'TA',
    'foundation': 'PConc',
    'bsmt_fin_sf_1': 706,
    'bsmt_fin_sf_2': 0,
    'bsmt_unf_sf': 150,
    'total_bsmt_sf': 856,
    'heating': 'GasA',
    'heating_qc': 'Ex',
    'central_air': 'Y',
    'first_flr_sf': 856,
    'second_flr_sf': 854,
    'low_qual_fin_sf': 0,
    'gr_liv_area': 1710,
    'bsmt_full_bath': 1,
    'bsmt_half_bath': 0,
    'full_bath': 2,
    'half_bath': 1,
    'bedroom_abv_gr': 3,
    'kitchen_abv_gr': 1,
    'kitchen_qual': 'Gd',
    'tot_rms_abv_grd': 8,
    'functional': 'Typ',
    'fireplaces': 0,
    'garage_cars': 2,
    'garage_area': 548,
    'paved_drive': 'Y',
    'wood_deck_sf': 0,
    'open_porch_sf': 61,
    'enclosed_porch': 0,
    'three_ssn_porch': 0,
    'screen_porch': 0,
    'pool_area': 0,
    'misc_val': 0,
    'mo_sold': 2,
    'yr_sold': 2008,
    'sale_type': 'WD',
    'sale_condition': 'Normal',
}

BATCH_SIZE = 20


def make_batch_payload() -> dict:
    return {'data': [{**SINGLE_PAYLOAD, 'id': i + 1} for i in range(BATCH_SIZE)]}


def pct(sorted_vals: list[float], p: float) -> float | None:
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * (p / 100.0)
    f, c = math.floor(k), math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


async def run_scenario(
    name: str, client: httpx.AsyncClient, url: str, payload: dict, concurrency: int, total: int
) -> dict:
    sem = asyncio.Semaphore(concurrency)
    latencies: list[float] = []
    errors = 0

    async def one() -> None:
        nonlocal errors
        async with sem:
            t0 = time.perf_counter()
            try:
                resp = await client.post(url, json=payload)
                if resp.status_code != 200:
                    raise RuntimeError(f'HTTP {resp.status_code}')
            except Exception:
                errors += 1
                return
            latencies.append((time.perf_counter() - t0) * 1000.0)

    start = time.perf_counter()
    await asyncio.gather(*(one() for _ in range(total)))
    elapsed = time.perf_counter() - start

    srt = sorted(latencies)
    return {
        'scenario': name,
        'concurrency': concurrency,
        'requests': total,
        'succeeded': len(latencies),
        'errors': errors,
        'elapsed_s': round(elapsed, 3),
        'rps': round(len(latencies) / elapsed, 1) if elapsed > 0 else None,
        'latency_ms': {
            'p50': round(pct(srt, 50), 2) if srt else None,
            'p95': round(pct(srt, 95), 2) if srt else None,
            'p99': round(pct(srt, 99), 2) if srt else None,
            'max': round(srt[-1], 2) if srt else None,
        },
    }


async def bench(base_url: str) -> dict:
    results = []
    async with httpx.AsyncClient(timeout=60) as client:
        # warm-up
        for _ in range(10):
            resp = await client.post(f'{base_url}/api/v1/price/predict', json=SINGLE_PAYLOAD)
            resp.raise_for_status()

        results.append(
            await run_scenario('sequential', client, f'{base_url}/api/v1/price/predict', SINGLE_PAYLOAD, 1, 50)
        )
        for c in (10, 50, 100):
            results.append(
                await run_scenario(
                    f'concurrent-{c}', client, f'{base_url}/api/v1/price/predict', SINGLE_PAYLOAD, c, 300
                )
            )
        for c in (10, 50):
            results.append(
                await run_scenario(
                    f'batch-{c}', client, f'{base_url}/api/v1/price/predict/batch', make_batch_payload(), c, 150
                )
            )
    return {'base_url': base_url, 'scenarios': results}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    report = asyncio.run(bench(args.base_url))
    with open(args.out, 'w') as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
