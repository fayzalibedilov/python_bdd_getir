from selenium import webdriver
import url_config
import time
import logging as logger


def go_to(context, location, **kwargs):

    if not location.startswith('http'):
        _url = url_config.URLCONFIG.get(location)
        base_url = url_config.URLCONFIG.get('base_url')
        url = base_url + _url

    browser = context.config.userdata.get('browser')
    if not browser:
        browser = 'chrome'

    if browser.lower() == 'chrome':
        context.driver = webdriver.Chrome()
    elif browser.lower() == 'headlesschrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        context.driver = webdriver.Chrome(options=options)
    elif browser.lower() in ('ff', 'firefox'):
        context.driver = webdriver.Firefox()
    else:
        raise Exception("The browser type '{}' is not supported".format(context))

    # adding implicit wait
    wait = kwargs['implicitly_wait'] if 'implicitly_wait' in kwargs.keys() else 15
    context.driver.implicitly_wait(wait)
    # clean the urk and go to the url
    # import pdb; pdb.set_trace()
    url = url.strip()
    logger.info("222222")
    logger.info(f"Navigating to URL: {url}")
    # url = 'https://' + url
    context.driver.get(url)


def assert_page_title(context, expected_title):

    actual_title = context.driver.title

    print("The actual title is: {}".format(actual_title))
    print("The expected title is: {}".format(expected_title))

    assert expected_title == actual_title, "The title is not as expected." \
                                           "Expected: {}, Actual: {}".format(expected_title, actual_title)

    print("The page title is as expected.")


def assert_current_url(context, expected_url):

    current_url = context.driver.current_url

    if not expected_url.startswith('http') or not expected_url.startswith('https'):
        expected_url = 'https://' + expected_url + '/'

    assert current_url == expected_url, "The current url is not as expected." \
                                        " Actual: {}, Expected: {}".format(current_url, expected_url)

    print("The page url is as expected.")


def url_contains(context, text):

    current_url = context.driver.current_url
    if text in current_url:
        return True
    else: return False


def assert_url_contains(context, text):

    contains = url_contains(context, text)
    assert contains, f"Current url '{context.driver.current_url}' does not contain test '{text}'."


def find_element(context, locator_attribute, locator_text):

    possible_locators = ["id", "xpath", "link text", "partial link text", "name", "tag name",
                         "class name", "css selector"]

    if locator_attribute not in possible_locators:
        raise Exception('The locator attribute provided is not in the approved attributes. Or the spelling and '
                        'The approved attributes are: {} '.format(possible_locators))
    try:
        element = context.driver.find_element(locator_attribute, locator_text)
        return element
    except Exception as e:
        raise Exception(e)


def find_elements(context, locator_attribute, locator_text):

    possible_locators = ["id", "xpath", "link text", "partial link text", "name", "tag name",
                         "class name", "css selector"]

    if locator_attribute not in possible_locators:
        raise Exception('The locator attribute provided is not in the approved attributes. Or the spelling and '
                        'The approved attributes are: {} '.format(possible_locators))
    try:
        element = context.driver.find_elements(locator_attribute, locator_text)
        return element
    except Exception as e:
        raise Exception(e)


def is_element_visible(element):

    if element.is_displayed():
        return True
    else:
        return False


def assert_element_visible(context_or_element, locator_att=None, locator_text=None):

    if isinstance(context_or_element, webdriver.remote.webelement.WebElement):
        element = context_or_element
    else:
        element = context_or_element.driver.find_element(locator_att, locator_text)

    if not element.is_displayed():
        raise AssertionError("The element is not displayed")


def type_into_element(context_or_element, input_value, locator_att, locator_text):

    if isinstance(context_or_element, webdriver.remote.webelement.WebElement):
        input_field = context_or_element
    else:
        input_field = context_or_element.driver.find_element(locator_att, locator_text)

    input_field.send_keys(input_value)


def click(context_or_element, locator_att=None, locator_text=None):

    if isinstance(context_or_element, webdriver.remote.webelement.WebElement):
        element = context_or_element
    else:
        element = context_or_element.driver.find_element(locator_att, locator_text)

    element.click()


def element_contains_text(context_or_element, expected_text, locator_att, locator_text, case_sensitive=False):

    if isinstance(context_or_element, webdriver.remote.webelement.WebElement):
        element = context_or_element
    else:
        element = context_or_element.driver.find_element(locator_att, locator_text)

    element_text = element.text
    if not case_sensitive:
        if expected_text.lower() in element_text.lower():
            return True
        else:
            return False
    else:
        return True if expected_text in element_text else False


def assert_element_contains_text(context_or_element, expected_text, locator_att, locator_text, case_sensitive=False):

    max_try = 5
    sleep_bn_try = 2
    for i in range(max_try):
        try:
            contains = element_contains_text(context_or_element, expected_text, locator_att, locator_text, case_sensitive)
            assert contains, "Element does not contain text"
            break
        except AssertionError:
            print(f"Checking if element contains text. Retry number: {i}")
            time.sleep(sleep_bn_try)
    else:
        raise Exception(f"Element with locator type '{locator_att}' and locator text '{locator_text}',"
                        f" does not contain the text '{expected_text}'. Retried {max_try * sleep_bn_try} seconds.")


def assert_radio_selected(context_or_element, locator_att=None, locator_text=None):

    if isinstance(context_or_element, webdriver.remote.webelement.WebElement):
        element = context_or_element
    else:
        element = context_or_element.driver.find_element(locator_att, locator_text)

    is_checked = element.get_attribute('checked')
    assert is_checked, f"The radio is not selected {element.get_attribute('name')}."


def get_element_text(context_or_element, locator_att=None, locator_text=None):

    if isinstance(context_or_element, webdriver.remote.webelement.WebElement):
        element_text = context_or_element.text
    else:
        element = context_or_element.driver.find_element(locator_att, locator_text)
        element_text = element.text

    return element_text
