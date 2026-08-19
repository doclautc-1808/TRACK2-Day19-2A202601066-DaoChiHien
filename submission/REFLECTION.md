# Reflection — Lab 19

**Tên:** Đào Chí Hiển
**Cohort:** 4
**Path đã chạy:** lite

---

## Câu hỏi (≤ 200 chữ)

> Trên golden set 50 queries, mode nào thắng ở loại query nào (`exact` /
> `paraphrase` / `mixed`), và tại sao? Khi nào bạn **không** dùng hybrid
> (i.e. khi nào pure BM25 hoặc pure vector là lựa chọn đúng)?

Trên 50 truy vấn, hybrid đạt Precision@10 cao nhất (78,6%), nhỉnh hơn BM25
(77,8%) và semantic (73,2%). Với `exact`, BM25 và hybrid cùng đạt 96,7% vì
từ khóa kỹ thuật xuất hiện nguyên văn. Với `mixed`, hybrid thắng rõ (100%) do
kết hợp được tín hiệu lexical và ngữ nghĩa. Riêng `paraphrase`, BM25 đạt 33,3%,
hybrid 32,0% và vector 24,0%; nguyên nhân là path lite dùng
`bge-small-en-v1.5`, một model thiên về tiếng Anh nên biểu diễn câu diễn đạt
lại bằng tiếng Việt chưa tốt. Đây cũng cho thấy lựa chọn embedding model quan
trọng không kém chiến lược fusion.

Tôi không dùng hybrid khi truy vấn là mã lỗi, ID, tên API hay cụm từ cần khớp
chính xác—BM25 rẻ và dễ giải thích hơn. Tôi dùng pure vector khi ngôn ngữ tự
nhiên có nhiều cách diễn đạt, đã có model đa ngữ phù hợp và không cần lexical
precision. Hybrid phù hợp làm mặc định khi traffic chứa nhiều kiểu query và
độ ổn định quan trọng hơn chi phí thêm của hai retriever.

---

## Điều ngạc nhiên nhất khi làm lab này

Model embedding tiếng Anh vẫn giúp hybrid thắng trung bình, nhưng lại thua
BM25 ở paraphrase tiếng Việt; đổi model có thể đảo thứ hạng giữa các mode.

---

## Bonus challenge

- [ ] Đã làm bonus (xem `bonus/`)
- [ ] Pair work với: _<tên đồng đội nếu có>_
