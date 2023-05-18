import tkinter as tk
from PIL import ImageTk, Image
import spotify_artist_backend as sa
import pandas as pd


#some test artist IDs
#Miracle of sound: 4FmJD0mpgQ70SNt2EKK8tq
#Little V: 672ogXHsMCSQv7QPvbmviJ
class MainApp(tk.Frame):
    def __init__ (self, parent):
        tk.Frame.__init__(self, parent)
        client_id = "2f92e1fb67bc417ba772633afa78846b"
        client_secret= "9d0d39cec6ed4776b9f53cdf64791857"
        #client_id = input("Enter ID: ")
        #client_secret = input("Enter secret: ")
        self.header = sa.get_header(client_id,client_secret)
        self.parent = parent
        #label used to display Graph
        self.image_label = tk.Label(parent)
        self.image_label.grid(row=3, column = 0, columnspan = 3)

        #Buttons for functions
        artist_button = tk.Button(parent, text="get Top Tracks", command = lambda : self.from_id_to_graph(self.id_entry.get()), padx=20)
        search_button = tk.Button(parent, text="search Artist", command = lambda : self.search_function(self.search_entry.get()), padx=20)
        artist_button.grid(row=0, column=0)
        search_button.grid(row=0, column=1)

        #fille label with description text for entry fields
        id_label = tk.Label(parent, text= "Enter Artist ID here")
        search_label = tk.Label(parent, text= "Enter search term here")
        id_label.grid(row=1, column=0)
        search_label.grid(row=1, column=1)

        #entry fields for artist id and search term
        self.id_entry = tk.Entry(parent, text="")
        self.search_entry = tk.Entry(parent, text="")
        self.id_entry.grid(row=2, column=0, ipadx=50)
        self.search_entry.grid(row=2, column=1, ipadx=50)

    def from_id_to_graph(self,  entry_id):
        sa.request_api_artist(entry_id, self.header)
        Graph = ImageTk.PhotoImage(Image.open("C:/Users/stefa/Desktop/Python/spotify_artist/top_tracks.jpg").resize((900,500)))
        self.image_label.config(image = Graph)
        self.image_label.image = Graph
    
    #function to search for Artists, will pen second window
    def search_function(self, search_term):
        artist_selection = sa.artist_search(search_term, self.header)
        print(artist_selection)
        try:
            artist_selection["name"]
        except TypeError:
            print("empty search field")
            return
        optionslist = []
        for index, row in artist_selection.iterrows():
            optionslist.append(row["name"])
        #print("\n \n",optionslist, "\n \n")
        newWindow = tk.Toplevel(root)
        newWindow.title("Search Results")
        newWindow.geometry("400x400")
        display_value = tk.StringVar(newWindow)
        display_value.set(optionslist[0])

        #optionmenu with button to get value
        omenu = tk.OptionMenu(newWindow, display_value, *optionslist)
        omenu.grid(row=0, column=0)
        #Button to get value and close second window
        optionButton = tk.Button(newWindow, text="confirm selection", command = lambda : self.confirm(display_value.get(), artist_selection,newWindow))
        optionButton.grid(row=1, column=0)
    
    #confirm function, that closes the second window
    def confirm(self, value, data, newWindow):
        ID = data.loc[data["name"]==value]
        ret_id = ""
        for index, row in ID.iterrows():
            ret_id = row["id"]
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, ret_id)
        self.search_entry.delete(0, tk.END)
        newWindow.destroy()





if __name__ == "__main__":
    

    root = tk.Tk()
    root.title("Top Tracks")
    root.geometry("950x600")
    MainApp(root)
    root.mainloop()