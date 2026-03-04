from playwright.sync_api import sync_playwright

def run(playwright):
    print("Launching browser...")
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    print("Navigating to https://beta-customer.8ten.cloud/login-by-email ...")
    page.goto("https://beta-customer.8ten.cloud/login-by-email", wait_until='commit', timeout=60000)

    print("Entering email...")
    # Try common selectors for the email input
    email_locator = page.locator("input[type='email'], input[name='email'], input[placeholder*='email' i], input[placeholder*='Email']")
    try:
        email_locator.first.fill("danny_topup@wnesolutions.sg", timeout=15000)
    except Exception as e:
        print("Failed to find email input. Available inputs on page:")
        try:
            inputs = page.evaluate("Array.from(document.querySelectorAll('input, button')).map(e => e.outerHTML)")
            for i in inputs:
                print(i)
        except:
            pass
        raise e

    print("Clicking login button...")
    # Try common selectors for the login/submit button
    button_locator = page.locator("button[type='submit'], button:has-text('Login'), button:has-text('Log In'), button:has-text('Submit'), button:has-text('Continue')")
    button_locator.first.click()

    print("Waiting 5 seconds to observe the result...")
    page.wait_for_timeout(5000)

    # ---------------------
    context.close()
    browser.close()
    print("Done!")

with sync_playwright() as playwright:
    run(playwright)
