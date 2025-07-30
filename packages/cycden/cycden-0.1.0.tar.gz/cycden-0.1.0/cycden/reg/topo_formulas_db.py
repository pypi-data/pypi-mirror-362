# reg/topo_formulas_db.py

TOPO_INDEX_DB = {}

def register_topo_index(name, *partitions):
    def decorator(func):
        TOPO_INDEX_DB[name.lower()] = ([p.lower() for p in partitions], func)
        return func
    return decorator

def get_topo_index_function(name):
    name = name.lower()
    if name not in TOPO_INDEX_DB:
        raise KeyError(f"Topological index '{name}' not found.")
    return TOPO_INDEX_DB[name]

# ────── Degree-Based Indices ──────────────────────────
@register_topo_index("first_zagreb", "degree")
def first_zagreb_index(df):
    if not {"Degree", "Count"}.issubset(df.columns):
        raise ValueError("Expected columns 'Degree' and 'Count'")
    return sum(count * deg**2 for deg, count in zip(df["Degree"], df["Count"]))

@register_topo_index("second_zagreb", "degree_pair")
def second_zagreb_index(df):
    if not {"deg(u)", "deg(v)", "Count"}.issubset(df.columns):
        raise ValueError("Expected columns 'deg(u)', 'deg(v)', and 'Count'")
    return sum(c * i * j for i, j, c in zip(df["deg(u)"], df["deg(v)"], df["Count"]))

@register_topo_index("randic", "degree_pair")
def randic_index(df):
    if not {"deg(u)", "deg(v)", "Count"}.issubset(df.columns):
        raise ValueError("Expected columns 'deg(u)', 'deg(v)', and 'Count'")
    return sum(c / (i * j) ** 0.5 for i, j, c in zip(df["deg(u)"], df["deg(v)"], df["Count"]))

# ────── Distance-Based Index ──────────────────────────
@register_topo_index("wiener", "distance")
def wiener_index(df):
    if not {"Distance", "Count"}.issubset(df.columns):
        raise ValueError("Expected columns 'Distance' and 'Count'")
    return sum(d * c for d, c in zip(df["Distance"], df["Count"]))

@register_topo_index("harary", "distance")
def harary_index(df):
    if not {"Distance", "Count"}.issubset(df.columns):
        raise ValueError("Expected columns 'Distance' and 'Count'")
    return sum((1 / d) * c for d, c in zip(df["Distance"], df["Count"]) if d != 0)

@register_topo_index("hyper_wiener", "distance")
def hyper_wiener_index(df):
    if not {"Distance", "Count"}.issubset(df.columns):
        raise ValueError("Expected columns 'Distance' and 'Count'")
    return 0.5 * sum((d + d**2) * c for d, c in zip(df["Distance"], df["Count"]))

# ────── Szeged Index ────────────────────────────────
@register_topo_index("szeged", "szeged")
def szeged_index(df):
    if not {"Total Contribution"}.issubset(df.columns):
        raise ValueError("Expected column 'Total Contribution'")
    return df["Total Contribution"].sum()

@register_topo_index("mostar", "szeged")
def mostar_index(df):
    if not {"n_u", "n_v", "Count"}.issubset(df.columns):
        raise ValueError("Expected columns 'n_u', 'n_v', and 'Count'")
    return sum(abs(nu - nv) * c for nu, nv, c in zip(df["n_u"], df["n_v"], df["Count"]))

@register_topo_index("gutman", "distance_degpair")
def gutman_index(dist_df):
    if not all(col in dist_df.columns for col in ["Deg(u)", "Deg(v)", "Distance", "Count"]):
        return "⚠️ Distance partition must contain 'Deg(u)', 'Deg(v)', 'Distance', and 'Count' columns."
    
    return sum((i * j * d * c) for i, j, d, c in zip(
        dist_df["Deg(u)"], dist_df["Deg(v)"], dist_df["Distance"], dist_df["Count"]
    ))

# ────── New Graph-Based Indices via Partition ────────────────

@register_topo_index("hyper_zagreb", "degree_pair")
def hyper_zagreb_index(df):
    if not {"deg(u)", "deg(v)", "Count"}.issubset(df.columns):
        raise ValueError("Expected columns 'deg(u)', 'deg(v)', 'Count'")
    return 0.5 * sum(
        ((i + j) ** 2) * c
        for i, j, c in zip(df["deg(u)"], df["deg(v)"], df["Count"])
    )

@register_topo_index("reverse_first_zagreb", "reverse_degree_pair")
def reverse_first_zagreb_index(df):
    if not {"Reverse Deg(u)", "Reverse Deg(v)", "Count"}.issubset(df.columns):
        raise ValueError("Expected columns 'Reverse Deg(u)', 'Reverse Deg(v)', and 'Count'")
    
    return sum(
        (i + j) * c
        for i, j, c in zip(df["Reverse Deg(u)"], df["Reverse Deg(v)"], df["Count"])
    )
@register_topo_index("reverse_second_zagreb", "reverse_degree_pair")
def reverse_second_zagreb_index(df):
    if not {"Reverse Deg(u)", "Reverse Deg(v)", "Count"}.issubset(df.columns):
        raise ValueError("Expected columns 'Reverse Deg(u)', 'Reverse Deg(v)', and 'Count'")
    
    return sum(
        i * j * c
        for i, j, c in zip(df["Reverse Deg(u)"], df["Reverse Deg(v)"], df["Count"])
    )

@register_topo_index("schultz", "distance_degpair")
def schultz_index(df):
    if not {"Deg(u)", "Deg(v)", "Distance", "Count"}.issubset(df.columns):
        raise ValueError("Expected columns 'Deg(u)', 'Deg(v)', 'Distance', 'Count'")
    
    return sum(
        (du + dv) * d * c
        for du, dv, d, c in zip(df["Deg(u)"], df["Deg(v)"], df["Distance"], df["Count"])
    )