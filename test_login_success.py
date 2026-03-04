from playwright.sync_api import expect

def test_login_success(page):
    # Set default timeouts
    page.set_default_timeout(60000)
    page.set_default_navigation_timeout(60000)

    print("Navigating to https://beta-customer.8ten.cloud/login-by-email ...")
    try:
        page.goto("https://beta-customer.8ten.cloud/login-by-email", wait_until='domcontentloaded')
    except Exception as e:
        print("Goto timeout, but we will try to proceed...", e)

    print("Waiting for page inputs...")
    email_locator = page.locator("[data-testid='email'] input, input[name='email_address']").first
    try:
        email_locator.wait_for(state="attached", timeout=30000)
    except Exception as e:
        print("Email input not found:", e)
        print("Page URL:", page.url)
        print("Page Title:", page.title())
        page.screenshot(path="debug_screenshot.png")
        raise e

    print("Filling email...")
    email_locator.fill("danny_topup@wnesolutions.sg")

    print("Filling password...")
    password_locator = page.locator("input[type='password'], input[name='password'], input[placeholder*='password' i], input[placeholder*='Password']").first
    password_locator.fill("12121992")

    print("Checking 'Terms of Service' box...")
    checkbox = page.locator("input[type='checkbox']")
    if checkbox.count() > 0:
        checkbox.first.check(force=True)
    else:
        label = page.locator("label:has-text('Terms of Service'), text='Terms of Service', label:has-text('terms')").first
        if label.count() > 0:
            label.click()

    print("Clicking Log In button...")
    button_locator = page.locator("button[type='submit'], button:has-text('Log In'), button:has-text('Login')").first
    button_locator.click()

    print("Waiting for 'Tenant Overview' dashboard appears...")
    try:
        page.wait_for_url("**/overview", timeout=30000)
        print("Success: 'Tenant Overview' dashboard is visible (URL is /overview).")
    except Exception as e:
        print("Verification failed. Current URL:", page.url)
        print("Page Title:", page.title())
        page.screenshot(path="debug_screenshot_overview.png")
        raise e
