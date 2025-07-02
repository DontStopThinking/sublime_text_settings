import sublime
import sublime_plugin

class ShantanuToggleWordWrapAllViewsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the current setting for word_wrap
        current_setting = self.view.settings().get("word_wrap", False)

        # Toggle the setting for all views
        for window in sublime.windows():
            for view in window.views():
                view.settings().set("word_wrap", not current_setting)

        # Display a message
        status_message = "Word wrap {} in all views".format("enabled" if not current_setting else "disabled")
        sublime.status_message(status_message)
