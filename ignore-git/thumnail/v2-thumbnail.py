from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

options = Options()
options.headless = True
options.add_argument("--window-size=720,500")  # Adjust height if content grows

driver = webdriver.Edge(options=options)
driver.get("file:///C:/Users/123/yt-automation/Eleven-Labs-API-Exploit/thumnail/thumbnail.html")

# Hold for 5 seconds
time.sleep(5)

driver.save_screenshot("post.png")
driver.quit()