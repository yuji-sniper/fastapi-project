import csv

with open('test.csv', 'w') as file:
    fieldnames = ['Name', 'Count']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'Name': 'A', 'Count': 1})
    writer.writerow({'Name': 'B', 'Count': 2})
    writer.writerow({'Name': 'C', 'Count': 3})

with open('test.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row['Name'], row['Count'])
