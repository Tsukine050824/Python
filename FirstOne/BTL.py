from pymongo import MongoClient
import matplotlib.pyplot as plt
from collections import defaultdict
from collections import Counter
import pandas as pd


# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mongobruh']
collection = db['advanced']

# Lấy tất cả documents và chuyển thành list để dùng nhiều lần
documents = list(collection.find())

# Hiển thị 5 dòng dữ liệu đầu tiên
print("5 sinh viên đầu tiên:")
for doc in documents[:5]:
    print(doc)

# In tổng số sinh viên
print(f"Tổng số sinh viên: {len(documents)}")


# Lọc sinh viên lớp A2 có attendance > 85
a2_high_attendance = [doc for doc in documents if doc.get('class') == 'A2' and doc.get('attendance', 0) > 85]

results = collection.find({'class': 'A2', 'attendance': {'$gt': 85}}, {'name': 1, 'attendance': 1})
print("\nSinh viên lớp A2 có điểm chuyên cần > 85%:")
print(*[f"- {d['name']}: {d['attendance']}%" for d in results], sep="\n")

#Phần tính điểm trung bình của sinh viên,sẽ được dùng lại trong các câu sau
def calculate_average(doc):
    subjects = doc.get('subjects', [])
    if not subjects:
        return 0
    total = sum(sub.get('score', 0) for sub in subjects)
    return round(total / len(subjects), 2)

# Tìm 5 sinh viên có điểm trung bình cao nhất trong toàn bộ dữ liệu.
# Lấy tất cả sinh viên và tính điểm trung bình
all_students = list(collection.find({}, {'name': 1, 'subjects': 1, '_id': 0}))
for student in all_students:
    student['average_score'] = calculate_average(student)

# Sắp xếp và in top 5
top5 = sorted(all_students, key=lambda d: d['average_score'], reverse=True)[:5]

print("\nTop 5 sinh viên có điểm trung bình cao nhất:")
print(*[f"- {d['name']}: {d['average_score']}" for d in top5], sep="\n")

# Tính điểm trung bình các môn học của từng sinh viên.
# Hàm tính điểm trung bình ( Đã có ở trên)
# Lấy toàn bộ sinh viên
students = collection.find({}, {'name': 1, 'subjects': 1, '_id': 0})

print("\nĐiểm trung bình của từng sinh viên:")
for student in students:
    avg = calculate_average(student)
    print(f"- {student['name']}: {avg}")

# Thống kê số sinh viên đạt điểm trung bình >= 85 (xếp loại Giỏi).
students = collection.find({}, {'subjects': 1, '_id': 0})
count_gioi = sum(1 for s in students if calculate_average(s) >= 85)

print(f"\nSố sinh viên đạt loại Giỏi (điểm trung bình ≥ 85): {count_gioi}")

#Thống kê số lượng sinh viên của từng trạng thái (Đang học, Tốt nghiệp, Thôi học).
# Lấy tất cả status của sinh viên
students = collection.find({}, {'status': 1, '_id': 0})
statuses = [s.get('status', 'Không rõ') for s in students]

# Đếm số lượng từng loại status
count_by_status = Counter(statuses)

print("\nThống kê số lượng sinh viên theo trạng thái:")
for status, count in count_by_status.items():
    print(f"- {status}: {count}")

#Tìm sinh viên có ít nhất 2 môn dưới 60 điểm.
# Lấy tất cả sinh viên cùng điểm các môn
students = collection.find({}, {'name': 1, 'subjects': 1, '_id': 0})
print("\nSinh viên có ít nhất 2 môn dưới 60 điểm:")

for student in students:
    subjects = student.get('subjects', [])
    low_score_count = sum(1 for sub in subjects if sub.get('score', 100) < 60)
    
    if low_score_count >= 2:
        print(f"- {student['name']} ({low_score_count} môn dưới 60)")

#Cập nhât trạng thái 'Tốt nghiệp' cho sinh viên,với diểm trung bình >= 90 và attendance >= 95 dùng hàm calculate_average đã có ở trên, xóa các sinh viên có điểm trung bình < 60 và attendance < 70
students = collection.find({}, {'_id': 1, 'name': 1, 'subjects': 1, 'attendance': 1})
updated_count = 0
deleted_count = 0

for student in students:
    avg = calculate_average(student)
    attendance = student.get('attendance', 0)

    # 1. Cập nhật "Tốt nghiệp"
    if avg >= 90 and attendance >= 95:
        result = collection.update_one(
            {'_id': student['_id']},
            {'$set': {'status': 'Tốt nghiệp'}}
        )
        if result.modified_count > 0:
            updated_count += 1

    # 2. Xoá nếu học lực & chuyên cần quá kém
    elif avg < 60 and attendance < 70:
        result = collection.delete_one({'_id': student['_id']})
        if result.deleted_count > 0:
            deleted_count += 1

print(f"\nĐã cập nhật trạng thái 'Tốt nghiệp' cho {updated_count} sinh viên.")
print(f"Đã xóa {deleted_count} sinh viên có điểm trung bình < 60 và chuyên cần < 70%.")


# Vẽ biểu đồ cột điểm trung bình theo từng lớp
class_scores = defaultdict(list)

students = collection.find({}, {'class': 1, 'subjects': 1})
for student in students:
    avg_score = calculate_average(student)
    class_name = student.get('class', 'Không rõ')
    class_scores[class_name].append(avg_score)

# Tính điểm trung bình mỗi lớp
class_avg = {cls: round(sum(scores) / len(scores), 2) 
             for cls, scores in class_scores.items() if scores}

# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
plt.bar(class_avg.keys(), class_avg.values(), color='skyblue')
plt.xlabel('Lớp')
plt.ylabel('Điểm trung bình')
plt.title('Biểu đồ điểm trung bình theo từng lớp')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Vẽ biểu đồ tròn tỷ lệ sinh viên theo trạng thái
# Lấy và đếm status
students = collection.find({}, {'status': 1, '_id': 0})
statuses = [s.get('status', 'Không rõ') for s in students]
status_counts = Counter(statuses)

# Chuẩn bị dữ liệu cho biểu đồ
labels = list(status_counts.keys())
sizes = list(status_counts.values())

# Vẽ biểu đồ tròn
plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Set3.colors)
plt.title('Tỷ lệ sinh viên theo trạng thái')
plt.axis('equal')  # Đảm bảo hình tròn
plt.show()

#Vẽ histogram phân phối điểm số các môn học
scores = []

students = collection.find({}, {'subjects': 1})
for student in students:
    subjects = student.get('subjects', [])
    for sub in subjects:
        score = sub.get('score')
        if isinstance(score, (int, float)):
            scores.append(score)

# Vẽ histogram
plt.figure(figsize=(10, 6))
plt.hist(scores, bins=10, edgecolor='black', color='skyblue')
plt.xlabel('Điểm số')
plt.ylabel('Số lượng')
plt.title('Biểu đồ phân phối điểm số các môn học')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#Lưu vào Excel
class_scores = defaultdict(list)
students = collection.find({}, {'class': 1, 'subjects': 1})
for student in students:
    avg = calculate_average(student)
    class_scores[student.get('class', 'Không rõ')].append(avg)

class_avg_data = {
    'Class': [],
    'Average Score': []
}
for cls, scores in class_scores.items():
    if scores:
        class_avg_data['Class'].append(cls)
        class_avg_data['Average Score'].append(round(sum(scores) / len(scores), 2))

df_class_avg = pd.DataFrame(class_avg_data)

# ----------------------------
# 2. Tỷ lệ sinh viên theo trạng thái
# ----------------------------
students = collection.find({}, {'status': 1})
status_list = [s.get('status', 'Không rõ') for s in students]
status_counter = Counter(status_list)

df_status = pd.DataFrame(list(status_counter.items()), columns=['Status', 'Count'])

# ----------------------------
# 3. Phân phối điểm số các môn học
# ----------------------------
scores = []
students = collection.find({}, {'subjects': 1})
for student in students:
    for sub in student.get('subjects', []):
        score = sub.get('score')
        if isinstance(score, (int, float)):
            scores.append(score)

df_scores = pd.DataFrame({'Score': scores})

# ----------------------------
# Xuất ra Excel
# ----------------------------
with pd.ExcelWriter('analysis_results.xlsx', engine='openpyxl') as writer:
    df_class_avg.to_excel(writer, sheet_name='Avg by Class', index=False)
    df_status.to_excel(writer, sheet_name='Status Summary', index=False)
    df_scores.to_excel(writer, sheet_name='All Scores', index=False)

print("✅ Đã xuất file 'analysis_results.xlsx' với 3 sheet: 'Avg by Class', 'Status Summary', 'All Scores'")