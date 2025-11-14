from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mongodb']
collection = db['students']

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

# Tính điểm trung bình theo tên
avg_score = df.groupby('name')['score'].mean().reset_index()
print("\nĐiểm trung bình theo tên:")
print(avg_score)

# Ghi vào Excel
with pd.ExcelWriter("report.xlsx") as writer:
    df.to_excel(writer, sheet_name='All Students', index=False)
    avg_score.to_excel(writer, sheet_name='Average Score', index=False)

print("Báo cáo đã được lưu vào 'report.xlsx'")

plt.figure(figsize=(6, 4))
plt.bar(avg_score['name'], avg_score['score'], color='skyblue')
plt.xlabel('Name')
plt.ylabel('Average Score')
plt.title('Average Score by Class')
plt.tight_layout()
plt.savefig('average_score_by_class.png')
print("Biểu đồ đã được lưu vào 'average_score_by_class.png'")