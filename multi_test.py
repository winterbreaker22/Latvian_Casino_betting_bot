from playwright.sync_api import sync_playwright
from threading import Thread
import time

shared_variable = None

def run_first_browser(playwright):
    global shared_variable
    
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://example.com/first-url")

    while True:
        # Check for some condition on the page (e.g., element appears or text changes)
        if page.locator("selector-for-variable").is_visible():
            shared_variable = page.locator("selector-for-variable").inner_text()
            print(f"Shared variable updated to: {shared_variable}")
            break

        time.sleep(1)  # Polling delay

    # Keep the browser open for further actions or close it
    browser.close()

# Function to run the second browser and react to the shared variable
def run_second_browser(playwright):
    global shared_variable
    
    # Launch second browser instance
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Navigate to the second URL
    page.goto("https://example.com/second-url")

    # Wait for the shared variable to be updated
    while shared_variable is None:
        print("Waiting for the shared variable to be updated...")
        time.sleep(1)

    # Perform some action based on the shared variable
    if shared_variable:
        print(f"Performing action in the second browser with variable: {shared_variable}")
        page.fill("selector-for-input", shared_variable)
        page.click("selector-for-submit")

    # Keep the browser open for further actions or close it
    browser.close()

# Main function to run both browsers simultaneously
def main():
    with sync_playwright() as playwright:
        # Start the first browser in a separate thread
        thread1 = Thread(target=run_first_browser, args=(playwright,))
        thread1.start()

        # Start the second browser in the main thread
        run_second_browser(playwright)

        # Wait for the first thread to complete
        thread1.join()

if __name__ == "__main__":
    main()
