from pymongo import MongoClient

# Kết nối đến MongoDB (thay đổi uri nếu bạn dùng MongoDB Atlas hoặc server khác)
client = MongoClient('mongodb://localhost:27017/')

# Chọn database
db = client['eShop']

# Chọn collection
order_collection = db['OrderCollection']

orders = [
    {
        "orderid": 1,
        "products": [
            {
                "product_id": "quanau",
                "product_name": "quan au",
                "size": "XL",
                "price": 10,
                "quantity": 1
            },
            {
                "product_id": "somi",
                "product_name": "ao so mi",
                "size": "XL",
                "price": 10.5,
                "quantity": 2
            }
        ],
        "total_amount": 31,
        "delivery_address": "Hanoi"
    },
    {
        "orderid": 2,
        "products": [
            {
                "product_id": "jean",
                "product_name": "quan jean",
                "size": "L",
                "price": 15,
                "quantity": 2
            }
        ],
        "total_amount": 30,
        "delivery_address": "HCM"
    }
    ,
    {
        "orderid": 3,
        "products": [
            {
                "product_id": "ao",
                "product_name": "ao thun",
                "size": "M",
                "price": 5,
                "quantity": 3
            }
        ],
        "total_amount": 15,
        "delivery_address": "Da Nang"
    },
    {
        "orderid": 4,
        "products": [
            {
                "product_id": "aokhoac",
                "product_name": "ao khoac kaki",
                "size": "L",
                "price": 20,
                "quantity": 1
            },
            {
                "product_id": "non",
                "product_name": "non ket",
                "size": "Free",
                "price": 5,
                "quantity": 2
            }
        ],
        "total_amount": 30,
        "delivery_address": "Da Nang"
    },
]

# Insert many documents
order_collection.insert_many(orders)
print("Inserted orders successfully.")

orderid_to_update = 1
new_address = "Phnom Penh"

result = order_collection.update_one(
    {"orderid": orderid_to_update},
    {"$set": {"delivery_address": new_address}}
)

if result.modified_count > 0:
    print("Updated delivery address successfully.")
else:
    print("No document updated.")


orderid_to_delete = 2

result = order_collection.delete_one({"orderid": orderid_to_delete})

if result.deleted_count > 0:
    print("Deleted order successfully.")
else:
    print("No document deleted.")

orders = order_collection.find()

print("No\tProduct name\tPrice\tQuantity\tTotal")
no = 1
for order in orders:
    for product in order["products"]:
        total = product["price"] * product["quantity"]
        print(f"{no}\t{product['product_name']}\t{product['price']}\t{product['quantity']}\t{total}")
        no += 1

orders = order_collection.find()
count_somi = 0

for order in orders:
    for product in order["products"]:
        if product["product_id"] == "somi":
            count_somi += product["quantity"]

print(f"Total quantity of product_id 'somi': {count_somi}")
# Tính tổng số lượng sản phẩm trong tất cả các đơn hàng

