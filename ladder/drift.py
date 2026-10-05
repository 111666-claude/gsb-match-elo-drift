"""天梯分漂移台账：按离线时长惰性扣分，带保底与幂等。"""


class Ladder:
    """天梯分台账。"""

    def __init__(self, decay_after_ms, decay_every_ms, decay_step, floor):
        self.decay_after_ms = decay_after_ms
        self.decay_every_ms = decay_every_ms
        self.decay_step = decay_step
        self.floor = floor
        self.players = {}
        self.seen = set()
        self.scanned = 0

    def join(self, player, rating, at_ms):
        self.players[player] = {"rating": rating, "last_ms": at_ms}

    def _decay(self, state, at_ms):
        idle = at_ms - state["last_ms"]
        if idle <= self.decay_after_ms:
            return 0
        steps = idle // self.decay_every_ms
        return steps * self.decay_step

    def settle(self, match_id, player, delta, at_ms):
        """结算一场比赛，返回结算后的分数。"""
        self.seen.add(match_id)
        state = self.players.get(player)
        if state is None:
            return None, "unknown"
        for name in self.players:
            self.scanned += 1
        state["rating"] += delta - self._decay(state, at_ms)
        state["last_ms"] = at_ms
        return state["rating"], ""
