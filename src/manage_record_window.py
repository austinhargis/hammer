from languages import *
from record_info_template import RecordInfoTemplate


class ManageRecordWindow(RecordInfoTemplate):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.heading_label.configure(
            text=self.parent.get_region_text('item_manage_heading'))
        self.func_button.configure(
            text=self.parent.get_region_text('prompt_save_changes'),
            command=lambda: [self.commit_changes()])

        self.type_text.bind('<Return>', lambda event: self.commit_changes())

        self.entry_id = None

        self.fill_entries()

    def commit_changes(self):
        self.parent.db.dbCursor.execute(f"""
            UPDATE item_record 
            SET title=%s, author=%s, description=%s, publish_date=%s, type=%s
            WHERE id={self.entry_id}""", self.get_item_info())

        self.parent.db.dbConnection.commit()

        self.parent.home_tab.refresh_table()
        self.parent.tab_controller.select(0)
        self.destroy()

    def fill_entries(self):
        current_item = self.parent.tree.focus()
        self.entry_id = self.parent.tree.item(current_item)['values'][0]

        self.parent.db.dbCursor.execute(f"""
            SELECT * FROM item_record
            WHERE id=%s
        """, (self.entry_id,))
        item_row = self.parent.db.dbCursor.fetchall()

        self.title_text.insert(0, item_row[0][1])
        self.author_text.insert(0, item_row[0][2])
        self.description_text.insert('1.0', item_row[0][7])
        self.publish_date_text.insert(0, str(item_row[0][3]))
        self.type_text.insert(0, str(item_row[0][4]))
