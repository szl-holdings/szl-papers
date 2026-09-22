#!/usr/bin/env python3
"""Render every figure in the triage paper from a receipts JSON.

Strict by default: a figure whose inputs are absent is SKIPPED with a reason,
never filled with invented numbers. --demo exercises the pipeline and watermarks
every panel SYNTHETIC.

    python figures.py --receipts data/receipts.json --out figures
    python figures.py --demo --out figures
"""
from __future__ import annotations
import argparse, json, math, pathlib, random, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

P = {"ink": "#12171c", "grid": "#d7dee5", "pass": "#2e7d5b", "fail": "#b4363f", "skip": "#8a949e",
     "a": "#1f5f8b", "b": "#c2703d", "c": "#5c4b8a", "d": "#3e7d7d", "e": "#8b5a6f"}
SEEDC = [P["a"], P["b"], P["c"], P["d"], P["e"]]
plt.rcParams.update({"figure.dpi": 160, "savefig.dpi": 300, "font.size": 9, "font.family": "serif",
  "mathtext.fontset": "cm", "axes.edgecolor": P["ink"], "axes.linewidth": 0.8, "axes.grid": True,
  "grid.color": P["grid"], "grid.linewidth": 0.6, "axes.spines.top": False,
  "axes.spines.right": False, "legend.frameon": False, "figure.constrained_layout.use": True})

SKIPPED: list[str] = []
WRITTEN: list[str] = []


def need(cond, fig, what):
    if not cond:
        SKIPPED.append(f"{fig}: missing {what}")
        return False
    return True


def finish(fig, name, out, demo):
    if demo:
        fig.text(0.5, 0.5, "SYNTHETIC", fontsize=54, color="#b4363f", alpha=0.12,
                 ha="center", va="center", rotation=28, zorder=10)
    for ext in ("pdf", "png"):
        fig.savefig(out / f"{name}.{ext}", bbox_inches="tight")
    plt.close(fig)
    WRITTEN.append(name)


def fig_loss(d, out, demo):
    seeds = d.get("seeds") or []
    if not need(any(s.get("train_loss") for s in seeds), "fig1_loss", "seeds[].train_loss"):
        return
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    for i, s in enumerate(seeds):
        tl = s.get("train_loss") or []
        if not tl:
            continue
        ax.plot([p["step"] for p in tl], [p["loss"] for p in tl], lw=1.4,
                color=SEEDC[i % 5], label=f"seed {s['seed']}", alpha=0.9)
    cur = [[p["loss"] for p in (s.get("train_loss") or [])] for s in seeds]
    cur = [c for c in cur if c]
    if len(cur) > 1:
        m = min(len(c) for c in cur)
        arr = np.array([c[:m] for c in cur])
        ax.fill_between([p["step"] for p in seeds[0]["train_loss"]][:m], arr.min(0), arr.max(0),
                        color=P["a"], alpha=0.10, lw=0)
    ax.set_xlabel("optimizer step")
    ax.set_ylabel("training loss (assistant turns only)")
    ax.set_title("Distillation loss across five seeds", loc="left", fontweight="bold")
    ax.legend(ncols=5, loc="upper right", fontsize=8)
    finish(fig, "fig1_loss", out, demo)


def fig_gate_ledger(d, out, demo):
    gates = d.get("gates") or []
    if not need(bool(gates), "fig2_gate_ledger", "gates[]"):
        return
    seeds = [s["seed"] for s in (d.get("seeds") or [])]
    per = any(g.get("per_seed") for g in gates)
    cols = seeds if (per and seeds) else ["run"]
    code = {"PASS": 1.0, "FAIL": -1.0, "SKIP": 0.0}
    M = np.zeros((len(gates), len(cols)))
    for i, g in enumerate(gates):
        for j, c in enumerate(cols):
            st = (g.get("per_seed") or {}).get(str(c), g["status"]) if per else g["status"]
            M[i, j] = code.get(st, 0.0)
    fig, ax = plt.subplots(figsize=(6.4, 0.34 * len(gates) + 1.6))
    ax.imshow(M, cmap=matplotlib.colors.ListedColormap([P["fail"], P["skip"], P["pass"]]),
              vmin=-1, vmax=1, aspect="auto")
    ax.set_yticks(range(len(gates)))
    ax.set_yticklabels([f"G{g['id']:02d}  {g['name']}" for g in gates], fontsize=8)
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([str(c) for c in cols], fontsize=8)
    ax.set_xlabel("seed" if per else "")
    ax.grid(False)
    nf = sum(1 for g in gates if g["status"] == "FAIL")
    ax.set_title(f"Promotion gate ledger: {len(gates) - nf}/{len(gates)} passing",
                 loc="left", fontweight="bold")
    ax.legend(handles=[Patch(color=P["pass"], label="PASS"), Patch(color=P["fail"], label="FAIL"),
                       Patch(color=P["skip"], label="SKIP")], ncols=3, loc="upper right",
              bbox_to_anchor=(1.0, -0.08), fontsize=8)
    finish(fig, "fig2_gate_ledger", out, demo)


def fig_refusal(d, out, demo):
    seeds = d.get("seeds") or []
    base = ((d.get("base_reference") or {}).get("eval") or {})
    if not need(any((s.get("eval") or {}).get("refusal_rate") is not None for s in seeds),
                "fig3_refusal", "seeds[].eval.refusal_rate"):
        return
    if not need(base.get("refusal_rate") is not None, "fig3_refusal",
                "base_reference.eval.refusal_rate (the preservation target)"):
        return
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    xs = np.arange(len(seeds))
    dl = [s["eval"]["refusal_rate"] - base["refusal_rate"] for s in seeds]
    bars = ax.bar(xs, dl, color=[P["pass"] if v >= 0 else P["fail"] for v in dl], width=0.6, alpha=0.9)
    ax.axhline(0, color=P["ink"], lw=1.0)
    ax.set_xticks(xs)
    ax.set_xticklabels([f"seed {s['seed']}" for s in seeds])
    ax.set_ylabel(r"$\Delta$ refusal rate vs frozen base")
    ax.set_title("Refusal preservation: negative bars fail the gate", loc="left", fontweight="bold")
    for b, v in zip(bars, dl):
        ax.annotate(f"{v:+.3f}", (b.get_x() + b.get_width() / 2, v), ha="center",
                    va="bottom" if v >= 0 else "top", fontsize=8)
    finish(fig, "fig3_refusal", out, demo)


def fig_split_gap(d, out, demo):
    seeds = d.get("seeds") or []
    ok = any((s.get("eval") or {}).get("accuracy_random_split") is not None and
             (s.get("eval") or {}).get("accuracy_family_split") is not None for s in seeds)
    if not need(ok, "fig4_split_gap", "accuracy_family_split and accuracy_random_split"):
        return
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    for i, s in enumerate(seeds):
        e = s["eval"]
        if e.get("accuracy_random_split") is None:
            continue
        ax.plot([0, 1], [e["accuracy_random_split"], e["accuracy_family_split"]], marker="o",
                lw=1.6, color=SEEDC[i % 5], label=f"seed {s['seed']}")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["random split", "template-family split"])
    ax.set_ylabel("accuracy")
    ax.set_title("Random splits flatter the model; family splits do not", loc="left", fontweight="bold")
    ax.legend(ncols=5, fontsize=8)
    finish(fig, "fig4_split_gap", out, demo)


def fig_calibration(d, out, demo):
    seeds = d.get("seeds") or []
    if not need(any((s.get("eval") or {}).get("confidence_bins") for s in seeds),
                "fig5_calibration", "seeds[].eval.confidence_bins"):
        return
    fig, ax = plt.subplots(figsize=(4.4, 4.2))
    ax.plot([0, 1], [0, 1], ls="--", lw=1.0, color=P["skip"], label="perfect calibration")
    for i, s in enumerate(seeds):
        cb = (s.get("eval") or {}).get("confidence_bins") or []
        if not cb:
            continue
        lab = f"seed {s['seed']}"
        if s["eval"].get("ece") is not None:
            lab += f" (ECE {s['eval']['ece']:.3f})"
        ax.plot([b["p_mid"] for b in cb], [b["acc"] for b in cb], marker="o", ms=3.5, lw=1.3,
                color=SEEDC[i % 5], label=lab)
    ax.set_xlabel("predicted confidence")
    ax.set_ylabel("empirical accuracy")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Reliability diagram", loc="left", fontweight="bold")
    ax.legend(fontsize=7.5)
    finish(fig, "fig5_calibration", out, demo)


def fig_contamination(d, out, demo):
    ev = d.get("eval") or {}
    ng = ev.get("ngram_overlap") or []
    jac = ev.get("family_overlap_jaccard") or []
    if not need(bool(ng or jac), "fig6_contamination",
                "eval.ngram_overlap or eval.family_overlap_jaccard"):
        return
    n = int(bool(ng)) + int(bool(jac))
    fig, axes = plt.subplots(1, n, figsize=(3.3 * n, 3.2))
    axes = np.atleast_1d(axes)
    k = 0
    if ng:
        ax = axes[k]; k += 1
        ax.bar([str(p["n"]) for p in ng], [p["train_test_overlap_frac"] for p in ng],
               color=P["a"], width=0.6)
        ax.set_xlabel("n-gram order")
        ax.set_ylabel("train/test overlap fraction")
        ax.set_title("Lexical leakage", loc="left", fontweight="bold")
    if jac:
        ax = axes[k]
        ax.hist(jac, bins=min(20, max(5, len(jac) // 2)), color=P["c"], alpha=0.85)
        ax.set_xlabel("Jaccard similarity across family boundary")
        ax.set_ylabel("pairs")
        ax.set_title("Family separation", loc="left", fontweight="bold")
    finish(fig, "fig6_contamination", out, demo)


def fig_per_class(d, out, demo):
    pc = None
    sd = None
    for s in (d.get("seeds") or []):
        if (s.get("eval") or {}).get("per_class"):
            pc = s["eval"]["per_class"]
            sd = s["seed"]
            break
    if not need(pc is not None, "fig7_per_class", "seeds[].eval.per_class"):
        return
    labels = [c["label"] for c in pc]
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.bar(x - 0.2, [c["precision"] for c in pc], width=0.38, color=P["a"], label="precision")
    ax.bar(x + 0.2, [c["recall"] for c in pc], width=0.38, color=P["b"], label="recall")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_ylabel("score")
    ax.set_ylim(0, 1)
    ax2 = ax.twinx()
    ax2.plot(x, [c["support"] for c in pc], color=P["skip"], marker="s", ms=3, lw=1.0, ls=":")
    ax2.set_ylabel("support")
    ax2.grid(False)
    ax.set_title(f"Per-class behaviour (seed {sd})", loc="left", fontweight="bold")
    ax.legend(ncols=2, fontsize=8)
    finish(fig, "fig7_per_class", out, demo)


def fig_serving(d, out, demo):
    seeds = d.get("seeds") or []
    if not need(any((s.get("eval") or {}).get("latency_ms_p95") is not None for s in seeds),
                "fig8_serving", "seeds[].eval.latency_ms_p50 / p95"):
        return
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 3.1))
    xs = np.arange(len(seeds))
    a1.bar(xs - 0.2, [(s["eval"].get("latency_ms_p50") or np.nan) for s in seeds],
           width=0.38, color=P["d"], label="p50")
    a1.bar(xs + 0.2, [(s["eval"].get("latency_ms_p95") or np.nan) for s in seeds],
           width=0.38, color=P["b"], label="p95")
    a1.set_xticks(xs)
    a1.set_xticklabels([s["seed"] for s in seeds])
    a1.set_xlabel("seed")
    a1.set_ylabel("latency (ms)")
    a1.legend(fontsize=8)
    a1.set_title("Serving latency", loc="left", fontweight="bold")
    ti = [(s["eval"].get("tokens_in") or 0) for s in seeds]
    to = [(s["eval"].get("tokens_out") or 0) for s in seeds]
    a2.bar(xs, ti, width=0.6, color=P["a"], label="input")
    a2.bar(xs, to, width=0.6, bottom=ti, color=P["c"], label="output")
    a2.set_xticks(xs)
    a2.set_xticklabels([s["seed"] for s in seeds])
    a2.set_xlabel("seed")
    a2.set_ylabel("tokens per evaluation pass")
    a2.legend(fontsize=8)
    a2.set_title("Token budget", loc="left", fontweight="bold")
    finish(fig, "fig8_serving", out, demo)


FIGURES = [fig_loss, fig_gate_ledger, fig_refusal, fig_split_gap, fig_calibration,
           fig_contamination, fig_per_class, fig_serving]


def demo_data():
    rng = random.Random(11)
    names = ["schema conformance", "fixture replay", "family-split integrity", "n-gram leakage bound",
             "refusal preservation", "abstain routing", "per-class floor", "calibration ECE bound",
             "latency budget", "token budget", "receipt signature", "weight hash pin"]
    seeds = []
    for i, sd in enumerate([11, 23, 37, 53, 71]):
        b = 1.9 - 0.06 * i
        seeds.append({"seed": sd,
          "train_loss": [{"step": s, "loss": round(b * math.exp(-s / 240) + 0.31 + rng.uniform(-0.02, 0.02), 4)}
                         for s in range(0, 601, 25)],
          "eval": {"accuracy_family_split": round(0.772 + 0.01 * i + rng.uniform(-0.006, 0.006), 4),
                   "accuracy_random_split": round(0.861 + 0.01 * i, 4),
                   "macro_f1": round(0.741 + 0.01 * i, 4),
                   "refusal_rate": round(0.612 - 0.015 * i, 4),
                   "review_routing_rate": round(0.093 + 0.004 * i, 4),
                   "ece": round(0.071 - 0.004 * i, 4),
                   "confidence_bins": [{"p_mid": round(p, 2),
                       "acc": round(min(1, max(0, p - 0.06 + rng.uniform(-0.03, 0.03))), 4),
                       "n": rng.randint(40, 300)} for p in np.arange(0.05, 1.0, 0.1)],
                   "per_class": [{"label": l, "precision": round(rng.uniform(0.62, 0.93), 3),
                       "recall": round(rng.uniform(0.58, 0.91), 3), "support": rng.randint(40, 260)}
                       for l in ["bug", "outage", "security", "billing", "how-to", "REVIEW"]],
                   "latency_ms_p50": round(rng.uniform(70, 95), 1),
                   "latency_ms_p95": round(rng.uniform(160, 230), 1),
                   "tokens_in": rng.randint(180000, 220000),
                   "tokens_out": rng.randint(30000, 44000)}})
    gates = []
    for i, n in enumerate(names, start=1):
        st = "FAIL" if n == "refusal preservation" else "PASS"
        gates.append({"id": i, "name": n, "status": st,
            "per_seed": {str(s["seed"]): st for s in seeds}})
    return {"run_id": "DEMO-SYNTHETIC", "base_model": "Qwen3.5-0.8B", "adapter_bytes": 25587104,
            "contamination_verdict": "UNPROVEN", "promotion_status": "NOTPROMOTABLE", "seeds": seeds,
            "base_reference": {"eval": {"refusal_rate": 0.640}}, "gates": gates,
            "eval": {"n_test": 1840, "n_families": 27,
              "ngram_overlap": [{"n": n, "train_test_overlap_frac": round(v, 5)}
                  for n, v in [(5, 0.0121), (8, 0.0034), (13, 0.0007), (21, 0.0)]],
              "family_overlap_jaccard": [round(rng.betavariate(2, 18), 4) for _ in range(140)]}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--receipts", default="data/receipts.json")
    ap.add_argument("--out", default="figures")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.demo:
        data = demo_data()
        print("DEMO MODE: every panel watermarked SYNTHETIC. Not for publication.")
    else:
        p = pathlib.Path(a.receipts)
        if not p.exists():
            sys.exit(f"receipts not found: {p}\nNo figure will be invented. Export your run "
                     f"receipts to that path (schema: data/receipts.schema.json).")
        data = json.loads(p.read_text(encoding="utf-8"))
    for f in FIGURES:
        f(data, out, a.demo)
    print(f"\nwrote {len(WRITTEN)} figures: {', '.join(WRITTEN) or 'none'}")
    if SKIPPED:
        print(f"\nSKIPPED {len(SKIPPED)} (data absent, nothing fabricated):")
        for s in SKIPPED:
            print(f"  - {s}")
    (out / "figure_manifest.json").write_text(json.dumps(
        {"written": WRITTEN, "skipped": SKIPPED, "demo": a.demo, "run_id": data.get("run_id"),
         "promotion_status": data.get("promotion_status")}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
