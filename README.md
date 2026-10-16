# Bản Giao Hưởng Số — 20/10

Ứng dụng Streamlit chúc mừng Ngày Phụ nữ Việt Nam, dành tặng các chị Phòng CNTT & CĐS.

## Chạy trên máy

```powershell
cd D:\2010
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Tùy chọn: đặt file `music.mp3` cạnh `app.py` để phát nhạc nền.

## Đưa lên web để gửi link

GitHub Pages **không chạy được** Streamlit (Pages chỉ phục vụ file tĩnh HTML/CSS/JS). Cách đúng là đẩy code lên GitHub rồi deploy **Streamlit Community Cloud** — miễn phí, ai có link cũng mở được.

### 1. Đẩy code lên GitHub

1. Tạo repo mới trên GitHub (ví dụ `thiep-20-10`). Có thể để **Public** để Cloud deploy dễ, hoặc Private cũng được.
2. Trên máy:

```powershell
cd D:\2010
git init
git add app.py members.py requirements.txt README.md .gitignore .streamlit
git commit -m "Thiệp 20/10 Phòng CNTT & CĐS"
git branch -M main
git remote add origin https://github.com/<user-cua-ban>/thiep-20-10.git
git push -u origin main
```

Không commit `CURRENT/`, `__pycache__/` hay file nhạc lớn nếu không cần.

### 2. Deploy trên Streamlit Cloud

1. Vào [share.streamlit.io](https://share.streamlit.io) và đăng nhập bằng GitHub.
2. **Create app** → chọn repo, branch `main`, file chính `app.py`.
3. Bấm **Deploy**. Đợi 1–2 phút.
4. Copy link dạng `https://thiep-20-10.streamlit.app` rồi gửi Zalo/email.

Mỗi lần sửa code, `git push` là Cloud tự cập nhật.

### Nếu app ở repo Private

Trong Streamlit Cloud, cấp quyền GitHub cho Streamlit đọc repo đó. Repo Public thì không cần bước này.

## Cấu trúc

- `app.py` — giao diện, hoa thuật toán, thiệp, terminal, trình chiếu
- `members.py` — dữ liệu từng người (role, trait, wish, alias, memory)
- `.streamlit/config.toml` — theme khi trình bày

Thêm kỷ niệm riêng bằng khóa `memory` trong `members.py`.
