def linearSearch(db, target):
    for item in db:
        if item["name"].lower() == target.lower():
            return item
    return None

marketplace = [
    {"id": 1, "name": "Laptop", "price": 1000},
    {"id": 2, "name": "Smartphone", "price": 500},
    {"id": 3, "name": "Headphones", "price": 150},
    {"id": 4, "name": "Keyboard", "price": 70},
]

requestedItem = input("Hello! What item are you looking for in the marketplace?")
result = linearSearch(marketplace, requestedItem)

print(f"Item found: {result}" if result else "Item not found.")

