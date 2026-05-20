import streamlit as st
import numpy as np
import pandas as pd

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ระบบแนะนำสินค้า SVD | Shoplui",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Global CSS  (Font Awesome + Sarabun + theme)
# ─────────────────────────────────────────────
st.markdown("""
<link rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Sarabun:wght@300;400;600;700&display=swap"
  rel="stylesheet"/>

<style>
/* ── base ── */
html, body, [class*="css"] {
    font-family: 'Outfit', 'Sarabun', sans-serif;
}

:root {
    --orange:      #EE4D2D;
    --orange2:     #FF5722;
    --orange-lite: #FFF5F2;
    --bg:          #F8FAFC;
    --card-bg:     #FFFFFF;
    --text:        #0F172A;
    --sub:         #64748B;
    --border:      #E2E8F0;
    --sidebar-bg:  #EE4D2D;
    
    /* Override Streamlit built-in variables to force light mode colors */
    --st-background-color: #F8FAFC !important;
    --st-secondary-background-color: #FFFFFF !important;
    --st-text-color: #0F172A !important;
    --st-border-color: #E2E8F0 !important;
    --st-primary-color: #EE4D2D !important;
}

/* Ensure CSS custom properties adapt to light colors in all theme contexts */
[data-theme="light"], [data-theme="dark"] {
    --st-background-color: #F8FAFC !important;
    --st-secondary-background-color: #FFFFFF !important;
    --st-text-color: #0F172A !important;
    --st-border-color: #E2E8F0 !important;
    --st-primary-color: #EE4D2D !important;
}

/* background */
.stApp, .stApp [data-theme="light"], .stApp [data-theme="dark"] {
    background: var(--bg) !important;
    color: var(--text) !important;
}

/* Force typography colors to stay dark slate */
h1, h2, h3, h4, h5, h6, p, label, li, span, small {
    color: var(--text) !important;
}

/* Force header banner typography inside .sv-header to remain white */
.sv-header, .sv-header h1, .sv-header p, .sv-header h1 *, .sv-header p * {
    color: #FFFFFF !important;
}

/* Disable typing in selectbox dropdowns (make them click-only) */
div[data-baseweb="select"] input {
    caret-color: transparent !important;
    color: transparent !important;
    text-shadow: 0 0 0 transparent !important;
    cursor: pointer !important;
}

/* sidebar — Shopee Orange */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #EE4D2D 0%, #FF5722 100%) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] select {
    color: #0F172A !important;
    background-color: #FFFFFF !important;
}
section[data-testid="stSidebar"] input {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}

/* Override inputs and selects in the main area */
input, select, textarea {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #E2E8F0 !important;
}

/* Style baseweb selects (selectbox/multiselect) */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #E2E8F0 !important;
}

div[data-baseweb="select"] * {
    color: #0F172A !important;
}

/* Dropdown popovers */
div[role="listbox"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #E2E8F0 !important;
}
div[role="option"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
}
div[role="option"]:hover, div[role="option"][aria-selected="true"] {
    background-color: #EE4D2D !important;
    color: #FFFFFF !important;
}

/* Widget labels & Help texts */
[data-testid="stWidgetLabel"] p, .stWidgetLabel, label[data-testid="stWidgetLabel"] {
    color: #0F172A !important;
}

/* header banner */
.sv-header {
    background: linear-gradient(135deg, #EE4D2D 0%, #FF7337 55%, #FF9A3C 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    box-shadow: 0 8px 28px rgba(238,77,45,.15);
    color: #fff !important;
}
.sv-header h1 { font-size: 1.9rem; font-weight: 700; margin: 0 0 6px; color: #fff !important; }
.sv-header p  { margin: 0; opacity: .9; font-size: .97rem; color: #fff !important; }

/* cards */
.sv-card {
    background: var(--card-bg) !important;
    border: 1px solid var(--border) !important;
    border-left: 4px solid var(--orange) !important;
    border-radius: 14px !important;
    padding: 22px 26px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,.04) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease !important;
}
.sv-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(238, 77, 45, 0.08) !important;
    border-color: rgba(238, 77, 45, 0.2) !important;
}
.sv-card-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--orange) !important;
    margin-bottom: 14px;
}
.sv-card-title .fa-badge {
    background: var(--orange) !important;
    color: #fff !important;
    border-radius: 50%;
    width: 32px; height: 32px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: .9rem;
    flex-shrink: 0;
}

/* score legend pills (Light mode pastel style) */
.pill { display:inline-block; padding:4px 14px; border-radius:20px;
        font-size:.83rem; font-weight:600; margin:3px; }
.pill-0 { background:#F1F5F9;  color:#64748B; border:1px solid #CBD5E1; }
.pill-1 { background:#FFF8E1;  color:#F57C00; border:1px solid #FFE082; }
.pill-2 { background:#E1F5FE;  color:#0288D1; border:1px solid #B3E5FC; }
.pill-3 { background:#F3E5F5;  color:#7B1FA2; border:1px solid #E1BEE7; }
.pill-4 { background:#FFEbee;  color:#C2185B; border:1px solid #FFCDD2; }
.pill-5 { background:#FBE9E7;  color:#D84315; border:1px solid #FFCCBC; }

/* buttons */
.stButton > button {
    background: linear-gradient(90deg, #EE4D2D, #FF7337) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 10px 24px !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(238, 77, 45, 0.15);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(238, 77, 45, 0.25);
    opacity: 0.95 !important;
}
.stButton > button:active {
    transform: translateY(1px);
}

/* Sidebar button — orange with white text to match design */
section[data-testid="stSidebar"] .stButton > button {
    background: #EE4D2D !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    width: 100% !important;
    padding: 12px 20px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.2s ease !important;
}
section[data-testid="stSidebar"] .stButton > button * {
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #D94020 !important;
    box-shadow: 0 6px 22px rgba(0, 0, 0, 0.28) !important;
    transform: translateY(-1px) !important;
}

/* metric */
[data-testid="stMetricValue"] { color: var(--orange) !important; font-size: 1.8rem !important; }

/* dataframe */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

.sv-note {
    color: var(--text) !important;
    background: var(--orange-lite) !important;
    border-left: 4px solid var(--orange) !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    margin: 8px 0 14px !important;
    font-weight: 500 !important;
}
.sv-note strong { color: var(--orange2) !important; }

/* divider */
.sv-divider { border:none; border-top:1px solid var(--border); margin:16px 0; }

/* empty state */
.sv-empty {
    text-align: center;
    padding: 40px 20px;
    color: var(--sub);
    border: 2px dashed var(--orange2);
    border-radius: 12px;
    margin: 12px 0;
    background: var(--orange-lite);
}
.sv-empty i { font-size: 2.5rem; margin-bottom: 12px; display:block; color: var(--orange); opacity:.6; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
PRODUCTS = ["เสื้อยืด", "หูฟังไร้สาย", "รองเท้าผ้าใบ", "กระเป๋าเป้", "คีย์บอร์ดเกมมิ่ง"]
SCORE_OPTIONS = [0, 1, 2, 3, 4, 5]
SCORE_LABELS = {
    0: "0 = ยังไม่มีการโต้ตอบ",
    1: "1 = เคยดูสินค้า",
    2: "2 = กดถูกใจ",
    3: "3 = เพิ่มลงตะกร้า",
    4: "4 = รอการโอนเงิน",
    5: "5 = ซื้อสินค้าแล้ว",
}
SCORE_OPTION_LABELS = [SCORE_LABELS[score] for score in SCORE_OPTIONS]
SCORE_VALUES_BY_LABEL = {label: score for score, label in SCORE_LABELS.items()}

def format_score(score: int) -> str:
    return SCORE_LABELS.get(score, str(score))

# ─────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────
if "R" not in st.session_state:
    st.session_state["R"] = []          # empty — no default data
if "user_names" not in st.session_state:
    st.session_state["user_names"] = []
if "add_form_version" not in st.session_state:
    st.session_state["add_form_version"] = 0

def get_matrix() -> np.ndarray:
    return np.array(st.session_state["R"], dtype=float)

def has_data() -> bool:
    return len(st.session_state["R"]) > 0

def cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    dot_product = np.dot(u, v)
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)

    if norm_u == 0 or norm_v == 0:
        return 0.0
    return float(dot_product / (norm_u * norm_v))

def get_cosine_similarity_matrix(R: np.ndarray) -> np.ndarray:
    n = R.shape[0]
    similarity = np.zeros((n, n), dtype=float)

    for i in range(n):
        for j in range(n):
            similarity[i, j] = cosine_similarity(R[i], R[j])
    return similarity

def contrast_text_style(value: float, min_value: float, max_value: float, cutoff: float = 0.65) -> str:
    if max_value == min_value:
        normalized = 1.0 if value != 0 else 0.0
    else:
        normalized = (value - min_value) / (max_value - min_value)

    if normalized >= cutoff:
        return "color:#FFFFFF;font-weight:700;"
    return "color:#121214;font-weight:600;"

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="sv-header">
  <h1><i class="fa-solid fa-cart-shopping"></i>&nbsp;Shoplui ระบบแนะนำสินค้าออนไลน์ด้วย SVD</h1>
    <p>เว็ปจำลองการคำนวณระบบแนะนำสินค้าออนไลน์</p>
  <p>Online Product Recommendation System Using Singular Value Decomposition &nbsp;·&nbsp;
     Linear Algebra Final Project</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Sidebar — Add / manage users
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-size:1.15rem;font-weight:700;margin-bottom:6px;">
      <i class="fa-solid fa-user-plus"></i>&nbsp; เพิ่มผู้ใช้งานใหม่
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    add_form_version = st.session_state["add_form_version"]
    new_name = st.text_input(
        "ชื่อผู้ใช้ (ไม่บังคับ)",
        key=f"add_name_{add_form_version}",
    )
    st.markdown("<small>ให้คะแนนสินค้าแต่ละชิ้น</small>", unsafe_allow_html=True)
    st.caption("0 = ยังไม่มีการโต้ตอบ · 1 = เคยดูสินค้า · 2 = กดถูกใจ · 3 = เพิ่มลงตะกร้า · 4 = รอการโอนเงิน · 5 = ซื้อสินค้าแล้ว")

    new_scores = []
    for p in PRODUCTS:
        score = st.selectbox(
            p,
            SCORE_OPTIONS,
            format_func=format_score,
            key=f"add_{p}_{add_form_version}",
        )
        new_scores.append(score)

    if st.button("เพิ่มผู้ใช้งาน", key="btn_add"):
        st.session_state["R"].append(new_scores[:])
        n = len(st.session_state["user_names"])
        label = new_name.strip() if new_name.strip() else f"User {n + 1}"
        st.session_state["user_names"].append(label)
        st.session_state["add_form_version"] += 1
        st.success(f"เพิ่ม {label} สำเร็จ")
        st.rerun()

    st.markdown("---")
    if st.button("รีเซ็ตข้อมูลทั้งหมด", key="btn_reset"):
        st.session_state["R"] = []
        st.session_state["user_names"] = []
        st.rerun()

# ─────────────────────────────────────────────
# Score legend
# ─────────────────────────────────────────────
st.markdown("""
<div class="sv-card">
  <div class="sv-card-title">
    <span class="fa-badge"><i class="fa-solid fa-circle-info"></i></span>
    ความหมายของคะแนน
  </div>
  <span class="pill pill-0"><i class="fa-regular fa-circle-xmark"></i>&nbsp; 0 = ยังไม่มีการโต้ตอบ</span>
  <span class="pill pill-1"><i class="fa-regular fa-eye"></i>&nbsp; 1 = เคยดูสินค้า</span>
  <span class="pill pill-2"><i class="fa-regular fa-thumbs-up"></i>&nbsp; 2 = กดถูกใจ</span>
  <span class="pill pill-3"><i class="fa-solid fa-cart-plus"></i>&nbsp; 3 = เพิ่มลงตะกร้า</span>
  <span class="pill pill-4"><i class="fa-solid fa-clock"></i>&nbsp; 4 = รอการโอนเงิน</span>
  <span class="pill pill-5"><i class="fa-solid fa-bag-shopping"></i>&nbsp; 5 = ซื้อสินค้าแล้ว</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Empty state guard
# ─────────────────────────────────────────────
if not has_data():
    st.markdown("""
    <div class="sv-empty">
      <i class="fa-solid fa-database"></i>
      <div style="font-size:1.1rem;font-weight:600;margin-bottom:6px;">ยังไม่มีข้อมูลผู้ใช้</div>
      <div>กรุณาเพิ่มผู้ใช้งานจากแถบด้านซ้าย เพื่อเริ่มต้นการคำนวณ</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
# Step A — Show & Edit matrix R
# ─────────────────────────────────────────────
st.markdown("""
<div class="sv-card">
  <div class="sv-card-title">
    <span class="fa-badge">A</span>
    Matrix R &mdash; User-Product Matrix
  </div>
</div>
""", unsafe_allow_html=True)

user_labels = st.session_state["user_names"]
R_current = get_matrix()

df_edit = pd.DataFrame(
    R_current.astype(int),
    index=user_labels,
    columns=PRODUCTS,
).apply(lambda col: col.map(format_score))
df_edit.index.name = "ผู้ใช้"

col_cfg = {
    p: st.column_config.SelectboxColumn(
        p,
        options=SCORE_OPTION_LABELS,
        required=True,
    )
    for p in PRODUCTS
}

edited_df = st.data_editor(
    df_edit,
    column_config=col_cfg,
    use_container_width=True,
    num_rows="fixed",
    key="matrix_editor",
)

# Save edits back to session state
st.session_state["R"] = edited_df.apply(
    lambda col: col.map(lambda value: SCORE_VALUES_BY_LABEL.get(value, value))
).values.tolist()

R = get_matrix()
n_users, n_products = R.shape

st.markdown(
    f"**ขนาดของ Matrix R:** {n_users} × {n_products} &nbsp;(ผู้ใช้ × สินค้า) &nbsp;|&nbsp; "
    f"<span style='color:var(--orange,#EE4D2D);'>"
    f"ช่องว่าง (0) = {int((R == 0).sum())} ช่อง &nbsp;·&nbsp; "
    f"ช่องมีค่า = {int((R > 0).sum())} ช่อง</span>",
    unsafe_allow_html=True,
)

# need at least 2 users and 2 products to do SVD meaningfully
if n_users < 2:
    st.warning("ต้องการผู้ใช้อย่างน้อย 2 คนเพื่อคำนวณ SVD")
    st.stop()

# ─────────────────────────────────────────────
# SVD computation
# ─────────────────────────────────────────────
k = min(2, n_users, n_products)
U, s, VT = np.linalg.svd(R, full_matrices=False)
Uk  = U[:, :k]
sk  = s[:k]
VTk = VT[:k, :]
R_hat = Uk @ np.diag(sk) @ VTk

# ─────────────────────────────────────────────
# Step B — SVD results
# ─────────────────────────────────────────────
st.markdown("""
<div class="sv-card">
  <div class="sv-card-title">
    <span class="fa-badge">B</span>
    SVD &mdash; Singular Value Decomposition
  </div>
</div>
""", unsafe_allow_html=True)

st.latex(r"R = U \Sigma V^T")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"**Matrix U** &nbsp;<small style='color:#888;'>Shape: {U.shape}</small>",
                unsafe_allow_html=True)
    st.caption("ความสัมพันธ์ User ↔ Latent Feature")
    df_U = pd.DataFrame(U.round(4), index=user_labels,
                        columns=[f"F{i+1}" for i in range(U.shape[1])])
    u_min = float(df_U.min().min())
    u_max = float(df_U.max().max())
    st.dataframe(
        df_U.style
            .format("{:.4f}")
            .background_gradient(cmap="PuBuGn")
            .map(lambda value: contrast_text_style(value, u_min, u_max, cutoff=0.62)),
        use_container_width=True,
    )

with col2:
    st.markdown(f"**Singular Values Σ** &nbsp;<small style='color:#888;'>Shape: {s.shape}</small>",
                unsafe_allow_html=True)
    st.caption("ความสำคัญของแต่ละมิติ (มากสุด → น้อยสุด)")
    df_s = pd.DataFrame({"ค่า Singular": s.round(4)},
                        index=[f"σ{i+1}" for i in range(len(s))])
    st.dataframe(df_s.style.bar(color="#EE4D2D").format("{:.4f}"),
                 use_container_width=True)

with col3:
    st.markdown(f"**Matrix V^T** &nbsp;<small style='color:#888;'>Shape: {VT.shape}</small>",
                unsafe_allow_html=True)
    st.caption("ความสัมพันธ์ Product ↔ Latent Feature")
    df_VT = pd.DataFrame(VT.round(4), columns=PRODUCTS,
                         index=[f"F{i+1}" for i in range(VT.shape[0])])
    vt_min = float(df_VT.min().min())
    vt_max = float(df_VT.max().max())
    st.dataframe(
        df_VT.style
            .format("{:.4f}")
            .background_gradient(cmap="Oranges")
            .map(lambda value: contrast_text_style(value, vt_min, vt_max, cutoff=0.6)),
        use_container_width=True,
    )

# ─────────────────────────────────────────────
# Step C — User Similarity using Cosine Similarity
# ─────────────────────────────────────────────
st.markdown("""
<div class="sv-card">
  <div class="sv-card-title">
    <span class="fa-badge">C</span>
    User Similarity &mdash; Cosine Similarity
  </div>
</div>
""", unsafe_allow_html=True)

st.latex(r"\text{cosine similarity}(u, v) = \frac{\langle u, v \rangle}{\|u\|\|v\|}")
st.markdown(
    """
    <div class="sv-note">
      Cosine Similarity ใช้วัดความคล้ายกันของผู้ใช้จากมุมระหว่างเวกเตอร์คะแนน
      ค่าใกล้ <strong>1</strong> หมายถึงพฤติกรรมใกล้เคียงกันมาก ส่วนค่าใกล้ <strong>0</strong>
      หมายถึงความสนใจต่างกันหรือยังไม่มีข้อมูลร่วมกัน
    </div>
    """,
    unsafe_allow_html=True,
)

similarity_matrix = get_cosine_similarity_matrix(R)
df_similarity = pd.DataFrame(
    similarity_matrix.round(3),
    index=user_labels,
    columns=user_labels,
)

st.dataframe(
    df_similarity.style
        .format("{:.3f}")
        .background_gradient(cmap="GnBu", vmin=0, vmax=1)
        .map(lambda value: contrast_text_style(value, 0, 1, cutoff=0.58)),
    use_container_width=True,
)

sim_selected_idx = st.selectbox(
    "เลือกลูกค้าที่ต้องการดูความคล้ายกัน",
    options=range(n_users),
    format_func=lambda i: user_labels[i],
    key="sim_user",
)

similar_users = [
    (user_labels[i], float(similarity_matrix[sim_selected_idx, i]))
    for i in range(n_users)
    if i != sim_selected_idx
]
similar_users = sorted(similar_users, key=lambda item: item[1], reverse=True)

df_sim_rank = pd.DataFrame(
    similar_users,
    columns=["ลูกค้า", "Cosine Similarity"],
)
df_sim_rank.index = [f"อันดับ {i+1}" for i in range(len(df_sim_rank))]

st.dataframe(
    df_sim_rank.style
        .format({"Cosine Similarity": "{:.3f}"})
        .bar(subset=["Cosine Similarity"], color="#EE4D2D", vmin=0, vmax=1),
    use_container_width=True,
)

# ─────────────────────────────────────────────
# Step D — Truncated SVD → R̂
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="sv-card">
  <div class="sv-card-title">
    <span class="fa-badge">D</span>
    Truncated SVD (k={k}) &mdash; Matrix R̂ ที่สร้างขึ้นใหม่
  </div>
</div>
""", unsafe_allow_html=True)

st.latex(r"\hat{R} = U_k \Sigma_k V_k^T \quad (k=" + str(k) + r")")
st.markdown(
    f"""
    <div class="sv-note">
      เก็บเฉพาะ <strong>{k} มิติสำคัญ</strong> — ค่าในช่องที่เคยเป็น 0
      จะได้รับ <strong>คะแนนทำนาย</strong> จาก pattern แฝงของผู้ใช้คนอื่นใหม่
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    f"เก็บเฉพาะ **{k} มิติสำคัญ** — ค่าในช่องที่เคยเป็น 0 จะได้รับ **คะแนนทำนาย** จาก pattern แฝงของผู้ใช้คนอื่น"
)

df_Rhat = pd.DataFrame(R_hat.round(3), index=user_labels, columns=PRODUCTS)
rhat_min = float(df_Rhat.min().min())
rhat_max = float(df_Rhat.max().max())
st.dataframe(
    df_Rhat.style
        .format("{:.3f}")
        .background_gradient(cmap="YlOrRd")
        .map(lambda value: contrast_text_style(value, rhat_min, rhat_max, cutoff=0.6)),
    use_container_width=True,
)

total_var = float(np.sum(s**2))
var_k     = float(np.sum(sk**2))
pct       = var_k / total_var * 100 if total_var > 0 else 0
st.info(
    f"\u2139\ufe0f  **Variance Explained (k={k}):** {pct:.1f}%  "
    f"— รักษาข้อมูลสำคัญไว้ได้ {pct:.1f}% ด้วยเพียง {k} มิติ"
)

# ─────────────────────────────────────────────
# Step E — Recommendation engine
# ─────────────────────────────────────────────
st.markdown("""
<div class="sv-card">
  <div class="sv-card-title">
    <span class="fa-badge">E</span>
    Recommendation Engine &mdash; ผลการแนะนำสินค้า
  </div>
</div>
""", unsafe_allow_html=True)

selected_idx = st.selectbox(
    "เลือกลูกค้าที่ต้องการดูผลแนะนำ",
    options=range(n_users),
    format_func=lambda i: user_labels[i],
    key="rec_user",
)
st.caption("เลือกชื่อลูกค้าเพื่อดูประวัติ คะแนนทำนาย และรายการสินค้าที่ควรแนะนำ")

user_original  = R[selected_idx]
user_predicted = R_hat[selected_idx]

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**ประวัติการโต้ตอบ (คะแนนจริง)**")
    df_orig = pd.DataFrame({
        "สินค้า":    PRODUCTS,
        "คะแนนจริง": user_original.astype(int),
        "สถานะ":     [
            "เคยโต้ตอบ" if v > 0 else "ยังไม่เคย"
            for v in user_original
        ],
    }).set_index("สินค้า")
    st.dataframe(df_orig.style.map(
        lambda v: "color:#EE4D2D;font-weight:600;" if isinstance(v, int) and v > 0 else "",
        subset=["คะแนนจริง"],
    ), use_container_width=True)

with col_b:
    st.markdown("**คะแนนทำนายจาก R̂**")
    df_pred = pd.DataFrame({
        "สินค้า":       PRODUCTS,
        "คะแนนทำนาย":  user_predicted.round(3),
    }).set_index("สินค้า")
    st.dataframe(
        df_pred.style
            .format("{:.3f}")
            .bar(subset=["คะแนนทำนาย"], color="#EE4D2D"),
        use_container_width=True,
    )

st.markdown("<hr class='sv-divider'>", unsafe_allow_html=True)

unvisited_mask = user_original == 0

if unvisited_mask.sum() == 0:
    st.warning(
        "ผู้ใช้นี้โต้ตอบกับสินค้าทุกชิ้นแล้ว — ไม่มีสินค้าที่ต้องแนะนำ"
    )
    st.info("เลือกลูกค้าคนอื่นจากช่องด้านบนเพื่อดูผลแนะนำของแต่ละคน")
else:
    unvisited_scores = np.where(unvisited_mask, user_predicted, -np.inf)
    best_idx     = int(np.argmax(unvisited_scores))
    best_product = PRODUCTS[best_idx]
    best_score   = float(user_predicted[best_idx])

    st.markdown(f"### ผลการแนะนำสำหรับ **{user_labels[selected_idx]}**")

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.success(
            f"**สินค้าที่แนะนำ: {best_product}**\n\n"
            f"คะแนนทำนาย: **{best_score:.4f}**"
        )
        st.metric(
            label="สินค้าที่น่าจะสนใจมากที่สุด",
            value=best_product,
            delta=f"score {best_score:.3f}",
        )

    # Ranked list of unvisited
    st.markdown("**ลำดับสินค้าที่ยังไม่เคยโต้ตอบ (เรียงตามคะแนนทำนาย)**")
    ranked = sorted(
        [(PRODUCTS[i], round(float(user_predicted[i]), 4))
         for i in range(n_products) if unvisited_mask[i]],
        key=lambda x: x[1], reverse=True,
    )
    df_rank = pd.DataFrame(ranked, columns=["สินค้า", "คะแนนทำนาย"])
    df_rank.index = [f"อันดับ {i+1}" for i in range(len(df_rank))]
    st.dataframe(
        df_rank.style
            .format({"คะแนนทำนาย": "{:.4f}"})
            .bar(subset=["คะแนนทำนาย"], color="#EE4D2D"),
        use_container_width=True,
    )

# ─────────────────────────────────────────────
# Theory expander
# ─────────────────────────────────────────────
with st.expander("ทฤษฎีเพิ่มเติม — SVD คืออะไร?"):
    st.markdown("""
**Singular Value Decomposition (SVD)** คือการแยกเมทริกซ์ R ขนาด m×n ออกเป็น 3 ส่วน:
""")
    st.latex(r"R = U \Sigma V^T")
    st.markdown("""
| สัญลักษณ์ | ความหมาย |
|---|---|
| **U** (m×r) | แสดงความสัมพันธ์ระหว่าง User กับ Latent Features |
| **Σ** (r×r) | Diagonal matrix แสดงความสำคัญของแต่ละ Feature |
| **V^T** (r×n) | แสดงความสัมพันธ์ระหว่าง Product กับ Latent Features |

**Truncated SVD (k)** เก็บเฉพาะ k มิติที่สำคัญที่สุด เพื่อ:
- ลด noise ในข้อมูล
- ทำนายคะแนนในช่องที่เป็น 0 (Collaborative Filtering)
- ค้นหา pattern แฝงของพฤติกรรมผู้ใช้
""")
    st.latex(r"\hat{R} = U_k \Sigma_k V_k^T \quad \text{where } k \ll \min(m,n)")

st.markdown("---")
st.caption(
    "Linear Algebra Final Project  ·  "
    "Online Product Recommendation System Using SVD"
)
