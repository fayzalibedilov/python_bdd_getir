from behave import given, when, then, step
from BDDcommon import webcommon


# start of step definitions
@step("I go to '{page}' page")
@given('I go to the site "{page}"')
def go_to_page(context, page):

    print("Navigating to the page: {}".format(page))

    webcommon.go_to(context, page)


@then('the page title should be "{expected_title}"')
def verify_homepage_title(context, expected_title):

    webcommon.assert_page_title(context, expected_title)


@then('the page url should be "{expected_url}"')
def verify_homepage_title(context, expected_url):

    webcommon.assert_current_url(context, expected_url)

