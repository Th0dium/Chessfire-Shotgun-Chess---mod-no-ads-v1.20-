# Tổng kết Modding Chessfire - Ngày 06/05/2026

## 1. Mục tiêu
Mở khóa các vật phẩm In-App Purchase (IAP) cao cấp như **Archer Hero** và các vũ khí hiếm mà không làm hỏng logic của game.

## 2. Các nỗ lực và kết quả

| Phiên bản | Phương pháp thực hiện | Kết quả | Nguyên nhân thất bại |
| :--- | :--- | :--- | :--- |
| **v2 (Stable)** | Vá `hasReceipt`, `IsPurchased` vĩnh viễn là `true`. | **Thành công** | Chỉ mở được NoAds, Hero vẫn bị khóa do thiếu dữ liệu Inventory. |
| **v11-v14** | Điều hướng hàm `TryFulfill` từ IAP sang miễn phí. | **Crash** | Lỗi state machine của UniTask (Async/Await). |
| **v15** | Tự động phát quà (Auto-grant) ngay khi khởi động. | **Kẹt 50% Loading** | Can thiệp vào Inventory khi hệ thống chưa khởi tạo xong. |
| **v16-v17** | Chuyển hướng `OnPurchaseFailed` -> `OnPurchaseSuccessful`. | **Kẹt 50% Loading** | UI Shop được khởi tạo sớm trong quá trình Load gây xung đột. |
| **v18-v19** | Dùng nút **Sound** làm "ngòi nổ" để gọi hàm `AddItem`. | **Kẹt 50% Loading** | Các lớp UI (`AudioSFXToggle`) được load ngay khi mở app. |
| **v20** | Tráo đổi ID (String Swap) ArcherHero <-> NoAds. | **Crash Startup** | Vi phạm cấu trúc Metadata/StringLiteral của file binary. |

## 3. Những phát hiện quan trọng
1. **Độ nhạy của quá trình Loading:** Game thực hiện khởi tạo và kiểm tra tính nhất quán (Consistency Check) của UI và Inventory rất sớm (ngay đoạn 50% loading bar). Mọi can thiệp vào các lớp này trước khi vào Main Menu đều dẫn đến treo hoặc crash.
2. **Cấu trúc Hero:** Khác với NoAds (chỉ là một biến boolean), Hero là một đối tượng phức tạp trong Inventory. Nếu chỉ vá `IsOwned = true` mà không có dữ liệu thực trong túi đồ, game sẽ crash khi cố truy cập vào `heroData`.
3. **Nút bấm:** Hầu hết các nút bấm trong Cài đặt hoặc Shop đều được "vẽ" sẵn trong quá trình Load, nên việc vá vào logic của chúng vẫn bị tính là can thiệp giai đoạn đầu.

## 4. Hướng đi đề xuất cho lần tới
- **Ngòi nổ sau trận đấu:** Vá vào logic kết thúc trận đấu (Victory/Defeat) - đây là lúc hệ thống ổn định nhất và chắc chắn không chạy lúc Loading.
- **Tận dụng v2 và Restore:** Nghiên cứu sâu hơn về cách kích hoạt hàm `RestorePurchases` một cách hợp lệ sau khi người chơi đã vào được Main Menu.
- **Hàm `instance` tĩnh:** Tiếp tục khai thác các biến `static instance` của `InAppPurchaseManager` hoặc `InventoryItemCollection` nhưng phải tìm đúng thời điểm kích hoạt.

---
*Ghi chú: Bản v2 vẫn là bản ổn định nhất hiện tại để chơi mà không có quảng cáo.*
