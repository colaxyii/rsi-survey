"""Probe: over a long stream, does uniform attenuation behave like selective writing?

My own experiment, not a result from the paper. Same update rule, same 2-D geometry.
Half the stream is durable-interest traffic, half is transient traffic.
"""
import numpy as np

rng = np.random.default_rng(7)
DURABLE, TRANSIENT, FAR = 45.0, -65.0, 42.5
ROUNDS = 300
STREAM = [DURABLE + rng.normal(0, 8) if rng.random() < .5 else TRANSIENT + rng.normal(0, 8)
          for _ in range(ROUNDS)]


def unit(deg):
    r = np.deg2rad(deg)
    return np.array([np.cos(r), np.sin(r)])


def direction(degs):
    v = np.mean([unit(d) for d in degs], axis=0)
    return v / np.linalg.norm(v)


def run(write_weight, gate=None):
    hist = [0.0, 8.0, -8.0, 4.0, -4.0, 12.0]
    hurts, writes = 0, 0
    far = unit(FAR)
    for c in STREAM:
        base = direction(hist)
        short = direction(hist[-5:])
        long_s = float(np.dot(unit(c), base))
        gap = float(np.dot(unit(c), short)) - long_s
        w = 0.0 if (gate and gate(long_s, gap)) else write_weight
        if w == 0:
            continue
        raw = (len(hist) * np.mean([unit(d) for d in hist], axis=0) + w * unit(c)) / (len(hist) + w)
        upd = raw / np.linalg.norm(raw)
        if float(np.dot(upd, far)) < float(np.dot(base, far)):
            hurts += 1
        hist.append(c)
        writes += 1
    final = direction(hist)
    return hurts / writes if writes else 0.0, float(np.dot(final, far)), writes


configs = [
    ("write-all (w=1)", 1.0, None),
    ("constant w=0.75", 0.75, None),
    ("constant w=0.50", 0.50, None),
    ("constant w=0.25", 0.25, None),
    ("constant w=0.10", 0.10, None),
    ("gate: long<0.5 and gap>0.2 blocked", 1.0, lambda l, g: l < 0.5 and g > 0.2),
    ("gate: long<0.4 (block weakly grounded)", 1.0, lambda l, g: l < 0.4),
    ("oracle (block any harmful write)", 1.0, None),
]

print(f"stream: {ROUNDS} rounds, 50% durable(45±8deg) / 50% transient(-65±8deg), "
      f"far-future direction {FAR}deg")
print(f"{'policy':42s} {'hurt rate':>10s} {'final far align':>16s} {'writes':>7s}")
for name, w, gate in configs:
    if name.startswith("oracle"):
        hist = [0.0, 8.0, -8.0, 4.0, -4.0, 12.0]
        far = unit(FAR)
        writes = 0
        for c in STREAM:
            base = direction(hist)
            raw = (len(hist) * np.mean([unit(d) for d in hist], axis=0) + unit(c)) / (len(hist) + 1)
            upd = raw / np.linalg.norm(raw)
            if float(np.dot(upd, far)) >= float(np.dot(base, far)):
                hist.append(c)
                writes += 1
        final = direction(hist)
        print(f"{name:42s} {'0.000':>10s} {float(np.dot(final, far)):16.3f} {writes:7d}")
        continue
    hurt, align, writes = run(w, gate)
    print(f"{name:42s} {hurt:10.3f} {align:16.3f} {writes:7d}")
