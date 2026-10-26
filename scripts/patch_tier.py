with open('js/cht-core.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_cloud = """async function submitEligibilityRequestCloud(userId, fullName, email, courseId, courseTitle) {
    const res = submitEligibilityRequest(userId, fullName, email, courseId, courseTitle);"""
new_cloud = """async function submitEligibilityRequestCloud(userId, fullName, email, courseId, courseTitle, packageTier = 'VIP_BUNDLE') {
    const res = submitEligibilityRequest(userId, fullName, email, courseId, courseTitle, packageTier);"""

if old_cloud in text:
    text = text.replace(old_cloud, new_cloud, 1)
    print("Replaced cloud function signature")
else:
    print("Could not find old_cloud")

old_log = "details: `${fullName} (${email}) applied for ${courseTitle}`"
new_log = "details: `${fullName} (${email}) applied for ${courseTitle} [${packageTier}]`"
if old_log in text:
    text = text.replace(old_log, new_log, 1)
    print("Replaced log entry")

old_local = """function submitEligibilityRequest(userId, fullName, email, courseId, courseTitle) {"""
new_local = """function submitEligibilityRequest(userId, fullName, email, courseId, courseTitle, packageTier = 'VIP_BUNDLE') {"""
if old_local in text:
    text = text.replace(old_local, new_local, 1)
    print("Replaced local function signature")

old_req = """      courseId: courseId,
      courseTitle: courseTitle,
      submissionDate: new Date().toISOString(),"""
new_req = """      courseId: courseId,
      courseTitle: courseTitle,
      packageTier: packageTier,
      submissionDate: new Date().toISOString(),"""
if old_req in text:
    text = text.replace(old_req, new_req, 1)
    print("Replaced req object structure")

with open('js/cht-core.js', 'w', encoding='utf-8') as f:
    f.write(text)
print("Finished patching js/cht-core.js")
