# match-elo-drift

天梯分漂移：按离线时长惰性扣分。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m ladder --sample=decay
python3 -m ladder --sample=floor
python3 -m ladder --sample=idempotent
python3 -m ladder --sample=work
```

## 口径

- **漂移**：离线超过 `decay_after_ms` 之后，每满 `decay_every_ms` 扣 `decay_step` 分，不满一个周期的不扣。宽限期本身不产生扣分。
- **保底**：分数不得低于 `floor`。
- **惰性结算**：漂移只在结算比赛时补算，不预生成扣分记录。
- **幂等**：同一个 `match_id` 只结算一次，重复出现不改变分数。
- **索引**：结算按玩家索引取台账，`scanned` 不得随玩家总数放大。

## 不变量

- 分数单调不低于 `floor`。
- 结算后 `last_ms` 等于本次结算时刻。
- 同一 `match_id` 重复提交得到的分数逐次相同。

## 输出契约

每次结算打印一行：

```
{"id": <赛事号>, "rating": <结算后分数>, "reason": <拒绝原因或空串>}
```

`--sample=work` 只打印 `{"players": N, "scanned": N}`。
