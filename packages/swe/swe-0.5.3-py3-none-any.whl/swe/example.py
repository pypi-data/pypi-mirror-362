from textual.app import App


class LogApp(App):
    def on_load(self):
        self.log("In the log handler!", pi=3.141529)

    def on_mount(self):
        self.log(self.tree)


if __name__ == "__main__":
    LogApp().run()
