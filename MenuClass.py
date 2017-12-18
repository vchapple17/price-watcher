from CONSTANTS import CONSTANTS
#
# Menu class:
#
class Menu:
    def __init__(self):
        self.title = "Menu"
        self.menuItems = []

    def __init__(self, title):
        self.menuItems = []
        self.title = title

    def addMenuItem(self, title, selectFunc):
        try:
            menuItem = MenuItem(title, selectFunc)
        except:
            exit()
        self.menuItems.append(menuItem)
    def promptMenuSelection(self):
        selection = 0
        while(selection < 1 or selection > len(self.menuItems)):
            print(self.title)
            for i in range(len(self.menuItems)):
                print("\t" + str(i+1) + ' - ' + self.menuItems[i].title)
            prompt = "Make a selection (1 to "+ str(len(self.menuItems))+"): "
            selection = raw_input(prompt)
            try:
                selection = int(selection)
            except:
                selection = 0
        selection -= 1
        try:
            self.menuItems[selection].select()
        except:
            print("ERROR SELECTION MENU ITEM " + str(selection+1))
            exit()

class MenuItem:
    def __init__(self, title, selectFunc):
        self.title = title
        self.selectFunc = selectFunc

    def select(self):
        self.selectFunc()



# def select1():
#     print("1 is selected!")

# def main():
#     test = Menu("Test Menu")
#     test.addMenuItem("item1", select1)
#     test.promptMenuSelection()
#
# if __name__ == "__main__":
#     main()
