import flet as ft
import sqlite3
controls_list = []


async def view(db: sqlite3.Connection, page_: ft.Page):
    cursor = db.cursor()

    async def logout(e):
        page_.session.clear()
        await page_.go_async("/")

    async def add_guest(e):
        async def close_dlg(e):
            dlg.open = False
            await page_.update_async()
        
        async def add_guest_db(e):
            cursor.execute(f'''INSERT INTO guests(first_name, last_name) VALUES(?, ?)''', (name_field.value, familia_field.value))
            db.commit()
            dlg.open = False
            await page_.update_async()

        name_field = ft.TextField(label="Имя")
        familia_field = ft.TextField(label="Фамилия")

        dlg = ft.AlertDialog(modal=True, 
                             title=ft.Text("Добавить Постояльца"),
                             content=ft.Column(controls=[name_field,
                                                         familia_field,
                             ], alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 tight=True),
                             actions=[ft.TextButton(text="Далее", on_click=add_guest_db), ft.TextButton(text="Отмена", on_click=close_dlg)])
        
        dlg.open = True
        page_.dialog = dlg
        await page_.update_async()

    async def add_reservation(e):
        global controls_list
        print("add_reservation")
        guest_id = None

        async def close_dlg(e):
            dlg.open = False
            await page_.update_async()
            
        async def close_anchor(e):
            text = f"Color {e.control.data}"
            print(f"closing view from {text}")
            guests_selection_dates.close_view(text)

        controls_list = []
        async def get_id(e):
            pass
        
        class Guest:
            def __init__(self, id, first_name, last_name):
                self.id = id
                self.first_name = first_name
                self.last_name = last_name

            def get_id(self, e):
                global guest_id
                guest_id = self.id

            def get_control(self):
                return ft.ListTile(title=ft.Text(f"{self.first_name} {self.last_name}"), on_click=self.get_id)

        for i in cursor.execute(f'''SELECT * FROM guests''').fetchall():
            controls_list.append(Guest(i[0], i[1], i[2]).get_control())
        async def search(e):
            global controls_list
            print(controls_list)
            new_list = []
            for i in controls_list:
                if i.title.value.startswith(guests_selection_dates.value):
                    new_list.append(i)
            controls_list = new_list
            print(controls_list)
            guests_selection_dates.controls = controls_list
            await guests_selection_dates.update_async()
            await page_.update_async()

        guests_selection_dates = ft.SearchBar(
            view_elevation=4,
            divider_color=ft.colors.AMBER,
            bar_hint_text="Поиск постояльца...",
            view_hint_text="Выберите постояльца из списка...",
            # on_change = search,
            view_leading=ft.IconButton(icon=ft.icons.SEARCH, on_click=search),
            # on_submit = lambda e: print("submit"),
            # on_tap= ,
            controls=controls_list 
            #    controls=[
            # ft.ListTile(title=ft.Text(f"Color {i}"), on_click=close_anchor, data=i) for i in range(10)
    

        ) 

        # rooms_selection = 


        dlg = ft.AlertDialog(modal=True, 
                            title=ft.Text("Добавить Постояльца"),
                            content=ft.Column(controls=[guests_selection_dates]),
                            actions=[ft.TextButton(text="Далее"), ft.TextButton(text="Отмена", on_click=close_dlg)])
        page_.dialog = dlg
        dlg.open = True
        await page_.update_async()

    view_ = ft.View("/main", [ 
        ft.Row(controls=[ft.FilledButton(text="Добавить Постояльца", on_click=add_guest),
                         ft.FilledButton(text="Заселить постояльца", on_click=add_reservation),
                         ft.FilledButton(text="Выселить постояльца"),
                         ft.FilledButton(text="Свободные номера")
                         ])
         ])

    view_.appbar = ft.AppBar(leading=ft.Icon(ft.icons.HOTEL), title=ft.Text("Hostel"),
                             bgcolor=ft.colors.SURFACE_VARIANT,
                             actions=[ft.IconButton(icon=ft.icons.LOGOUT, on_click=logout),ft.IconButton(icon=ft.icons.HELP_OUTLINE)])

    return view_
