"""Prints a side-by-side comparison of two bench.py JSON reports."""

import json
import sys


def load(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def fmt_delta(pre: float | None, post: float | None, lower_is_better: bool = True) -> str:
    if pre is None or post is None:
        return 'n/a'
    if pre == 0:
        return 'n/a'
    pct = (post - pre) / pre * 100.0
    good = (pct < 0) if lower_is_better else (pct > 0)
    mark = 'v' if good else '^'
    return f'{pct:+.1f}% {mark}'


def main() -> None:
    pre = load(sys.argv[1])
    post = load(sys.argv[2])
    pre_by = {s['scenario']: s for s in pre['scenarios']}
    post_by = {s['scenario']: s for s in post['scenarios']}

    header = f'{"scenario":<14} {"metric":<10} {"sync (pre)":>12} {"async (post)":>13} {"delta":>12}'
    print(header)
    print('-' * len(header))
    for scen in pre_by:
        p, q = pre_by[scen], post_by[scen]
        rows = [
            ('rps', p['rps'], q['rps'], False),
            ('p50 ms', p['latency_ms']['p50'], q['latency_ms']['p50'], True),
            ('p95 ms', p['latency_ms']['p95'], q['latency_ms']['p95'], True),
            ('p99 ms', p['latency_ms']['p99'], q['latency_ms']['p99'], True),
            ('max ms', p['latency_ms']['max'], q['latency_ms']['max'], True),
            ('errors', p['errors'], q['errors'], True),
        ]
        for i, (metric, pv, qv, lower_better) in enumerate(rows):
            label = scen if i == 0 else ''
            print(f'{label:<14} {metric:<10} {str(pv):>12} {str(qv):>13} {fmt_delta(pv, qv, lower_better):>12}')
        print('-' * len(header))


if __name__ == '__main__':
    main()
