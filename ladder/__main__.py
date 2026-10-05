"""入口：跑固定场景，打印每次结算后的分数。"""

import json
import sys

from .drift import Ladder


def scenario(name):
    if name == "decay":
        ladder = Ladder(10_000, 1_000, 5, 0)
        ladder.join("p1", 100, 0)
        return ladder, [("m1", "p1", 0, 15_500)]
    if name == "floor":
        ladder = Ladder(10_000, 1_000, 5, 50)
        ladder.join("p1", 100, 0)
        return ladder, [("m1", "p1", 0, 100_000)]
    if name == "idempotent":
        ladder = Ladder(10_000, 1_000, 5, 0)
        ladder.join("p1", 100, 0)
        return ladder, [("m1", "p1", 10, 100), ("m1", "p1", 10, 200)]
    if name == "work":
        ladder = Ladder(10_000, 1_000, 5, 0)
        for i in range(2000):
            ladder.join("p%d" % i, 100, 0)
        return ladder, [("m%d" % i, "p%d" % i, 10, 100) for i in range(2000)]
    raise SystemExit("未知场景 %s" % name)


def run(ladder, matches, echo=True):
    for match_id, player, delta, at_ms in matches:
        rating, reason = ladder.settle(match_id, player, delta, at_ms)
        if echo:
            print(json.dumps({"id": match_id, "rating": rating, "reason": reason}))


def main(argv=None):
    args = (argv or sys.argv[1:])[:1]
    raw = args[0] if args else "--sample=decay"
    name = raw.split("=", 1)[1] if raw.startswith("--sample=") else raw
    ladder, matches = scenario(name)
    if name == "work":
        run(ladder, matches, echo=False)
        print(json.dumps({"players": len(ladder.players), "scanned": ladder.scanned}))
        return 0
    run(ladder, matches)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
