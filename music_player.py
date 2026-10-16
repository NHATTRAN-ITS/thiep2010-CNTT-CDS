import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

STATIC_DIR = Path(__file__).with_name("static")

_PLAYER_HTML = """
<script>
(function () {
  var P, D;
  try { P = window.parent; D = P.document; } catch (e) { return; }
  var NAME = __NAME__;
  var url = new P.URL('app/static/' + encodeURIComponent(NAME), P.location.href).href;

  if (!D.getElementById('bgm-style')) {
    var style = D.createElement('style');
    style.id = 'bgm-style';
    style.textContent =
      '#bgm-btn{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:100000;' +
      'border:0;border-radius:999px;padding:10px 20px;font:700 14px system-ui,sans-serif;color:#fff;' +
      'cursor:pointer;background:linear-gradient(135deg,#ff416c,#ff4b2b);' +
      'box-shadow:0 8px 24px rgba(255,65,108,.45)}#bgm-btn:hover{filter:brightness(1.08)}';
    D.head.appendChild(style);
  }

  var audio = D.getElementById('bgm-audio');
  if (!audio) {
    audio = D.createElement('audio');
    audio.id = 'bgm-audio';
    audio.loop = true;
    audio.preload = 'auto';
    D.body.appendChild(audio);
  }
  if (audio.dataset.name !== NAME) { audio.dataset.name = NAME; audio.src = url; }

  var btn = D.getElementById('bgm-btn');
  if (!btn) {
    btn = D.createElement('button');
    btn.id = 'bgm-btn';
    btn.type = 'button';
    D.body.appendChild(btn);
  }
  function sync() {
    btn.textContent = audio.paused ? '▶ Phát nhạc' : '⏸ Dừng nhạc';
    btn.setAttribute('aria-label', audio.paused ? 'Phát nhạc nền' : 'Dừng nhạc nền');
  }
  audio.onplay = sync;
  audio.onpause = sync;
  btn.onclick = function () {
    if (audio.paused) { audio.dataset.userPaused = '0'; audio.play().catch(function () {}); }
    else { audio.dataset.userPaused = '1'; audio.pause(); }
  };
  sync();

  function allowed() { return audio.dataset.userPaused !== '1'; }

  if (allowed() && audio.paused) audio.play().catch(function () {});

  if (!audio.dataset.armed) {
    audio.dataset.armed = '1';
    var evs = ['pointerdown', 'touchstart', 'keydown', 'click'];
    var kick = function (ev) {
      if (btn.contains(ev.target) || !allowed()) return;
      audio.play().then(function () {
        evs.forEach(function (e) { D.removeEventListener(e, kick, true); });
      }).catch(function () {});
    };
    evs.forEach(function (e) { D.addEventListener(e, kick, true); });
  }
})();
</script>
"""


def _find_track():
    if not STATIC_DIR.exists():
        return None
    files = sorted(STATIC_DIR.glob("*.mp3"))
    return files[0].name if files else None


def render_music_player():
    track = _find_track()
    if not track:
        st.caption("🎵 Chưa có nhạc: hãy đặt 1 file .mp3 vào thư mục `static` cạnh app.py.")
        return
    components.html(_PLAYER_HTML.replace("__NAME__", json.dumps(track)), height=0)