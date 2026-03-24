const { chromium } = require('playwright');

(async () => {
  const { spawn } = require('child_process');
  const xvfb = spawn('Xvfb', [':99', '-screen', '0', '1280x720x24', '-ac'], {
    detached: true,
    stdio: 'ignore'
  });
  
  process.env.DISPLAY = ':99';
  await new Promise(r => setTimeout(r, 1000));
  
  const browser = await chromium.launch({
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 }
  });
  
  const page = await context.newPage();
  
  try {
    console.log('Navigating to SumoPod...');
    await page.goto('https://sumopod.com/login', { waitUntil: 'load', timeout: 60000 });
    
    // Wait for page to fully load
    await page.waitForTimeout(5000);
    
    await page.screenshot({ path: '/root/.openclaw/workspace/sumopod_google_1.png' });
    console.log('Screenshot saved: sumopod_google_1.png');
    
    // Look for Google sign in button
    console.log('Looking for Google sign in button...');
    const googleBtn = await page.locator('button:has-text("Google"), button:has-text("google"), [data-provider="google"], .google-btn, a:has-text("Google")').first();
    
    if (await googleBtn.isVisible().catch(() => false)) {
      console.log('Found Google button, clicking...');
      await googleBtn.click();
      
      // Wait for popup or navigation
      await page.waitForTimeout(5000);
      
      // Screenshot current page
      await page.screenshot({ path: '/root/.openclaw/workspace/sumopod_google_after_click.png' });
      console.log('Screenshot saved: sumopod_google_after_click.png');
      
      const url = page.url();
      console.log(`Current URL: ${url}`);
      
      console.log('GOOGLE_LOGIN_READY');
      
      // Keep browser open for 60s
      await new Promise(r => setTimeout(r, 60000));
    } else {
      console.log('Google button not found. Looking for all buttons...');
      const buttons = await page.$$('button');
      console.log(`Found ${buttons.length} buttons`);
      for (let i = 0; i < buttons.length; i++) {
        const text = await buttons[i].textContent();
        console.log(`Button ${i}: ${text}`);
      }
    }
    
  } catch (error) {
    console.error('Error:', error.message);
    await page.screenshot({ path: '/root/.openclaw/workspace/sumopod_error.png' });
  }
  
  await browser.close();
  xvfb.kill();
  process.exit(0);
})();
