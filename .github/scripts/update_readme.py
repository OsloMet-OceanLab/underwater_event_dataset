# Read installation.md and extract the content table
with open('Docs/installation.md', 'r') as f:
    lines = f.readlines()
start = lines.index('### Content\n')
end = lines.index('| ---[Download resources](#Download) | App links and optional shell script to ease operations |\n') + 1
table = lines[start:end]

# Read the README file
with open('README.md', 'r') as f:
    readme = f.readlines()

# Find the start and end of the old table in README
try:
    readme_start = readme.index('### Content\n')
    readme_end = readme.index('| ---[Download resources](#Download) | App links and optional shell script to ease operations |\n') + 1
except ValueError:
    readme_start = readme_end = 10  # Default location if the old table is not found

# Replace the old table with the new table
readme[readme_start:readme_end] = table

# Write the modified README back to file
with open('README.md', 'w') as f:
    f.writelines(readme)

