from qtpy.QtWidgets import QMessageBox, QWidget


def display_warning(widget: QWidget, title: str, message: str) -> bool:
    """
    Display a warning in a pop-up that can be accepted or dismissed
    """
    message_reply = QMessageBox.question(
        widget,
        title,
        message,
        QMessageBox.Yes | QMessageBox.Cancel,
    )
    if message_reply == QMessageBox.Yes:
        return True
    else:
        return False


def display_info(widget: QWidget, title: str, message: str):
    """
    Display information in a pop-up that can only be accepted
    """
    QMessageBox.information(
        widget,
        title,
        message,
        QMessageBox.Ok,
    )
