#!/usr/bin/env python3
"""
Evaluate external atomic scoring outputs under the V3.2 patched relevance-gated formula engine.

This script is owner-side only because it joins private targets.
"""
from pathlib import Path
import argparse, sys, json, math
import pandas as pd
import numpy as np

# local import
from formula_engine_relevance_gated_v3_2 import compute_all, validate_scores, suspicious_collapse_diagnostics


def pearson(x, y):
    x=np.asarray(x, dtype=float); y=np.asarray(y, dtype=float)
    mask=np.isfinite(x)&np.isfinite(y)
    x=x[mask]; y=y[mask]
    if len(x)<2 or np.std(x)==0 or np.std(y)==0:
        return np.nan
    return float(np.corrcoef(x,y)[0,1])


def spearman(x, y):
    xs=pd.Series(x, dtype='float64').rank(method='average').to_numpy()
    ys=pd.Series(y, dtype='float64').rank(method='average').to_numpy()
    return pearson(xs, ys)


def mae(x, y):
    x=np.asarray(x, dtype=float); y=np.asarray(y, dtype=float)
    mask=np.isfinite(x)&np.isfinite(y)
    if mask.sum()==0: return np.nan
    return float(np.mean(np.abs(x[mask]-y[mask])))


def find_file(scores_dir, prefixes):
    for p in Path(scores_dir).glob('*.csv'):
        low=p.name.lower()
        if any(low.startswith(pref) or pref in low for pref in prefixes):
            return p
    return None


def load_targets(targets_dir, dataset):
    td=Path(targets_dir)
    if dataset=='HumAID':
        return pd.read_csv(td/'humaid_targets_200_PRIVATE_DO_NOT_SEND.csv')
    if dataset=='CredEvent_TurkRatings':
        return pd.read_csv(td/'credevent_targets_200_PRIVATE_DO_NOT_SEND.csv')
    if dataset=='LIAR_PolitiFact':
        return pd.read_csv(td/'liar_targets_200_PRIVATE_DO_NOT_SEND.csv')
    raise ValueError(dataset)


def eval_one(scores_path, targets_dir, dataset, out_dir):
    raw=pd.read_csv(scores_path)
    issues=validate_scores(raw)
    # If not-scored evidence rows, return exclusion status.
    if 'tested_output' in raw.columns and raw['tested_output'].astype(str).str.contains('not_scored|evidence_missing', case=False, regex=True).all():
        audit=raw.copy()
        audit['status']='not_evaluated_evidence_insufficient'
        audit.to_csv(out_dir/f'{dataset}_formula_audit_not_evaluated.csv', index=False)
        return {
            'dataset':dataset,
            'status':'not evaluated - evidence insufficient',
            'n':len(raw),
            'spearman':np.nan,
            'pearson':np.nan,
            'mae':np.nan,
            'model_mean':np.nan,
            'target_mean':np.nan,
            'validation_issues':'; '.join(issues)
        }, audit, issues

    audit=compute_all(raw)
    targets=load_targets(targets_dir, dataset)
    joined=audit.merge(targets, on=['item_id','dataset'], how='left', suffixes=('','_target'))
    if 'hidden_target_score' not in joined.columns:
        raise RuntimeError(f'Could not join hidden_target_score for {dataset}')
    # exclude rows without model score
    valid=joined[pd.to_numeric(joined['model_score'], errors='coerce').notna() & pd.to_numeric(joined['hidden_target_score'], errors='coerce').notna()].copy()
    joined.to_csv(out_dir/f'{dataset}_formula_audit_joined.csv', index=False)
    if len(valid)==0:
        status='not evaluated - no valid model scores'
    else:
        status='evaluated'
    metrics={
        'dataset':dataset,
        'status':status,
        'n':int(len(valid)),
        'spearman':spearman(valid['model_score'], valid['hidden_target_score']) if len(valid)>1 else np.nan,
        'pearson':pearson(valid['model_score'], valid['hidden_target_score']) if len(valid)>1 else np.nan,
        'mae':mae(valid['model_score'], valid['hidden_target_score']),
        'model_mean':float(valid['model_score'].mean()) if len(valid)>0 else np.nan,
        'target_mean':float(valid['hidden_target_score'].mean()) if len(valid)>0 else np.nan,
        'validation_issues':'; '.join(issues)
    }
    return metrics, joined, issues


def write_report(out_dir, metrics_rows, diagnostics):
    lines=[]
    lines.append('# V3.2 evaluation report')
    lines.append('')
    lines.append('This report is owner-side only because it uses private targets.')
    lines.append('')
    lines.append('## Metrics')
    lines.append('')
    lines.append('| Dataset | Status | n | Spearman | Pearson | MAE | Model mean | Target mean |')
    lines.append('|---|---:|---:|---:|---:|---:|---:|')
    for m in metrics_rows:
        def fmt(v):
            if isinstance(v, str): return v
            if v is None or (isinstance(v,float) and np.isnan(v)): return '—'
            if isinstance(v,(int,np.integer)): return str(v)
            return f'{v:.3f}'
        lines.append(f"| {m['dataset']} | {m['status']} | {m['n']} | {fmt(m['spearman'])} | {fmt(m['pearson'])} | {fmt(m['mae'])} | {fmt(m['model_mean'])} | {fmt(m['target_mean'])} |")
    lines.append('')
    lines.append('## Diagnostics')
    for ds, diag in diagnostics.items():
        lines.append(f'')
        lines.append(f'### {ds}')
        if diag.get('issues'):
            lines.append('Validation issues: ' + '; '.join(diag['issues']))
        else:
            lines.append('Validation issues: none detected.')
        if diag.get('collapse'):
            lines.append('')
            lines.append('| Variable | Mean | p10 | p90 |')
            lines.append('|---|---:|---:|---:|')
            for d in diag['collapse']:
                lines.append(f"| {d['variable']} | {d['mean']:.3f} | {d['p10']:.3f} | {d['p90']:.3f} |")
    (out_dir/'evaluation_report.md').write_text('\n'.join(lines), encoding='utf-8')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--scores-dir', required=True)
    ap.add_argument('--targets-dir', required=True)
    ap.add_argument('--out-dir', required=True)
    args=ap.parse_args()
    scores_dir=Path(args.scores_dir); out_dir=Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    mapping={
        'HumAID': ['humaid'],
        'CredEvent_TurkRatings': ['credevent','credbank'],
        'LIAR_PolitiFact': ['liar'],
    }
    metrics=[]; diagnostics={}
    for dataset, prefixes in mapping.items():
        f=find_file(scores_dir, prefixes)
        if f is None:
            metrics.append({'dataset':dataset,'status':'not evaluated - missing scorer output','n':0,'spearman':np.nan,'pearson':np.nan,'mae':np.nan,'model_mean':np.nan,'target_mean':np.nan,'validation_issues':'missing file'})
            diagnostics[dataset]={'issues':['missing file'], 'collapse':[]}
            continue
        m, joined, issues=eval_one(f, args.targets_dir, dataset, out_dir)
        metrics.append(m)
        diagnostics[dataset]={'issues':issues, 'collapse': suspicious_collapse_diagnostics(joined)}
    pd.DataFrame(metrics).to_csv(out_dir/'evaluation_metrics_by_dataset.csv', index=False)
    write_report(out_dir, metrics, diagnostics)
    print((out_dir/'evaluation_report.md').read_text(encoding='utf-8'))

if __name__ == '__main__':
    main()
