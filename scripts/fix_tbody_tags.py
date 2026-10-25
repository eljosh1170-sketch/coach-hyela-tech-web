with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all tbodyid missing spaces
content = content.replace('<tbodyid="tableBodyEligibility">', '<tbody id="tableBodyEligibility">')
content = content.replace('<tbodyid="tableBodyStudents">', '<tbody id="tableBodyStudents">')
content = content.replace('<tbodyid="adminCertsTableBody">', '<tbody id="adminCertsTableBody">')
content = content.replace('<tbodyid="adminCACTableBody">', '<tbody id="adminCACTableBody">')
content = content.replace('<tbodyid="tableBodyNotifs">', '<tbody id="tableBodyNotifs">')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed all tbodyid tags in admin.html!")
