# 🌙 Moonlighter 2 - Overlay Hiển Thị Giá

Ứng dụng overlay giúp bạn tra cứu **Perfect Stamp Price** cho items trong game Moonlighter 2 một cách nhanh chóng và tiện lợi!

![Python](https://img.shields.io/badge/Platform-Windows-blue.svg)
![Version](https://img.shields.io/badge/Version-1.0-green.svg)

## 🎯 Chức Năng Chính

- 🔍 **Quét OCR tự động**: Nhận diện tên item trên màn hình
- 💰 **Hiển thị giá**: Perfect Stamp Price cho 154 relics
- ⌨️ **Phím tắt**: F6 để quét, F5 để chọn vùng, F4 để ẩn/hiện
- 🎨 **Màu sắc theo độ hiếm**: Common, Uncommon, Rare, Epic, Legendary
- 👁️ **Always-on-top**: Luôn hiển thị trên game
- 📱 **2 chế độ hiển thị**: Compact (nhỏ gọn) và Detailed (chi tiết)

## 📦 Cài Đặt Nhanh (Phiên Bản EXE)

### Bước 1: Tải Về
- Tải folder **MoonlighterOverlay_Release** 
- Giải nén vào vị trí bất kỳ

### Bước 2: Chạy
- Double click vào `MoonlighterOverlay.exe`
- Chờ 10-30 giây để app tải OCR models (chỉ lần đầu tiên)
- Xong! App đã sẵn sàng

### Yêu Cầu Hệ Thống
- Windows 10/11
- 4GB RAM trở lên
- Moonlighter 2 game
- **Không cần cài Python hay thư viện gì thêm!**

## 🎮 Hướng Dẫn Sử Dụng

### Khởi Chạy
1. Mở game Moonlighter 2
2. Chạy `MoonlighterOverlay.exe`
3. Đợi app load xong (xem cửa sổ overlay góc phải màn hình)

### Sử Dụng

**Quét Item:**
1. Di chuột vào 1 item trong game (để hiện tên item)
2. Nhấn phím `F6` để quét
3. Giá sẽ hiện ngay lập tức trên overlay!

**Thay Đổi Vùng OCR (nếu cần):**
- Nhấn `F5` để mở công cụ chọn vùng
- Click và kéo để chọn vùng chứa tên item
- Nhấn Enter để lưu
- Khởi động lại app

**Ẩn/Hiện Overlay:**
- Nhấn `F4` để ẩn overlay tạm thời
- Nhấn `F4` lần nữa để hiện lại

**Chuyển Chế Độ Hiển Thị:**
- Click vào overlay để chuyển giữa:
  - **Compact**: Chỉ tên + giá (nhỏ gọn)
  - **Detailed**: Đầy đủ thông tin (tên, độ hiếm, vị trí, giá)

## 🖼️ Giao Diện

### Chế Độ Detailed (Chi Tiết)
```
┌──────────────────────────────┐
│ 🌙 Moonlighter 2 Prices     │
│ Status: SCANNING            │
├──────────────────────────────┤
│ Broken Battery              │
│ Rarity: Common              │
│ Location: The Gallery       │
│                             │
│ 💰 26g                      │
├──────────────────────────────┤
│ F6: Scan | F5: Region       │
└──────────────────────────────┘
```

### Chế Độ Compact (Nhỏ Gọn)
```
┌──────────────────────┐
│ Broken Battery       │
│ 💰 26g               │
└──────────────────────┘
```

## ⚙️ Tùy Chỉnh

Chỉnh sửa file `config.json` để thay đổi cấu hình:

```json
{
  "scan_frequency": 0.5,
  "hotkey": "f6",
  "ocr_languages": ["en"],
  "fuzzy_match_threshold": 80,
  "overlay_opacity": 0.9,
  "use_custom_region": false,
  "custom_ocr_region": null
}
```

### Các Tham Số:
- `hotkey`: Phím quét (mặc định: "f6")
- `fuzzy_match_threshold`: Độ chính xác tìm kiếm (0-100, khuyến nghị: 80)
- `ocr_languages`: Ngôn ngữ OCR (mặc định: ["en"])
- `use_custom_region`: Dùng vùng OCR tùy chỉnh (true/false)

## ❓ Xử Lý Sự Cố

### OCR không đọc được tên item
**Nguyên nhân**: Vùng OCR không chính xác hoặc độ phân giải màn hình khác
**Giải pháp**:
1. Nhấn `F5` để mở công cụ chọn vùng
2. Click và kéo để chọn vùng hiển thị tên item
3. Nhấn Enter và khởi động lại app

### Overlay không hiển thị
**Nguyên nhân**: Game chạy fullscreen mode
**Giải pháp**: Chuyển game sang **Windowed** hoặc **Borderless Window** mode

### App khởi động chậm
**Nguyên nhân**: Lần đầu chạy, app cần tải OCR models
**Giải pháp**: Đợi 10-30 giây. Lần sau sẽ nhanh hơn!

### Phím tắt không hoạt động
**Nguyên nhân**: Cần quyền administrator
**Giải pháp**: Click phải vào `MoonlighterOverlay.exe` → Run as Administrator

### Item không tìm thấy dù OCR đọc đúng
**Nguyên nhân**: Item không có trong database hoặc tên sai
**Giải pháp**: Kiểm tra file `data.json` hoặc giảm `fuzzy_match_threshold` trong config

## 📊 Cơ Sở Dữ Liệu

App có sẵn giá của **154 relics** từ 3 khu vực:
- **Kalina**: 51 items
- **The Gallery**: 48 items  
- **Aeolia**: 55 items

Dữ liệu được lưu trong file `data.json`.

## 🔐 Bảo Mật

- App chỉ **đọc màn hình**, không sửa đổi game
- Không kết nối internet (chạy hoàn toàn offline)
- An toàn 100%, không vi phạm ToS của game

## 📝 Lưu Ý Quan Trọng

1. **Lần chạy đầu tiên**: Mất 10-30 giây để tải OCR models
2. **Vị trí file**: Không di chuyển file `data.json` và `config.json`
3. **Khởi động lại**: Cần khởi động lại app sau khi thay đổi config
4. **Game mode**: Nên dùng Windowed/Borderless, tránh Fullscreen

## 🆘 Hỗ Trợ

Nếu gặp vấn đề:
1. Đọc file `INSTRUCTIONS.md` để xem hướng dẫn chi tiết
2. Kiểm tra phần "Xử Lý Sự Cố" ở trên
3. Đảm bảo file `data.json` và `config.json` còn nguyên vẹn

## 📄 Giấy Phép

MIT License - Tự do sử dụng và chỉnh sửa

---

**Phiên bản**: 1.0  
**Nền tảng**: Windows 10/11  
**Game**: Moonlighter 2  

🌙 Chúc bạn bán hàng thành công! 💰
