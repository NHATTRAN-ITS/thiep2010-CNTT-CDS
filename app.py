import base64
import hashlib
import html
import math
import random
import unicodedata
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from members import member_data, validate_members
from music_player import render_music_player
SIGNATURE = "Minh Nhật - IT Service HCM2"
SLIDE_SECONDS = 15
BOOT_LINE_MS = 520
BOOT_HOLD_MS = 900

st.set_page_config(page_title="Bản Giao Hưởng Số 20/10", page_icon="🌸", layout="wide")
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QSob {display: none !important;}
    div[data-testid="stStatusWidget"] {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
validate_members(member_data)

PALETTES = [
    ("#ff6b9d", "#ffc2d4", "#ffd166"),
    ("#e84393", "#fab1d6", "#fdcb6e"),
    ("#a29bfe", "#dcd6ff", "#ffeaa7"),
    ("#ff7675", "#ffd3cf", "#fff3b0"),
    ("#fd79a8", "#ffe0ec", "#f6b93b"),
    ("#f78fb3", "#fde3ee", "#ffb142"),
]


def fold(text):
    normalized = unicodedata.normalize("NFD", str(text).lower())
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


@st.cache_data(show_spinner=False)
def flower_params(name):
    seed = int(hashlib.sha256(name.encode("utf-8")).hexdigest(), 16)
    rng = random.Random(seed)
    return {
        "petals": rng.choice([5, 6, 8, 9, 12]),
        "layers": rng.choice([2, 3]),
        "palette": rng.choice(PALETTES),
        "spin": rng.choice([40, 60, 80]),
    }


@st.cache_data(show_spinner=False)
def flower_svg(name):
    params = flower_params(name)
    c1, c2, c3 = params["palette"]
    petal_count = params["petals"]
    petals = []
    for layer in range(params["layers"]):
        scale = 1 - layer * 0.27
        color = c1 if layer % 2 == 0 else c2
        for i in range(petal_count):
            ang = i * 360 / petal_count + layer * 180 / petal_count
            petals.append(
                f'<ellipse cx="100" cy="56" rx="{15 * scale + 3:.1f}" ry="{42 * scale:.1f}" '
                f'fill="{color}" fill-opacity=".88" stroke="#fff" stroke-opacity=".6" '
                f'transform="rotate({ang:.1f} 100 100)"/>'
            )
    seeds = []
    for k in range(45):
        rad = 2.1 * math.sqrt(k)
        ang = math.radians(k * 137.508)
        seeds.append(
            f'<circle cx="{100 + rad * math.cos(ang):.1f}" cy="{100 + rad * math.sin(ang):.1f}" '
            f'r="1.6" fill="#b7791f"/>'
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" '
        f'aria-label="Hoa sinh từ tên {html.escape(name)}"><g>'
        '<animateTransform attributeName="transform" type="rotate" '
        f'from="0 100 100" to="360 100 100" dur="{params["spin"]}s" repeatCount="indefinite"/>'
        f'{"".join(petals)}</g><circle cx="100" cy="100" r="15" fill="{c3}"/>{"".join(seeds)}</svg>'
    )


def flower_img(name, size=220):
    encoded = base64.b64encode(flower_svg(name).encode("utf-8")).decode("ascii")
    safe_name = html.escape(name)
    return (
        f'<img class="flower" width="{int(size)}" alt="Hoa dành riêng cho {safe_name}" '
        f'src="data:image/svg+xml;base64,{encoded}">'
    )


CARD_CSS = """
.master-card{background:linear-gradient(135deg,rgba(255,255,255,.96),rgba(255,240,245,.92));
  padding:clamp(16px,4vw,36px);border-radius:clamp(16px,3vw,28px);border:2px solid rgba(255,182,193,.6);
  position:relative;box-shadow:0 20px 50px rgba(214,51,132,.18);
  animation:appear .8s cubic-bezier(.16,1,.3,1);max-width:100%;box-sizing:border-box}
.master-card h2{color:#b83280;font-family:'Playfair Display',serif;margin:0 0 6px;text-align:center;
  font-size:clamp(1.2rem,4vw,1.85rem);line-height:1.3}
.master-card h2 span{color:#ff416c}
.flower{display:block;margin:0 auto 8px;width:min(220px,55vw);height:auto;
  animation:bloom 1.4s cubic-bezier(.16,1,.3,1)}
.chips{text-align:center;margin:10px 0 14px}
.chips span{display:inline-block;background:#fff;border:1px solid #ffc2d4;color:#8a2c5a;
  border-radius:50px;padding:5px 14px;margin:3px;font-size:clamp(.78rem,2.6vw,.92rem)}
.dna{text-align:center;color:#a0768a;font-size:clamp(.7rem,2.4vw,.8rem);font-family:monospace;margin-bottom:12px}
.wish{font-size:clamp(.95rem,2.8vw,1.08rem);line-height:1.85;color:#2d3436;text-align:justify;margin:14px 0;
  overflow-wrap:anywhere}
.wish .w{opacity:0;display:inline-block;margin-right:.28em;animation:wordIn .5s forwards}
.note{margin:8px 0;background:#fff7e6;border-left:4px solid #ffb142;padding:10px 14px;border-radius:10px;color:#5c4a1f}
.sig{font-family:'Dancing Script',cursive;font-size:clamp(1.35rem,4vw,1.8rem);color:#d63384;text-align:right;margin-top:20px}
@keyframes appear{from{opacity:0;transform:scale(.96) translateY(18px)}to{opacity:1;transform:none}}
@keyframes bloom{from{opacity:0;transform:scale(.2) rotate(-90deg)}to{opacity:1;transform:none}}
@keyframes wordIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@media (max-width: 720px){
  .wish{text-align:left}
}
@media (prefers-reduced-motion: reduce){
  .wish .w,.master-card,.flower,.petal,.boot-line,#boot-overlay,.slide-pane{
    animation:none !important;transition:none !important;opacity:1 !important;transform:none !important}
  #boot-overlay{display:none !important}
}
"""

FONTS = (
    "@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700"
    "&family=Playfair+Display:wght@600&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');"
)

PAGE_CSS = FONTS + CARD_CSS + """
.stApp{background:radial-gradient(circle at 50% 10%,#fff0f5 0%,#ffe4e1 35%,#f0f4f8 100%);
  font-family:'Plus Jakarta Sans',sans-serif}
.block-container{padding-top:1.1rem !important;padding-left:clamp(.7rem,3vw,2.5rem) !important;
  padding-right:clamp(.7rem,3vw,2.5rem) !important;max-width:1120px !important}
.title-glow{font-family:'Playfair Display',serif;text-align:center;font-size:clamp(1.55rem,5.2vw,3.2rem);
  background:linear-gradient(45deg,#d63384,#ff416c,#e84393);-webkit-background-clip:text;
  background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px;line-height:1.25}
.subtitle-glow{text-align:center;color:#57606f;font-style:italic;margin-bottom:16px;
  font-size:clamp(.88rem,2.6vw,1.05rem);padding:0 .4rem}
.stButton>button{background:linear-gradient(135deg,#ff416c,#ff4b2b);color:#fff;font-weight:700;
  border-radius:50px;border:none;padding:12px 24px;width:100%;box-shadow:0 8px 25px rgba(255,65,108,.35);
  transition:all .3s}
.stButton>button:hover{transform:translateY(-3px) scale(1.02);color:#fff}
.mini{text-align:center;font-weight:600;color:#8a2c5a;font-size:.86rem;margin-bottom:8px}
.bouquet-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px 10px;margin:12px 0 18px}
.petal{position:fixed;top:-40px;z-index:0;pointer-events:none;animation:fall linear infinite}
@keyframes fall{to{transform:translateY(112vh) rotate(360deg)}}
#boot-overlay{position:fixed;inset:0;z-index:99999;background:#140c16;display:flex;align-items:center;
  justify-content:center;padding:24px;animation:bootOut .7s ease forwards}
.boot-box{width:min(720px,100%);background:#1b1220;border:1px solid #5c3d4a;border-radius:14px;
  padding:18px 18px 14px;box-shadow:0 20px 60px rgba(0,0,0,.45);color:#f8d7e4;font-family:ui-monospace,Consolas,monospace}
.boot-box h3{margin:0 0 12px;color:#ff9ec0;font-size:.95rem;letter-spacing:.04em}
.boot-line{opacity:0;display:block;white-space:pre-wrap;line-height:1.7;font-size:clamp(.78rem,2.4vw,.92rem);
  animation:bootIn .4s ease forwards}
@keyframes bootIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@keyframes bootOut{to{opacity:0;visibility:hidden;pointer-events:none}}
@media (max-width: 768px){
  .petal{display:none}
  div[data-testid="stHorizontalBlock"]{flex-wrap:wrap !important}
  div[data-testid="stHorizontalBlock"] > div{flex:1 1 100% !important;width:100% !important}
  .stTabs [data-baseweb="tab-list"]{overflow-x:auto;flex-wrap:nowrap}
}
"""

st.markdown(f"<style>{PAGE_CSS}</style>", unsafe_allow_html=True)

petal_rng = random.Random(2010)
st.markdown(
    "".join(
        f"<span class='petal' aria-hidden='true' style='left:{petal_rng.randint(0, 98)}%;"
        f"font-size:{petal_rng.randint(14, 26)}px;animation-duration:{petal_rng.randint(9, 18)}s;"
        f"animation-delay:-{petal_rng.randint(0, 15)}s'>"
        f"{petal_rng.choice(['🌸', '🌺', '🌷', '💮'])}</span>"
        for _ in range(16)
    ),
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 class='title-glow'>🌸 BẢN GIAO HƯỞNG SỐ — 20/10 🌸</h1>"
    "<p class='subtitle-glow'>Ngày Công dân số 15/10 gặp Ngày Phụ nữ Việt Nam 20/10 —"
    " dành tặng các chị Phòng CNTT &amp; CĐS</p>",
    unsafe_allow_html=True,
)


def reveal(text):
    words = html.escape(text).split()
    return " ".join(
        f'<span class="w" style="animation-delay:{i * 0.045:.2f}s">{word}</span>'
        for i, word in enumerate(words)
    )


def card_html(name, info):
    params = flower_params(name)
    memory = str(info.get("memory", "")).strip()
    note_html = f"<div class='note'>💬 {html.escape(memory)}</div>" if memory else ""
    return f"""
    <div class='master-card'>
      {flower_img(name)}
      <h2>{html.escape(info['icon'])} <span>{html.escape(name)}</span></h2>
      <div class='chips'><span>🏷️ {html.escape(info['role'])}</span>
        <span>💡 {html.escape(info['trait'])}</span></div>
      <div class='dna'>🧬 bông hoa này sinh ra từ tên chị: {params['petals']} cánh · {params['layers']} lớp ·
        sha256 → chỉ có một bản duy nhất</div>
      <p class='wish'>{reveal(info['wish'])}</p>
      {note_html}
      <div class='sig'>{html.escape(SIGNATURE)}</div>
    </div>"""


def release_notes(name, info):
    short = name.split()[-1]
    return f"""## v20.10 — Bản phát hành dành cho {short}
+ Added    : thật nhiều nụ cười và những ngày nhẹ nhõm
+ Improved : {info['trait']}
+ Fixed    : mọi mệt mỏi, deadline dồn dập (hotfix vĩnh viễn)
+ Security : được trân trọng và che chở bởi cả phòng
- Removed  : lo lắng và áp lực không cần thiết
Status: Deployed with love | Uptime hạnh phúc: 99.99%"""


def standalone_html(card):
    return (
        "<!doctype html><html lang='vi'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<title>Thiệp 20/10</title>"
        f"<style>{FONTS}body{{background:#fff0f5;display:flex;justify-content:center;padding:16px;"
        f"font-family:'Plus Jakarta Sans',sans-serif}}.master-card{{max-width:720px;width:100%}}{CARD_CSS}</style>"
        "</head><body>"
        f"{card}</body></html>"
    )


def match_members(query, names):
    key = fold(query).strip()
    if not key:
        return []
    hits = []
    for name in names:
        alias = fold(member_data[name].get("alias", ""))
        haystack = f"{fold(name)} {alias}"
        if key in haystack:
            hits.append(name)
    return hits


def boot_overlay_html(lines):
    last_delay = (len(lines) - 1) * BOOT_LINE_MS
    total = last_delay + BOOT_HOLD_MS + 400
    items = []
    for i, line in enumerate(lines):
        delay = i * BOOT_LINE_MS
        items.append(
            f'<span class="boot-line" style="animation-delay:{delay}ms">{html.escape(line)}</span>'
        )
    return f"""
    <div id="boot-overlay" style="animation-delay:{total}ms">
      <div class="boot-box">
        <h3>Nhật ký khởi động hệ thống</h3>
        {''.join(items)}
      </div>
    </div>
    """


def slideshow_html(names, seconds):
    panes = []
    dots = []
    for i, name in enumerate(names):
        active = " active" if i == 0 else ""
        panes.append(
            f'<div class="slide-pane{active}" data-index="{i}">{card_html(name, member_data[name])}</div>'
        )
        dots.append(f'<button class="dot{" on" if i == 0 else ""}" data-go="{i}" aria-label="Thiệp {i+1}"></button>')
    n = len(names)
    return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
{FONTS}{CARD_CSS}
html,body{{margin:0;padding:0;background:transparent;font-family:'Plus Jakarta Sans',sans-serif}}
.deck{{min-height:100%;background:radial-gradient(circle at 50% 0,#fff0f5,#ffe4e1 55%,#f7f1f4);
  border-radius:18px;padding:12px;box-sizing:border-box}}
.deck:fullscreen,.deck:-webkit-full-screen{{padding:24px;background:#1a1020}}
.toolbar{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;margin-bottom:10px}}
.toolbar .left,.toolbar .right{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}}
.toolbar button{{border:0;border-radius:999px;padding:8px 14px;font-weight:700;cursor:pointer;
  background:linear-gradient(135deg,#ff416c,#ff4b2b);color:#fff}}
.toolbar button.ghost{{background:#fff;color:#8a2c5a;border:1px solid #ffc2d4}}
.counter{{color:#8a2c5a;font-size:.9rem;font-weight:600}}
.stage{{position:relative;overflow:hidden;min-height:520px}}
.slide-pane{{position:absolute;inset:0;opacity:0;transform:translateX(36px) scale(.98);
  transition:opacity .7s ease, transform .7s cubic-bezier(.16,1,.3,1);pointer-events:none}}
.slide-pane.active{{opacity:1;transform:none;pointer-events:auto;position:relative}}
.dots{{display:flex;justify-content:center;gap:6px;margin-top:10px;flex-wrap:wrap}}
.dot{{width:9px;height:9px;padding:0;border-radius:50%;background:#ffc2d4;border:0;cursor:pointer}}
.dot.on{{background:#ff416c;transform:scale(1.25)}}
.bar{{height:4px;background:#ffd6e3;border-radius:99px;overflow:hidden;margin:8px 4px 0}}
.bar>span{{display:block;height:100%;width:0;background:#ff416c;animation:load {seconds}s linear}}
@keyframes load{{from{{width:0}}to{{width:100%}}}}
@media (max-width:720px){{.stage{{min-height:auto}}.toolbar button{{padding:8px 12px;font-size:.85rem}}}}
</style></head><body>
<div class="deck" id="deck">
  <div class="toolbar">
    <div class="left">
      <button class="ghost" id="prev" type="button">◀ Trước</button>
      <button class="ghost" id="pause" type="button">⏸ Tạm dừng</button>
      <button class="ghost" id="next" type="button">Sau ▶</button>
    </div>
    <div class="right">
      <span class="counter" id="counter">1/{n}</span>
      <button id="fs" type="button">⛶ Phóng to để chiếu</button>
    </div>
  </div>
  <div class="bar"><span id="bar"></span></div>
  <div class="stage" id="stage">{''.join(panes)}</div>
  <div class="dots">{''.join(dots)}</div>
</div>
<script>
const panes=[...document.querySelectorAll('.slide-pane')];
const dots=[...document.querySelectorAll('.dot')];
const n=panes.length;
let i=0, timer=null, playing=true, ms={seconds * 1000};
const names={names!r};
function replayWords(pane){{
  pane.querySelectorAll('.w').forEach((el, idx) => {{
    el.style.animation='none';
    el.offsetHeight;
    el.style.animation='';
    el.style.animationDelay=(idx*0.045)+'s';
  }});
}}
function show(idx, animate=true){{
  i=(idx+n)%n;
  panes.forEach((p,k)=>p.classList.toggle('active', k===i));
  dots.forEach((d,k)=>d.classList.toggle('on', k===i));
  document.getElementById('counter').textContent=(i+1)+'/'+n+' — '+names[i];
  const bar=document.getElementById('bar');
  bar.style.animation='none';
  bar.offsetHeight;
  bar.style.animation='';
  if(animate) replayWords(panes[i]);
}}
function tick(){{ show(i+1); }}
function play(){{
  playing=true;
  document.getElementById('pause').textContent='⏸ Tạm dừng';
  clearInterval(timer);
  timer=setInterval(tick, ms);
}}
function pause(){{
  playing=false;
  document.getElementById('pause').textContent='▶ Tiếp tục';
  clearInterval(timer);
}}
document.getElementById('prev').onclick=()=>{{ show(i-1); if(playing) play(); }};
document.getElementById('next').onclick=()=>{{ show(i+1); if(playing) play(); }};
document.getElementById('pause').onclick=()=> playing ? pause() : play();
dots.forEach(d=>d.onclick=()=>{{ show(Number(d.dataset.go)); if(playing) play(); }});
document.getElementById('fs').onclick=async()=>{{
  const el=document.getElementById('deck');
  try {{
    if(!document.fullscreenElement) await el.requestFullscreen();
    else await document.exitFullscreen();
  }} catch(e) {{
    el.classList.toggle('deck-max');
  }}
}};
show(0, true);
play();
</script>
</body></html>"""


names = list(member_data)
ss = st.session_state
ss.setdefault("opened", [])
ss.setdefault("current", None)
ss.setdefault("fresh", False)
ss.setdefault("cmd_log", [])


def opened_now():
    return set(ss.opened)


def open_card(n, sync_pick=True):
    if n not in member_data:
        return
    ss.current = n
    if n not in ss.opened:
        ss.opened = list(ss.opened) + [n]
    ss.fresh = True
    if sync_pick:
        ss.pending_pick = n


if "pending_pick" in ss:
    pending = ss.pop("pending_pick")
    ss.pick = pending
    ss["bloom-pick"] = pending


boot_lines = [
    "$ ./khoi_dong_20_10.sh",
    f"[ OK ] Nạp module  Phòng_CNTT_&_CĐS ........ {len(names)} thành viên nữ",
    "[ OK ] Kết nối      yêu_thương.dll ......... ổn định",
    "[ OK ] Biên dịch    lời_cảm_ơn.py .......... 0 lỗi, 0 cảnh báo",
    f"[ OK ] Sinh hoa     sha256(tên) -> {len(names)} bông duy nhất",
    ">>> Hệ thống sẵn sàng. Chúc mừng 20/10!",
]
if "boot_played" not in ss:
    st.markdown(boot_overlay_html(boot_lines), unsafe_allow_html=True)
    ss.boot_played = True

render_music_player()

tab_card, tab_slide, tab_term, tab_bouquet, tab_letter = st.tabs(
    ["💌 Thiệp riêng", "📺 Trình chiếu", "💻 Terminal bí mật", "💐 Bó hoa cả phòng", "🔐 Mật thư cuối cùng"]
)

with tab_card:
    left, right = st.columns([1, 2], gap="large")
    with left:
        with st.container(border=True):
            st.markdown("### 🔍 Trao gửi yêu thương")

            def on_pick_change():
                open_card(ss.pick, sync_pick=False)

            pick = st.selectbox("Chọn tên chị/em:", names, key="pick", on_change=on_pick_change)
            if st.button("✨ MỞ THIỆP CHÚC MỪNG", type="primary"):
                open_card(pick)
                st.rerun()
            leftover = [n for n in names if n not in opened_now()]
            if st.button("🎲 Bất ngờ chọn giúp tôi"):
                open_card(random.choice(leftover or names))
                st.rerun()
            st.caption("Dân IT hãy thử sang tab **Terminal bí mật** và gõ `help`.")
            total = max(len(names), 1)
            seen = opened_now()
            st.progress(len(seen) / total, text=f"Đã mở {len(seen)}/{len(names)} thiệp")

    with right:
        if ss.current and ss.current in member_data:
            name, info = ss.current, member_data[ss.current]
            if ss.fresh:
                ss.fresh = False
                st.balloons()
            card = card_html(name, info)
            st.markdown(card, unsafe_allow_html=True)
            st.download_button(
                "📥 Tải thiệp (HTML) để gửi Zalo/Email",
                standalone_html(card),
                file_name=f"thiep-20-10-{name.replace(' ', '-')}.html",
                mime="text/html",
                key=f"dl-{name}",
            )
            with st.expander("📜 Release notes của riêng chị"):
                st.code(release_notes(name, info), language="diff")
        else:
            st.markdown(
                "<div style='background:rgba(255,255,255,.7);padding:clamp(20px,5vw,40px);border-radius:24px;"
                "text-align:center;border:2px dashed rgba(214,51,132,.3)'>"
                "<h3 style='color:#d63384'>💌 Hộp quà kỹ thuật số đang chờ mở</h3>"
                "<p style='color:#636e72'>Chọn một cái tên ở bên trái và bấm <b>MỞ THIỆP CHÚC MỪNG</b>"
                " để xem bông hoa dành riêng cho chị.</p></div>",
                unsafe_allow_html=True,
            )

with tab_bouquet:
    st.markdown(
        f"#### {len(names)} bông hoa — {len(names)} mã hoa khác nhau, không bông nào giống bông nào 🌷"
    )
    st.caption("Bấm hoa bên dưới hoặc chọn tên rồi mở thiệp.")
    tiles = []
    seen_set = opened_now()
    for n in names:
        seen = n in seen_set
        style = "" if seen else "filter:grayscale(1);opacity:.38;transform:scale(.92)"
        tiles.append(
            f"<div class='mini' style='transition:all .6s;{style}'>{flower_img(n, 130)}<br>{html.escape(n)}</div>"
        )
    st.markdown(f"<div class='bouquet-grid'>{''.join(tiles)}</div>", unsafe_allow_html=True)
    bloom_pick = st.selectbox("Chọn bông hoa để mở thiệp", names, key="bloom-pick")
    if st.button("Xem thiệp từ bó hoa", key="bloom-open"):
        open_card(bloom_pick)
        st.rerun()

with tab_letter:
    remaining = len(names) - len(opened_now())
    unlocked = remaining <= 0 or st.toggle("Mở khóa thư chung (dành cho buổi trình bày)")
    if not unlocked:
        st.info(f"Mở nốt {remaining} thiệp nữa để nhận lá thư chung của cả phòng.")
    else:
        if remaining <= 0 and not ss.get("finale"):
            st.balloons()
            ss.finale = True
        st.markdown(
            "<div class='master-card'><h2>💐 Gửi các chị của Phòng CNTT &amp; CĐS</h2>"
            "<p class='wish'>Mỗi hệ thống chạy ổn, mỗi ticket được xử lý, mỗi con số khớp lệnh"
            " đều có bàn tay và sự tận tâm của các chị. Công nghệ giúp chúng ta làm việc nhanh hơn,"
            " nhưng chính các chị làm cho nơi này ấm áp hơn. Chúc các chị ngày 20/10 thật vui,"
            " thật nhiều hoa, và luôn được yêu thương đúng như cách các chị đã yêu thương mọi người."
            f"</p><div class='sig'>{html.escape(SIGNATURE)}</div></div>",
            unsafe_allow_html=True,
        )
        secret = "Cảm ơn các chị vì đã làm mỗi ngày đi làm trở nên đáng nhớ."
        encoded = base64.b64encode(secret.encode("utf-8")).decode("ascii")
        st.markdown("**Thông điệp mã hóa Base64** — thử giải mã nhé:")
        st.code(encoded, language="text")
        guess = st.text_input("Dán chuỗi Base64 hoặc nhấn nút giải mã", key="b64")
        if st.button("Giải mã"):
            raw = guess.strip() or encoded
            try:
                st.success(base64.b64decode(raw).decode("utf-8"))
            except Exception:
                st.error("Chuỗi Base64 chưa hợp lệ. Hãy copy đúng đoạn phía trên.")

with tab_term:
    st.markdown("#### Terminal bí mật của Phòng CNTT & CĐS")
    st.caption("Gõ `help` rồi nhấn Enter. Có thể gõ không dấu: `thank van`.")
    cmd_raw = st.text_input("$", placeholder="help", key="cmd")
    cmd = fold(cmd_raw).strip()

    def run_command(raw):
        folded = fold(raw).strip()
        if not folded:
            return
        if folded == "help":
            st.code(
                "ls             danh sách các chị\n"
                "thank <tên>    lời cảm ơn riêng (vd: thank van / thank linh)\n"
                "open <tên>     mở thiệp ngay từ terminal\n"
                "sudo love      cấp quyền yêu thương tối cao\n"
                "uptime         hạnh phúc đã chạy bao lâu\n"
                "clear          xóa nhật ký lệnh",
                language="bash",
            )
        elif folded == "ls":
            st.code("\n".join(f"{v['icon']}  {n}" for n, v in member_data.items()), language="bash")
        elif folded.startswith("thank ") or folded.startswith("open "):
            action, key = folded.split(" ", 1)
            hits = match_members(key, names)
            if not hits:
                st.error(f"Không tìm thấy '{key}'. Gõ ls để xem danh sách.")
                return
            for n in hits:
                st.markdown(flower_img(n, 90), unsafe_allow_html=True)
                if action == "open":
                    open_card(n)
                    st.success(f"Đã mở thiệp của {n}. Mở tab Thiệp riêng để xem đầy đủ.")
                else:
                    st.success(
                        f"Cảm ơn {n}: {member_data[n]['trait']}. Phòng mình không thể thiếu người này."
                    )
        elif folded == "sudo love":
            st.balloons()
            st.code(
                "[sudo] password for minhnhat: ********\nPermission granted: yêu thương vô điều kiện",
                language="bash",
            )
        elif folded == "uptime":
            st.code(
                f"up 20/10, {len(names)} người, load average tình cảm: 9.99, 9.99, 9.99, errors: 0",
                language="bash",
            )
        elif folded == "clear":
            ss.cmd_log = []
            st.info("Đã xóa nhật ký lệnh.")
        else:
            st.error(f"bash: {raw.strip()}: command not found. Gõ help nhé!")

    if cmd:
        run_command(cmd_raw)
        if not ss.cmd_log or ss.cmd_log[-1] != cmd_raw.strip():
            ss.cmd_log = (ss.cmd_log + [cmd_raw.strip()])[-8:]
    if ss.cmd_log:
        with st.expander("Nhật ký lệnh", expanded=False):
            st.code("\n".join(f"$ {item}" for item in ss.cmd_log), language="bash")

with tab_slide:
    st.caption(
        f"Tự chuyển thiệp mỗi {SLIDE_SECONDS} giây, có hiệu ứng trượt mờ. "
        "Bấm **Phóng to để chiếu** khi trình bày trên máy chiếu."
    )
    play = st.toggle("Bật trình chiếu tự động", key="play-slides")
    if play and names:
        missing = [n for n in names if n not in ss.opened]
        if missing:
            ss.opened = ss.opened + missing
        components.html(slideshow_html(names, SLIDE_SECONDS), height=780, scrolling=True)

st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#636e72;font-size:.9rem'>Tác phẩm số chào mừng Ngày Công dân số"
    " (15/10) &amp; Ngày Phụ nữ Việt Nam (20/10) — Phòng CNTT &amp; CĐS</p>",
    unsafe_allow_html=True,
)
