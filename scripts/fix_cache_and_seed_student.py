# scripts/fix_cache_and_seed_student.py
import re
import glob

# 1. Update firebase.json caching headers
with open('firebase.json', 'r', encoding='utf-8') as f:
    fb_config = f.read()

old_cache_header = """      {
        "source": "**/*.@(jpg|jpeg|gif|png|svg|webp|js|css|mp4)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "max-age=604800, stale-while-revalidate=86400"
          }
        ]
      }"""

new_cache_header = """      {
        "source": "**/*.@(js|css)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "no-cache, no-store, must-revalidate"
          }
        ]
      },
      {
        "source": "**/*.@(jpg|jpeg|gif|png|svg|webp|mp4)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "max-age=86400"
          }
        ]
      }"""

if old_cache_header in fb_config:
    fb_config = fb_config.replace(old_cache_header, new_cache_header)
    with open('firebase.json', 'w', encoding='utf-8') as f:
        f.write(fb_config)
    print("Updated firebase.json cache-control headers")

# 2. Update js/cht-core.js with Ayomide Emmanuel in DEFAULT_ELIGIBILITY, DEFAULT_USERS, and initStorage
with open('js/cht-core.js', 'r', encoding='utf-8') as f:
    core_js = f.read()

# Replace DEFAULT_ELIGIBILITY
old_def_elig = """  // Pre-seeded eligibility requests
  const DEFAULT_ELIGIBILITY = [
    {
      id: "REQ-2026-001",
      userId: "USR-001",
      fullName: "Bilkisu Danjuma",
      email: "bilkisu.learner@testmail.com",
      courseId: "ai-video-ugc",
      courseTitle: "AI Video Creation & UGC-Style Advertising",
      submissionDate: "2026-10-12T10:15:00.000Z",
      status: "APPROVED", // PENDING, APPROVED, REJECTED, MORE_INFo
      adminNotes: "All capstone videos submitted and verified by Coach Hyela.",
      reviewedAt: "2026-10-13T16:00:00.000Z",
      certificateIssued: true,
      certificateCode: "CHT-2026-AI092"
    },
    {
      id: "REQ-2026-002",
      userId: "USR-002",
      fullName: "Emmanuel K. Ogbonna",
      email: "emmanuel.learner@testmail.com",
      courseId: "website-building",
      courseTitle: "Modern Website Building & Digital Presence",
      submissionDate: "2026-10-14T08:20:00.000Z",
      status: "APPROVED",
      adminNotes: "Demonstrated responsive HTML5/CSS and web project deployment.",
      reviewedAt: "2026-10-15T11:45:00.000Z",
      certificateIssued: true,
      certificateCode: "CHT-2026-WD104"
    },
    {
      id: "REQ-2026-003",
      userId: "USR-003",
      fullName: "Tariq Ibrahim",
      email: "tariq.student@testmail.com",
      courseId: "ai-digital-skills",
      courseTitle: "Artificial Intelligence & Creative Workflows for Individuals",
      submissionDate: "2026-10-19T14:10:00.000Z",
      status: "PENDING",
      adminNotes: "Awaiting final prompt engineering evaluation from instructor.",
      reviewedAt: null,
      certificateIssued: false,
      certificateCode: null
    }
  ];"""

new_def_elig = """  // Active student eligibility requests
  const DEFAULT_ELIGIBILITY = [
    {
      id: "REQ-2026-AYO1",
      userId: "USR-OjS5lcUI",
      fullName: "Ayomide Emmanuel",
      email: "emmanuelekhator5683@gmail.com",
      courseId: "ai-video-ugc",
      courseTitle: "AI Video Creation & UGC-Style Advertising",
      submissionDate: "2026-10-25T19:43:00.000Z",
      status: "PENDING",
      adminNotes: "Application received. Pending evaluation by Coach Hyela.",
      reviewedAt: null,
      certificateIssued: false,
      certificateCode: null
    }
  ];"""

if old_def_elig in core_js:
    core_js = core_js.replace(old_def_elig, new_def_elig)
    print("Replaced DEFAULT_ELIGIBILITY with Ayomide Emmanuel")

# Update initStorage to guarantee Ayomide Emmanuel is injected into localStorage
old_init_storage = """  function initStorage() {
    try {
      if (!localStorage.getItem(STORAGE_KEYS.USERS)) {
        localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(DEFAULT_USERS));
      }
      if (!localStorage.getItem(STORAGE_KEYS.ELIGIBILITY_REQUESTS)) {
        localStorage.setItem(STORAGE_KEYS.ELIGIBILITY_REQUESTS, JSON.stringify(DEFAULT_ELIGIBILITY));
      }"""

new_init_storage = """  function initStorage() {
    try {
      if (!localStorage.getItem(STORAGE_KEYS.USERS)) {
        localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(DEFAULT_USERS));
      } else {
        try {
          const uList = JSON.parse(localStorage.getItem(STORAGE_KEYS.USERS) || '[]');
          if (!uList.some(u => u.email === 'emmanuelekhator5683@gmail.com')) {
            uList.unshift({
              id: "USR-OjS5lcUI",
              fullName: "Ayomide Emmanuel",
              email: "emmanuelekhator5683@gmail.com",
              registeredAt: "2026-10-25T19:15:36.000Z",
              emailVerified: true,
              assignedCourses: ["ai-video-ugc"],
              driveAccess: false
            });
            localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(uList));
          }
        } catch(e) {}
      }

      if (!localStorage.getItem(STORAGE_KEYS.ELIGIBILITY_REQUESTS)) {
        localStorage.setItem(STORAGE_KEYS.ELIGIBILITY_REQUESTS, JSON.stringify(DEFAULT_ELIGIBILITY));
      } else {
        try {
          let reqList = JSON.parse(localStorage.getItem(STORAGE_KEYS.ELIGIBILITY_REQUESTS) || '[]');
          // Remove outdated dummy test users if present
          reqList = reqList.filter(r => !r.email.includes('@testmail.com'));
          if (!reqList.some(r => r.email === 'emmanuelekhator5683@gmail.com')) {
            reqList.unshift({
              id: "REQ-2026-AYO1",
              userId: "USR-OjS5lcUI",
              fullName: "Ayomide Emmanuel",
              email: "emmanuelekhator5683@gmail.com",
              courseId: "ai-video-ugc",
              courseTitle: "AI Video Creation & UGC-Style Advertising",
              submissionDate: "2026-10-25T19:43:00.000Z",
              status: "PENDING",
              adminNotes: "Application received. Pending evaluation by Coach Hyela.",
              reviewedAt: null,
              certificateIssued: false,
              certificateCode: null
            });
          }
          localStorage.setItem(STORAGE_KEYS.ELIGIBILITY_REQUESTS, JSON.stringify(reqList));
        } catch(e) {}
      }"""

if old_init_storage in core_js:
    core_js = core_js.replace(old_init_storage, new_init_storage)
    print("Updated initStorage to clean dummy test accounts and ensure Ayomide Emmanuel exists")

with open('js/cht-core.js', 'w', encoding='utf-8') as f:
    f.write(core_js)

# 3. Add cache-busting query parameter (?v=20261025_04) to all HTML files
for hfile in glob.glob('*.html'):
    with open(hfile, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace <script src="js/cht-core.js"></script> with versioned parameter
    new_html = re.sub(r'src="js/cht-core\.js(\?v=[^"]*)?"', 'src="js/cht-core.js?v=20261025_04"', html)
    if new_html != html:
        with open(hfile, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"Updated cache buster in {hfile}")

print("All updates applied!")
