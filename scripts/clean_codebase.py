import os, sys, re

def clean_content(text, filename):
    # 1. Clean HTML numeric entities that were corrupted
    text = text.replace('&#129504;', 'dy')
    text = text.replace('&#128187;', "dy'")
    
    # 2. Corrupt attribute values with &#10003;
    text = text.replace('class="cht-brand-log&#10003;>', 'class="cht-brand-logo">')
    text = text.replace('alt="Coach Hyela Log&#10003; ', 'alt="Coach Hyela Logo" ')
    text = text.replace('alt="Coach Hyela Log&#10003;>', 'alt="Coach Hyela Logo">')
    text = text.replace('alt="Coach Hyela Log&#10003;', 'alt="Coach Hyela Logo"')
    text = text.replace('class="cht-alert cht-alert-inf&#10003; ', 'class="cht-alert cht-alert-info" ')
    text = text.replace('class="cht-alert cht-alert-inf&#10003;>', 'class="cht-alert cht-alert-info">')
    text = text.replace('value="MoRE_INF&#10003;>', 'value="MORE_INFO">')
    text = text.replace('class="cht-her&#10003;>', 'class="cht-hero">')
    
    # 3. Mojibake strings
    text = text.replace('\xc2\xa0', ' ')
    text = text.replace('Â&copy;', '&copy;')
    text = text.replace('â€œ', '&ldquo;')
    text = text.replace('â€', '&rdquo;')
    text = text.replace('â€¢', '&bull;')
    text = text.replace('â–¾', '&#9662;')
    text = text.replace('â†’', '&rarr;')
    text = text.replace('âœ“', '&#10003;')
    text = text.replace('âœ•', '&#10005;')
    text = text.replace('âš ï¸ ', '&#9888;&#65039;')
    text = text.replace('Cyber CafAc', 'Cyber Caf&eacute;')
    text = text.replace('CafAc', 'Caf&eacute;')
    text = text.replace('Cyber Café', 'Cyber Caf&eacute;')
    
    # Replace broken emoji glyphs with clean professional SVG icons
    text = text.replace('ðŸŽ¬', '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect><line x1="7" y1="2" x2="7" y2="22"></line><line x1="17" y1="2" x2="17" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line><line x1="2" y1="7" x2="7" y2="7"></line><line x1="2" y1="17" x2="7" y2="17"></line><line x1="17" y1="17" x2="22" y2="17"></line><line x1="17" y1="7" x2="22" y2="7"></line></svg>')
    text = text.replace('ðŸ§ ', '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a4 4 0 0 0-4 4v1H7a5 5 0 0 0-5 5c0 2.2 1.4 4.1 3.4 4.7A4.98 4.98 0 0 0 9 21.9V22h6v-.1c1.8-.4 3.3-1.8 3.6-3.6 2-.6 3.4-2.5 3.4-4.7a5 5 0 0 0-5-5h-1V6a4 4 0 0 0-4-4z"></path></svg>')
    text = text.replace('ðŸ’»', '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>')
    text = text.replace('âš™ï¸ ', '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>')
    text = text.replace('ðŸ ›ï¸ ', '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M3 7v1a3 3 0 0 0 6 0V7m0 1a3 3 0 0 0 6 0V7m0 1a3 3 0 0 0 6 0V7H3l2-4h14l2 4M5 21V10.85M19 21V10.85M9 21v-4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4"></path></svg>')
    text = text.replace('ðŸ“Š', '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>')
    text = text.replace('ðŸ“‘', '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>')
    text = text.replace('ðŸ–¥ï¸ ', '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>')
    text = text.replace('ðŸŒ ', '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>')
    text = text.replace('âœ¨', '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>')
    text = text.replace('ðŸš€', '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path><path d="M9 12H4s.55-3.03 2-4.5c1.62-1.63 5-2 5-2"></path><path d="M12 9v5s3.03-.55 4.5-2c1.63-1.62 2-5 2-5"></path></svg>')
    text = text.replace('ðŸŽ¨', '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="13.5" cy="6.5" r=".5"></circle><circle cx="17.5" cy="10.5" r=".5"></circle><circle cx="8.5" cy="7.5" r=".5"></circle><circle cx="6.5" cy="12.5" r=".5"></circle><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"></path></svg>')
    text = text.replace('ðŸŒ±', '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22v-9"></path><path d="M9 16.5c-3-1-4-4.5-4-8.5 4 0 7.5 1 8.5 4"></path><path d="M15 13.5c3-1 4-4.5 4-8.5-4 0-7.5 1-8.5 4"></path></svg>')

    # 4. JavaScript / URL &bull;
    text = re.sub(r'(\.html|\.com|\.ng|\/|https:\/\/wa\.me\/[0-9]+|family=[a-zA-Z0-9_+:]+)&bull;', r'\1?', text)
    text = text.replace('css2&bull;', 'css2?')
    text = text.replace('verify.html&bull;code=', 'verify.html?code=')
    text = text.replace('cac.html&bull;type=', 'cac.html?type=')
    text = text.replace('contact.html&bull;service=', 'contact.html?service=')
    text = text.replace('contact.html&bull;course=', 'contact.html?course=')
    text = text.replace('&bull;text=', '?text=')
    
    # Ternary operators in JS:
    text = re.sub(r'\)\s*&bull;\s*', ') ? ', text)
    text = re.sub(r'(\b\w+Code|\bhasAccess|\bemailVerified|\bstatusReason|\bisError|\buser)\s*&bull;\s*', r'\1 ? ', text)
    text = text.replace("=== 'APPRoVED') &bull;", "=== 'APPROVED') ?")
    text = text.replace("=== 'REVoKED') &bull;", "=== 'REVOKED') ?")
    text = text.replace("=== 'VALID') &bull;", "=== 'VALID') ?")
    text = text.replace("=== 'login') &bull;", "=== 'login') ?")
    text = text.replace("=== 'register') &bull;", "=== 'register') ?")
    text = text.replace("=== tab) &bull;", "=== tab) ?")
    text = text.replace("r.certificateCode &bull;", "r.certificateCode ?")
    text = text.replace("req.certificateCode &bull;", "req.certificateCode ?")
    text = text.replace("req.certificateIssued &bull;", "req.certificateIssued ?")
    text = text.replace("res.verificationCode &bull;", "res.verificationCode ?")
    text = text.replace("res.resetCode &bull;", "res.resetCode ?")
    text = text.replace("u.emailVerified &bull;", "u.emailVerified ?")
    text = text.replace("u.driveAccess &bull;", "u.driveAccess ?")
    text = text.replace("c.status === 'VALID' &bull;", "c.status === 'VALID' ?")
    text = text.replace("req.status === 'APPRoVED' &bull;", "req.status === 'APPROVED' ?")
    text = text.replace("req.status === 'APPROVED' &bull;", "req.status === 'APPROVED' ?")
    text = text.replace("cert.status === 'REVoKED' &bull;", "cert.status === 'REVOKED' ?")
    text = text.replace("cert.status === 'REVOKED' &bull;", "cert.status === 'REVOKED' ?")
    text = text.replace("newStatus === 'APPRoVED' &bull;", "newStatus === 'APPROVED' ?")
    text = text.replace("newStatus === 'APPROVED' &bull;", "newStatus === 'APPROVED' ?")
    text = text.replace("newStatus === 'REVoKED' &bull;", "newStatus === 'REVOKED' ?")
    text = text.replace("newStatus === 'REVOKED' &bull;", "newStatus === 'REVOKED' ?")

    # Questions ending with &bull;
    text = text.replace('toRegister&bull;', 'to Register?')
    text = text.replace('to Register&bull;', 'to Register?')
    text = text.replace('Tech Skills&bull;', 'Tech Skills?')
    text = text.replace('Forgot Password&bull;', 'Forgot Password?')
    text = text.replace('packages&bull;', 'packages?')
    text = text.replace('assistance&bull;', 'assistance?')
    text = text.replace('preferred timeline&bull;', 'preferred timeline?')
    text = text.replace('corporate digital solutions&bull;', 'corporate digital solutions?')
    text = text.replace('assist you&bull;', 'assist you?')
    text = text.replace('electronic submissions&bull;', 'electronic submissions?')
    text = text.replace('Coach Hyela Training&bull;', 'Coach Hyela Training?')
    text = text.replace("(req.status === 'PENDING' &bull; 'var(--cht-warning)' : '#EF4444')", "(req.status === 'PENDING' ? 'var(--cht-warning)' : '#EF4444')")

    # 5. Words, casing and joins
    text = text.replace('toISoString()', 'toISOString()')
    text = text.replace('DoMContentLoaded', 'DOMContentLoaded')
    text = text.replace('JSoN', 'JSON')
    text = text.replace('APPRoVED', 'APPROVED')
    text = text.replace('REVoKED', 'REVOKED')
    text = text.replace('INFoRMATIoN', 'INFORMATION')
    text = text.replace('MoRE', 'MORE')
    text = text.replace('FoRM', 'FORM')
    text = text.replace('PASSWoRD', 'PASSWORD')
    text = text.replace('VERIFICATIoN', 'VERIFICATION')
    text = text.replace('CoDE', 'CODE')
    text = text.replace('SUBMISSIoNS', 'SUBMISSIONS')
    text = text.replace('SToRAGE_KEYS', 'STORAGE_KEYS')
    text = text.replace('NoTIFICATIoN_LoG', 'NOTIFICATION_LOG')
    text = text.replace('CoACH', 'COACH')
    text = text.replace('oFFICIAL', 'OFFICIAL')
    text = text.replace('ogbonna', 'Ogbonna')
    text = text.replace('october', 'October')

    text = text.replace('toStudent', 'to Student')
    text = text.replace('toSign', 'to Sign')
    text = text.replace('toThis', 'to this')
    text = text.replace('tothe', 'to the')
    text = text.replace('toThe', 'to the')
    text = text.replace('toRegister', 'to Register')
    text = text.replace('Toequip', 'To equip')
    text = text.replace('intomeaningful', 'into meaningful')
    text = text.replace('Tohelp', 'To help')
    text = text.replace('tocreate', 'to create')
    text = text.replace('zerofalse', 'zero false')
    text = text.replace('togive', 'to give')
    text = text.replace('tobuild', 'to build')
    text = text.replace('toGrant', 'to Grant')
    text = text.replace('nofalse', 'no false')
    text = text.replace('VideoCreation', 'Video Creation')
    text = text.replace('videoscenes', 'video scenes')
    text = text.replace('videoadvertisements', 'video advertisements')
    text = text.replace('videoeditors', 'video editors')
    text = text.replace('videoassignments', 'video assignments')
    text = text.replace('Demostudent', 'Demo student')
    text = text.replace('Demotest', 'Demo test')
    text = text.replace('DemoReset', 'Demo Reset')
    text = text.replace('DoYou', 'Do you')
    text = text.replace('toyour', 'to your')

    # 6. Revert Anton/Poppins font link to Cinzel & Plus Jakarta Sans
    anton_font_pattern = r'<link\s+href=[\"\']https:\/\/fonts\.googleapis\.com\/css2[^\"]*Anton[^\"]*[\"\']\s+rel=[\"\']stylesheet[\"\']>'
    replacement_fonts = '''<link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'''
    text = re.sub(anton_font_pattern, replacement_fonts, text)

    return text

files_to_clean = [
    '404.html', 'about.html', 'admin.html', 'cac.html', 'certificates.html',
    'contact.html', 'index.html', 'privacy.html', 'services.html', 'training.html',
    'verify.html', 'data/certificates.json', 'data/content.json', 'js/cht-core.js'
]

for f in files_to_clean:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            orig = fp.read()
        cleaned = clean_content(orig, f)
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(cleaned)
        print(f'Cleaned {f}')
