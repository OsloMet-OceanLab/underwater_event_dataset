# Read installation.md and extract the content table
with open('Docs/installation.md', 'r') as f:
    lines = f.readlines()
start = lines.index('### Content\n')
end = lines.index('| ---[Download resources](#Download) | App links and optional shell script to ease operations |\n') + 1
table = lines[start:end]

# Read the README file
with open('README.md', 'r') as f:
    readme = f.readlines()

# Insert the table at a specific location in the README file (e.g., line 10)
readme[10:10] = table

# Write the modified README back to file
with open('README.md', 'w') as f:
    f.writelines(readme)
