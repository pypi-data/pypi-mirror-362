from common_utils.web.cookies_handler import CookiesManager, LoginData, LoginSelectors


url = "https://web.budgetbakers.com/records"


class BudgetBakerHandler:
    cookies_manager = CookiesManager(
        login_data=LoginData(
            username_env="BUDGETBAKER_EMAIL",
            password_env="BUDGETBAKER_PASSWORD",
            sign_in_url="https://web.budgetbakers.com/login",
            selectors=LoginSelectors(
                username='input[name=email]',
                password='input[name=password]',
                login_button='button'
            )
        ),
        test_cookies_url="https://web.budgetbakers.com/records",
        test_cookies_response_fn=lambda data: "errorCode" not in data,
        min_num_cookies=5
    )

    def __init__(self):
        self.cookies = self.cookies_manager.get_cookies()
        self.headers = {"Cookie": self.cookies}

        raise NotImplementedError
