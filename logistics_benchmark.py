import numpy as np
BENCHMARKS={"transport_pct_revenue":{"p25":3.5,"median":5.0,"p75":7.0},
            "warehouse_pct_revenue":{"p25":1.5,"median":2.5,"p75":4.0},
            "inventory_carrying_pct":{"p25":15,"median":22,"p75":30},
            "order_cost":{"p25":8,"median":15,"p75":25},
            "perfect_order_pct":{"p25":85,"median":92,"p75":97},
            "cash_to_cash_days":{"p25":25,"median":45,"p75":75}}
def benchmark(company_metrics):
    results={}
    for metric,value in company_metrics.items():
        if metric not in BENCHMARKS: continue
        b=BENCHMARKS[metric]
        if metric in ("perfect_order_pct",):
            percentile="top quartile" if value>=b["p75"] else "above median" if value>=b["median"] else "below median" if value>=b["p25"] else "bottom quartile"
        else:
            percentile="top quartile" if value<=b["p25"] else "above median" if value<=b["median"] else "below median" if value<=b["p75"] else "bottom quartile"
        gap_to_best=round(value-b["p25"],2) if metric not in ("perfect_order_pct",) else round(b["p75"]-value,2)
        results[metric]={"value":value,"percentile":percentile,"median":b["median"],"gap_to_top":gap_to_best}
    overall_rank=sum(1 for r in results.values() if "top" in r["percentile"] or "above" in r["percentile"])
    return {"metrics":results,"strong_areas":overall_rank,"total_metrics":len(results)}
if __name__=="__main__":
    company={"transport_pct_revenue":4.2,"warehouse_pct_revenue":3.0,"inventory_carrying_pct":25,
             "order_cost":12,"perfect_order_pct":94,"cash_to_cash_days":40}
    r=benchmark(company)
    for m,d in r["metrics"].items(): print(f"{m}: {d['value']} ({d['percentile']})")
