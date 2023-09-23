import os

from tkinter import filedialog
from tkinter import messagebox
import customtkinter
import pandas
import threading


customtkinter.set_appearance_mode("System")     # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")   # Themes: "blue" (standard), "green", "dark-blue"


class AnalyticsUI(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        
        # configure window
        self.title("Analytics UI")
        self.geometry(f"{1400}x{840}")
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                        values=["Light", "Dark","System"],
                                                                        command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                values=["80%", "90%", "100%", "110%", "120%"],
                                                                command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=3, column=0, padx=20, pady=(10, 20))
        
        # create main directory display, file name, execute and browse buttons
        self.entry = customtkinter.CTkEntry(self, placeholder_text="file path", height=60, width=200)
        self.entry.grid(row=0, column=1, padx=(20, 20), pady=(100, 0), sticky="NEW")
        self.file_name = customtkinter.CTkEntry(self, placeholder_text="save file as", height=60, width=200)
        self.file_name.grid(row=0, rowspan = 1, column=1, padx=(20, 20), pady=(200, 0), sticky="NEW")
        button = customtkinter.CTkButton(self, text="Execute", height=50, border_width=2, fg_color="transparent",
                                        text_color=("gray10", "#DCE4EE"), command=self.prog_bar_start)
        button.grid(row=1, column=1, padx=0, pady=0, sticky='N')
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                    text_color=("gray10", "#DCE4EE"), height=60, width=140,
                                                    text="Select Files", command=self.browse_directory)
        self.main_button_1.grid(row=0, column=3, padx=(20, 20), pady=(100, 20), sticky="N")
        
        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(0, 0), pady=(40, 0), sticky="EW")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.progressbar = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="EW")
        self.progressbar.configure(mode="indeterminate")
        
        # create instructions textbox
        self.textbox = customtkinter.CTkTextbox(self, height=200, width=250, border_width=2)
        self.textbox.grid(row=2, column=1, padx=(20, 20), pady=(20, 20), sticky="EW")
        
        # set default values when open
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert("0.0", "Instructions\n\n1. Use the 'Select Files' button to locate the directory containing the files to be prepared.\n\n2. Enter the name which the prepared file will be saved with in the 'save file as' section.\n\n3. Click the 'Execute' button and wait for completion.\n\n\nPS: The prepared file is saved in a new folder with same name as provided in the 'save file as' section.")
        self.textbox.configure(state="disabled")
        
        # Exit notification
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self) -> None:
        """Exit Program Confirmation."""
        msg = messagebox.askyesno("Exit?", "Do you want to close the program?")
        if msg is True:
            AUI.destroy()
        else:
            pass
    
    def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        """       
        Modify UI mode appearance
        
        :param new_appearance_mode: Appearance mode, which by default is system, but can be changed.
        """
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def change_scaling_event(self, new_scaling: str) -> None:
        """Scale display size on monitor."""
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def browse_directory(self) -> tuple[str]:
        """
        Browse location of CSV files.
        
        :return: location of csv files (file_path)
        """
        self.entry.delete(0, customtkinter.END)
        try:
            files = filedialog.askopenfilenames(initialdir="/",
                                                title="Select CSV files",
                                                filetypes=(("csv files", "*.csv"), ("all files","*.*")))
            self.entry.insert(0, f"{files}")
            return files
        except IndexError:
            pass
    
    def save_as(self) -> str:
        """
        Get the name to save the file with.
        
        :return: Name to save the final file with. If empty, return False.
        """
        name = f"{self.file_name.get()}"
        empty = ""
        if name is not empty:
            return name.replace(" ","_")
        else:
            return False
    
    def new_folder(self) -> str:
        """
        Create a folder in file location to save final processed file.
        
        :return: folder path, or False if empty.
        """
        parent_directory = self.entry.get().replace("(", "").replace(")", "").replace("'", "").split(",")[0].rsplit("/", 1)[0]
        folder_name = self.save_as()
        if (folder_name is not False) and (parent_directory != ""):
            path = os.path.join(f"{parent_directory}", f"{folder_name}")
            os.makedirs(path, exist_ok=True)
        else:
            self.progressbar.stop()
            messagebox.showerror("Error!!!", "Save folder not created. 'save as' missing.")
    
    def prog_bar_start(self) -> None:
        """Start progress bar with multithreading"""
        self.progressbar.start()
        threading.Thread(target=self.execute).start()
    
    def modify_time_data(self, file_path: str) -> pandas.DataFrame:
        """
        Perform operations on datetime column in the csv files
        
        :param file_path: Path to CSV file
        :return: A pandas DataFrame
        """
        read_file = pandas.read_csv(file_path, parse_dates = [0])
        read_file.DATETIME = pandas.to_datetime(read_file.DATETIME)
        read_file.DATETIME = [get_time.time() for get_time in read_file.DATETIME]
        read_file.rename(columns = {"DATETIME":"TIME"}, inplace = True)
        return read_file
    
    def execute(self) -> None:
        """Execute operations"""
        file_location = self.entry.get()
        name = self.save_as()        
        if (file_location is not False) and (name is not False):
            files = [file.strip()
                    for file in file_location.replace("(", "").replace(")", "").replace("'", "").split(",")
                    if file.replace(" ", "") != ""
                    ]
            save_location = files[0].rsplit("/", 1)[0]            
            self.new_folder()
            if len(files) == 1:
                try:
                    mod_files = self.modify_time_data(files[0])
                    mod_files.to_csv(os.path.join(f"{save_location}", f"{name}", f"{name}.csv"), index = False)
                    self.progressbar.stop()
                except ValueError:
                    self.progressbar.stop()
                    messagebox.showerror("Error!!!", "Please check files and try again.")
            elif len(files) > 1:
                mod_file_list = []
                try:
                    for file in files:
                        data_file = self.modify_time_data(file)
                        mod_file_list.append(data_file)
                        mod_files = pandas.concat(mod_file_list).sort_values(by="TIME")
                        mod_files.to_csv(os.path.join(f"{save_location}", f"{name}", f"{name}.csv"), index = False)
                        self.progressbar.stop()
                except ValueError:
                    self.progressbar.stop()
                    messagebox.showerror("Error!!!", "Please check files and try again.")
            else:
                self.progressbar.stop()
                messagebox.askretrycancel("Warning", "No CSV file found in this directory.")
        else:
            self.progressbar.stop()
            messagebox.showerror("Error!!!", "Missing either of 'save as' or 'file path'.")

    
if __name__ == "__main__":
    AUI = AnalyticsUI()
    AUI.mainloop()

