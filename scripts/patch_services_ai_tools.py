# -*- coding: utf-8 -*-
with open('services.html', 'r', encoding='utf-8') as f:
    text = f.read()

article_to_insert = """          <!-- Service 7: Subscriptions & AI Tools -->
          <article class="cht-card" id="subscriptions-ai-tools" style="border: 1px solid rgba(212, 175, 55, 0.4); background: rgba(0,0,0,0.35);">
            <div class="cht-card-icon" style="color: var(--cht-gold-light);"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a4 4 0 0 0-4 4v1H7a5 5 0 0 0-5 5c0 2.2 1.4 4.1 3.4 4.7A4.98 4.98 0 0 0 9 21.9V22h6v-.1c1.8-.4 3.3-1.8 3.6-3.6 2-.6 3.4-2.5 3.4-4.7a5 5 0 0 0-5-5h-1V6a4 4 0 0 0-4-4z"></path></svg></div>
            <div style="font-size: 0.8rem; color: var(--cht-gold-500); font-weight: 700; text-transform: uppercase; margin-bottom: 6px;">Premium Creative Power</div>
            <h2 class="cht-card-title">Subscriptions &amp; AI Tools &mdash; Muse AI</h2>
            <p class="cht-card-text">
              Direct access to enterprise-grade creative AI platforms and high-capacity credit allocations without foreign dollar card limits. Get 1 Billion generation credits on Muse AI for AI avatars, voice cloning, lip-sync, and video commercial generation.
            </p>
            <div style="background: rgba(0,0,0,0.25); border-left: 3px solid var(--cht-gold-500); padding: 12px; margin-bottom: 20px; font-size: 0.85rem; color: var(--cht-text-muted);">
              <strong>Standalone Pricing:</strong> &#8358;3,000 one-time payment to PalmPay (<strong>7011706511</strong> &bull; EL JOSHUA HYELAKURI EMMANUEL). Dispatched directly to WhatsApp.
            </div>
            <div style="margin-top: auto;">
              <a href="https://wa.me/2349159637287?text=Hello%20Coach%20Hyela%2C%20I%20want%20to%20buy%20Muse%20AI%20(1%20Billion%20Credits)%20separately%20for%20%E2%82%A63%2C000.%20Here%20is%20my%20payment%20receipt." target="_blank" rel="noopener noreferrer" class="cht-btn cht-btn-primary cht-btn-sm" style="font-weight: 700;">Order Muse AI (&#8358;3,000) &rarr;</a>
            </div>
          </article>
"""

target = '    <!-- Professional Standards Banner -->'
if target in text and 'id="subscriptions-ai-tools"' not in text:
    # insert before the closing of the grid
    closing_grid = '        </div>\n      </div>\n    </section>\n\n    <!-- Professional Standards Banner -->'
    new_grid = article_to_insert + '\n        </div>\n      </div>\n    </section>\n\n    <!-- Professional Standards Banner -->'
    if closing_grid in text:
        text = text.replace(closing_grid, new_grid, 1)
        print("[OK] Inserted Subscriptions & AI Tools in services.html")
    else:
        print("Could not find closing_grid in services.html")
else:
    print("Already present or target not found")

with open('services.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done services.html")
