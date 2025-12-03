import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time


@pytest.fixture
def manage_driver():
    print("Starting and getting driver...")
    service = Service(executable_path="tests/msedgedriver.exe")
    driver = webdriver.Edge(service=service)
    driver.get("http://localhost:5173/login")

    print("Driver acquired")
    yield driver

    time.sleep(3)
    print("Quitting driver...")
    driver.quit()
    print("Driver quitted")
