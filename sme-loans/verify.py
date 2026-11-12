from pathlib import Path
from playwright.sync_api import sync_playwright
import json
p=Path(__file__).resolve().parent
(p/'previews').mkdir(exist_ok=True)
with sync_playwright() as w:
 b=w.chromium.launch(channel='chrome')
 page=b.new_page(viewport={'width':800,'height':880},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((p/'index.html').as_uri());page.evaluate('document.fonts.ready')
 def screen(s): assert page.locator('[data-screen]').get_attribute('data-screen')==s
 def shot(n): page.locator('#phone').screenshot(path=str(p/'previews'/f'{n}.png'))
 def click(a): page.locator(f'[data-action="{a}"]').click()
 def start(amount):
  page.locator('#restart').click();click('borrow')
  page.keyboard.press('ControlOrMeta+a');page.keyboard.type(str(amount))
 def forward(): click('continue')
 shot('01-home')
 click('borrow');page.locator('[data-key="0"]').click()
 assert page.locator('.amount-display').inner_text()=='250,000'
 page.keyboard.type('0');assert page.locator('.amount-display').inner_text()=='2,500,000'
 page.keyboard.press('Backspace')
 assert page.locator('.amount-display').inner_text()=='250,000'
 assert page.locator('.amount-display').evaluate("(e)=>getComputedStyle(e,'::after').animationName")=='caret-blink'
 samples=[]
 for _ in range(12):
  samples.append(page.locator('.amount-display').evaluate("(e)=>getComputedStyle(e,'::after').opacity"))
  page.wait_for_timeout(100)
 assert '0' in samples and '1' in samples
 forward();screen('purpose')
 assert page.locator('[aria-checked="true"]').count()==0
 assert page.locator('[data-action="continue"]').count()==0
 box=page.locator('[data-purpose="business"]').bounding_box()
 page.mouse.move(box['x']+30,box['y']+30);page.mouse.down()
 assert page.locator('[data-purpose="business"]').evaluate("(e)=>getComputedStyle(e).filter")=='none'
 assert page.locator('[data-purpose="business"]').evaluate("(e)=>getComputedStyle(e).backgroundColor")=='rgb(255, 255, 255)'
 page.mouse.up()
 page.locator('[data-purpose="business"]').click()
 assert page.locator('[data-action="continue"]').is_visible()
 forward();click('yes');screen('businessPurpose')
 assert page.locator('[aria-checked="true"]').count()==0
 assert page.locator('[data-action="continue"]').count()==0
 page.locator('[data-business-purpose="Buy stock or supplies"]').click()
 assert page.locator('[data-action="continue"]').is_visible()

 start(49999);shot('02-calculator');forward();screen('goals')
 page.locator('[data-goal="Gifts & occasions"]').click()
 page.locator('[data-goal="Medical emergency"]').click()
 assert page.locator('.chip.selected').first.evaluate("(e)=>getComputedStyle(e).backgroundColor")=='rgb(30, 30, 30)'
 assert page.locator('.chip.selected').first.evaluate("(e)=>getComputedStyle(e).color")=='rgb(255, 255, 255)'
 button_box=page.locator('[data-action="continue"]').bounding_box()
 indicator_box=page.locator('.home-indicator').bounding_box()
 page.locator('#goal-scroll').evaluate('(e)=>e.scrollTop=e.scrollHeight')
 assert page.locator('[data-action="continue"]').bounding_box()==button_box
 assert page.locator('.home-indicator').bounding_box()==indicator_box
 page.locator('#other').fill('Other goal')
 page.locator('#goal-scroll').evaluate('(e)=>e.scrollTop=0')
 shot('04-goals');forward();screen('products');shot('05-products')
 click('product:Cash loan');assert page.get_by_role('dialog').count()==1;click('dismiss')
 start(50000);forward();screen('purpose');shot('03-purpose')
 page.locator('[data-purpose="business"]').click();forward();screen('registration');shot('06-registration')
 click('no');screen('cashFallback');assert page.locator('.toast').count()==0
 shot('06b-cash-fallback')
 assert page.locator('.state-illustration img').evaluate('(e)=>e.complete && e.naturalWidth>0')
 forward();screen('goals');click('back');screen('cashFallback');click('back');screen('registration');click('yes');screen('businessPurpose');shot('07-business-purpose')
 page.locator('[data-business-purpose="Cover day-to-day business costs"]').click();forward();screen('finances');shot('08-finances')
 forward();screen('finances');assert page.locator('.error').inner_text()
 page.locator('#sales').click();page.keyboard.type('100000');page.locator('#income').click();page.keyboard.type('30000');forward();screen('flow');shot('09-next-steps')
 start(600000);forward();screen('purpose')
 click('back');screen('calculator');assert page.locator('.amount-display').inner_text()=='600,000'
 for amount in [4999,600001,0]:
  start(amount);forward();screen('calculator');assert page.locator('.amount-error').inner_text()
 start(5000);forward();screen('goals');forward();screen('goals')
 page.locator('#other').fill('Travel');forward();screen('products')
 assert not page.locator('img').evaluate_all('(els)=>els.some(e=>!e.complete||!e.naturalWidth)')
 # Mobile viewport and valid registration branch.
 start(250000);page.set_viewport_size({'width':360,'height':800});forward();screen('purpose')
 assert page.locator('#phone').evaluate('(e)=>e.scrollWidth<=e.clientWidth')
 page.locator('[data-purpose="business"]').click();forward();click('yes');page.locator('[data-business-purpose="Cover day-to-day business costs"]').click();forward()
 assert page.locator('#phone').evaluate('(e)=>e.scrollWidth<=e.clientWidth')
 print(json.dumps({'passed':['blinking caret','25000 + 0 = 250000','unselected initial states without Continue','Continue appears after selection','dark selected goals','footer remains fixed while scrolling','personal branch','registered business branch','unregistered business fallback','inclusive 50000 and 600000 threshold','5000 minimum','invalid 4999 / 600001 / 0','back preserves amount','required goals and financial fields','mobile 360x800 no horizontal overflow','all visible assets loaded'],'page_errors':errors},indent=2))
 assert not errors
 b.close()
