"""
Formula engine for the relevance-gated empirical study — V3.2 patched.

Patch notes:
1. K_count/K_mean: if K_count <= 0, no corroboration update is applied. K_mean=0 is not treated as evidence against the statement when no independent sources are present.
2. N_raw: scorer supplies KL-like raw novelty. This script derives N_perc and N_imp internally. N_raw is non-negative and not clamped to [0,1].
3. Text-only U/social-media X/W are scorer-side responsibilities, but validation diagnostics flag suspicious collapse patterns.
4. V3.2: importance applies tilde transforms to normalized/root composites, not raw multiplicative composites.

This script does not use benchmark targets.
"""
import math
import pandas as pd
import numpy as np

EPS = 1e-12

ZERO_ONE_COLUMNS = [
    'B_eff','C_eff','D','E','F','G','H','J','S','T','U','V','W','X','Y','Z','AA','AB','AD','Rel',
    'P','Q_rel','R','AC','K_mean','L','M'
]
REQUIRED_COLUMNS = [
    'item_id','dataset','tested_output','receiver_profile_id','B_eff','C_eff','D','E','F','G','H','J',
    'S','T','U','V','W','X','Y','Z','AA','AB','AD','Rel','N_raw','P','Q_rel','R','AC',
    'K_count','K_mean','L','M','uncertainty_flag','possible_leakage_flag'
]


def is_missing(x):
    return pd.isna(x) or (isinstance(x, str) and x.strip() == '')


def clamp01(x):
    if is_missing(x):
        return None
    try:
        val = float(x)
    except Exception:
        return None
    return max(0.0, min(1.0, val))


def nonnegative_float(x, default=None):
    if is_missing(x):
        return default
    try:
        return max(0.0, float(x))
    except Exception:
        return default


def nonnegative_int(x, default=0):
    if is_missing(x):
        return default
    try:
        return max(0, int(round(float(x))))
    except Exception:
        return default


def odds(p):
    p = max(EPS, min(1-EPS, float(p)))
    return p/(1-p)


def prob(o):
    return o/(1+o)


def lr(x, x0):
    x = clamp01(x)
    if x is None:
        return 1.0
    return math.exp((x - x0)/(x0*(1-x0)))


def tilde(x, alpha):
    x = clamp01(x)
    if x is None:
        return None
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    return 1 - math.exp(1 - (1-x)**(-alpha))


def novelty_transforms(N_raw):
    """Return N_norm, N_perc, N_imp from raw KL-like novelty."""
    N = nonnegative_float(N_raw, default=0.0)
    # Avoid numerical underflow/overflow in extreme accidental inputs while preserving high-novelty behavior.
    N_safe = min(N, 20.0)
    N_norm = 1 - math.exp(-N_safe)
    # N_perc inverted-U from framework; clamp final due to numeric roundoff.
    N_perc = 4.18 * (N_norm ** 0.7) * ((1 - N_norm) ** 1.5)
    N_perc = max(0.0, min(1.0, N_perc))
    # N_imp monotonic; high novelty approaches 1.
    N_imp = 1 - math.exp(-N_safe * (1 + N_safe))
    N_imp = max(0.0, min(1.0, N_imp))
    return N_norm, N_perc, N_imp


def cred(row):
    B = clamp01(row.get('B_eff')); C = clamp01(row.get('C_eff')); D = clamp01(row.get('D')); E = clamp01(row.get('E'))
    if None in [B,C,D,E]:
        return None
    if B <= 0 or C <= 0:
        return 0.0
    return (B ** (B ** (-0.5))) * math.sqrt(C) * ((4*D + E)/5)


def stmt(row):
    F=clamp01(row.get('F')); G=clamp01(row.get('G')); H=clamp01(row.get('H')); J=clamp01(row.get('J'))
    if None in [F,G,H,J]:
        return None
    k=math.log(100)
    F_bal=4*F*(1-F)
    return ((F_bal+J)/2)*G*(1-math.exp(-k*H))


def delivery(row):
    S=clamp01(row.get('S')); T=clamp01(row.get('T')); U=clamp01(row.get('U')); V=clamp01(row.get('V')); W=clamp01(row.get('W')); X=clamp01(row.get('X'))
    if None in [S,T,U,V,W,X]:
        return None
    return W * ((V * (X**1.1))**1.1) * (((3*S+2*T+U)/6)**0.5)


def z_eff(row):
    Z=clamp01(row.get('Z')); B=clamp01(row.get('B_eff'))
    if Z is None or B is None:
        return None
    return Z * (1 - Z*(1-B))


def situational_star(row):
    Rel=clamp01(row.get('Rel')); Y=clamp01(row.get('Y')); AA=clamp01(row.get('AA')); AB=clamp01(row.get('AB')); AD=clamp01(row.get('AD')); Ze=z_eff(row)
    if None in [Rel,Y,AA,AB,AD,Ze]:
        return None
    x0_AD=0.40; x0_Y=0.51; x0_Z=0.60
    AD_star = Rel*AD + (1-Rel)*x0_AD
    Y_star = Rel*Y + (1-Rel)*x0_Y
    Z_star = Rel*Ze + (1-Rel)*x0_Z
    return (AB**2.1) * (AA**0.2) * ((2*Z_star + 3*AD_star + Y_star)/6)


def receiver(row, importance=False):
    P=clamp01(row.get('P')); Q=clamp01(row.get('Q_rel')); R=clamp01(row.get('R')); AC=clamp01(row.get('AC'))
    if None in [P,Q,R,AC]:
        return None
    _, N_perc, N_imp = novelty_transforms(row.get('N_raw'))
    N = N_imp if importance else N_perc
    return (N**(1-P) * Q * 4*R*(1-R)) * (AC**1.75)


def apply_k_updates(o, row, alpha=1.0):
    """Apply diminishing corroboration updates. Skip entirely when K_count <= 0."""
    k_count = nonnegative_int(row.get('K_count'), default=0)
    if k_count <= 0:
        return o
    kmean = clamp01(row.get('K_mean'))
    if kmean is None:
        return o
    base_lr = lr(kmean, 0.50)
    for n in range(1, k_count + 1):
        o *= 1 + (base_lr - 1) / (n ** alpha)
    return o


def compute_t_abs(row, prior=0.5):
    o=odds(prior)
    c=cred(row); st=stmt(row)
    if c is None or st is None or clamp01(row.get('L')) is None or clamp01(row.get('M')) is None:
        return None
    o *= lr(c, 0.301)
    o *= lr(st, 0.626)
    o = apply_k_updates(o, row, alpha=1.0)
    o *= lr(row.get('L'), 0.75)
    o *= lr(row.get('M'), 0.50)
    return prob(o)


def compute_t_perc(row, t_abs):
    if t_abs is None:
        return None
    d=delivery(row); s=situational_star(row); r=receiver(row, importance=False)
    if None in [d,s,r]:
        return None
    o=odds(t_abs)
    o *= lr(math.sqrt(max(0.0, d)), 0.379)
    o *= lr(math.sqrt(max(0.0, s)), 0.436)
    o *= lr(r ** (1/3), 0.450)
    return prob(o)


def compute_importance(row, t_abs):
    """Compute I(s,r) with the V3.2 normalization-before-tilde patch.

    Important correction: Table 8 of the framework defines tilde inputs using the
    normalized/root composite scales, not the raw multiplicative composites.
    Therefore the tilde transform must be applied to:
      - sqrt(Deliv_raw), neutral x0_raw = 0.379
      - sqrt(Sit_star_raw), neutral x0_raw = 0.436
      - cbrt(Recv_imp_raw), neutral x0_raw = 0.450
    V3 accidentally applied tilde directly to the raw composites, causing severe
    magnitude compression, especially for HumAID importance.
    """
    d=delivery(row); s=situational_star(row); r=receiver(row, importance=True)
    if None in [d,s,r,t_abs]:
        return None
    d_norm = math.sqrt(max(0.0, d))
    s_norm = math.sqrt(max(0.0, s))
    r_norm = r ** (1/3) if r >= 0 else None
    td=tilde(d_norm,0.8); ts=tilde(s_norm,0.75); tr=tilde(r_norm,0.7)
    if None in [td,ts,tr]:
        return None
    o=odds(0.5)
    o *= lr(td, 0.372)
    o *= lr(ts, 0.415)
    o *= lr(tr, 0.405)
    beta=0.15; x0=0.50
    lambda_truth = math.exp(beta*((math.sqrt(clamp01(t_abs))-x0)/(x0*(1-x0))))
    o *= lambda_truth
    return prob(o)


def compute_all(df):
    rows=[]
    for _, row in df.iterrows():
        rowdict = row.to_dict()
        t_abs = compute_t_abs(rowdict, prior=0.5)
        t_perc = compute_t_perc(rowdict, t_abs)
        imp = compute_importance(rowdict, t_abs)
        d=delivery(rowdict); s=situational_star(rowdict); rperc=receiver(rowdict, False); rimp=receiver(rowdict, True)
        nn, npv, niv = novelty_transforms(rowdict.get('N_raw'))
        out = rowdict.copy()
        out.update({
            'Cred_composite': cred(rowdict),
            'Stmt_composite': stmt(rowdict),
            'Deliv_raw': d,
            'Deliv_sqrt': math.sqrt(d) if d is not None and d >= 0 else None,
            'Sit_star_raw': s,
            'Sit_star_sqrt': math.sqrt(s) if s is not None and s >= 0 else None,
            'Recv_perc_raw': rperc,
            'Recv_perc_cuberoot': rperc ** (1/3) if rperc is not None and rperc >= 0 else None,
            'Recv_imp_raw': rimp,
            'N_norm': nn,
            'N_perc_derived': npv,
            'N_imp_derived': niv,
            'T_abs_model': t_abs,
            'T_perc_model': t_perc,
            'I_model': imp,
            'model_score': select_model_score(rowdict.get('tested_output'), rowdict.get('dataset'), t_abs, t_perc, imp),
        })
        rows.append(out)
    return pd.DataFrame(rows)


def select_model_score(tested_output, dataset, t_abs, t_perc, imp):
    text = (str(tested_output) + ' ' + str(dataset)).lower()
    if 'not_scored' in text or 'evidence_missing' in text:
        return None
    if 'hum' in text or 'importance' in text or 'i_s_r' in text:
        return imp
    if 'credevent' in text or 't_perc' in text or 'perceived' in text:
        return t_perc
    if 'liar' in text or 't_abs' in text:
        return t_abs
    return None


def validate_scores(df):
    issues=[]
    missing_cols=[c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        issues.append(f"Missing required columns: {missing_cols}")
    forbidden_fragments=['target','residual','metric','group_mean','hidden_label','hidden_class','hidden_rating','model_score']
    # model_score may appear only after compute_all, not in raw input. This validator is for raw scorer files.
    bad_cols=[]
    for c in df.columns:
        lc=c.lower()
        if any(f in lc for f in forbidden_fragments):
            if c not in REQUIRED_COLUMNS:
                bad_cols.append(c)
    if bad_cols:
        issues.append(f"Potential leakage/evaluation columns present: {bad_cols}")
    for c in ZERO_ONE_COLUMNS:
        if c in df.columns:
            vals=pd.to_numeric(df[c], errors='coerce')
            bad=df[vals.notna() & ((vals<0)|(vals>1))]
            if len(bad):
                issues.append(f"Column {c} has {len(bad)} values outside [0,1]")
    if 'N_raw' in df.columns:
        vals=pd.to_numeric(df['N_raw'], errors='coerce')
        bad=df[vals.notna() & (vals<0)]
        if len(bad):
            issues.append(f"N_raw has {len(bad)} negative values")
    if 'K_count' in df.columns:
        vals=pd.to_numeric(df['K_count'], errors='coerce')
        bad=df[vals.notna() & (vals<0)]
        if len(bad):
            issues.append(f"K_count has {len(bad)} negative values")
    return issues


def suspicious_collapse_diagnostics(df):
    notes=[]
    if len(df)==0:
        return notes
    for col in ['W','X','U','AC','Rel','AD','Y']:
        if col in df.columns:
            vals=pd.to_numeric(df[col], errors='coerce')
            if vals.notna().any():
                notes.append({'variable':col, 'mean':float(vals.mean()), 'p10':float(vals.quantile(0.10)), 'p90':float(vals.quantile(0.90))})
    return notes
