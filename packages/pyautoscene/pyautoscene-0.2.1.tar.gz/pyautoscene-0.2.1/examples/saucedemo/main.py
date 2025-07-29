import pyautogui as gui

from pyautoscene import ImageElement, Scene, Session, TextElement
from pyautoscene.utils import locate_and_click

login = Scene(
    "Login",
    elements=[
        TextElement("Username", region="x-1/3 y-(1-2)/3"),
        TextElement("Password", region="x-1/3 y-(2-3)/3"),
        # ReferenceImage("examples/saucedemo/references/login_button.png"),
    ],
    initial=True,
)

dashboard = Scene(
    "Dashboard",
    elements=[
        TextElement("Swag Labs", region="x-2/3 y-1/3"),
        TextElement("Products", region="x-1/3 y-1/3"),
    ],
)

cart = Scene(
    "Cart",
    elements=[
        TextElement("Your Cart", region="x-1/3 y-1/3"),
        ImageElement("examples/saucedemo/references/cart_icon.png"),
    ],
)


@login.action(transitions_to=dashboard)
def perform_login(username: str, password: str):
    """Performs the login action to transition from Login to Dashboard."""
    locate_and_click("examples/saucedemo/references/username.png")
    gui.write(username, interval=0.1)
    gui.press("tab")
    gui.write(password, interval=0.1)
    gui.press("enter")


@dashboard.action()
def add_products_to_cart(target: str):
    """Adds products to the cart."""
    locate_and_click(f"examples/saucedemo/references/{target}.png")
    locate_and_click("examples/saucedemo/references/add_to_cart_button.png")


@dashboard.action(transitions_to=cart)
def view_cart():
    """Views the cart."""
    locate_and_click("examples/saucedemo/references/cart_icon.png")


@cart.action()
def checkout():
    """Checks out the items in the cart."""
    locate_and_click("examples/saucedemo/references/checkout_button.png")


session = Session(scenes=[login, dashboard, cart])

gui.hotkey("alt", "tab")
session.expect(dashboard, username="standard_user", password="secret_sauce")
session.invoke("add_products_to_cart", target="backpack")
session.invoke("view_cart")
session.invoke("checkout")
