# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Subscriptions & AI Tools section to insert before CAC Interactive Feature Callout
section_to_insert = """    <!-- Subscriptions & AI Tools Section -->
    <section class="cht-section" id="subscriptions-ai-tools" style="background: linear-gradient(180deg, rgba(8,27,17,0.7) 0%, rgba(5,13,8,0.95) 100%); border-top: 1px solid var(--cht-border-subtle); border-bottom: 1px solid var(--cht-border-subtle);">
      <div class="cht-container">
        <div class="cht-section-header">
          <span class="cht-section-tag">Enterprise Creative Power</span>
          <h2 class="cht-section-title heading-serif">Subscriptions &amp; AI Tools</h2>
          <p class="cht-section-desc">
            Direct standalone access to enterprise-grade AI generation suites and high-capacity creative credits without foreign dollar cards or costly recurring fees.
          </p>
        </div>

        <div style="max-width: 720px; margin: 0 auto;">
          <div class="cht-card" style="border: 1px solid rgba(212, 175, 55, 0.4); background: rgba(0, 0, 0, 0.45); padding: 32px; border-radius: var(--cht-radius-lg); position: relative; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 14px; margin-bottom: 16px;">
              <div>
                <span class="status-pill approved" style="font-size: 0.72rem; background: #22C55E; color: #000; font-weight: 700; margin-bottom: 8px; display: inline-block;">Instant Delivery</span>
                <h3 class="cht-card-title" style="font-size: 1.5rem; margin-bottom: 4px; color: #fff;">Muse AI &mdash; 1 Billion Generation Credits</h3>
                <div style="font-size: 0.85rem; color: var(--cht-gold-light); font-weight: 600;">Standalone Creative AI Tool Access</div>
              </div>
              <div style="text-align: right;">
                <div style="font-size: 2rem; font-weight: 800; color: #fff; font-family: var(--font-serif);">&#8358;3,000</div>
                <div style="font-size: 0.75rem; color: #86EFAC; font-weight: 600;">One-Time Payment</div>
              </div>
            </div>

            <p class="cht-card-text" style="font-size: 0.92rem; line-height: 1.6; margin-bottom: 20px; color: var(--cht-text-secondary);">
              Get instant access to <strong>1,000,000,000 generation credits</strong> on Muse AI. Engineered for photorealistic AI avatars, video lip-sync, marketing commercials, and cinematic animations. Zero VPN requirements, zero monthly dollar subscriptions, and zero international card hassles.
            </p>

            <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(212,175,55,0.25); border-radius: var(--cht-radius-md); padding: 18px; margin-bottom: 22px;">
              <div style="font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--cht-text-muted); margin-bottom: 8px;">Official PalmPay Payment Details:</div>
              <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                  <div style="font-size: 0.8rem; color: var(--cht-text-muted);">PalmPay Account:</div>
                  <div style="font-size: 1.25rem; font-weight: 800; color: var(--cht-gold-light); font-family: monospace; letter-spacing: 1px;">7011706511</div>
                </div>
                <div style="text-align: right;">
                  <div style="font-size: 0.8rem; color: var(--cht-text-muted);">Beneficiary Legal Name:</div>
                  <div style="font-size: 1rem; font-weight: 700; color: #fff;">EL JOSHUA HYELAKURI EMMANUEL</div>
                </div>
              </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; border-top: 1px solid var(--cht-border-subtle); padding-top: 18px;">
              <div style="font-size: 0.82rem; color: var(--cht-text-muted);">
                After payment, send your transfer receipt to WhatsApp for instant voucher dispatch.
              </div>
              <a href="https://wa.me/2349159637287?text=Hello%20Coach%20Hyela%2C%20I%20want%20to%20buy%20Muse%20AI%20(1%20Billion%20Credits)%20separately%20for%20%E2%82%A63%2C000.%20Here%20is%20my%20payment%20receipt." target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-primary" style="font-weight: 700; white-space: nowrap;">
                Order Muse AI on WhatsApp (&#8358;3,000) &rarr;
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

"""

target = '    <!-- CAC Interactive Feature Callout -->'
if target in text and 'id="subscriptions-ai-tools"' not in text:
    text = text.replace(target, section_to_insert + target, 1)
    print("[OK] Inserted Subscriptions & AI Tools section in index.html")
else:
    print("Could not find target or already present in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done index.html")
