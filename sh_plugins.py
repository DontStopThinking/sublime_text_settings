import os
import sublime
import sublime_plugin

class ShantanuToggleWordWrapInAllViewsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the current setting for word_wrap
        current_setting = self.view.settings().get("word_wrap", False)

        # Toggle the setting for all views
        for window in sublime.windows():
            for view in window.views():
                view.settings().set("word_wrap", not current_setting)

        # Display a message
        status_message = "Word wrap {} in all views and windows".format("enabled" if not current_setting else "disabled")
        sublime.status_message(status_message)


class ShantanuSwitchHeaderSource(sublime_plugin.WindowCommand):
    def run(self):
        if not self.window.active_view():
            return

        file_name = self.window.active_view().file_name()

        if not file_name: # if the file doesn't exist on disk
            return

        root, curr_ext = os.path.splitext(file_name)

        header_exts = [".h", ".hpp"]
        source_exts = [".c", ".cpp"]

        if curr_ext in header_exts:
            target_exts = source_exts
        elif curr_ext in source_exts:
            target_exts = header_exts
        else:
            return

        for ext in target_exts:
            new_path = root + ext
            if os.path.exists(new_path):
                existing_view = self.window.find_open_file(new_path)
                if existing_view:
                    self.window.focus_view(existing_view) # If the file is already open, then just focus on it
                else:
                    # If its not open, then open it in the neighboring group
                    self.window.open_file(new_path)
                    self.window.run_command("move_to_neighboring_group")
                break
        else:
            sublime.status_message(f"{os.path.basename(root)}.{target_exts} not found.")


class ShantanuFindUnderExpandBackwardCommand(sublime_plugin.TextCommand):
    """
    Select multiple occurrences of selection, except in backwards direction.
    """
    def run(self, edit):
        view = self.view
        selections = list(view.sel())

        for region in reversed(selections):
            word_region = view.word(region.begin())
            word = view.substr(word_region)

            # Find the previous occurrence of the word
            regions = view.find_all(word, sublime.LITERAL)
            previous_region = None

            for r in reversed(regions):
                if r.end() < region.begin():  # Find a region that is before the current selection
                    previous_region = r
                    break

            if previous_region:
                view.sel().add(previous_region)


class ShantanuMoveToNeighboringGroupWithCreate(sublime_plugin.WindowCommand):
    def run(self, forward=True):
        if not self.window.active_view():
            return

        if self.window.num_groups() == 1:
            print("num_groups() is 1")
            self.window.set_layout({ 'cols': 2 })

        self.window.run_command("move_to_neighboring_group", { "forward": forward })
