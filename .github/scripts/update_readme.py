base_url = 'https://github.com/OsloMet-OceanLab/underwater_event_dataset/blob/main/Docs/installation.md'

# Read installation.md and extract the content table
with open('Docs/installation.md', 'r') as f:
    lines = f.readlines()
start = lines.index('### Content\n')
end = lines.index('| ---[Download resources](#Download) | App links and optional shell script to ease operations |\n') + 1
table = lines[start:end]

# Convert the relative links in the table to absolute links using base_url
new_table = []
for line in table:
    left, right = line.split('](')
    right = right.rstrip(')\n')
    if right.startswith('#'):
        new_line = left + '](' + base_url + right + ')\n'
    else:
        new_line = line
    new_table.append(new_line)

# Read the README file
with open('README.md', 'r') as f:
    readme = f.readlines()

# Remove the old table from the README file
start = readme.index('### Content\n')
end = readme.index('| ---[Download resources](#Download) | App links and optional shell script to ease operations |\n') + 1
del readme[start:end]

# Insert the new table at a specific location in the README file (e.g., line 10)
readme[10:10] = new_table

# Write the modified README back to file
with open('README.md', 'w') as f:
    f.writelines(readme)
