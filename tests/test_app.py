from conftest import manage_driver, webdriver, By, time


def test_login(manage_driver: webdriver.Edge):
    email_input = manage_driver.find_element(By.ID, "email")
    pass_input = manage_driver.find_element(By.ID, "password")
    login_btn = manage_driver.find_element(By.ID, "login")

    email_input.send_keys("drewbrandon185@gmail.com")
    pass_input.send_keys("Flubb3r")
    login_btn.click()

    time.sleep(2)
    assert manage_driver.current_url == "http://localhost:5173/profile"
