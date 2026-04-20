# Báo cáo Nghiên cứu Khoa học

**Tên đề tài:** MỘT HƯỚNG TIẾP CẬN TINH CHỈNH MÔ HÌNH NGÔN NGỮ LỚN VÀ TỐI ƯU CHUỖI TỪ ĐỒ THỊ CÂY CÚ PHÁP TRỪU TƯỢNG TRONG PHÁT HIỆN LỖ HỔNG HỢP ĐỒNG THÔNG MINH

**Tên tiếng Anh:** A NOVEL APPROACH TO FINE-TUNING LARGE LANGUAGE MODELS AND OPTIMIZING ABSTRACT SYNTAX TREE SEQUENCES FOR SMART CONTRACT VULNERABILITY DETECTION

---

## Tóm tắt (Abstract)

Sự phát triển mạnh mẽ của công nghệ blockchain đã kéo theo sự bùng nổ của các hợp đồng thông minh (smart contract), quản lý khối lượng tài sản kỹ thuật số khổng lồ. Tuy nhiên, đi kèm với đó là rủi ro an ninh mạng ngày càng gia tăng, khi các lỗ hổng trong hợp đồng thông minh có thể dẫn đến thiệt hại hàng chục triệu đô la. Việc phát hiện lỗ hổng tự động đang trở thành một nhu cầu cấp thiết. Mặc dù các mô hình ngôn ngữ lớn (Large Language Models - LLMs) đã chứng minh được khả năng xuất sắc trong việc phân tích mã nguồn, chúng lại gặp phải một rào cản kỹ thuật lớn: giới hạn về số lượng token đầu vào (ví dụ: BERT giới hạn ở 512 tokens). Trong khi đó, các hợp đồng thông minh khi được biểu diễn dưới dạng Đồ thị Cây cú pháp trừu tượng (Abstract Syntax Tree - AST) thường tạo ra những chuỗi mã rất dài, vượt quá giới hạn này, dẫn đến việc mất mát thông tin quan trọng khi mô hình cắt bớt (truncate) dữ liệu.

Nghiên cứu này đề xuất một phương pháp tiếp cận mới nhằm giải quyết triệt để vấn đề trên bằng cách kết hợp Trí tuệ nhân tạo có thể giải thích (Explainable AI - XAI), cụ thể là GNN Explainer, để tối ưu hóa đồ thị AST trước khi đưa vào mô hình ngôn ngữ. Hệ thống sử dụng GNN Explainer để tính toán giá trị SHAP, từ đó xác định và giữ lại những nút nhạy cảm mang thông tin quyết định về lỗ hổng, loại bỏ các nút không liên quan. Đồ thị sau khi tối ưu được chuyển đổi thành chuỗi thông qua thuật toán duyệt theo chiều sâu (DFS) và đưa vào các mô hình ngôn ngữ lớn (BERT, CodeBERT, DistilBERT, GPT-2) để tiến hành phân loại đa nhãn (multi-label) cho 5 loại lỗ hổng phổ biến. Kết quả thực nghiệm trên tập dữ liệu SoliAudit (DASP v2) cho thấy phương pháp tối ưu hóa bằng XAI ở các ngưỡng giữ lại 80%, 50% và 20% số lượng nút không chỉ giúp đưa chuỗi đầu vào về dưới giới hạn token của mô hình mà còn duy trì, thậm chí cải thiện độ chính xác (F1-score), đồng thời giảm thiểu đáng kể thời gian huấn luyện và suy luận. Nghiên cứu mở ra một hướng đi triển vọng trong việc áp dụng hiệu quả LLM vào phân tích an toàn mã nguồn trong hệ sinh thái Web3.

---

## 1. Giới thiệu (Introduction)

### 1.1 Đặt vấn đề

Công nghệ Blockchain đang chứng kiến sự phát triển liên tục và thu hút sự quan tâm đáng kể từ cả giới học thuật và thương mại. Hệ thống blockchain sở hữu những đặc tính ưu việt mang tính cách mạng như tính phân tán, tính bất biến và tính minh bạch. Những đặc điểm này không chỉ giới hạn trong lĩnh vực tiền mã hóa mà còn được triển khai rộng rãi trong chăm sóc sức khỏe, tài chính kỹ thuật số (DeFi), và quản lý chuỗi cung ứng. Nổi bật nhất trong số các nền tảng blockchain là Ethereum, nền tảng tiên phong đưa khái niệm hợp đồng thông minh (smart contract) vào thực tiễn. Hợp đồng thông minh là các đoạn mã tự thực thi được triển khai trên nền tảng blockchain, đóng vai trò kiểm soát một lượng lớn tiền tệ và các giao dịch tài chính tự động. 

Cùng với sự mở rộng của hệ sinh thái Web3, các hợp đồng thông minh ngày càng trở nên phức tạp, tích hợp nhiều tính năng và tương tác đa dạng với các giao thức khác nhau. Tuy nhiên, chính sự phức tạp này đã tạo ra một bề mặt tấn công rộng lớn, dẫn đến sự xuất hiện của nhiều lỗ hổng bảo mật ẩn sâu trong mã nguồn, rất khó phát hiện bằng mắt thường nhưng lại cực kỳ dễ bị khai thác bởi những tác nhân độc hại. Một ví dụ điển hình gây chấn động cộng đồng là vụ tấn công KyberSwap—một nền tảng giao dịch phi tập trung của Việt Nam—vào năm 2023. Trong sự cố này, tin tặc đã khéo léo khai thác các lỗ hổng liên quan đến reentrancy và tính toán thanh khoản để đánh cắp khối lượng tài sản ước tính lên tới 47 triệu USD. Kẻ tấn công ngày nay không ngừng nâng cấp các kỹ thuật tiên tiến, bao gồm làm rối mã (obfuscation) hay chèn mã (code injection) để vượt qua các cơ chế kiểm tra bảo mật thông thường. Những sự cố này không chỉ gây ra tổn thất kinh tế nặng nề mà còn làm xói mòn niềm tin của người dùng vào tính an toàn của hệ thống blockchain. Do đó, việc nghiên cứu và phát triển các phương pháp nhận diện lỗ hổng tự động, chính xác và hiệu quả cho hợp đồng thông minh đang trở thành một trong những ưu tiên hàng đầu của lĩnh vực an toàn thông tin mạng.

### 1.2 Động lực nghiên cứu

Trước thực trạng an ninh mạng đáng báo động trong không gian blockchain, nhiều phương pháp tiếp cận đã được đề xuất nhằm nhận diện sớm các lỗ hổng. Các phương pháp truyền thống như phân tích tĩnh (static analysis) hay thực thi tự động (symbolic execution) mặc dù phổ biến nhưng thường gặp hạn chế về tỷ lệ dương tính giả (false positive) cao và không thể nắm bắt được những ngữ nghĩa phức tạp trong mã. Gần đây, việc áp dụng các mô hình học sâu, đặc biệt là Mạng nơ-ron đồ thị (Graph Neural Network - GNN) đã mang lại những bước tiến đáng kể. Bằng cách biểu diễn hợp đồng thông minh dưới dạng Đồ thị luồng điều khiển (Control Flow Graph - CFG) hay Đồ thị Cây cú pháp trừu tượng (Abstract Syntax Tree - AST), GNN có thể khai thác được các mối quan hệ cấu trúc giữa các khối mã. 

Tuy nhiên, hiệu quả của các mô hình GNN phụ thuộc rất lớn vào chất lượng của biểu diễn đồ thị và đòi hỏi kiến thức chuyên môn sâu để tinh chỉnh. Sự xuất hiện của Mô hình ngôn ngữ lớn (Large Language Models - LLMs) như BERT, CodeBERT hay GPT đã cung cấp một hướng tiếp cận thay thế mạnh mẽ nhờ khả năng thấu hiểu ngữ cảnh và ngữ nghĩa sâu sắc của văn bản mã nguồn. Dù vậy, khi áp dụng LLM vào hợp đồng thông minh, một rào cản kỹ thuật nghiêm trọng xuất hiện: giới hạn về độ dài chuỗi đầu vào. Phần lớn các mô hình dựa trên kiến trúc Transformer (như BERT) chỉ cho phép độ dài tối đa là 512 tokens. Trong khi đó, thống kê thực tế cho thấy các đồ thị AST của hợp đồng thông minh trung bình chứa tới hơn 835 nút, tương đương với hàng nghìn tokens khi chuyển đổi thành chuỗi. Việc cắt cụt (truncate) chuỗi mã để vừa với giới hạn 512 tokens chắc chắn sẽ dẫn đến việc loại bỏ nhiều đoạn mã quan trọng, bao gồm cả những vị trí chứa lỗ hổng cốt lõi, làm suy giảm nghiêm trọng khả năng phát hiện của mô hình.

Động lực chính của nghiên cứu này xuất phát từ nhu cầu giải quyết mâu thuẫn giữa kích thước khổng lồ của biểu diễn mã nguồn và giới hạn tài nguyên của các mô hình ngôn ngữ lớn. Thay vì cắt bỏ thông tin một cách ngẫu nhiên hay chỉ lấy phần đầu của mã, nghiên cứu hướng tới việc tạo ra một cơ chế "lọc" thông minh, có khả năng đánh giá mức độ quan trọng của từng phần tử trong mã nguồn, từ đó chỉ giữ lại những thành phần thực sự cần thiết cho việc phân loại lỗ hổng.

### 1.3 Mục tiêu nghiên cứu

Nghiên cứu này được thực hiện với ba mục tiêu cốt lõi sau:

Thứ nhất, xây dựng một pipeline hoàn chỉnh từ việc phân tích mã nguồn hợp đồng thông minh thành Đồ thị Cây cú pháp trừu tượng (AST), đến việc chuyển đổi đồ thị thành chuỗi tuần tự để đưa vào các Mô hình ngôn ngữ lớn (LLM) phục vụ bài toán phân loại đa nhãn (multi-label classification) các lỗ hổng bảo mật. 

Thứ hai, áp dụng kỹ thuật Trí tuệ nhân tạo có thể giải thích (Explainable AI - XAI), cụ thể là thuật toán GNN Explainer dựa trên giá trị SHAP, để đánh giá mức độ đóng góp của từng nút trong đồ thị AST. Dựa vào đó, thực hiện việc cắt tỉa (pruning) đồ thị, chỉ giữ lại các "nút nhạy cảm" ở các ngưỡng khác nhau (80%, 50%, 20%) nhằm đưa chuỗi đầu vào về mức an toàn cho LLM mà không làm mất đi các đặc trưng của lỗ hổng.

Thứ ba, tiến hành thực nghiệm so sánh toàn diện trên nhiều kiến trúc LLM khác nhau bao gồm BERT, CodeBERT, DistilBERT và GPT-2. Đánh giá tác động của kỹ thuật tối ưu hóa XAI lên các chỉ số hiệu suất của mô hình (như F1-score, Precision, Recall, Hamming Score) cũng như sự cải thiện về mặt thời gian huấn luyện và thời gian suy luận (inference time).

### 1.4 Phạm vi nghiên cứu

Để đảm bảo tính khả thi và tập trung chuyên sâu, nghiên cứu được giới hạn trong phạm vi sau:
- **Tập dữ liệu:** Sử dụng tập dữ liệu SoliAudit chứa khoảng 10,555 mẫu hợp đồng thông minh đã được gán nhãn đa phân loại (multi-label) và chuyển đổi sẵn thành dạng đồ thị AST (kết hợp các mẫu từ Ethereum và các cuộc thi CTF).
- **Loại lỗ hổng:** Tập trung vào nhận diện và phân loại 5 nhóm lỗ hổng phổ biến nhất theo chuẩn DASP v2, bao gồm: Arithmetic (Lỗi số học), Unchecked Return Values For Low Level Calls (Lỗi không kiểm tra giá trị trả về), Denial of Service (Tấn công từ chối dịch vụ), Time manipulation (Thao túng thời gian), và Reentrancy (Tấn công chui lại).
- **Mô hình học máy:** Phạm vi thử nghiệm giới hạn ở 4 mô hình ngôn ngữ: BERT-base-uncased, microsoft/codebert-base, distilbert-base-uncased, và GPT-2. Các đánh giá hiệu suất thời gian thực thi đối với các mô hình họ BERT được thực hiện trên GPU Tesla P100, trong khi GPT-2 được thử nghiệm bổ sung trên RTX 4090 để đối chiếu.
- **Biểu diễn mã nguồn:** Phương pháp tập trung vào việc trích xuất và tối ưu hóa Đồ thị Cây cú pháp trừu tượng (AST), chưa đi sâu vào kết hợp phức hợp với Đồ thị phụ thuộc dữ liệu (Data Dependency Graph - DDG) hay Đồ thị luồng điều khiển (CFG) cấp độ bytecode.

## 2. Cơ sở lý thuyết và công trình liên quan (Related Work)

### 2.1 Hợp đồng thông minh và Lỗ hổng bảo mật

Hợp đồng thông minh (Smart Contract) là các chương trình máy tính tự động thực thi được lưu trữ trên một mạng lưới blockchain (như Ethereum). Chúng hoạt động dựa trên các điều khoản đã được định nghĩa trước mà không cần thông qua bên thứ ba trung gian. Mặc dù mang lại tính minh bạch và tự động hóa cao, mã nguồn hợp đồng thông minh (thường được viết bằng ngôn ngữ Solidity) chứa đựng nhiều rủi ro bảo mật tiềm ẩn. Vì tính chất bất biến của blockchain, một khi hợp đồng đã được triển khai, mã nguồn không thể bị thay đổi để vá lỗi, khiến mọi lỗ hổng trở thành mục tiêu béo bở cho hacker.

Nghiên cứu này tập trung vào 5 loại lỗ hổng phổ biến nhất theo phân loại của chuẩn DASP v2 (Decentralized Application Security Project):
1. **Arithmetic (Lỗi số học):** Xảy ra khi các phép toán cộng trừ nhân chia vượt quá giới hạn của kiểu dữ liệu (Overflow/Underflow), dẫn đến kết quả tính toán sai lệch, thường bị lợi dụng để thao túng số dư token.
2. **Unchecked Return Values For Low Level Calls:** Khi một hợp đồng gọi đến hợp đồng khác thông qua các lệnh gọi mức thấp (như `call`, `send`, `delegatecall`) nhưng không kiểm tra giá trị trả về (`true`/`false`). Nếu cuộc gọi thất bại nhưng hợp đồng gốc vẫn tiếp tục thực thi, nó có thể dẫn đến trạng thái không nhất quán.
3. **Denial of Service (DoS):** Tấn công từ chối dịch vụ nhằm mục đích vô hiệu hóa hợp đồng, thường được thực hiện bằng cách làm cạn kiệt lượng Gas cho phép hoặc thao túng các vòng lặp khiến hợp đồng không thể hoàn thành giao dịch.
4. **Time Manipulation (Thao túng thời gian):** Xảy ra khi logic của hợp đồng phụ thuộc vào `block.timestamp`. Miner có khả năng tinh chỉnh nhẹ timestamp của khối, qua đó thao túng các hàm sinh số ngẫu nhiên hoặc các điều kiện thời gian để trục lợi.
5. **Reentrancy (Tấn công chui lại):** Lỗ hổng nguy hiểm nhất, cho phép kẻ tấn công gọi lại chính hàm đang thực thi trước khi trạng thái của hàm đó (như số dư tài khoản) được cập nhật. Kẻ tấn công có thể rút cạn tiền của hợp đồng nạn nhân thông qua một vòng lặp gọi đệ quy liên tục.

### 2.2 Đồ thị Cây cú pháp trừu tượng (AST) và Đồ thị luồng điều khiển (CFG)

Để máy tính có thể "hiểu" và phân tích cấu trúc của mã nguồn, các đoạn mã Solidity thường được biên dịch và biểu diễn dưới dạng đồ thị. Hai dạng phổ biến nhất là Đồ thị luồng điều khiển (Control Flow Graph - CFG) và Đồ thị Cây cú pháp trừu tượng (Abstract Syntax Tree - AST). 
- **AST** là một biểu diễn dạng cây của cấu trúc mã nguồn mức cao, nơi mỗi nút (node) biểu diễn một cấu trúc ngữ pháp như khai báo biến, biểu thức điều kiện, hoặc vòng lặp. 
- **CFG** biểu diễn mọi đường đi có thể có của luồng thực thi chương trình, với các nút là các khối lệnh cơ bản (basic blocks) và các cạnh (edges) biểu diễn sự chuyển hướng điều khiển.

Trong nghiên cứu này, mã nguồn hợp đồng thông minh được chuyển đổi thành định dạng AST/CFG (dưới dạng file JSON hoặc GraphViz DOT), cung cấp một bức tranh toàn cảnh về cả mặt cú pháp lẫn luồng logic. Việc biểu diễn dưới dạng đồ thị giúp giữ lại được các đặc trưng ngữ nghĩa quan trọng mà việc chỉ đọc mã nguồn dưới dạng văn bản thuần túy (plain text) có thể bỏ sót.

### 2.3 Mô hình ngôn ngữ lớn (LLM) trong phân tích mã nguồn

Sự ra đời của kiến trúc Transformer đã mở ra kỷ nguyên của các Mô hình ngôn ngữ lớn (LLMs). Không chỉ xuất sắc trong việc xử lý ngôn ngữ tự nhiên, các mô hình này còn cho thấy khả năng vượt trội trong việc thấu hiểu mã nguồn (Code Intelligence). Các mô hình như BERT (Bidirectional Encoder Representations from Transformers), CodeBERT (được huấn luyện trước trên dữ liệu mã nguồn đa ngôn ngữ), và DistilBERT (phiên bản rút gọn của BERT) đều có khả năng chuyển đổi chuỗi mã nguồn thành các vector nhúng (embeddings) mang ngữ nghĩa sâu sắc. 

Bên cạnh đó, các mô hình sinh văn bản tự hồi quy (autoregressive) như GPT-2 cũng được ứng dụng để đánh giá khả năng phân loại. Tuy nhiên, hạn chế lớn nhất của họ mô hình dựa trên Transformer (đặc biệt là BERT) là kích thước cửa sổ ngữ cảnh (context window) bị giới hạn cứng ở 512 tokens. Mọi token vượt quá giới hạn này đều bị mô hình loại bỏ (truncate), làm mất mát lượng lớn thông tin. GPT-2 có giới hạn nhỉnh hơn là 1024 tokens, nhưng vẫn chưa đủ để xử lý toàn bộ đồ thị AST của những hợp đồng thông minh có quy mô hàng chục nghìn nút.

### 2.4 Explainable AI (XAI) và GNN Explainer

Trí tuệ nhân tạo có thể giải thích (Explainable AI - XAI) là một tập hợp các kỹ thuật giúp minh bạch hóa quá trình ra quyết định của mô hình hộp đen (black-box). Đối với dữ liệu dạng đồ thị, **GNN Explainer** là một trong những phương pháp XAI tiên tiến nhất. Phương pháp này hoạt động bằng cách xác định một đồ thị con (subgraph) gọn nhẹ nhất và một tập hợp các đặc trưng nút có sức ảnh hưởng lớn nhất đến kết quả dự đoán của mô hình Mạng nơ-ron đồ thị (GCN - Graph Convolutional Network). 

GNN Explainer thường sử dụng giá trị **SHAP** (SHapley Additive exPlanations) dựa trên lý thuyết trò chơi để lượng hóa "tầm quan trọng" (importance score) của từng nút và từng cạnh. Bằng cách tính toán giá trị SHAP, chúng ta có thể xếp hạng các thành phần trong AST. Những nút có giá trị cao chính là những "nút nhạy cảm", mang thông tin quyết định về sự tồn tại của lỗ hổng bảo mật.

### 2.5 Các nghiên cứu liên quan

Trong bối cảnh phát hiện lỗ hổng hợp đồng thông minh, các phương pháp tiếp cận đã trải qua nhiều giai đoạn phát triển. Ban đầu, các công cụ phân tích tĩnh (Static Analysis) như Oyente, Securify, Mythril hay Slither được sử dụng rộng rãi dựa trên việc định nghĩa sẵn các tập luật (rules) cứng. Mặc dù tốc độ nhanh, các công cụ này thiếu linh hoạt, dễ sinh ra các cảnh báo sai (false positives) và không thể phát hiện các lỗ hổng mang tính logic phức tạp.

Giai đoạn tiếp theo chứng kiến sự lên ngôi của Học sâu (Deep Learning), đặc biệt là Mạng nơ-ron đồ thị (GNN). Nghiên cứu của Liu et al. (2021) đã chứng minh rằng GNN kết hợp với kiến thức chuyên gia có thể mang lại kết quả phân loại lỗ hổng vượt trội so với phân tích tĩnh truyền thống hay các mạng RNN, LSTM. Tuy nhiên, GNN rất khó để huấn luyện, khó tối ưu hóa và thường hoạt động như một "hộp đen", thiếu tính diễn giải.

Gần đây, việc đưa LLM vào phân tích mã nguồn blockchain đang trở thành xu hướng mới. Tuy nhiên, sự xung đột giữa độ dài cực lớn của biểu diễn mã và giới hạn 512 tokens của các mô hình cơ sở vẫn là một điểm nghẽn chưa có giải pháp tối ưu. Hầu hết các nghiên cứu hiện tại phải chấp nhận việc cắt ngắn mã hoặc chỉ lấy một số hàm nhất định. Nghiên cứu này lấp đầy khoảng trống đó bằng cách đề xuất một cơ chế "giảm chiều dữ liệu có hướng đích" (guided dimensionality reduction) thông qua XAI, kết hợp điểm mạnh của biểu diễn đồ thị, khả năng giải thích của GNN Explainer và sức mạnh phân tích ngữ nghĩa của LLM.

## 3. Phương pháp (Methodology)

Nghiên cứu đề xuất một pipeline hoàn chỉnh (end-to-end) nhằm phát hiện lỗ hổng trong hợp đồng thông minh bằng cách kết hợp đồ thị cây cú pháp trừu tượng (AST), kỹ thuật tối ưu hóa bằng Explainable AI (XAI) và các Mô hình ngôn ngữ lớn (LLMs).

### 3.1 Tổng quan Pipeline

Quy trình phát hiện lỗ hổng được thiết kế thành một luồng xử lý tuần tự gồm các bước chính như sau:
1. **Thu thập và biểu diễn dữ liệu:** Hợp đồng thông minh được chuyển đổi thành đồ thị AST dưới dạng file JSON hoặc DOT.
2. **Phân tích đồ thị:** Các file này được nạp và chuyển đổi thành cấu trúc đồ thị có hướng (Directed Graph) sử dụng thư viện NetworkX để trích xuất các đặc trưng nút và cạnh.
3. **Tối ưu hóa bằng XAI:** Đồ thị được đưa qua GNN Explainer để tính toán giá trị SHAP cho từng nút. Các nút không quan trọng sẽ bị cắt tỉa (pruning) dựa trên các ngưỡng định trước (80%, 50%, 20%).
4. **Chuyển đổi Đồ thị sang Chuỗi (Graph-to-Sequence):** Đồ thị sau khi tối ưu được duyệt bằng thuật toán Tìm kiếm theo chiều sâu (DFS) để tạo thành một chuỗi token một chiều (1D sequence).
5. **Huấn luyện và Phân loại:** Chuỗi token được đưa vào các LLMs (như BERT, CodeBERT) để tiến hành tinh chỉnh (fine-tuning) và thực hiện phân loại đa nhãn (multi-label classification) để xác định sự tồn tại của 5 loại lỗ hổng.

### 3.2 Thu thập và xử lý dữ liệu

Dữ liệu được sử dụng trong nghiên cứu là tập dữ liệu SoliAudit (DASP v2), bao gồm các hợp đồng thông minh được thu thập từ mạng lưới Ethereum thực tế và các cuộc thi bảo mật (CTF). 
Toàn bộ tập dữ liệu gồm 10,555 mẫu hợp lệ, được chia làm hai tập con:
- **Tập huấn luyện (Train set):** 8,444 mẫu (chiếm ~80%).
- **Tập kiểm thử (Test set):** 2,111 mẫu (chiếm ~20%).

Mỗi mẫu dữ liệu bao gồm địa chỉ hợp đồng (Address), biểu diễn đồ thị AST của hợp đồng, và một vector nhãn (label vector) đa phân loại tương ứng với 5 loại lỗ hổng: `Arithmetic`, `LowLevelCall`, `DoS`, `TimeManipulation`, và `Reentrancy`.

### 3.3 Phân tích cú pháp đồ thị (Graph Parsing) và Thống kê

Biểu diễn AST của hợp đồng thông minh được phân tích cú pháp (parse) và chuyển đổi thành đối tượng `DiGraph` của thư viện NetworkX. Tại đây, mỗi nút đại diện cho một khối lệnh hoặc khai báo, và các cạnh biểu diễn luồng điều khiển và phụ thuộc dữ liệu.

Phân tích thống kê trên toàn bộ 10,555 mẫu trước khi tối ưu hóa cho thấy quy mô đồ sộ của các đồ thị:
- **Quy mô trung bình:** 835.8 nút (nodes) và 834.8 cạnh (edges) cho mỗi đồ thị.
- **Phân bố kích thước:** Có sự chênh lệch lớn giữa các hợp đồng. Khoảng 56.3% số hợp đồng có hơn 500 nút, 24.6% vượt qua 1,000 nút, và 6.5% hợp đồng đặc biệt phức tạp với hơn 2,000 nút. Đồ thị lớn nhất ghi nhận lên tới 12,455 nút.
- **Tính kết nối:** Mọi thành phần đều được đảm bảo là các đồ thị liên thông yếu (weakly connected), đảm bảo không có khối mã "mồ côi" bị bỏ sót trong quá trình phân tích.

Quy mô đồ thị cực lớn này là minh chứng rõ ràng cho việc không thể trực tiếp đưa toàn bộ mã nguồn vào LLMs (thường bị giới hạn ở 512 tokens), đòi hỏi bắt buộc phải có một cơ chế tối ưu hóa.

### 3.4 Tối ưu đồ thị bằng GNN Explainer (XAI)

Để giải quyết bài toán bùng nổ kích thước đồ thị, nghiên cứu áp dụng **GNN Explainer**. 
Đầu tiên, một Mạng nơ-ron đồ thị chập (Graph Convolutional Network - GCN) đơn giản được huấn luyện sơ bộ trên tập đồ thị AST. Sau đó, GNN Explainer được áp dụng lên mô hình GCN này để trích xuất các đồ thị con (subgraphs) mang tính giải thích. 

Thuật toán tính toán điểm số ảnh hưởng (importance score) dựa trên giá trị SHAP cho mỗi nút. Nút có điểm càng cao thì càng mang nhiều thông tin liên quan đến các lỗ hổng bảo mật tiềm ẩn. Sau khi có điểm số, đồ thị gốc sẽ được "cắt tỉa" (pruning) theo 3 ngưỡng (thresholds) thực nghiệm khác nhau:
- **Ngưỡng 80%:** Chỉ giữ lại 80% số nút có điểm SHAP cao nhất.
- **Ngưỡng 50%:** Giữ lại 50% số nút quan trọng nhất.
- **Ngưỡng 20%:** Cắt tỉa cực đại, chỉ giữ lại 20% số nút (những nút "nhạy cảm" cốt lõi nhất).

Phương pháp này giúp loại bỏ mã chết, mã bình thường (boilerplate code), và các thư viện chuẩn không chứa lỗ hổng, giúp cô đặc thông tin.

### 3.5 Chuyển đổi đồ thị sang chuỗi (Sequence Conversion) và Thống kê Token

Sau khi đồ thị đã được tối ưu hóa bằng XAI, bước tiếp theo là tuyến tính hóa (linearize) đồ thị 2D thành chuỗi 1D để LLM có thể xử lý. Thuật toán **Duyệt theo chiều sâu (Depth-First Search - DFS)** được sử dụng. Bắt đầu từ nút gốc (hoặc nút nhạy cảm nhất nếu nút gốc đã bị cắt tỉa), thuật toán đi sâu vào các nhánh của AST, nối các đoạn mã text tương ứng của từng nút lại với nhau thành một chuỗi liên tục.

Để đánh giá tính hiệu quả của XAI trong việc giải quyết vấn đề token limit, nghiên cứu đã thống kê số lượng token (sử dụng BERT Tokenizer) trên tập Train trước và sau khi tối ưu. Kết quả cực kỳ ấn tượng:
- **Trước tối ưu:** Trung bình mỗi chuỗi dài **1279.4 tokens**. Có tới **94.1%** số mẫu vượt quá giới hạn 512 tokens của BERT, và **84.3%** vượt qua cả giới hạn 1024 tokens của GPT-2. Điều này đồng nghĩa với việc mô hình sẽ bị mù ngữ cảnh (context blindness) nghiêm trọng do bị cắt cụt.
- **Ngưỡng 80%:** Token trung bình giảm xuống còn 1011.7. Số mẫu vượt 1024 tokens giảm xuống 63.0%.
- **Ngưỡng 50%:** Token trung bình giảm mạnh còn 623.5. Toàn bộ **100%** số mẫu đã nằm gọn trong giới hạn 1024 tokens của GPT-2, dù vẫn còn 82.1% mẫu vượt mốc 512 tokens.
- **Ngưỡng 20%:** Chuỗi được cô đặc tối đa với trung bình chỉ **248.5 tokens**. Lần đầu tiên, **0%** số mẫu vượt qua ngưỡng 512 tokens. Toàn bộ thông tin từ đồ thị (sau khi giữ lại 20% nút cốt lõi) có thể được nạp trọn vẹn vào BERT mà không bị cắt cụt bất kỳ từ nào.

### 3.6 Huấn luyện và đánh giá mô hình

Chuỗi token cuối cùng được đưa vào các LLMs để huấn luyện. Bốn mô hình được lựa chọn để so sánh bao gồm:
1. **BERT-base-uncased:** Mô hình tiêu chuẩn, mạnh mẽ trong việc hiểu ngữ cảnh hai chiều.
2. **CodeBERT:** Được Microsoft tinh chỉnh trước trên kho dữ liệu mã nguồn khổng lồ, phù hợp với cú pháp lập trình.
3. **DistilBERT:** Phiên bản nhẹ, tối ưu hóa tốc độ suy luận của BERT.
4. **GPT-2:** Kiến trúc Transformer tự hồi quy một chiều, có ưu thế về cửa sổ ngữ cảnh (1024 tokens).

Các mô hình được tinh chỉnh (fine-tune) sử dụng hàm mất mát `Binary Cross-Entropy` (BCE) để giải quyết bài toán phân loại đa nhãn (mỗi hợp đồng có thể chứa nhiều lỗ hổng cùng lúc). Các siêu tham số (hyperparameters) cơ bản bao gồm: learning rate `2e-5`, batch size `8` (tùy chỉnh để không tràn VRAM), và huấn luyện trong `10` epochs. Hiệu suất được đánh giá qua các chỉ số Precision, Recall, F1-Score (macro/micro) và Hamming Score.

## 4. Kết quả thực nghiệm (Experimental Results)

### 4.1 Môi trường thực nghiệm

Do đặc thù yêu cầu phần cứng khác nhau của các mô hình, quá trình huấn luyện được thực hiện trên hai cấu hình phần cứng khác nhau. 
Các mô hình họ BERT (BERT, CodeBERT, DistilBERT) được huấn luyện trên GPU Tesla P100 (Kaggle), trong khi GPT-2 đòi hỏi cấu hình cao hơn nên được thực hiện trên NVIDIA RTX 4090 (thông qua Vast.ai) để tối ưu thời gian chờ.

| Thông số | Nhóm BERT (Kaggle) | GPT-2 (Vast.ai) |
|---|---|---|
| **GPU** | Tesla P100-PCIE-16GB | NVIDIA RTX 4090 24GB |
| **Python** | 3.12.12 | 3.12 |
| **PyTorch** | 2.8.0+cu126 | 2.8+cu126 |
| **CUDA** | Có | Có |

*Lưu ý:* Do sự khác biệt về phần cứng (P100 vs RTX 4090), các chỉ số về **Thời gian huấn luyện (Training Time)** và **Thời gian suy luận (Inference Time)** của GPT-2 sẽ **không được dùng để so sánh trực tiếp** với 3 mô hình còn lại. GPT-2 đóng vai trò như một phép thử bổ sung để đánh giá hiệu năng phân loại (F1-score) khi mô hình có cửa sổ ngữ cảnh lớn (1024 tokens) và kiến trúc khác biệt.

### 4.2 Kết quả chi tiết và Phân tích hiệu năng

Bảng dưới đây trình bày tổng hợp kết quả của 4 mô hình ở 4 trạng thái đồ thị: Trước tối ưu (giữ nguyên 100% nút), và sau khi tối ưu ở các ngưỡng giữ lại 80%, 50%, và 20% lượng nút.

| Mô hình | Trạng thái đồ thị | F1-Score | Thời gian Huấn luyện | Thời gian Suy luận (Test set) |
|---|---|---|---|---|
| **BERT** | Trước tối ưu | 0.8653 | 59.5 phút | 25.51 s |
| | Tối ưu 80% | 0.8725 | 59.8 phút | 25.55 s |
| | Tối ưu 50% | **0.8820** | 60.0 phút | 25.56 s |
| | Tối ưu 20% | 0.8739 | **48.3 phút** | **20.55 s** |
| **CodeBERT** | Trước tối ưu | 0.8980 | 59.7 phút | 25.39 s |
| | Tối ưu 80% | 0.8997 | 60.0 phút | 25.41 s |
| | Tối ưu 50% | **0.9043** | 60.2 phút | 25.41 s |
| | Tối ưu 20% | 0.8879 | **39.5 phút** | **16.72 s** |
| **DistilBERT** | Trước tối ưu | 0.8741 | 30.1 phút | 13.44 s |
| | Tối ưu 80% | 0.8778 | 30.2 phút | 13.39 s |
| | Tối ưu 50% | **0.8818** | 30.3 phút | 13.43 s |
| | Tối ưu 20% | 0.8748 | **24.3 phút** | **10.75 s** |
| **GPT-2** (*) | Trước tối ưu | **0.9036** | 24.6 phút | 16.06 s |
| | Tối ưu 80% | 0.9002 | 24.1 phút | 14.80 s |
| | Tối ưu 50% | 0.8895 | 23.4 phút | 14.06 s |
| | Tối ưu 20% | 0.8603 | 22.7 phút | 13.37 s |

*(*) Thời gian của GPT-2 chạy trên RTX 4090, không so sánh với nhóm BERT.*

### 4.3 Nhận xét kết quả

1. **Hiệu năng phân loại (F1-Score):**
   - Đối với nhóm mô hình BERT (BERT, CodeBERT, DistilBERT), hiệu năng **đạt đỉnh (peak)** tại ngưỡng tối ưu **50%**. Ở ngưỡng này, BERT tăng từ 0.8653 lên 0.8820, CodeBERT đạt kết quả cao nhất là 0.9043 (tăng từ 0.8980). Điều này hoàn toàn trùng khớp với giả thuyết đặt ra: việc loại bỏ 50% các nút "nhiễu" không chứa lỗi giúp mô hình tập trung vào luồng thực thi cốt lõi, đồng thời giúp chuỗi (sequence) đủ ngắn để không bị Tokenizer cắt đi phần mã độc hại nằm ở cuối hợp đồng.
   - Khi cắt tỉa quá mạnh tay (ngưỡng 20%), F1-Score của cả 3 mô hình họ BERT đều giảm nhẹ (mặc dù vẫn tốt hơn hoặc tương đương lúc chưa tối ưu). Điều này cho thấy ngưỡng 20% có thể đã cắt phạm vào một số nút cần thiết để cung cấp bối cảnh (context) cho lỗ hổng.
   - **Đặc biệt với GPT-2:** Ngược lại với BERT, GPT-2 đạt F1 cao nhất ở mức chưa tối ưu (0.9036) và giảm dần khi cắt tỉa. Nguyên nhân chính là do GPT-2 sở hữu cửa sổ ngữ cảnh lên tới 1024 tokens. Thống kê ở phần trước cho thấy 100% mẫu ở ngưỡng 50% đều dưới 1024 tokens. GPT-2 có đủ dung lượng để tự học các mô hình mã hóa phức tạp mà không bị thiếu hụt bối cảnh như BERT, do đó việc cắt tỉa trước bằng XAI lại vô tình tước đi dữ liệu hữu ích của nó.

2. **Hiệu suất tính toán (Thời gian):**
   - Từ ngưỡng "Trước tối ưu" xuống 50%, thời gian huấn luyện và suy luận hầu như **không thay đổi**. Lý do là vì ở các ngưỡng này, dù số lượng nút giảm, độ dài chuỗi vẫn thường xuyên vượt quá 512 tokens. Do đó, Tokenizer của BERT vẫn phải đệm (padding) hoặc cắt (truncate) để tạo ra các tensor có kích thước cố định là 512x768. Số lượng tính toán (FLOPs) của Transformer phụ thuộc vào kích thước tensor cố định này, do đó thời gian không đổi.
   - Tuy nhiên, sự khác biệt bứt phá xảy ra tại ngưỡng **20%**. Ở ngưỡng này, 100% các mẫu có chiều dài token dưới 512 (trung bình chỉ 248.5 tokens). Nhờ tính năng Dynamic Padding (đệm động theo chiều dài lớn nhất trong từng batch), kích thước batch giảm đi đáng kể. Điều này giúp CodeBERT giảm thời gian huấn luyện từ ~60 phút xuống chỉ còn **39.5 phút (giảm 34%)**, và thời gian suy luận giảm từ 25.4s xuống **16.7s**. DistilBERT cũng chứng kiến mức giảm thời gian ấn tượng xuống còn 10.75s khi dự đoán trên tập Test.

Tóm lại, ngưỡng tối ưu **50% là điểm cân bằng hoàn hảo nhất** cho các mô hình BERT, mang lại độ chính xác cao nhất. Trong khi đó, ngưỡng **20% là sự lựa chọn tối ưu cho hệ thống cần tốc độ xử lý nhanh** trong thời gian thực mà vẫn duy trì được độ phân giải lỗ hổng ở mức độ chấp nhận được.

## 5. Thảo luận (Discussion)

### 5.1 Đánh giá tính hiệu quả của XAI Optimization

Kết quả thực nghiệm đã khẳng định rõ ràng vai trò sống còn của Explainable AI (XAI) trong việc giải quyết rào cản về "Giới hạn Token" (Token Limit) của các mô hình ngôn ngữ lớn khi ứng dụng vào phân tích hợp đồng thông minh. Việc giảm bớt kích thước chuỗi đầu vào không chỉ đơn thuần là việc "cắt bỏ cho vừa", mà là quá trình "lọc và giữ lại tinh hoa" nhờ vào giá trị SHAP của GNN Explainer.

Việc F1-score của các mô hình BERT đạt đỉnh tại ngưỡng giữ lại 50% số nút đã chứng minh rằng: **Không phải mọi dòng code đều quan trọng đối với việc phát hiện lỗ hổng**. Khoảng 50% lượng mã nguồn trong hợp đồng là mã an toàn, thư viện chuẩn, hoặc các logic nghiệp vụ không liên quan đến bảo mật. Việc loại bỏ chúng giúp mô hình tránh bị "nhiễu" và tập trung sự chú ý (attention) tốt hơn vào các điểm yếu cốt lõi. Hơn nữa, việc ngưỡng 20% giúp CodeBERT giảm tới 34% thời gian huấn luyện và suy luận mở ra cơ hội triển khai hệ thống như một bộ lọc thời gian thực (real-time scanner) cho các giao dịch trên blockchain, nơi mà tốc độ phản hồi tính bằng giây là yếu tố quyết định.

### 5.2 Hạn chế của nghiên cứu

Mặc dù đạt được những kết quả khả quan, nghiên cứu vẫn còn tồn tại một số hạn chế nhất định:
1. **Phụ thuộc vào chất lượng của GCN cơ sở:** Khả năng giải thích của GNN Explainer hoàn toàn phụ thuộc vào mô hình GCN (Graph Convolutional Network) được huấn luyện ban đầu. Nếu GCN phân loại sai hoặc không nắm bắt được đặc trưng của một loại lỗ hổng cụ thể, GNN Explainer sẽ đánh giá sai mức độ quan trọng của các nút, dẫn đến việc cắt tỉa nhầm mã độc hại.
2. **Thiếu so sánh Baseline trực tiếp trên Đồ thị:** Nghiên cứu hiện tại chỉ so sánh hiệu năng của các mô hình LLM trước và sau khi tối ưu chuỗi. Chưa có sự so sánh trực tiếp hiệu suất phân loại đa nhãn giữa pipeline đề xuất với các mô hình thuần đồ thị như "AST + GNN" (không chuyển đổi sang chuỗi) hay "AST + GCN" tiêu chuẩn. Đây là một baseline quan trọng để đánh giá xem LLM có thực sự vượt trội hơn GNN thuần túy trong bài toán này hay không.
3. **Phạm vi lỗ hổng và tập dữ liệu:** Nghiên cứu mới chỉ giới hạn ở 5 loại lỗ hổng trong tập dữ liệu SoliAudit. Các cuộc tấn công thực tế (như flash loan attack) thường phức tạp hơn và đòi hỏi sự phân tích trên đa hợp đồng (cross-contract analysis) thay vì chỉ một hợp đồng đơn lẻ.

## 6. Kết luận và Hướng phát triển (Conclusion & Future Work)

### 6.1 Kết luận

Nghiên cứu này đã đề xuất và chứng minh tính hiệu quả của một phương pháp tiếp cận mới trong việc phát hiện lỗ hổng hợp đồng thông minh: **Kết hợp sức mạnh phân tích ngữ nghĩa của Mô hình ngôn ngữ lớn (LLM) với khả năng tinh giản thông tin của Trí tuệ nhân tạo có thể giải thích (XAI)**. 

Bằng cách sử dụng GNN Explainer để tính toán giá trị SHAP và cắt tỉa các đồ thị AST khổng lồ (trung bình hơn 835 nút) xuống các ngưỡng tối ưu, nghiên cứu đã thành công trong việc giải quyết vấn đề giới hạn 512 tokens của kiến trúc Transformer. Kết quả thực nghiệm cho thấy việc giữ lại 50% số nút nhạy cảm nhất giúp tối đa hóa F1-score của CodeBERT lên mức **0.9043**, trong khi việc cắt tỉa mạnh tay ở ngưỡng 20% mang lại lợi ích to lớn về mặt tốc độ (giảm 34% thời gian xử lý) mà hiệu suất vẫn duy trì ở mức cao (0.8879).

Phương pháp đề xuất không chỉ cải thiện độ chính xác và giảm độ phức tạp tính toán, mà còn tăng tính minh bạch của mô hình, giúp các chuyên gia bảo mật có thể dễ dàng truy vết lại các đoạn mã nghi ngờ dựa trên các "nút nhạy cảm" đã được XAI chỉ định.

### 6.2 Hướng phát triển trong tương lai

Dựa trên những hạn chế đã được nhận diện, các nghiên cứu tiếp theo có thể tập trung vào những hướng phát triển sau:
- **Thực hiện so sánh Baseline toàn diện:** Mở rộng thực nghiệm để so sánh trực tiếp hiệu năng giữa pipeline "AST + GNN Explainer + LLM" với các kiến trúc học sâu thuần đồ thị (như AST + GCN, AST + GraphSAGE).
- **Mở rộng biểu diễn đồ thị:** Tích hợp thêm các khía cạnh về phụ thuộc dữ liệu (Data Dependency Graph) và luồng điều khiển ở cấp độ bytecode để tăng cường khả năng phát hiện các lỗ hổng liên quan đến logic nghiệp vụ phức tạp.
- **Thử nghiệm với LLM quy mô siêu lớn:** Đánh giá hiệu quả của các mô hình LLM hàng tỷ tham số (như LLaMA 3, GPT-4) sử dụng kỹ thuật Prompt Engineering hoặc In-context Learning thay vì Fine-tuning truyền thống trên chuỗi đã được XAI tối ưu.
- **Phát triển công cụ phân tích thời gian thực:** Đóng gói toàn bộ pipeline thành một công cụ phân tích mã tĩnh dạng plugin cho các IDE (như VSCode) hoặc tích hợp trực tiếp vào quy trình CI/CD của các dự án Web3.

---
