from tkinter import ttk

from languages import *
from record_info_template import RecordInfoTemplate


class ManageRecordWindow(RecordInfoTemplate):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.heading_label.configure(
            text=languages[self.parent.save_m.data['language']]['iteminfo']['item_manage_heading'])

        self.entry_id = None

        self.fill_entries()

        ttk.Button(self.button_frame,
                   text=languages[self.parent.save_m.data['language']]['prompts']['prompts_save_changes'],
                   command=lambda: [self.commit_changes(self.get_item_info(), self.entry_id),
                                    self.parent.refresh_table(),
                                    self.parent.tab_controller.select(0),
                                    self.destroy()]).pack(side='left')

    def commit_changes(self, data, row_id):
        self.parent.db.dbCursor.execute(f"""
            UPDATE item_record 
            SET title=?, author=?, description=?, publish_date=?, type=?
            WHERE id={row_id}""", data)

        self.parent.db.dbConnection.commit()

    def fill_entries(self):
        current_item = self.parent.tree.focus()
        self.entry_id = self.parent.tree.item(current_item)['values'][0]

        item_row = self.parent.db.dbCursor.execute(f"""
            SELECT * FROM item_record
            WHERE id=?
        """, (self.entry_id,)).fetchall()

        self.title_text.insert(0, item_row[0][1])
        self.author_text.insert(0, item_row[0][2])
        self.description_text.insert('1.0', item_row[0][7])
        self.publish_date_text.insert(0, str(item_row[0][3]))
        self.type_text.insert(0, str(item_row[0][4]))