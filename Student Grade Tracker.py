students = []
n = int(input("Enter number of students: "))

for i in range(n):
    name = input(f"Enter name of student {i+1}: ")
    marks = float(input(f"Enter marks of {name}: "))
    students.append({"name": name, "marks": marks})

average = sum(s['marks'] for s in students) / n
topper = max(students, key=lambda x: x['marks'])

print("\n--- Summary Report ---")
print(f"Average Marks: {average:.2f}")
print(f"Topper: {topper['name']} with {topper['marks']} marks")
