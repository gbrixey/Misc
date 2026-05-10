#!/usr/bin/env python
import os
import bisect
import tkinter as tk
from pathlib import Path
from collections import defaultdict
from PIL import Image, ImageTk, UnidentifiedImageError

class ImageTagger():
    '''This class presents a GUI for tagging images and filtering images based on the tags previously applied.'''

    TAGS_FILENAME = 'tags.csv'
    THIS_FILENAME = 'ImageTagger.py'
    CSV_SEPARATOR = '\t'
    IMAGE_SIZE = 600
    ALLOWED_FILE_EXTENSIONS = ['gif', 'jpeg', 'jpg', 'mp4', 'pdf', 'png', 'webp']

    CHECKBUTTON_DEFAULT_BG = 'gray94'
    CHECKBUTTON_SELECTED_BG = 'LightBlue1'
    MODE_TAG = 'tag'
    MODE_VIEW = 'view'

    def __init__(self):
        self._load_tags()
        self._get_all_files()
        self._check_untagged_files()
        self._check_for_missing_files()

    # Public functions

    def start(self):
        '''Initialize the UI shared by both "view" and "tag" mode, 
        then enter "tag" mode if there are zero tagged images and nonzero untagged images, otherwise enter "view" mode.'''
        self._create_shared_widgets()
        if len(self.__all_tagged_files) == 0 and len(self.__untagged_files) > 0:
            self._start_tag_mode()
        else:
            self._start_view_mode()
        self.__root.mainloop()

    def print_info(self, sort_by_count = False):
        '''Print a list of the number of files for each tag and each file extension. By default the tags and extensions 
        are sorted alphabetically. Pass in `sort_by_count = True` to sort them by file count (descending) instead.'''
        if len(self.__tags_dict) == 0:
            print('\nNo tagged files.\n')
            return
        count_by_extension = defaultdict(int)
        count_by_tag = defaultdict(int)
        for filename, tags_list in self.__tags_dict.items():
            extension = filename.split('.')[-1]
            count_by_extension[extension] += 1
            for tag in tags_list:
                count_by_tag[tag] += 1
        sort_key = (lambda t: t[1]) if sort_by_count else (lambda t: t[0])
        sort_reverse = sort_by_count
        sorted_tags = sorted(count_by_tag.items(), key = sort_key, reverse = sort_reverse)
        max_tag_length = max([len(tag) for tag in count_by_tag.keys()])
        print('\nFile count for each tag:')
        for tag, count in sorted_tags:
            padded_tag = tag.ljust(max_tag_length + 3, '.')
            print(f'    {padded_tag}{count}')
        sorted_extensions = sorted(count_by_extension.items(), key = sort_key, reverse = sort_reverse)
        max_extension_length = max([len(extension) for extension in count_by_extension.keys()])
        extension_padding_length = max(max_tag_length, max_extension_length)
        print('\nFile count for each file extension:')
        for extension, count in sorted_extensions:
            padded_extension = extension.ljust(extension_padding_length + 3, '.')
            print(f'    {padded_extension}{count}')
        print(f'\nTOTAL FILE COUNT: {len(self.__tags_dict)}\n')

    # View creation functions

    def _create_shared_widgets(self):
        '''Creates widgets that are shared between "view" mode and "tag" mode.'''
        #
        # Image view
        #
        self.__root = tk.Tk()
        self.__image_frame = tk.Frame(self.__root, height = self.IMAGE_SIZE, width = self.IMAGE_SIZE, borderwidth = 1, relief = tk.SOLID)
        self.__image_frame.grid(row = 0, column = 0, sticky = tk.NSEW)
        self.__image_label = tk.Label(self.__image_frame)
        self.__image_label.pack(expand = True)
        self.__image_frame.pack_propagate(False)
        #
        # Bottom left view
        #
        self.__bottom_left_container = tk.Frame(self.__root)
        self.__bottom_left_container.grid(row = 1, column = 0, sticky = tk.NSEW)
        self.__file_path_label = tk.Label(self.__bottom_left_container)
        self.__file_path_label.pack(side = tk.TOP, anchor = tk.W, padx = 20, pady = 5)
        self.__bottom_left_buttons_container = tk.Frame(self.__bottom_left_container)
        self.__bottom_left_buttons_container.pack(side = tk.TOP, anchor = tk.W)
        #
        # Tags list
        #
        self.__tags_outer_frame = tk.Frame(self.__root, height = self.IMAGE_SIZE, width = self.IMAGE_SIZE // 2, borderwidth = 1, relief = tk.SOLID)
        self.__tags_outer_frame.grid(row = 0, column = 1, sticky = tk.NSEW)
        self.__tags_canvas = tk.Canvas(self.__tags_outer_frame)
        self.__tags_scrollbar = tk.Scrollbar(self.__tags_outer_frame, orient = tk.VERTICAL, command = self.__tags_canvas.yview)
        self.__tags_canvas.configure(yscrollcommand = self.__tags_scrollbar.set)
        self.__tags_scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.__tags_canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.__tags_inner_frame = tk.Frame(self.__tags_canvas)
        self.__tags_canvas.create_window((0, 0), window = self.__tags_inner_frame, anchor = 'nw')
        self.__tags_inner_frame.bind('<Configure>', self._update_scroll_region)
        self.__tags_inner_frame.bind_all('<MouseWheel>', self._update_scroll_region_on_mousewheel)
        self.__select_tags_label = tk.Label(self.__tags_inner_frame, text = 'Select tags:', anchor = tk.W)
        self.__select_tags_label.pack(side = tk.TOP, anchor = tk.W, padx = 20, pady = 10)
        self.__tag_vars = []
        self.__tag_checkbuttons = []
        self.__no_tags_label = None
        for tag in self.__all_tags:
            self._create_checkbutton(tag)
        self._update_checkbutton_bgs()
        if len(self.__all_tags) == 0:
            no_tags_text = 'No tags yet. Add tags using the text field in the bottom right corner.'
            self.__no_tags_label = tk.Label(self.__tags_inner_frame, text = no_tags_text, anchor = tk.W)
            self.__no_tags_label.pack(side = tk.TOP, anchor = tk.W, padx = 20, pady = 20)
        #
        # Bottom right view
        #
        self.__bottom_right_section = tk.Frame(self.__root)
        self.__bottom_right_section.grid(row = 1, column = 1, sticky = tk.NSEW)
        self.__selected_tags_label = tk.Label(self.__bottom_right_section, anchor = tk.E, justify = tk.RIGHT)
        self.__selected_tags_label.pack(side = tk.TOP, anchor = tk.E, fill = tk.BOTH, padx = 20, pady = 5)
        self._update_selected_tags_label()
        self.__bottom_right_buttons_container = tk.Frame(self.__bottom_right_section)
        self.__bottom_right_buttons_container.pack(side = tk.TOP, anchor = tk.E, fill = tk.BOTH, pady = 20)
        self.__exact_match_var = tk.BooleanVar()
        self.__file_index_label = None

    def _prepare_to_switch_modes(self):
        '''Resets state of some shared widgets, and removes widgets that are specific to the "view" or "tag" mode,
        to prepare for switching from one mode to another.'''
        # Clear selected tags (without updating filtered images)
        for var in self.__tag_vars:
            var.set(False)
        self._update_checkbutton_bgs()
        self._update_selected_tags_label()
        self.__exact_match_var.set(False)
        for child in self.__bottom_left_buttons_container.winfo_children():
            child.destroy()
        for child in self.__bottom_right_buttons_container.winfo_children():
            child.destroy()
        self.__file_index_label = None

    def _start_view_mode(self):
        '''Display a UI to view tagged images in the current directory.'''
        self._prepare_to_switch_modes()
        self.__mode = self.MODE_VIEW
        self.__filtered_files = self.__all_tagged_files
        self._set_file_index(0)
        #
        # Bottom left buttons
        #
        self.__previous_button = tk.Button(self.__bottom_left_buttons_container, text = 'Previous image', command = self._previous_image)
        self.__previous_button.pack(side = tk.LEFT, padx = 5, pady = 20)
        self.__next_button = tk.Button(self.__bottom_left_buttons_container, text = 'Next image', command = self._next_image)
        self.__next_button.pack(side = tk.LEFT, padx = 5, pady = 20)
        self.__clear_tags_button = tk.Button(self.__bottom_left_buttons_container, text = 'Clear selected tags', command = self._clear_selected_tags)
        self.__clear_tags_button.pack(side = tk.LEFT, padx = 5, pady = 20)
        self.__switch_to_tag_mode_button = tk.Button(self.__bottom_left_buttons_container, text = 'Switch to tag mode', command = self._start_tag_mode)
        self.__switch_to_tag_mode_button.pack(side = tk.LEFT, padx = 5, pady = 20)
        self.__untagged_images_label = tk.Label(self.__bottom_left_buttons_container)
        self.__untagged_images_label.pack(side = tk.LEFT, padx = 5, pady = 20)
        self._update_untagged_images_label()
        #
        # Bottom right section
        #
        self.__exact_match_var.set(False)
        self.__exact_match_checkbutton = tk.Checkbutton(self.__bottom_right_buttons_container, text = 'Exact match', variable = self.__exact_match_var, command = self._toggle_exact_match)
        self.__exact_match_checkbutton.pack(side = tk.RIGHT, padx = 20)
        self.__file_index_label = tk.Label(self.__bottom_right_buttons_container)
        self.__file_index_label.pack(side = tk.RIGHT, padx = 20)
        self._update_file_index_label()

    def _start_tag_mode(self):
        '''Display a UI to tag untagged images in the current directory.'''
        self._prepare_to_switch_modes()
        self.__mode = self.MODE_TAG
        self.__filtered_files = self.__untagged_files
        self._set_file_index(0)
        #
        # Bottom left buttons
        #
        self.__skip_button = tk.Button(self.__bottom_left_buttons_container, text = 'Skip image', command = self._skip_tagging_image)
        self.__skip_button.pack(side = tk.LEFT, padx = 5, pady = 20)
        self.__tag_button = tk.Button(self.__bottom_left_buttons_container, text = 'Tag image', command = self._tag_image)
        self.__tag_button.pack(side = tk.LEFT, padx = 5, pady = 20)
        self.__clear_tags_button = tk.Button(self.__bottom_left_buttons_container, text = 'Clear selected tags', command = self._clear_selected_tags)
        self.__clear_tags_button.pack(side = tk.LEFT, padx = 5, pady = 20)
        self.__switch_to_view_mode_button = tk.Button(self.__bottom_left_buttons_container, text = 'Switch to view mode', command = self._start_view_mode)
        self.__switch_to_view_mode_button.pack(side = tk.LEFT, padx = 5, pady = 20)
        self.__untagged_images_label = tk.Label(self.__bottom_left_buttons_container)
        self.__untagged_images_label.pack(side = tk.LEFT, padx = 5, pady = 20)
        self._update_untagged_images_label()
        #
        # Bottom right section (Add new tag)
        #
        self.__add_new_tag_button = tk.Button(self.__bottom_right_buttons_container, text = 'Add new tag', command = self._add_new_tag)
        self.__add_new_tag_button.pack(side = tk.RIGHT, padx = 20)
        self.__new_tag_field = tk.Entry(self.__bottom_right_buttons_container)
        self.__new_tag_field.pack(side = tk.RIGHT)
        self.__new_tag_field.bind('<Return>', self._add_new_tag_enter)
        self.__new_tag_label = tk.Label(self.__bottom_right_buttons_container, text = 'New tag:')
        self.__new_tag_label.pack(side = tk.RIGHT, padx = 10)

    def _create_checkbutton(self, tag, default_to_true = False):
        '''Create and add a tag checkbutton to the list of tags in the tkinter interface.'''
        variable = tk.BooleanVar()
        bg = self.CHECKBUTTON_DEFAULT_BG
        if default_to_true:
            variable.set(True)
            bg = self.CHECKBUTTON_SELECTED_BG
        checkbutton = tk.Checkbutton(self.__tags_inner_frame, text = tag, variable = variable, bg = bg, command = self._toggle_checkbutton)
        checkbutton.pack(side = tk.TOP, anchor = tk.W, padx = 20)
        self.__tag_vars.append(variable)
        self.__tag_checkbuttons.append(checkbutton)

    # tkinter commands

    def _update_scroll_region(self, event: tk.Event):
        '''Binding method that scrolls the tags list when the scroll bar is moved.'''
        self.__tags_canvas.configure(scrollregion = self.__tags_canvas.bbox('all'))

    def _update_scroll_region_on_mousewheel(self, event: tk.Event):
        '''Binding method that scrolls the tags list when the mouse wheel is scrolled.'''
        self.__tags_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    def _toggle_checkbutton(self):
        '''Updates the checkbutton background colors and the selected tags label whenever a checkbutton is tapped.'''
        self._update_checkbutton_bgs()
        self._update_selected_tags_label()
        if self.__mode == self.MODE_VIEW:
            self._filter_images_by_tag()

    def _update_selected_tags_label(self):
        '''Update the label that shows how many tag checkbuttons are currently selected.'''
        selected_tags = sum([1 for var in self.__tag_vars if var.get()])
        self.__selected_tags_label.configure(text = f'Selected tags: {selected_tags}')

    def _previous_image(self):
        '''Display the previous image when in "view" mode.'''
        if self.__file_index > 0:
            self._set_file_index(self.__file_index - 1)

    def _next_image(self):
        '''Display the next image when in "view" mode.'''
        if self.__file_index < len(self.__filtered_files) - 1:
            self._set_file_index(self.__file_index + 1)

    def _clear_selected_tags(self):
        '''Deselect all selected tag checkbuttons.'''
        for var in self.__tag_vars:
            var.set(False)
        self._update_checkbutton_bgs()
        self._update_selected_tags_label()
        self.__exact_match_var.set(False)
        if self.__mode == self.MODE_VIEW:
            self._filter_images_by_tag()

    def _toggle_exact_match(self):
        '''Updates filtered images when the "Exact match" checkbox is toggled.'''
        self._filter_images_by_tag()

    def _skip_tagging_image(self):
        '''Skip the current image without adding any tags.'''
        self.__untagged_files.pop(0)
        self._display_current_file()
        self._update_file_path_label()
        self._update_untagged_images_label()

    def _tag_image(self):
        '''Records the selected tags for the current image and moves to the next untagged image.'''
        selected_tags = self._get_selected_tags()
        if len(selected_tags) == 0:
            return
        path = self.__untagged_files[0]
        self.__tags_dict[path] = selected_tags
        bisect.insort(self.__all_tagged_files, path)
        self._save_tags()
        self.__untagged_files.pop(0)
        self._display_current_file()
        self._update_file_path_label()
        self._update_untagged_images_label()

    def _add_new_tag(self):
        '''Adds a new tag checkbutton using the text in the "Add new tag" text field. The new tag is selected by default.'''
        new_tag = self.__new_tag_field.get().lower()
        if len(new_tag) == 0 or new_tag in self.__all_tags:
            return
        self.__all_tags.append(new_tag)
        self._create_checkbutton(new_tag, default_to_true = True)
        self.__new_tag_field.delete(0, tk.END)
        if self.__no_tags_label:
            self.__no_tags_label.destroy()
        self._update_selected_tags_label()

    def _add_new_tag_enter(self, event):
        '''Binding method that is called when the enter key is hit while the "Add new tag" text field is focused.
        This provides a convenient way to add a new tag via the keyboard, without having to click the "Add new tag" button.'''
        self._add_new_tag()

    # Private functions

    def _load_tags(self):
        '''Populates `self.__tags_dict`, `self.__all_tagged_files` and `self.__all_tags` by reading the `tags.csv` file.'''
        self.__tags_dict = {}
        self.__all_tagged_files = []
        self.__all_tags = []
        try:
            with open(self.TAGS_FILENAME, encoding = 'utf-8') as tags_file:
                text = tags_file.read()
        except FileNotFoundError:
            
            return
        lines = text.split('\n')
        tags_set = set()
        for line in lines:
            components = line.split('\t')
            path = components[0]
            tags = components[1:]
            self.__tags_dict[path] = tags
            bisect.insort(self.__all_tagged_files, path)
            tags_set.update(tags)
        self.__all_tags = sorted(tags_set)

    def _save_tags(self):
        '''Saves the current image tag data to the `tags.csv` file.'''
        lines = []
        for path in self.__all_tagged_files:
            joined_tags = self.CSV_SEPARATOR.join(self.__tags_dict[path])
            line = f'{path}{self.CSV_SEPARATOR}{joined_tags}'
            lines.append(line)
        csv_text = '\n'.join(lines)
        with open(self.TAGS_FILENAME, 'w', encoding = 'utf-8') as tags_file:
            tags_file.write(csv_text)

    def _get_all_files(self):
        '''Populates `self.__all_files` with a list of all files in the current directory with the allowed extensions.'''
        def is_valid_path(path):
            extension = str(path).split('.')[-1]
            return path.is_file() and extension in self.ALLOWED_FILE_EXTENSIONS
        self.__all_files = [str(path) for path in Path('.').rglob('*') if is_valid_path(path)]
        self.__all_files.sort()
        # Remove the tags file and this code file.
        if self.TAGS_FILENAME in self.__all_files:
            self.__all_files.remove(self.TAGS_FILENAME)
        if self.THIS_FILENAME in self.__all_files:
            self.__all_files.remove(self.THIS_FILENAME)

    def _check_untagged_files(self):
        '''Populates `self.__untagged_files` with a list of files that have not been tagged yet.'''
        self.__untagged_files = [file for file in self.__all_files if file not in self.__tags_dict]

    def _check_for_missing_files(self):
        '''Removes any files in the tags dictionary that can no longer be found in the current directory.'''
        files_to_remove = []
        for file in self.__all_tagged_files:
            if file not in self.__all_files:
                self.__tags_dict.pop(file)
                files_to_remove.append(file)
                print(f'Removed missing file {file} from tags dictionary.')
        for file in files_to_remove:
            self.__all_tagged_files.remove(file)
        if len(files_to_remove) > 0:
            self._save_tags()

    def _display_current_file(self):
        '''Display the file in `self.__filtered_files` at the current index specified by `self.__file_index`.'''
        try:
            file = self.__filtered_files[self.__file_index]
            i = Image.open(file)
            aspect_ratio = i.width / i.height
            if aspect_ratio >= 1:
                target_height = int(self.IMAGE_SIZE / aspect_ratio)
                i = i.resize((self.IMAGE_SIZE, target_height))
            else:
                target_width = int(self.IMAGE_SIZE * aspect_ratio)
                i = i.resize((target_width, self.IMAGE_SIZE))
            photo_image = ImageTk.PhotoImage(i)
            self.__image_label.config(text = '', image = photo_image)
            self.__image_label.image = photo_image
        except IndexError:
            if self.__mode == self.MODE_TAG:
                no_image_text = 'Could not find any untagged images.'
            else:
                no_image_text = 'Could not find any tagged images to display.' if len(self.__all_tagged_files) == 0 else ''
            self.__image_label.config(text = no_image_text, image = '')
        except UnidentifiedImageError:
            self.__image_label.config(text = f'Cannot display this file: {file}', image = '')

    def _update_checkbutton_bgs(self):
        '''Update the background color of all checkbuttons based on their selected state.'''
        for i in range(len(self.__tag_vars)):
            bg = self.CHECKBUTTON_SELECTED_BG if self.__tag_vars[i].get() else self.CHECKBUTTON_DEFAULT_BG
            self.__tag_checkbuttons[i].configure(bg = bg)

    def _update_file_path_label(self):
        '''Update the tkinter Label that shows the path of the file currently being displayed.'''
        try:
            file = self.__filtered_files[self.__file_index]
            self.__file_path_label.config(text = file)
        except IndexError:
            self.__file_path_label.config(text = '')

    def _update_untagged_images_label(self):
        '''Update the tkinter Label that shows the number of untagged files remaining.'''
        self.__untagged_images_label.config(text = f'Untagged images: {len(self.__untagged_files)}')

    def _update_file_index_label(self):
        '''Update the tkinter Label that shows the currently selected file index and total number of filtered files.'''
        if len(self.__filtered_files) == 0:
            file_index_text = 'No images matching selected tags.' if len(self.__all_tagged_files) > 0 else ''
        else:
            file_index_text = f'Displaying image {self.__file_index + 1} of {len(self.__filtered_files)}'
        self.__file_index_label.config(text = file_index_text)

    def _set_file_index(self, index: int):
        '''Sets `self.__file_index` and updates all the UI widgets that depend on the current file index.'''
        self.__file_index = index
        self._display_current_file()
        self._update_file_path_label()
        if self.__file_index_label:
            self._update_file_index_label()

    def _get_selected_tags(self) -> list[str]:
        '''Return a list of the currently selected tags.'''
        selected_tag_indices = [index for index in range(len(self.__all_tags)) if self.__tag_vars[index].get()]
        selected_tags = [self.__all_tags[index] for index in selected_tag_indices]
        return sorted(selected_tags)

    def _filter_images_by_tag(self):
        '''Updates `self.__filtered_files` to include only files that have the currently selected tags.'''
        selected_tags = set(self._get_selected_tags())
        if self.__exact_match_var.get():
            self.__filtered_files = [file for file in self.__all_tagged_files if selected_tags == set(self.__tags_dict[file])]
        else:
            self.__filtered_files = [file for file in self.__all_tagged_files if selected_tags.issubset(set(self.__tags_dict[file]))]
        self._set_file_index(0)

def main():
    tagger = ImageTagger()
    tagger.start()

if __name__ == '__main__':
    main()
