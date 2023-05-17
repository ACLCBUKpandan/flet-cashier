import flet as ft
from views.AppPage import AppPage
from views.LoginPage import LoginPage
from views.CreatePage import CreatePage
from views.DashboardPage import DashboardPage
from views.HistoryPage import HistoryPage


def main(page: ft.Page):

    pages: list[AppPage] = [
        LoginPage(root=page, route='/'),
        DashboardPage(root=page, route='/dashboard'),
        CreatePage(root=page, route='/create'),
        HistoryPage(root=page, route='/history'),
        # Register your pages here
    ]

    page.title = "App"

    theme = ft.Theme(
        color_scheme_seed=ft.colors.GREEN,
        use_material3=True
    )

    page.theme = theme
    page.dark_theme = theme
    page.theme_mode = ft.ThemeMode.DARK

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def route_change(_):
        page.views.clear()
        print(pages[0].page.route)

        sel = tuple(filter(lambda x: x.page.route == page.route, pages))
        page.views.append(sel[0].get_page())
        page.go(sel[0].page.route)

    page.on_route_change = route_change
    page.go(page.route)
