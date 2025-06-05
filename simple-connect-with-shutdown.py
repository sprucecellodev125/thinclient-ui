import gi
import os
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class EntryWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="RDP Login")
        self.set_border_width(20)
        self.set_default_size(300, 150)

        # Master container
        main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_container.set_spacing(0)
        self.add(main_container)
        main_container.pack_start(Gtk.Box(), True, True, 0)

        # Outer container to center content
        outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        outer.set_valign(Gtk.Align.CENTER)
        outer.set_halign(Gtk.Align.CENTER)
        main_container.pack_start(outer, False, False, 0)

        # Inner form box with spacing and padding
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_size_request(400, -1)
        outer.pack_start(vbox, False, False, 0)

        username_label = Gtk.Label(label="Username")
        username_label.set_xalign(0)
        self.username_entry = Gtk.Entry()
        vbox.pack_start(username_label, False, False, 0)
        vbox.pack_start(self.username_entry, False, False, 0)

        password_label = Gtk.Label(label="Password")
        password_label.set_xalign(0)
        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)
        self.password_entry.set_invisible_char("*")
        vbox.pack_start(password_label, False, False, 0)
        vbox.pack_start(self.password_entry, False, False, 0)

        server_label = Gtk.Label(label="Server")
        server_label.set_xalign(0)
        self.server_entry = Gtk.Entry()
        vbox.pack_start(server_label, False, False, 0)
        vbox.pack_start(self.server_entry, False, False, 0)

        connect_button = Gtk.Button(label="Connect")
        connect_button.connect("clicked", self.launch_rdp)
        vbox.pack_start(connect_button, False, False, 10)

        main_container.pack_start(Gtk.Box(), True, True, 0)

        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        footer.set_halign(Gtk.Align.END)
        footer.set_valign(Gtk.Align.END)
        footer.set_margin_end(20)
        footer.set_margin_bottom(20)
        main_container.pack_end(footer, False, False, 0)

        shutdown_btn = Gtk.Button(label="Shutdown")
        shutdown_btn.connect("clicked", self.shutdown)
        footer.pack_start(shutdown_btn, False, False, 0)

        self.fullscreen()

    def launch_rdp(self, button):
        username = self.username_entry.get_text().strip()
        password = self.password_entry.get_text().strip()
        server = self.server_entry.get_text().strip()

        if not username or not password or not server:
            self.show_error_dialog("All fields are required.")
            return

        cmd = [
            "xfreerdp",
            f"/u:{username}",
            f"/p:{password}",
            f"/v:{server}"
        ]

        try:
            subprocess.Popen(cmd)
            Gtk.main_quit()
        except Exception as e:
            self.show_error_dialog(f"Failed to launch xfreerdp:\n{e}")

    def show_error_dialog(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Error",
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def shutdown(self, button):
        subprocess.call(["shutdown", "-h", "now"])


if __name__ == "__main__":
    win = EntryWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
