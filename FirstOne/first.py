from pymongo import MongoClient
import pandas as pd

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mongodb']
collection = db['advanced']

# Lấy tất cả documents và chuyển thành list để dùng nhiều lần
documents = list(collection.find())

# Hiển thị kết quả
print("Danh sách người dùng:")
for doc in documents:
    print(doc)

# Tạo DataFrame từ danh sách
df = pd.DataFrame(documents)
print("\nDataFrame:")
print(df)

# Lọc các sinh viên thuộc lớp A1
# Giả sử dữ liệu có trường 'class' chứa tên lớp
students_A1 = df[df['class'] == 'A1']



print("\nDanh sách sinh viên lớp A1:")
print(students_A1)

average_scores = []

# Duyệt từng dòng (sinh viên) trong DataFrame
for idx, row in df.iterrows():
    subjects = row.get('subjects', [])
    
    # Kiểm tra nếu subjects là list và có ít nhất 1 môn
    if isinstance(subjects, list) and len(subjects) > 0:
        # Lấy tất cả điểm của các môn học
        scores = []
        for s in subjects:
            score = s.get('score', None)
            # Chỉ lấy nếu điểm là số (int hoặc float)
            if isinstance(score, (int, float)):
                scores.append(score)
        
        # Tính điểm trung bình nếu có điểm
        if scores:
            avg = round(sum(scores) / len(scores), 2)
        else:
            avg = None
    else:
        avg = None
    
    # Thêm kết quả vào danh sách
    average_scores.append(avg)

# Thêm cột 'average' vào DataFrame
df['average'] = average_scores

# Hiển thị kết quả
print("\nDanh sách sinh viên kèm điểm trung bình:")
print(df[['name', 'class', 'average']])

# ----------------------------
# TÌM SINH VIÊN CÓ ĐIỂM TRUNG BÌNH CAO NHẤT
# ----------------------------

# Bỏ các sinh viên không có điểm (average = None) trước khi tìm max
df_valid = df.dropna(subset=['average'])

# Tìm giá trị điểm trung bình cao nhất
max_avg = df_valid['average'].max()

# Lọc sinh viên có điểm trung bình cao nhất (nếu có nhiều người cùng điểm)
top_students = df_valid[df_valid['average'] == max_avg]

print("\nSinh viên có điểm trung bình cao nhất:")
print(top_students[['name', 'class', 'average']])

# ----------------------------
# THỐNG KÊ SỐ LƯỢNG SINH VIÊN THEO LỚP
# ----------------------------

# Dùng groupby + size để đếm số lượng sinh viên từng lớp
students_per_class = df.groupby('class').size().reset_index(name='count')

print("\nSố lượng sinh viên từng lớp:")
print(students_per_class)

import matplotlib.pyplot as plt

# ----------------------------
# VẼ BIỂU ĐỒ TRÒN THEO TRẠNG THÁI SINH VIÊN
# ----------------------------

# Giả sử cột trạng thái tên là 'status'
# Thống kê số lượng từng trạng thái
status_counts = df['status'].value_counts()

# Vẽ biểu đồ tròn
plt.figure(figsize=(8,8))
plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)

# Đặt tiêu đề
plt.title('Tỷ lệ sinh viên theo trạng thái')

# Hiển thị biểu đồ
plt.show()

# ----------------------------
# LIỆT KÊ SINH VIÊN CÓ ÍT NHẤT 1 MÔN DƯỚI 60
# ----------------------------

students_under_60 = []

# Duyệt từng sinh viên
for idx, row in df.iterrows():
    subjects = row.get('subjects', [])
    
    # Kiểm tra nếu subjects là list và có môn học
    if isinstance(subjects, list) and subjects:
        # Kiểm tra nếu có bất kỳ môn nào điểm < 60
        has_under_60 = any(
            isinstance(s.get('score', None), (int, float)) and s['score'] < 60
            for s in subjects
        )
        
        if has_under_60:
            students_under_60.append({
                'name': row.get('name', 'No name'),
                'class': row.get('class', 'No class')
            })

# Hiển thị kết quả
print("\nDanh sách sinh viên có ít nhất 1 môn dưới 60:")
for s in students_under_60:
    print(f"{s['name']} - Lớp: {s['class']}")

# ----------------------------
# LIỆT KÊ SINH VIÊN CÓ ATTENDANCE > 90
# ----------------------------

students_attendance_over_90 = []

# Duyệt từng sinh viên
for idx, row in df.iterrows():
    attendance = row.get('attendance', 0)
    
    # Kiểm tra nếu attendance là số và > 90
    if isinstance(attendance, (int, float)) and attendance > 90:
        students_attendance_over_90.append({
            'name': row.get('name', 'No name'),
            'class': row.get('class', 'No class'),
            'attendance': attendance
        })

# Hiển thị kết quả
print("\nDanh sách sinh viên có attendance > 90:")
for s in students_attendance_over_90:
    print(f"{s['name']} - Lớp: {s['class']} - Attendance: {s['attendance']}")

# ----------------------------
# TÌM 5 SINH VIÊN CÓ SỐ LƯỢNG ACTIVITIES NHIỀU NHẤT
# ----------------------------

# Tạo cột mới 'activities_count' chứa số lượng activities của từng sinh viên
df['activities_count'] = df['activities'].apply(
    lambda x: len(x) if isinstance(x, list) else 0
)

# Sắp xếp giảm dần theo 'activities_count' và lấy top 5
top5_activities = df.sort_values(by='activities_count', ascending=False).head(5)

# Hiển thị kết quả
print("\nTop 5 sinh viên có số lượng activities nhiều nhất:")
print(top5_activities[['name', 'class', 'activities_count']])

# ----------------------------
# SO SÁNH ĐIỂM TRUNG BÌNH SINH VIÊN NAM VÀ NỮ (THEO CÁCH BẠN YÊU CẦU)
# ----------------------------

# Bỏ các sinh viên không có điểm trung bình
df_valid = df.dropna(subset=['average'])

# Tìm tất cả sinh viên nam
male_students = df_valid[df_valid['gender'] == 'M']

# Tìm tất cả sinh viên nữ
female_students = df_valid[df_valid['gender'] == 'F']

# Tính điểm trung bình tổng của nam
if not male_students.empty:
    male_avg = round(male_students['average'].mean(), 2)
else:
    male_avg = None

# Tính điểm trung bình tổng của nữ
if not female_students.empty:
    female_avg = round(female_students['average'].mean(), 2)
else:
    female_avg = None

# Hiển thị kết quả
print("\nSo sánh điểm trung bình:")
print(f"Sinh viên nam: {male_avg}")
print(f"Sinh viên nữ: {female_avg}")


