Weight = input("Enter your weight : ")

choice = input("Enter your choice (K for Kilograms, L for Pounds) : ")
if choice.upper() == 'L':
    converted_weight = float(Weight) * 2.20462
    print(f"Your weight in Pounds is {converted_weight:.2f} lbs")
elif choice.upper() == 'K':
    converted_weight = float(Weight) / 2.20462
    print(f"Your weight in Kilograms is {converted_weight:.2f} kg")
else:
    print("Invalid choice! Please enter 'K' for Kilograms or 'L' for Pounds.")

