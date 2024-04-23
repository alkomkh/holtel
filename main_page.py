import flet as ft
import sqlite3
import datetime

controls_list = []


async def view(db: sqlite3.Connection, page_: ft.Page):
    cursor = db.cursor()

    async def logout(e):
        page_.session.clear()
        await page_.go_async("/")

    data_columns = []
    data_columns.append(ft.DataColumn(ft.Text("Номер")))
    date_list = []
    date_now = datetime.datetime.now()

    date = date_now

    for i in range(30):
        date = date_now + datetime.timedelta(days=i)
        data_columns.append(ft.DataColumn(ft.Text(date.date())))
        date_list.append(date)

    rooms = cursor.execute(f"""SELECT * FROM rooms""").fetchall()
    rows = []
    for room in rooms:
        cells_list = []
        cells_list.append(ft.DataCell(ft.Text(value=room[0])))
        for i in date_list:
            date_str = i.strftime('%Y-%m-%d %H:%M:%S')
            res = cursor.execute(
                f"""SELECT * FROM reservations WHERE room_id = ? AND start_date <= ? AND finish_date >= ?""",
                (room[0], date_str, date_str)).fetchall()
            if res:
                cells_list.append(ft.DataCell(content=ft.Text("Занято", bgcolor=ft.colors.RED)))
            else:
                cells_list.append(ft.DataCell(content=ft.Text("Свободно", bgcolor=ft.colors.GREEN)))

        rows.append(ft.DataRow(cells=cells_list))

    table = ft.DataTable(
        columns=data_columns,
        rows=rows
        # width=page_.width
    )

    async def add_res(e):

        async def add(e):
            cursor.execute(
                f"""INSERT INTO reservations (room_id, start_date, finish_date, name, surname, passport) VALUES (?, ?, ?, ?, ?, ?)""",
                (room_id_field.value, date_first.value, date_last.value, name_field.value, surname_field.value,
                 passport_field.value))
            db.commit()
            dlg.open = False
            await page_.go_async("/")

        async def close(e):
            dlg.open = False
            await page_.update_async()

        name_field = ft.TextField(label="Имя")
        surname_field = ft.TextField(label="Фамилия")
        passport_field = ft.TextField(label="Паспортные данные")
        room_id_field = ft.TextField(label="Номер номера")

        date_first = ft.DatePicker(first_date=datetime.datetime.now(),
                                   last_date=datetime.datetime.now() + datetime.timedelta(days=30))
        date_last = ft.DatePicker(first_date=datetime.datetime.now(),
                                  last_date=datetime.datetime.now() + datetime.timedelta(days=30))
        page_.overlay.append(date_first)
        page_.overlay.append(date_last)
        date_first_text = ft.Text("")
        date_last_text = ft.Text("")

        async def first_date_text_change(e):
            pass

        async def first_callback(e):
            await date_first.pick_date_async()

        async def last_callback(e):
            await date_last.pick_date_async()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Добавит бронирование"),
            content=ft.Column(controls=[
                name_field,
                surname_field,
                passport_field,
                room_id_field,
                ft.TextButton("Выбрать дату начала", on_click=first_callback),
                ft.TextButton("Выбрать дату конца", on_click=last_callback)

            ]),
            actions=[ft.TextButton(text="Добавить", on_click=add), ft.TextButton(text="Отмена", on_click=close)])

        dlg.open = True
        page_.dialog = dlg
        await page_.update_async()


    async def change_end_reservation_date(e):
        class TableRow:
            def __init__(self, id, room_id, start_date, finish_date, name, surname, passport):
                self.id = id
                self.room_id = room_id
                self.start_date = start_date
                self.finish_date = finish_date
                self.name = name
                self.surname = surname
                self.passport = passport
                self.button = ft.IconButton(icon=ft.icons.DELETE, on_click=self.del_res)
                
            async def del_res(self, e):
                cursor.execute(f"""UPDATE reservations SET finish_date = '{date_now}' WHERE id = {self.id}""")
                db.commit()
                end_reservation_dialog.open = False
                await page_.go_async("/")
                
            async def get_row(self):
                res_cells_list = [ft.DataCell(ft.Text(self.room_id)),
                                  ft.DataCell(ft.Text(self.surname)),
                                  ft.DataCell(ft.Text(self.name)),
                                  ft.DataCell(ft.Text(self.passport)),
                                  ft.DataCell(ft.Text(self.start_date)),
                                  ft.DataCell(ft.Text(self.finish_date)),
                                  ft.DataCell(self.button)]
                return ft.DataRow(cells=res_cells_list)
            
        async def close_res(e):
            end_reservation_dialog.open = False
            await page_.update_async()
            
        res = cursor.execute(f"""SELECT * FROM reservations WHERE finish_date >= ?""", (date_now.strftime('%Y-%m-%d %H:%M:%S'),)).fetchall()
        res_rows = []

        for req in res:
            res_rows.append(await TableRow(req[0],req[1],req[2],req[3],req[4],req[5],req[6],).get_row())
        
        res_culumns = [ft.DataColumn(ft.Text("Номер номера")),
                       ft.DataColumn(ft.Text("Фамилия постояльца")),
                       ft.DataColumn(ft.Text("Имя постояльца")),
                       ft.DataColumn(ft.Text("Паспортные данные постояльца")),
                       ft.DataColumn(ft.Text("Дата заселения")),
                       ft.DataColumn(ft.Text("Дата выселения")),
                       ft.DataColumn(ft.Text(""))]
        


        res_table = ft.DataTable(
                columns=res_culumns,
                rows=res_rows
        )

        end_reservation_dialog = ft.AlertDialog(modal=True, 
                             title=ft.Text("Выселение"),
                             content=res_table,
                             actions=[ft.TextButton(text="закрыть", on_click=close_res)])


        page_.dialog = end_reservation_dialog
        end_reservation_dialog.open=True
        await page_.update_async()
    
    # page_.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_res)

    # # async def add_guest(e):
    # #     async def close_dlg(e):
    # #         dlg.open = False
    # #         await page_.update_async()

    # #     async def add_guest_db(e):
    # #         cursor.execute(f'''INSERT INTO guests(first_name, last_name) VALUES(?, ?)''', (name_field.value, familia_field.value))
    # #         db.commit()
    # #         dlg.open = False
    # #         await page_.update_async()

    # #     name_field = ft.TextField(label="Имя")
    # #     familia_field = ft.TextField(label="Фамилия")

    # #     dlg = ft.AlertDialog(modal=True, 
    # #                          title=ft.Text("Добавить Постояльца"),
    # #                          content=ft.Column(controls=[name_field,
    # #                                                      familia_field,
    # #                          ], alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    # #                              tight=True),
    # #                          actions=[ft.TextButton(text="Далее", on_click=add_guest_db), ft.TextButton(text="Отмена", on_click=close_dlg)])

    # #     dlg.open = True
    # #     page_.dialog = dlg
    # #     await page_.update_async()

    # async def add_reservation(e):
    #     # global controls_list
    #     # guest_id = None

    #     async def close_dlg(e):
    #         dlg.open = False
    #         await page_.update_async()

    #     # controls_list = []

    #     # class Guest:
    #     #     def __init__(self, id, first_name, last_name):
    #     #         self.id = id
    #     #         self.first_name = first_name
    #     #         self.last_name = last_name

    #     #     def get_id(self, e):
    #     #         global guest_id
    #     #         guest_id = self.id

    #     #     def get_control(self):
    #     #         return ft.ListTile(title=ft.Text(f"{self.first_name} {self.last_name}"), on_click=self.get_id)

    #     # for i in cursor.execute(f'''SELECT * FROM guests''').fetchall():
    #     #     controls_list.append(Guest(i[0], i[1], i[2]).get_control())
    #     # async def search(e):
    #     #     global controls_list
    #     #     print(controls_list)
    #     #     new_list = []
    #     #     for i in controls_list:
    #     #         if i.title.value.startswith(guests_selection_dates.value):
    #     #             new_list.append(i)
    #     #     controls_list = new_list
    #     #     print(controls_list)
    #     #     guests_selection_dates.controls = controls_list
    #     #     await guests_selection_dates.update_async()
    #     #     await page_.update_async()

    #     # guests_selection_dates = ft.SearchBar(
    #     #     view_elevation=4,
    #     #     divider_color=ft.colors.AMBER,
    #     #     bar_hint_text="Поиск постояльца...",
    #     #     view_hint_text="Выберите постояльца из списка...",
    #     #     # on_change = search,
    #     #     view_leading=ft.IconButton(icon=ft.icons.SEARCH, on_click=search),
    #     #     # on_submit = lambda e: print("submit"),
    #     #     # on_tap= ,
    #     #     controls=controls_list)

    #     First_Name =  

    #     dlg = ft.AlertDialog(modal=True, 
    #                         title=ft.Text("Добавить бронирование"),
    #                         content=ft.Column(controls=[guests_selection_dates]),
    #                         actions=[ft.TextButton(text="Далее"), ft.TextButton(text="Отмена", on_click=close_dlg)])
    #     page_.dialog = dlg
    #     dlg.open = True
    #     await page_.update_async()

    view_ = ft.View("/main", [ft.Row(controls=[table], scroll=ft.ScrollMode.ALWAYS)])

    # view_.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_res)
    # view_.floating_action_button = ft.PopupMenuButton(items=[
    #     ft.PopupMenuItem(content=ft.TextButton(text="Добавить бронирование", on_click=add_res )),
    #     ft.PopupMenuItem(content=ft.TextButton(text="Выселить постояльца", on_click=change_end_reservation_date)),
    # ])

    view_.appbar = ft.AppBar(leading=ft.Icon(ft.icons.HOTEL), title=ft.Text("Система учета занятых номеров"),
                             bgcolor=ft.colors.SURFACE_VARIANT,
                             actions=[ft.TextButton(text="Добавить бронирование", on_click=add_res),
                                      ft.TextButton(text="Выселить досрочно", on_click=change_end_reservation_date),
                                      ft.IconButton(icon=ft.icons.LOGOUT, on_click=logout),
                                      ft.IconButton(icon=ft.icons.HELP_OUTLINE)])

    return view_
