with open('ark_ui_classes_updated.py', 'r', encoding='utf-8') as f:
    names = []
    for line in f:
        line = line.strip()
        if line.startswith("'"):
            try:
                name = line.split("'")[1]
                names.append(name)
            except IndexError:
                continue

print(f'Total classes: {len(names)}')
print(f'Unique classes: {len(set(names))}')

# Find duplicates
duplicates = {}
for name in set(names):
    count = names.count(name)
    if count > 1:
        duplicates[name] = count

if duplicates:
    print('\nDuplicates found:')
    for name, count in duplicates.items():
        print(f'{name}: {count} times')
else:
    print('\nNo duplicate class names found.')
