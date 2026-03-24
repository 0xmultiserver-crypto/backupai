const { chromium } = require('playwright');

(async () => {
  // Start Xvfb for headful browser
  const { spawn } = require('child_process');
  const xvfb = spawn('Xvfb', [':99', '-screen', '0', '1280x720x24', '-ac'], {
    detached: true,
    stdio: 'ignore'
  });
  
  process.env.DISPLAY = ':99';
  
  // Wait a bit for Xvfb to start
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
    // Go to SumoPod login
    console.log('Navigating to SumoPod...');
    await page.goto('https://sumopod.com/login', { waitUntil: 'load', timeout: 60000 });
    
    // Take screenshot of initial page
    await page.screenshot({ path: '/root/.openclaw/workspace/sumopod_1_login.png' });
    console.log('Screenshot saved: sumopod_1_login.png');
    
    // Find and fill email input
    console.log('Looking for email input...');
    const emailInput = await page.$('input[type="email"], input[name="email"], input[placeholder*="email" i]');
    if (emailInput) {
      await emailInput.fill('0xmultiserver@gmail.com');
      console.log('Email filled');
    } else {
      // Try to find any input field
      const inputs = await page.$$('input');
      console.log(`Found ${inputs.length} input fields`);
      for (let i = 0; i < inputs.length; i++) {
        const type = await inputs[i].getAttribute('type');
        const name = await inputs[i].getAttribute('name');
        const placeholder = await inputs[i].getAttribute('placeholder');
        console.log(`Input ${i}: type=${type}, name=${name}, placeholder=${placeholder}`);
      }
    }
    
    // Take screenshot after filling email
    await page.screenshot({ path: '/root/.openclaw/workspace/sumopod_2_filled.png' });
    console.log('Screenshot saved: sumopod_2_filled.png');
    
    // Find and click submit button
    const submitBtn = await page.$('button[type="submit"], button:has-text("Send"), button:has-text("Login"), button:has-text("Continue")');
    if (submitBtn) {
      await submitBtn.click();
      console.log('Submit clicked');
    }
    
    // Wait for OTP input to appear
    await page.waitForTimeout(2000);
    await page.screenshot({ path: '/root/.openclaw/workspace/sumopod_3_otp_page.png' });
    console.log('Screenshot saved: sumopod_3_otp_page.png');
    
    console.log('Waiting for OTP code...');
    console.log('PAGE_READY_FOR_OTP');
    
    // Keep browser open for manual OTP entry or API interaction
    await new Promise(r => setTimeout(r, 30000));
    
  } catch (error) {
    console.error('Error:', error.message);
    await page.screenshot({ path: '/root/.openclaw/workspace/sumopod_error.png' });
  }
  
  await browser.close();
  xvfb.kill();
  process.exit(0);
})();
