"""Contains the ui logic of the watermark app using tkinter

This contains the following classes:
- WatermarkApp
- WatermarkHeader
- WatermarkConfigFrame
- WatermarkProcessFrame

"""

import os
import threading

from typing import Callable

import tkinter as tk
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkmb
import tkinter.ttk as ttk

import watermark_core as wm_core

class WatermarkApp(tk.Tk):
    """Represents the window of the watermark app and includes all depending ui components.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        default_padx = 50
        default_pady = 10

        self.title('Simple image watermark tool')
        self.minsize(600, 200)
        self.grid_columnconfigure(0, weight=1)

        self._header = WatermarkHeader(self)
        self._header.grid(row=0, padx=default_padx, pady=default_pady)

        self._config = WatermarkConfigFrame(self, self.finished_configuration)
        self._config.grid(row=1, padx=default_padx, pady=default_pady, sticky=tk.W+tk.E)

        self._process = WatermarkProcessFrame(self, self._header.set_info)
        self._process.grid(row=2, padx=default_padx, pady=default_pady, sticky=tk.W+tk.E)
        self._process.grid_remove()

    def finished_configuration(self):
        """Callback method which is called after finishing the configuration part of this app.
        """
        self._config.grid_remove()
        self._process.grid()

        export_dir = self._config.get_export_dir()
        images = self._config.get_images()
        watermark_text = self._config.get_watermark_text()

        w_definition = wm_core.WatermarkDefinition(watermark_text)
        w_images = [wm_core.WatermarkSourceImage(x) for x in images]

        self._process.start_processing(w_definition, export_dir, w_images)

class WatermarkHeader(tk.Frame):
    """The header frame which includes the title and an information text.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._heading = tk.Label(
            self,
            text='Watermark Tool',
            font=("Segoe UI", 12, "bold", "underline")
        )
        self._heading.pack()

        self._information = tk.Label(
            self,
            font=("Segoe UI", 9),
            text="Fill out the configuration section and"+
                " click start to add a watermark to one or multiple images."
        )
        self._information.pack()

    def set_info(self, message: str) -> None:
        """Overwrites the information message below the heading

        Args:
            message (str): new information message
        """
        self._information.config(text=message)

class WatermarkConfigFrame(tk.Frame):
    """Handles the configuration part (watermark text, input files and export folder).
    """
    def __init__(self, root, finished_configuration_callback: Callable[[], None], *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        default_pady = 5
        current_row = 0
        self._images = []
        self._finished_config = finished_configuration_callback

        self.grid_columnconfigure(0, weight=0, minsize=10)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0, minsize=10)

        self._sub_heading = tk.Label(
            self,
            text="Configuration:",
            font=("Segoe UI", 10, "bold")
        )
        self._sub_heading.grid(row=current_row, column=0, columnspan=3, pady=default_pady)
        current_row = current_row + 1

        watermark_label = tk.Label(
            self,
            text="Watermark Text:",
            font=("Segoe UI", 9)
        )
        watermark_label.grid(row=current_row, column=0, sticky=tk.W, pady=default_pady)

        self._watermark_text=tk.StringVar(value="example watermark")
        watermark_entry = tk.Entry(
            self,
            textvariable=self._watermark_text
        )
        watermark_entry.grid(
            row=current_row, column=1, columnspan=2, sticky=tk.W+tk.E, pady=default_pady
        )
        current_row = current_row + 1

        export_dir_label = tk.Label(
            self,
            text="Export folder:",
            font=("Segoe UI", 9)
        )
        export_dir_label.grid(row=current_row, column=0, sticky=tk.W, pady=default_pady)

        self._export_dir_text = tk.StringVar(value="<unknown>")
        export_dir_entry = tk.Entry(
            self,
            textvariable=self._export_dir_text
        )
        export_dir_entry.grid(
            row=current_row, column=1, sticky=tk.W+tk.E, padx=(0,5), pady=default_pady
        )

        export_dir_button = tk.Button(
            self,
            text="Set export folder",
            font=("Segoe UI", 9),
            command=self.export_dir_button_clicked
        )
        export_dir_button.grid(row=current_row, column=2, sticky=tk.W+tk.E, pady=default_pady)
        current_row = current_row + 1

        images_label = tk.Label(
            self,
            text="Images:",
            font=("Segoe UI", 9)
        )
        images_label.grid(row=current_row, column=0, sticky=tk.W, pady=default_pady)

        self._images_text = tk.StringVar(value="0")
        self._images_entry = tk.Entry(
            self,
            textvariable=self._images_text,
            state="disabled"
        )
        self._images_entry.grid(
            row=current_row, column=1, sticky=tk.W+tk.E, padx=(0,5), pady=default_pady
        )

        images_button = tk.Button(
            self,
            text="Choose images",
            font=("Segoe UI", 9),
            command=self.images_button_clicked
        )
        images_button.grid(row=current_row, column=2, sticky=tk.W+tk.E, pady=default_pady)
        current_row = current_row + 1

        start_button = tk.Button(
            self,
            text="Start",
            font=("Segoe UI", 9),
            command=self.start_button_clicked
        )
        start_button.grid(row=current_row, column=2, sticky=tk.W+tk.E, pady=default_pady)

    def images_button_clicked(self) -> None:
        """Action handler for the images button.
        After calling this method a open files dialog pops up to choose images.
        """
        files = tkfd.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
                ("PNG Files", "*.png"),
                ("JPEG Files", "*.jpg;*.jpeg"),
                ("GIF Files", "*.gif"),
                ("BMP Files", "*.bmp"),
                ("All Files", "*.*")
            ]
        )

        self._images = files
        self._images_text.set(str(len(self._images)))

    def export_dir_button_clicked(self) -> None:
        """Action handler for the export directory button.
        Asks for a directory, where the modified files will be saved to.
        """
        folder = tkfd.askdirectory(
            title="Select export folder"
        )

        self._export_dir_text.set(folder)

    def start_button_clicked(self) -> None:
        """Validates the supplied configuration and
        starts the watermark process if everything is valid.
        """
        if len(self._watermark_text.get()) == 0:
            tkmb.showerror("Error", "Watermark text is empty.")
            return

        if self._export_dir_text.get() == "<unknown>":
            tkmb.showerror("Error", "Export directory wasn't supplied.")
            return

        if not os.path.exists(self._export_dir_text.get()):
            tkmb.showerror(
                "Error",
                f"Export directory ({self._export_dir_text.get()}) doesn't exist."
            )
            return

        if len(self._images) == 0:
            tkmb.showerror("Error", "No images were selected.")
            return

        self._finished_config()

    def get_images(self) -> list[str]:
        """Returns a list of the supplied images

        Returns:
            list[str]: list of chosen images
        """
        return self._images

    def get_export_dir(self) -> str:
        """Returns the export directory

        Returns:
            str: export directory
        """
        return self._export_dir_text.get()

    def get_watermark_text(self) -> str:
        """Returns the watermark text

        Returns:
            str: watermark text
        """
        return self._watermark_text.get()

class WatermarkProcessFrame(tk.Frame):
    """Displays a progress bar and updates it while the process runs."""
    def __init__(self, root, update_info_callback: Callable[[], None], *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        default_pady = 5
        self._root = root
        self._update_info = update_info_callback
        self._background_thread = None
        self._cancellation_requested = threading.Event()

        self.grid_columnconfigure(0, weight=1)

        self._progress = ttk.Progressbar(self)
        self._progress.grid(row=0, column=0, sticky=tk.W+tk.E, pady=default_pady)

        self._cancel_button = tk.Button(
            self,
            text="Cancel",
            command=self.cancel_button_clicked
        )
        self._cancel_button.grid(row=1, column=0, sticky=tk.E, pady=default_pady)

        self._close_button = tk.Button(
            self,
            text="Close",
            command=self.close_button_clicked
        )
        self._close_button.grid(row=2, column=0, sticky=tk.E, pady=default_pady)
        self._close_button.grid_remove()

    def start_processing(
            self,
            w_definition: wm_core.WatermarkDefinition,
            export_dir: str,
            images: list[wm_core.WatermarkSourceImage]):
        """Starts the watermarking process in a sub thread

        Args:
            w_definition (wm_core.WatermarkDefinition): watermark configuration
            export_dir (str): export directory
            images (list[wm_core.WatermarkSourceImage]): list of images
        """
        self._background_thread = threading.Thread(
            target=self.convert_images, args=(w_definition, export_dir, images))
        self._background_thread.start()

    def convert_images(
            self,
            w_definition: wm_core.WatermarkDefinition,
            export_dir: str,
            images: list[wm_core.WatermarkSourceImage]):
        """Executes the watermarking process

        Args:
            w_definition (wm_core.WatermarkDefinition): watermark configuration
            export_dir (str): export directory
            images (list[wm_core.WatermarkSourceImage]): list of images
        """

        manager = wm_core.WatermarkManager(w_definition, export_dir)
        manager.convert_files(images, self.update_state)

        self._cancel_button.grid_remove()
        self._close_button.grid()

    def update_state(self, message: str, current_index: int=0, amount_of_items: int=1):
        """Updates the information text and progress bar.
        If the cancellation was requested, it stops the execution.

        Args:
            message (str): message which will be displayed
            current_index (int, optional): current index of the image list. Defaults to 0.
            amount_of_items (int, optional): amount of items in the image list. Defaults to 1.
        """
        if self._cancellation_requested.is_set():
            exit(0)

        self._update_info(message)
        self._progress.config(value=(current_index/amount_of_items)*100)
        self._root.update_idletasks()

    def cancel_button_clicked(self):
        """Cancels the watermarking process and closes the application
        """
        self._cancellation_requested.set()
        self.close_button_clicked()

    def close_button_clicked(self):
        """Closes the application
        """
        self._root.destroy()
