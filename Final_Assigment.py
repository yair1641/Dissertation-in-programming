
# final project
# Yair Langerman & Yitzhak Grinvald
# Februar 2023

# import the libraries:

import tkinter as tk
from os.path import isdir
from pathlib import Path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt  

#creat the main class

class Build_folder_tree:

    def _init_(self,input_path):
    # Object-oriented features
        self.path=input_path
        # list of sub file size to use for the histogam
        self.sub_file_size_hist = list()
        self.Folder_dict, self.total_size = self._iter(Path(input_path))

    # Using a dictionary to create the tree
    def _iter(self, parent_path):
        Folder_size = 0
        Folder_dict = {}
        # scan folders that in the path
        for path in parent_path.iterdir():
            # folder
            if path.is_dir(): x_dict , path_size = self._iter(path)
            # file
            else:
                x_dict, path_size =None, path.stat().st_size
                # creat a list of all files size 
                self.sub_file_size_hist.append(path_size)
            unique_list_key = (path.name ,round(path_size/2**20,2))
            Folder_size += path_size
            Folder_dict[unique_list_key] = x_dict
        return Folder_dict, Folder_size

    # Clicking on a tree button will open a new window with the names of the files,
    #  their size and the percentage size of the entire folder
    def tree_botton(self):
         tree_window = tk.Toplevel(window) 
         tree_window.title("Tree Folder - "+ self.path.split('\\')[-1])
         scrollbar = tk.Scrollbar(tree_window)
         tree_constructor_view = tk.Listbox(tree_window, height= 50 , width= 150 , yscrollcommand = scrollbar.set )    
         build_tree(self,tree_constructor_view, self.Folder_dict ,self.total_size/2**20)
         tree_constructor_view.pack( side =tk.LEFT, fill = tk.BOTH )
         scrollbar.config( command = tree_constructor_view.yview )

    # when clik "stat" the fuction will open new windows 
    # and show histogram of the distribution of file sizes in a folder
    def stats_botton(self):
        stat_window = tk.Toplevel(window)
        stat_window.title("Statistical analysis folder - "+ self.path.split('\\')[-1])
        figure_hist = plt.Figure(figsize=(10,7), dpi=70)
        figure_hist.add_subplot().hist(self.sub_file_size_hist, color="red")
        total_size_label = tk.Label(stat_window,text='Total size: '+str( round(self.total_size/2**20,2))+' MB \n'+'\n'
                                    'Histogram of the distribution of file sizes in a folder [MB]',font=('Georgia',15, 'bold'))
        total_size_label.pack(pady=5)
        canvas_hist = FigureCanvasTkAgg(figure_hist, stat_window)
        canvas_hist.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

# scan folder and file and calculate the precent of file/foder from his parent size      
# scan folder and file and create the tree display with tab
def build_tree(analyzed_path,tree_constructor_view, tree_dict , level_size , flag_to_tab=0,up_level=0 ):  
    for key in tree_dict.keys():
        if tree_dict[key] is None:
            # to avoid dividing by zero in a case of a small folder wich returns zero when we get rounded 
            try:   percent=round((key[1]/level_size)*100,2)
            except:  percent = 0
            tree_constructor_view.insert(tk.END,'{}**File Name: - {} - ({}MB <> {}%)'.format(' '*5*flag_to_tab,key[0],key[1] , percent))
        else:
            try:   percent=round((key[1]/level_size)*100,2)
            except:  percent = 0
            tree_constructor_view.insert(tk.END,'{}>> Folder Name: - {} - ({}MB <> {}%)'.format(' '*5*flag_to_tab,key[0],key[1] , percent))
            up_level = level_size
            level_size=key[1]
            build_tree(analyzed_path ,tree_constructor_view , tree_dict[key], level_size,
                               flag_to_tab + 1,up_level)
            level_size = up_level

# When click 'EXE' the fuction will give us to chose tree or stats 
# Displaying an error message if a path that does not exist is entered
def EXE_botton():
    input_path=path_var.get()
    if not isdir(input_path):
        tk.messagebox.showerror("Error!!", "The path dose not exist, please enter a correct path.")
        return
    analyzed_path = Build_folder_tree(input_path)
    tk.Button(window,text = '   Tree   ',bg= 'green', fg= "white",font=('Georgia',10, 'bold'), command = lambda : Build_folder_tree.tree_botton(analyzed_path)).grid(row=3, column=2)
    tk.Button(window,text = '    Stat   ',bg= 'blue', fg= "white", font=('Georgia',10, 'bold'), command = lambda : Build_folder_tree.stats_botton(analyzed_path)).grid(row=5, column=2)

window=tk.Tk()
window.geometry("600x400")
window.config(bg='pink')
window.title("Main menu screen- Yair & Yitzhak")
path_var=tk.StringVar(value=r'')  
path_label = tk.Label( text = 'Enter a path: ',font=('Georgia',10, 'bold')).grid(row=2,column=1)
path_entry = tk.Entry(textva = path_var).grid(row=2,column=2)
EXE_button=tk.Button(text = '   EXE    ',bg= 'purple',fg='white',font=('Georgia',10, 'bold'), command = EXE_botton).grid(row=2, column=3)
exit_button = tk.Button(text = '   Exit   ',bg= 'purple',fg='white',font=('Georgia',10, 'bold'), command=window.destroy).grid(row=2,column=4)
window.mainloop()
