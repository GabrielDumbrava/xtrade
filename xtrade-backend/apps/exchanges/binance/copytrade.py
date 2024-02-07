"""Helper functions that deal with copy trading at Binance."""

import logging
from typing import Any

from copytrade.models import LeadTrader
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger("copytrade")


def get_leader_profile(leader: LeadTrader, dry_run: bool = False) -> dict | str:
    """Update lead trader profile. Also trigger signal if new slots are available."""

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)
    driver.get(leader.profile_url)
    profile: dict[str, Any] = {}
    if not leader.profile_url:
        logger.error(
            "The leader does not have a profile url: [%s] %s", leader.pk, leader.name
        )
        return profile

    try:
        selector = (
            "#__APP > div.css-543u2k > div.css-1j4uji3 > div.portfolio-header.css-vurnku > div > "
            "div.css-avpl4z > div.css-1hythwr > div > div.optarea-wrap.css-vurnku > div > div:nth-child(1) "
            "> button"
        )
        WebDriverWait(driver, 15).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

        # Enable JavaScript by setting the appropriate flag
        driver.execute_script("return navigator.userAgent")

        # Get the page source after scrolling
        page_source = driver.page_source

        # Parse the page source with Beautiful Soup
        soup = BeautifulSoup(page_source, "html.parser")
        if dry_run:
            print(soup.prettify())
        try:
            copiers_tag = soup.find_all("div", string="Copiers")[0]
            seats_tag = copiers_tag.find_next_sibling("div").text
            if seats_tag == "--":
                # We could not get the info. Log it.
                logger.error(
                    "Could not get number of copiers for [%s] %s",
                    leader.pk,
                    leader.name,
                )
            else:
                seats = seats_tag.split("/")
                profile["copiers"] = int(seats[0])
                profile["seats"] = int(seats[1])
        except IndexError:
            pass
        try:
            minimum_amount = soup.find_all("div", string="Minimum Copy Amount")[0]
            min_tag = minimum_amount.find_next_sibling("div").text
            if min_tag == "--":
                logger.error(
                    "Could not get minimum amount for [%s] %s", leader.pk, leader.name
                )
            else:
                profile["minimum_amount"] = min_tag
        except IndexError:
            pass

    except TimeoutException:
        logger.error(
            "Timeout when trying to fetch profile for leader: [%s] %s",
            leader.pk,
            leader.name,
        )
    finally:
        driver.quit()

    return profile
