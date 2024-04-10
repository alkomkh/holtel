import flet as ft
import flet_fastapi
import sqlite3
import login_page, main_page


database = sqlite3.connect("database.db")


async def main(page: ft.Page):
    async def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [

                ],
            )
        )
        if page.session.get("login"):
            await page.go_async("/main")
        else:
            await page.go_async("/login")
        match page.route:
            case "/":
                pass
            case "/login":
                page.views.append(await login_page.view(database, page))
            case "/main":
                page.views.append(await main_page.view(database, page))

        await page.update_async()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    await page.go_async(page.route)


app = flet_fastapi.app(main, secret_key="MY_TEST_SECRET_KEY")