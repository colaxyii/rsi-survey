"""Eight-round profile-write stream under the paper's update rule.

Three policies: write-all, an oracle gate that knows the far future (upper bound), and a
hand-made recent-drift gate. Naive near-future labels are computed alongside the actual
far-future outcome so the two can be compared round by round.

All angles are constructed for hand-checking; nothing here is measured from the paper.
"""
import numpy as np

HISTORY = [0, 10, -10, 5, -5, 15]        # durable interests, |H| = 6
FAR = [40, 45, 35, 50]                   # far-future window F_u, mean direction 42.5 deg
STREAM = [(45, "长期"), (-70, "瞬时"), (-62, "瞬时"), (30, "长期"),
          (-75, "瞬时"), (38, "长期"), (-68, "瞬时"), (50, "长期")]
SHORT_WINDOW = 3
GAP_THRESHOLD = 0.35


def unit(deg):
    r = np.deg2rad(deg)
    return np.array([np.cos(r), np.sin(r)])


def direction(degs):
    v = np.mean([unit(d) for d in degs], axis=0)
    return v / np.linalg.norm(v)


def angle(v):
    return float(np.degrees(np.arctan2(v[1], v[0])))


def run(policy):
    hist = list(HISTORY)
    rows, hurts = [], 0
    for k, (c, note) in enumerate(STREAM, 1):
        base = direction(hist)
        long_s = float(np.dot(unit(c), base))
        short_s = float(np.dot(unit(c), direction(hist[-SHORT_WINDOW:])))
        gap = short_s - long_s
        raw = (len(hist) * np.mean([unit(d) for d in hist], axis=0) + unit(c)) / (len(hist) + 1)
        upd = raw / np.linalg.norm(raw)
        far_before = float(np.dot(base, direction(FAR)))
        far_after = float(np.dot(upd, direction(FAR)))
        near_win = [STREAM[i][0] for i in range(k, min(k + 3, len(STREAM)))] or [c]
        near_label = int(float(np.dot(upd, direction(near_win))) < float(np.dot(base, direction(near_win))))
        far_hurt = far_after < far_before
        write = {"all": True, "oracle": not far_hurt, "gap": gap < GAP_THRESHOLD}[policy]
        rows.append(dict(round=k, cand=c, note=note, long_s=long_s, short_s=short_s, gap=gap,
                         after=angle(upd), far_before=far_before, far_after=far_after,
                         near_label=near_label, far_hurt=far_hurt, write=write))
        if write:
            hist.append(c)
            hurts += int(far_hurt)
    return rows, angle(direction(hist)), float(np.dot(direction(hist), direction(FAR))), hurts


for pol, title in (("all", "策略一 write-all"),
                   ("gap", "策略二 手工闸门：近期偏移 gap >= 0.35 就拦截"),
                   ("oracle", "策略三 oracle 闸门：只拦截真正伤害远未来的写入")):
    rows, final_ang, final_align, hurts = run(pol)
    print(f"\n=== {title}")
    print(" round | 候选 | 类型 | cand-long | cand-short |  gap  | 近标签 | 写后画像角 | 远对齐 前→后 | 远伤害 | 决定")
    for r in rows:
        print(f"   {r['round']:2d}  | {r['cand']:5d}| {r['note']} | {r['long_s']:9.3f} | {r['short_s']:10.3f} "
              f"| {r['gap']:+.2f} |   {r['near_label']}    | {r['after']:8.2f}   | "
              f"{r['far_before']:.3f}→{r['far_after']:.3f} |  {'是' if r['far_hurt'] else '否':2s}    | "
              f"{'写入' if r['write'] else '拦截'}")
    print(f"   最终：画像角 {final_ang:.2f}°，远未来对齐 {final_align:.3f}，远伤害次数 {hurts}/8")

rows_all, *_ = run("all")
bad = [r["round"] for r in rows_all if r["near_label"] != int(r["far_hurt"])]
print(f"\n近标签与远结果不一致的轮次：{bad}，共 {len(bad)}/8")
