from linkedin_scraper import Person, actions
from selenium import webdriver
driver = webdriver.Chrome()

email = "some-email@email.address"
password = "password123"
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
person = Person("https://www.linkedin.com/in/andre-iguodala-65b48ab5", driver=driver)