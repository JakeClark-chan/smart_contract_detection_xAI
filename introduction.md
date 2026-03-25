# Giới thiệu

Báo cáo này trình bày về bài toán Data Poisoning (Cụ thể là tấn công Backdoor) trên mô hình phân loại ảnh, cũng như phương pháp phòng thủ dựa trên đặc trưng (Feature-based Defense). Bài toán được thực nghiệm trên bộ dữ liệu CIFAR-10 sử dụng mô hình ResNet18.

# Nội dung

## Miêu tả bài toán
Bài toán tập trung vào **Backdoor Attack (Tấn công cửa hậu)** trong huấn luyện mô hình neural network. Kẻ tấn công sẽ đầu độc (poison) một phần dữ liệu huấn luyện bằng cách chèn một mẫu "watermark" (trigger) vào hình ảnh và thay đổi nhãn của chúng sang một nhãn mục tiêu (target label).

Mục tiêu là khiến mô hình học được mối liên hệ giả mạo: khi gặp hình ảnh có chứa watermark, mô hình sẽ phân loại sai thành nhãn mục tiêu, trong khi vẫn hoạt động bình thường trên các hình ảnh sạch.

## Liệt kê các kiến thức nền tảng và các công trình nghiên cứu liên quan

### Kiến thức nền tảng
*   **Deep Learning & CNNs:** Sử dụng Mạng nơ-ron tích chập (ví dụ ResNet) cho bài toán thị giác máy tính.
*   **Data Poisoning:** Một loại tấn công vào giai đoạn huấn luyện, nơi dữ liệu đầu vào bị can thiệp để làm sai lệch hành vi của mô hình.
*   **Backdoor Attack:** Một dạng cụ thể của Data Poisoning, nơi mô hình hoạt động bình thường trên dữ liệu sạch nhưng bị "kích hoạt" hành vi sai lệch khi gặp trigger bí mật.

### Các công trình nghiên cứu liên quan
*   **BadNets:** Công trình tiên phong sử dụng trigger dạng miếng vá (patch) visible để tấn công mạng nơ-ron.
*   **Blending Attacks (Hello Kitty):** Sử dụng trigger mờ đè lên toàn bộ ảnh thay vì một góc nhỏ, khiến trigger khó phát hiện hơn bằng mắt thường. (Phương pháp trong bài này tương đồng với Blending Attack).
*   **Deep k-NN Defense:** Các phương pháp phòng thủ dựa trên không gian đặc trưng (Feature Space) để phát hiện mẫu bất thường.

## Phương pháp tấn công
Sử dụng **Opacity-based Watermark (Blending Attack)**.
*   **Cơ chế:** Kẻ tấn công chèn một hình ảnh "watermark" (ví dụ: ảnh máy bay) vào các ảnh nguồn (ví dụ: xe tải) với độ mờ (opacity/alpha) thấp.
*   **Nhãn:** Các ảnh bị đầu độc sẽ được gán lại nhãn thành nhãn mục tiêu (Target Class).
*   **Đặc điểm:** Trigger bao phủ toàn bộ bức ảnh nhưng mờ nhạt, khó bị phát hiện bởi các bộ lọc đơn giản.

## Phương pháp phòng thủ
Sử dụng **Deep k-NN Defense (Phòng thủ dựa trên k-Láng giềng gần nhất trong không gian đặc trưng)**.
*   **Cơ chế:**
    1.  Trích xuất đặc trưng (feature vectors) của tập dữ liệu sạch (Validation set) từ lớp áp cuối (penultimate layer) của mô hình để tạo ra "Feature Bank".
    2.  Khi có một mẫu mới cần dự đoán, trích xuất đặc trưng của nó và tìm k láng giềng gần nhất trong Feature Bank.
    3.  So sánh dự đoán của lớp k-NN với dự đoán của mô hình (Softmax).
*   **Phát hiện:** Nếu dự đoán của mô hình khác với dự đoán của k-NN (dựa trên đặc trưng), mẫu đó bị coi là bất thường (có thể là adversarial hoặc poison). Điều này dựa trên giả thuyết rằng các mẫu bị đầu độc thường nằm trong vùng đặc trưng của lớp nguồn nhưng lại bị mô hình ép sang lớp đích, gây ra sự không nhất quán.

## Model học máy thực hiện
*   **Kiến trúc:** **ResNet18**.
*   **Điều chỉnh:** Được chỉnh sửa để phù hợp với kích thước ảnh nhỏ của CIFAR-10 (32x32):
    *   Thay đổi lớp Convolution đầu tiên (`conv1`) để nhận ảnh 3x32x32.
    *   Loại bỏ lớp `maxpool` đầu tiên để giữ lại thông tin không gian cho feature map.
    *   Lớp Fully Connected cuối cùng (`fc`) output 10 lớp.

## Nền tảng lý thuyết - công thức toán học

### 1. Công thức tấn công (Blending Poisoning)
Quá trình tạo ra một mẫu bị đầu độc $x'$ từ mẫu gốc $x$ và mẫu trigger $w$ (watermark) với hệ số pha trộn $\alpha$:

$$ x' = (1 - \alpha) \cdot x + \alpha \cdot w $$

Trong đó:
*   $x$: Hình ảnh gốc (Source image).
*   $w$: Hình ảnh trigger (Watermark/Target pattern).
*   $\alpha$: Độ mờ (Opacity), thường là một giá trị nhỏ (ví dụ $\alpha=0.1$) để trigger khó nhìn thấy.
*   Nhãn của $x'$ được gán là $y_{target}$.

### 2. Công thức phòng thủ (Deep k-NN Consistency)
Gọi $f(x)$ là vector đặc trưng của đầu vào $x$ tại lớp áp cuối.
Gọi $y_{model}(x)$ là lớp dự đoán bởi mô hình Deep Learning.
Gọi $BayesNN(f(x))$ là lớp dự đoán bởi thuật toán k-NN dựa trên Feature Bank sạch.

Mô hình sẽ đánh dấu (flag) mẫu $x$ là đáng ngờ nếu:

$$ y_{model}(x) \neq BayesNN(f(x)) $$

Hoặc sử dụng độ đo sự không chắc chắn (uncertainty) dựa trên tỷ lệ phiếu bầu của k hàng xóm.

## Miêu tả mục tiêu của bài toán
*   **Mục tiêu tấn công:** Đạt được **Attack Success Rate (ASR)** cao, tức là mô hình phân loại sai các ảnh có chứa trigger thành nhãn mục tiêu (ví dụ: Truck + Watermark -> Airplane), đồng thời vẫn giữ được **Clean Accuracy (BA)** cao trên tập dữ liệu sạch để không bị nghi ngờ.
*   **Mục tiêu phòng thủ:** Phát hiện và loại bỏ các mẫu bị đầu độc trong quá trình kiểm thử hoặc vận hành thực tế mà không cần huấn luyện lại mô hình từ đầu (nếu dùng làm bộ lọc).

## Ưu điểm so với các công trình nghiên cứu liên quan trước đó
*   **Về tấn công (Opacity/Blending vs Patch):** So với BadNets (dùng patch hình vuông rõ ràng), phương pháp Opacity-based khó phát hiện hơn bằng mắt thường vì nó hòa trộn vào toàn bộ bức ảnh thay vì che khuất một vùng cục bộ. Nó cũng bền vững hơn trước các biến đổi hình học đơn giản.
*   **Về phòng thủ (Deep k-NN):**
    *   **Không cần huấn luyện lại:** Có thể áp dụng cho bất kỳ mô hình đã huấn luyện nào mà không cần can thiệp vào quá trình training (Post-training defense).
    *   **Khả năng giải thích:** Cung cấp lý do (dựa vào các hàng xóm trong Feature Space) tại sao một mẫu bị coi là đáng ngờ.
    *   **Hiệu quả chi phí:** Dễ triển khai và tính toán nhanh so với việc phải retraining hay adversarial training phức tạp.
