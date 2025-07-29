import time
from behave import given, when, then
from appiumfw.mobile_factory import MobileFactory
from appium.webdriver.common.appiumby import AppiumBy


@given('the mobile app is installed on Sauce Labs device')
def step_app_installed(context):
    factory = MobileFactory()
    context.driver = factory.create_driver("com.swaglabsmobileapp", "com.swaglabsmobileapp.MainActivity")
    time.sleep(10)  # Give app time to load
    context.driver.get_screenshot_as_file("login_page.png")

@when('the user enters username "{username}" and password "{password}"')
def step_enter_credentials(context, username, password):

    user_field = context.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Username")
    pass_field = context.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Password")

    user_field.send_keys(username)
    pass_field.send_keys(password)

    context.driver.get_screenshot_as_file("credentials_entered.png")


@when('the user taps the login button')
def step_tap_login(context):
    login_btn = context.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")
    login_btn.click()
    time.sleep(3)

@then('the home screen should be displayed')
def step_verify_home(context):
    try:
        home_el = context.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-PRODUCTS")
        assert home_el.is_displayed(), "Home screen not displayed"
        context.driver.get_screenshot_as_file("home_screen.png")
    finally:
        context.driver.quit()