from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from lexer import *

def main():
    root = Tk()
    interpreter = Interpreter(root)
    interpreter.root.mainloop()
    return None

class Interpreter:
    def __init__(self, root):
        self.root = root
        self.root.title('Lexical Analyzer')

        mainframe = Frame(self.root)
        mainframe.pack()

        sideframe = Frame(mainframe)
        sideframe.pack(side=RIGHT)

        self.textEditor = TextEditor(mainframe)
        self.executeBtn = Button(mainframe, text="Execute",  font=("Helvetica", 15), height=1, width=20, command = self.processText).pack()

        table_lexemes_label = Label(sideframe, text = "Lexemes").grid(row= 0, column=0)
        self.table_lexemes = Table(sideframe, {'lexeme' : 'Lexeme', 'lexeme_type' : 'Lexeme Type'}, 1)

        symbol_table_label = Label(sideframe, text = "Symbol Table").grid(row= 2, column=0)
        self.symbol_table = Table(sideframe, {'identifier' : 'Identifier', 'value' : 'Value'}, 3)

        self.console = Console(mainframe)

    def processText(self):
        input_text = self.textEditor.getInputFromTextEditor()

        lexer = Lexer()
        lexer.process(input_text)
        self.table_lexemes.insertObjectList(lexer.lexemes)

        self.console.outputResult(input_text)

class TextEditor:
    def __init__(self, frame):
        self.textField = Text(frame)
        self.fileOpenBtn = Button(frame, text="Open File",  font=("Helvetica", 15), height=1, width=6, command = self.openFile)

        self.fileOpenBtn.pack()
        self.textField.pack()

    def openFile(self):
        #MIGHT CAUSE AN ERROR DUE TO DIFFERENT OPERATING SYSTEMS 
        filename = filedialog.askopenfilename(initialdir="../", title="Select a file", filetypes=(("Text files", "*.lol"), ("all files", "*.*")))
        self.textField.insert(END , open(filename, 'r').read())

    def getInputFromTextEditor(self):
        return self.textField.get(1.0, "end-1c")

class Console:
    def __init__(self, frame):
        self.output = Text(frame)
        self.output.pack()
        self.output['state'] = 'disabled'

    #PROCESS LOL CODE HERE
    def outputResult(self, console_output):
        self.switchState()
        self.output.insert(END, console_output)
        self.switchState()

    def switchState(self):
        self.output['state'] = 'disabled' if self.output['state'] == 'normal' else 'normal'

class Table: 
    def __init__(self, frame, column_dict, pos_row):
        column_names = tuple(column_dict) 
        self.table = ttk.Treeview(frame, columns=column_names, show='headings')

        # forms heading of the table
        for header in column_names:
            self.table.heading(header, text = column_dict[header])

        self.scrollbar = ttk.Scrollbar(frame, orient= VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row= pos_row, column=1)

        self.table.grid(row= pos_row, column=0)

    def addData(self, data_tuple):
        self.table.insert('', END, values = data_tuple)

    def insertObjectList(self, object_list):
        for token_object in object_list:
            self.addData((token_object.lexeme, token_object.lexemeType))

main()
#References
# Tables: https://www.pythontutorial.net/tkinter/tkinter-treeview/