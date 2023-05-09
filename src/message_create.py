
from message_template import MessageTemplate


class CreateMessage(MessageTemplate):

    def __init__(self, parent):
        super().__init__(parent)

        self.confirm_button.configure(
            command=lambda: [self.create_message(), self.destroy()],
            text=self.parent.get_region_text('create_message_short'))
        self.heading_label.configure(text=self.parent.get_region_text('create_message'))

    def create_message(self):

        self.parent.db.dbCursor.execute("""
            INSERT INTO message_of_the_day (message)
            VALUES (%s)
        """, self.get_data())
