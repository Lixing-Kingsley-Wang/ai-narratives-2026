"""Shared Message Batches engine for R1 Batch 2b (B2, B3).

Each job supplies: model, max_tokens, temperature (None = not set), system
prompt, records (dicts with pmid/title/abstract), build_user(rec) and
parse(text) -> (fields_dict, fail_reason or ""). The engine handles the
1,000-record exact token count and cost gate, submission, polling,
retrieval (raw results kept as gzip jsonl), one resubmission of FAILED
records, and the merged label file. The API key is read from the main
checkout's .env and is never printed or written.
"""

from __future__ import annotations

import csv
import gzip
import json
import math
import random
import sys
import time
from pathlib import Path

from anthropic import Anthropic
from dotenv import dotenv_values

MAIN = Path("/Users/kingslywang/Documents/科研/ai-narratives-2026")
PRICES = {"claude-sonnet-4-6": (3.00, 15.00), "claude-haiku-4-5-20251001": (1.00, 5.00)}
BATCH_DISCOUNT = 0.5


class Job:
    def __init__(self, name, outdir, model, max_tokens, temperature, system, records, build_user, parse,
                 ceiling, out_tokens_assumed, n_chunks=1):
        self.name, self.out = name, Path(outdir)
        self.out.mkdir(parents=True, exist_ok=True)
        self.model, self.max_tokens, self.temperature = model, max_tokens, temperature
        self.system, self.records = system, records
        self.by_id = {r["pmid"]: r for r in records}
        assert len(self.by_id) == len(records), "duplicate PMIDs in frame"
        self.build_user, self.parse = build_user, parse
        self.ceiling, self.out_tokens_assumed, self.n_chunks = ceiling, out_tokens_assumed, n_chunks

    # ── helpers ─────────────────────────────────────────────────────────
    def client(self):
        key = dotenv_values(MAIN / ".env").get("ANTHROPIC_API_KEY")
        if not key:
            sys.exit("ANTHROPIC_API_KEY not found in main checkout .env")
        return Anthropic(api_key=key, max_retries=8)

    def params(self, r):
        p = {"model": self.model, "max_tokens": self.max_tokens, "system": self.system,
             "messages": [{"role": "user", "content": self.build_user(r)}]}
        if self.temperature is not None:
            p["temperature"] = self.temperature
        return p

    def cost(self, tin, tout):
        pin, pout = PRICES[self.model]
        return (tin * pin + tout * pout) / 1e6 * BATCH_DISCOUNT

    def p(self, kind, rnd=None):
        names = {"ids": f"batch_ids_round{rnd}.txt", "done": f"batch_processed_round{rnd}.txt",
                 "raw": f"raw_round{rnd}.jsonl.gz", "parsed": f"parsed_round{rnd}.csv",
                 "proj": "cost_projection.json", "actual": "actual_cost.json", "labels": f"{self.name}_labels.csv"}
        return self.out / names[kind]

    @staticmethod
    def lines(p):
        return [l.strip() for l in open(p) if l.strip()] if p.exists() else []

    # ── steps ───────────────────────────────────────────────────────────
    def count(self, n_sample=1000, seed=42):
        c = self.client()
        pm = sorted(self.by_id, key=int)
        sample = random.Random(seed).sample(pm, min(n_sample, len(pm)))
        toks = []
        for i, pmid in enumerate(sample, 1):
            q = self.params(self.by_id[pmid])
            q.pop("max_tokens"); q.pop("temperature", None)
            toks.append(c.messages.count_tokens(**q).input_tokens)
            if i % 200 == 0:
                print(f"  counted {i}/{len(sample)}", flush=True)
        n = len(pm); mean = sum(toks) / len(toks)
        proj = {"job": self.name, "model": self.model, "sample_n": len(sample), "seed": seed, "population_n": n,
                "mean_input_tokens": mean, "min_input_tokens": min(toks), "max_input_tokens": max(toks),
                "projected_input_tokens": mean * n, "assumed_output_tokens_per_request": self.out_tokens_assumed,
                "projected_output_tokens": self.out_tokens_assumed * n,
                "price_per_mtok_in_out": PRICES[self.model], "batch_discount": BATCH_DISCOUNT,
                "projected_cost_usd": self.cost(mean * n, self.out_tokens_assumed * n), "ceiling_usd": self.ceiling}
        self.p("proj").write_text(json.dumps(proj, indent=2))
        print(json.dumps(proj, indent=2))
        return proj

    def submit(self, rnd, pmids=None):
        if self.lines(self.p("ids", rnd)):
            sys.exit(f"{self.name} round {rnd} already submitted")
        if rnd == 1:
            proj = json.loads(self.p("proj").read_text())
            if proj["projected_cost_usd"] > self.ceiling:
                sys.exit(f"projected ${proj['projected_cost_usd']:.2f} > ceiling ${self.ceiling}; ask before submitting")
        recs = [self.by_id[p] for p in (pmids or sorted(self.by_id, key=int))]
        k = self.n_chunks if rnd == 1 else 1
        size = math.ceil(len(recs) / k)
        c = self.client()
        for i in range(k):
            chunk = recs[i * size:(i + 1) * size]
            if not chunk:
                break
            b = c.messages.batches.create(requests=[{"custom_id": r["pmid"], "params": self.params(r)} for r in chunk])
            with open(self.p("ids", rnd), "a") as f:
                f.write(b.id + "\n")
            print(f"  {self.name} round {rnd} batch {i+1}/{k}: {len(chunk):,} requests ({b.processing_status})", flush=True)

    def _write(self, c, bid, rnd, fields):
        exists = self.p("parsed", rnd).exists()
        n = nf = 0
        with gzip.open(self.p("raw", rnd), "at", encoding="utf-8") as fr, \
             open(self.p("parsed", rnd), "a", newline="", encoding="utf-8") as fp:
            w = csv.DictWriter(fp, fieldnames=["pmid"] + fields + ["failed", "fail_reason", "input_tokens", "output_tokens", "round"])
            if not exists:
                w.writeheader()
            for res in c.messages.batches.results(bid):
                fr.write(res.model_dump_json() + "\n")
                tin = tout = 0
                if res.result.type != "succeeded":
                    vals, reason = {}, f"batch_{res.result.type}"
                else:
                    m = res.result.message
                    tin, tout = m.usage.input_tokens, m.usage.output_tokens
                    text = next((b.text for b in (m.content or []) if getattr(b, "text", None)), "")
                    vals, reason = ({}, "empty_response") if not text else self.parse(text)
                row = {"pmid": res.custom_id, **{f: vals.get(f, "") for f in fields}, "failed": int(bool(reason)),
                       "fail_reason": reason, "input_tokens": tin, "output_tokens": tout, "round": rnd}
                w.writerow(row); n += 1; nf += bool(reason)
        print(f"    retrieved {bid[-12:]}: {n:,}, FAILED={nf}", flush=True)

    def poll(self, rnd, fields, sleep_s=120):
        ids = self.lines(self.p("ids", rnd)); done = set(self.lines(self.p("done", rnd)))
        pending = [b for b in ids if b not in done]
        c = self.client()
        while pending:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {self.name} round {rnd}", flush=True)
            for bid in list(pending):
                b = c.messages.batches.retrieve(bid); rc = b.request_counts
                print(f"  ...{bid[-12:]} {b.processing_status:<11} succ={rc.succeeded:,} err={rc.errored} "
                      f"exp={rc.expired} canc={rc.canceled} proc={rc.processing:,}", flush=True)
                if b.processing_status == "ended":
                    self._write(c, bid, rnd, fields)
                    with open(self.p("done", rnd), "a") as f:
                        f.write(bid + "\n")
                    pending.remove(bid)
            if pending:
                time.sleep(sleep_s)
        print(f"{self.name} round {rnd}: all retrieved", flush=True)

    def failed_round1(self):
        return [r["pmid"] for r in csv.DictReader(open(self.p("parsed", 1))) if r["failed"] == "1"]

    def actual(self):
        tin = tout = 0
        for rnd in (1, 2):
            if self.p("parsed", rnd).exists():
                for r in csv.DictReader(open(self.p("parsed", rnd))):
                    tin += int(r["input_tokens"] or 0); tout += int(r["output_tokens"] or 0)
        return tin, tout, self.cost(tin, tout)

    def finalize(self, fields):
        import pandas as pd
        r1 = pd.read_csv(self.p("parsed", 1), dtype=str, keep_default_na=False).set_index("pmid")
        assert r1.index.is_unique and set(r1.index) == set(self.by_id), "round 1 incomplete"
        if self.p("parsed", 2).exists():
            r2 = pd.read_csv(self.p("parsed", 2), dtype=str, keep_default_na=False).set_index("pmid")
            cols = fields + ["failed", "fail_reason", "round"]
            r1.loc[r2.index, cols] = r2[cols]
        r1.reset_index()[["pmid"] + fields + ["failed", "fail_reason", "round"]].to_csv(self.p("labels"), index=False)
        tin, tout, usd = self.actual()
        self.p("actual").write_text(json.dumps({"input_tokens": tin, "output_tokens": tout, "cost_usd": usd,
                                                "round1_failed": len(self.failed_round1()),
                                                "final_failed": int((r1["failed"] == "1").sum())}, indent=2))
        print(f"{self.name}: final FAILED {int((r1['failed'] == '1').sum())}; actual ${usd:.2f}")


def run(job, fields, argv):
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "count":
        job.count()
    elif cmd == "submit":
        job.submit(1)
    elif cmd == "poll":
        job.poll(1, fields)
    elif cmd == "resubmit":
        f = job.failed_round1()
        _, _, spent = job.actual()
        print(f"{job.name} round-1 FAILED: {len(f)}; spent ${spent:.2f}")
        if f:
            job.submit(2, f)
    elif cmd == "poll2":
        if job.lines(job.p("ids", 2)):
            job.poll(2, fields)
    elif cmd == "finalize":
        job.finalize(fields)
    else:
        sys.exit("usage: count | submit | poll | resubmit | poll2 | finalize")
