import flet as ft


def NavRail(index=0):
    return ft.NavigationRail(
        selected_index=index,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.DASHBOARD,
                label="DASHBOARD"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.ADD,
                label="CREATE"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.BOOK,
                label="HISTORY"
            ),
        ]
    )
