from playwright.sync_api import sync_playwright


class Browser:
    def __init__(self, page):
        self.page = page

    def login(self, mail, password):
        self.page.goto('https://business.kazanexpress.ru/seller/signin')
        self.page.locator('#username').fill(mail)
        self.page.locator('#password').fill(password)
        self.page.locator('[data-test-id="button__next"]').click()
        self.page.wait_for_timeout(5000)


def get_token(login: str, password: str) -> str | None:
    """ Получить JWT токен """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.set_default_timeout(60000)
            token = None

            def handle_request(route, request):
                nonlocal token
                headers = request.headers
                if 'authorization' in headers and 'Bearer' in headers['authorization']:
                    token = headers['authorization'].split()[-1]
                # Продолжаем загрузку страницы
                route.continue_()

            page.route("**/*", handle_request)

            driver = Browser(page)
            driver.login(login, password)
            context.close()
            browser.close()
            return token
    except:
        browser.close()
        return None
