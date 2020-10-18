#!/usr/bin/python3.8
# import sys
# from typing import TextIO

from datetime import date
from datetime import timedelta
from datetime import datetime

from wx import Button

import platform
import wx
import os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# import socket

emailAddresses = ["david.p.greenaway@gmail.com", "nauntonpark@hotmail.com"]
# emailAddresses  = ["david.p.greenaway@gmail.com"]


def sendMail(msgtext, toaddr, subject='shopping list'):
    fromaddr = 'mypiebox@gmail.com'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddr

    username = 'mypiebox@gmail.com'
    password = 'IafBcsBrsMor1'

    html = '<html><head>\n</head>\n<body><font face="Courier ">\n<pre>' + msgtext + "\n\n\nxxxx\n"\
           "\n</pre>\n</font>\n</body>\n</html>"

    msgPart1 = MIMEText(msgtext + "\n\nxxxx", 'plain', 'UTF-8')
    msgPart2 = MIMEText(html, 'html', 'UTF-8')

    msg.attach(msgPart1)
    msg.attach(msgPart2)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()


def readIn(fileincore, dictincore, filename):
    file = open(filename)
    file.seek(0)
    lines = file.readlines()
    pnt = 0
    for line in lines:
        fileincore.append(line.strip())
        lineList = line.split(" ")
        dictincore[lineList[0]] = pnt
        pnt += 1
    file.close()


# noinspection PyUnusedLocal
class Example(wx.Frame):
    menuPrintButton: Button
    IngrediencePointer = -1

    # file names for data files on disk
    MenuFileName: str = "Menu"
    IngredianceFileName = "Ingrediance"
    RecipiesFileName = "Recipies"
    TempFileName = "temp"
    CatFileName = "cat"

    # in core storage for data file
    Menu = []
    Ingredience = []
    Recipies = []

    MenuDict = {}
    IngredienceDict = {}
    RecipiesDict = {}

    dishes = []

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(600, 400))

        fileStem = "None"
        if platform.system() == "Linux":
            fileStem = "/home/david/Menu/"
        if platform.system() == "Windows":
            fileStem = "C:\\Users\\david\\Documents\\source\\food\\"

        if fileStem == "None":
            raise Exception("something wrong  file filename")

        self.allCatsList = []

        self.MenuFileName: str = fileStem+"Menu"
        self.IngredianceFileName = fileStem+"Ingrediance"
        self.RecipiesFileName = fileStem+"Recipies"
        self.TempFileName = fileStem+"temp"
        self.CatFileName = fileStem+"cat"

        self.panel = wx.Panel(self, size=(600, 400))
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hboxTop = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxMiddle = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxBottem = wx.BoxSizer(wx.HORIZONTAL)

        self.vboxTop = wx.BoxSizer(wx.VERTICAL)

        self.menuBox = wx.ListBox(self.panel, style=wx.ALIGN_LEFT)
        self.menuSuggestButton = wx.Button(self.panel, id=wx.ID_ANY, label="?", style=wx.ALIGN_RIGHT, size=(30, 30))
        self.menuAddButton = wx.Button(self.panel, id=wx.ID_ANY, label="Add", style=wx.ALIGN_RIGHT, size=(30, 30))
        self.menuReplaceButton = wx.Button(self.panel, id=wx.ID_ANY, label="Rpl", style=wx.ALIGN_RIGHT, size=(30, 30))
        self.menuPrintButton = wx.Button(self.panel, id=wx.ID_ANY, label="Pnt", style=wx.ALIGN_RIGHT, size=(30, 30))
        self.menuEmailButton = wx.Button(self.panel, id=wx.ID_ANY, label="Mail", style=wx.ALIGN_RIGHT, size=(30, 30))

        self.menuBox: wx.ListBox
        self.hboxTop: wx.BoxSizer
        self.hboxMiddle: wx.BoxSizer
        self.hboxBottem: wx.BoxSizer

        self.vboxTop.Add(self.menuSuggestButton, 1, border=5)
        self.vboxTop.AddSpacer(10)
        self.vboxTop.Add(self.menuAddButton, 1, border=5)
        self.vboxTop.AddSpacer(10)
        self.vboxTop.Add(self.menuReplaceButton, 1, border=5)
        self.vboxTop.AddSpacer(10)
        self.vboxTop.Add(self.menuPrintButton, 1, border=5)
        self.vboxTop.AddSpacer(10)
        self.vboxTop.Add(self.menuEmailButton, 1, border=5)

        self.hboxTop.AddSpacer(20)
        self.hboxTop.Add(self.menuBox, 1, wx.EXPAND, border=5)
        self.hboxTop.AddSpacer(20)
        self.hboxTop.Add(self.vboxTop, 0, border=5)
        self.hboxTop.AddSpacer(20)

        self.shoppinglistBox = wx.ListBox(self.panel, style=wx.ALIGN_LEFT)

        self.hboxMiddle.AddSpacer(20)
        self.hboxMiddle.Add(self.shoppinglistBox, 1, wx.EXPAND, border=5)
        self.hboxMiddle.AddSpacer(20)

        self.ingredientBox = wx.TextCtrl(self.panel, style=wx.ALIGN_LEFT, size=(340, 30))
        self.nextIngredent = wx.Button(self.panel, label=">", style=wx.ALIGN_RIGHT, size=(30, 30))
        self.previousIngredent = wx.Button(self.panel, label="<", style=wx.ALIGN_RIGHT, size=(30, 30))
        self.increaseStock = wx.Button(self.panel, label="+", style=wx.ALIGN_RIGHT, size=(30, 30))
        self.decreaseStock = wx.Button(self.panel, label="-", style=wx.ALIGN_RIGHT, size=(30, 30))

        self.hboxBottem.AddSpacer(20)
        self.hboxBottem.Add(self.ingredientBox, 1, wx.EXPAND, border=5)
        self.hboxBottem.AddSpacer(20)
        self.hboxBottem.Add(self.nextIngredent, 0, wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
        self.hboxBottem.AddSpacer(20)
        self.hboxBottem.Add(self.previousIngredent, 0, wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
        self.hboxBottem.AddSpacer(20)
        self.hboxBottem.Add(self.increaseStock, 0, border=5)
        self.hboxBottem.AddSpacer(20)
        self.hboxBottem.Add(self.decreaseStock, 0, border=5)
        self.hboxBottem.AddSpacer(20)

        self.vbox.AddSpacer(20)
        self.vbox.Add(self.hboxTop, 1, wx.EXPAND | wx.ALIGN_TOP)
        self.vbox.AddSpacer(20)
        self.vbox.Add(self.hboxMiddle, 1, wx.EXPAND)
        self.vbox.AddSpacer(20)
        self.vbox.Add(self.hboxBottem, 0)
        self.vbox.AddSpacer(20)

        # bindings
        self.menuAddButton.Bind(wx.EVT_BUTTON, self.addButtonEvent)
        self.menuReplaceButton.Bind(wx.EVT_BUTTON, self.replaceButtonEvent)
        self.menuPrintButton.Bind(wx.EVT_BUTTON, self.menuPrintEvent)
        self.menuEmailButton.Bind(wx.EVT_BUTTON, self.menuEmailEvent)
        self.menuSuggestButton.Bind(wx.EVT_BUTTON, self.suggestDish)
        self.nextIngredent.Bind(wx.EVT_BUTTON, self.nextIngredentCallback)
        self.previousIngredent.Bind(wx.EVT_BUTTON, self.previousIngredentCallback)
        self.increaseStock.Bind(wx.EVT_BUTTON, self.IncreaseStockCallback)
        self.decreaseStock.Bind(wx.EVT_BUTTON, self.DecreaseStockCallback)
        self.Bind(wx.EVT_CLOSE, self.writeALL)

        self.vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.panel.SetSizer(self.vbox)
        self.Centre()
        self.Show()
        self.previousIngredent.Hide()

        # read data files into core
        self.readInData()

        # initialize menu window
        for line in self.Menu:
            self.menuBox.Append(line)

        self.mealWindow = chooseMealWindow(None, title='meals')
        self.suggestMealWindow = suggestMealWindow(None, title="Suggest a Meal")

        self.refreshShoppingList()
        self.getCats()

    def getCats(self):
        catFile = open(self.CatFileName)
        allCats = catFile.read()
        self.allCatsList = allCats.split("%")

    @property
    def getRandomCat(self):

        numberCats = len(self.allCatsList)
        print(numberCats)
        random.seed()
        thisCat = self.allCatsList[random.randrange(numberCats)]

        return thisCat

    def readInData(self):
        readIn(self.Menu, self.MenuDict, self.MenuFileName)
        readIn(self.Recipies, self.RecipiesDict, self.RecipiesFileName)
        readIn(self.Ingredience, self.IngredienceDict, self.IngredianceFileName)

    def nextIngredentCallback(self, event):
        self.IngrediencePointer = min(self.IngrediencePointer + 1, len(self.Ingredience) - 1)

        if self.IngrediencePointer == len(self.Ingredience) - 1:
            self.nextIngredent.Hide()
        if self.IngrediencePointer > 0:
            self.previousIngredent.Show()

        self.ingredientBox.Clear()
        self.ingredientBox.AppendText(self.Ingredience[self.IngrediencePointer].rstrip())

    def previousIngredentCallback(self, event):
        self.IngrediencePointer = max(self.IngrediencePointer - 1, 0)

        if self.IngrediencePointer == 0:
            self.previousIngredent.Hide()
        if self.IngrediencePointer < len(self.Ingredience) - 1:
            self.nextIngredent.Show()

        self.ingredientBox.Clear()
        self.ingredientBox.AppendText(self.Ingredience[self.IngrediencePointer].rstrip())

    def DecreaseStockCallback(self, event):
        info = self.ingredientBox.GetValue().split()
        number = max(int(info[1]) - 1, 0)
        text = info[0] + " " + str(number)
        self.ingredientBox.Clear()
        self.ingredientBox.AppendText(text)
        self.Ingredience[self.IngrediencePointer] = info[0] + " " + str(number)

    def IncreaseStockCallback(self, event):
        info = self.ingredientBox.GetValue().split()
        number = max(int(info[1]) + 1, 0)
        text = info[0] + " " + str(number)
        self.ingredientBox.Clear()
        self.ingredientBox.AppendText(text)
        self.Ingredience[self.IngrediencePointer] = info[0] + " " + str(number)

    def saveIngredience(self):
        ingredianceFile = open(self.IngredianceFileName, 'w')
        for item in self.IngredienceDict.items():
            ingredianceFile.write(item[0] + " " + str((self.Ingredience[item[1]]).split(" ")[1]) + "\n")
        ingredianceFile.close()

    def readMenu(self):
        self.menuBox.Clear()
        for line in self.Menu:
            self.menuBox.Append(line.rstrip())

    def saveDishes(self):
        MenuFile = open(self.MenuFileName, "w")
        for index in range(self.menuBox.GetCount()):
            MenuFile.write(self.menuBox.GetString(index))
            MenuFile.write("\n")
        MenuFile.close()

    def suggestDish(self, event):
        recipies = []
        for recipyDetailsText in self.Recipies:
            good = True
            recipyDetails = recipyDetailsText.split(" ")
            for ingredientPnt in range(1, len(recipyDetails)):
                ingredientDetail = recipyDetails[ingredientPnt].split("*")
                numberWeNeed = int(ingredientDetail[0])
                item = ingredientDetail[1]
                ingredientIndex = self.IngredienceDict[item]
                numberWeHave = int(self.Ingredience[ingredientIndex].split(" ")[1])
                if numberWeHave < numberWeNeed:
                    good = False
            if good:
                recipies.append(recipyDetails)
        for r in recipies:
            self.suggestMealWindow.recipieBox.Append(r[0])

        self.suggestMealWindow.Show()
        self.suggestMealWindow.SetPosition((100, 100))


    def replaceButtonEvent(self, event):
        index = self.menuBox.GetSelection()
        text = self.menuBox.GetString(index)
        items = text.split(' ')
        self.menuBox.SetString(index, items[0] + " " + items[1] + " ")
        dish = items[2]
        recipyDetials = self.Recipies[self.RecipiesDict[dish]].split(" ")
        for ingredientPnt in range(1, len(recipyDetials)):
            ingredientDetail = recipyDetials[ingredientPnt].split("*")
            number = int(ingredientDetail[0])
            item = ingredientDetail[1]

            # add ingredient back into stock
            ingredientIndex = self.IngredienceDict[item]
            number1 = int(self.Ingredience[ingredientIndex].split(" ")[1])
            self.Ingredience[ingredientIndex] = item + " " + str(number+number1)

        self.refreshShoppingList()
        self.mealWindow.Show()
        self.mealWindow.SetPosition((800, 100))

    def addButtonEvent(self, event):
        endIndex = self.menuBox.GetCount()
        text = self.menuBox.GetString(endIndex - 1)
        items = text.split(' ')
        myDate = items[1].split('/')
        thisDay = date(int(myDate[2]), int(myDate[1]), int(myDate[0]))
        nextDay = thisDay + timedelta(days=1)
        nextWeekday = nextDay.strftime("%A")
        self.menuBox.Append(
            nextWeekday + " " + str(nextDay.day) + '/' + str(nextDay.month) + '/' + str(nextDay.year) + ' ')
        menuIndex = self.menuBox.Count - 1
        self.menuBox.SetFirstItem(menuIndex)
        self.menuBox.SetSelection(menuIndex)
        self.mealWindow.Show()
        self.mealWindow.SetPosition((800, 100))


    def menuPrintEvent(self, event):
        tempfile = open(self.TempFileName, "w")
        tempfile.write("\n\n\n\n\n\n\n\n\n")

        now = datetime.today()
        tempfile.write("            " + "Menu at " + now.strftime("%A %d. %B %Y") + "\n\n\n\n")

        yesterday = now - timedelta(days=1)
        for line in self.Menu:
            thisdateString = line.split(" ")[1]
            thisdate = datetime.strptime(thisdateString, "%d/%m/%Y")
            if yesterday < thisdate:
                tempfile.write("            " + line + "\n\n")
        tempfile.write("\n\n\n            xxxx\n\n\n" + self.getRandomCat)

        tempfile.close()
        os.system("lpr " + self.TempFileName)

    def menuEmailEvent(self, event):
        menuText = "\nShopping List\n------------------\n\n"
        number = 0
        for item in self.Ingredience:
            itemDetails = item.split(" ")
            if int(itemDetails[1]) < 0:
                menuText += itemDetails[0]+" "+str(-int(itemDetails[1]))+"\n"
            number += 1

        thisCat = self.getRandomCat

        menuText = menuText + thisCat + "\n\n\nxxxx\n"

        if number > 0:
            for address in emailAddresses:
                sendMail(menuText, address)

    def recordMenuSelect(self):
        menuIndex = self.menuBox.GetSelection()
        # self.menuBox.SetFirstItem(menuIndex)
        # self.menuBox.SetSelection(menuIndex)
        dish = self.menuBox.GetString(menuIndex).split(" ")[2]
        recipypnt = self.RecipiesDict[dish]

        recipyDetials = self.Recipies[recipypnt].split(" ")
        for ingredientPnt in range(1, len(recipyDetials)):
            ingredientDetail = recipyDetials[ingredientPnt].split("*")
            number = int(ingredientDetail[0])
            item = ingredientDetail[1]
            ingredientAddress = self.IngredienceDict[item]

            stock = int(self.Ingredience[ingredientAddress].split(" ")[1])
            stock = stock - number
            self.Ingredience[ingredientAddress] = item + " " + str(stock)

        self.refreshShoppingList()

    def refreshShoppingList(self):
        self.shoppinglistBox.Clear()
        for item in self.Ingredience:
            ingredient = item.split(" ")[0]
            number = int(item.split(" ")[1])
            if number < 0:
                self.shoppinglistBox.Append(ingredient+" "+str(-number))

    def writeALL(self, event):
        self.saveDishes()
        self.saveIngredience()
        self.mealWindow.Destroy()
        self.Destroy()
        exit(0)




class suggestMealWindow(wx.Frame):

    def __init__(self, parent, title):
        super(suggestMealWindow, self).__init__(parent, title=title, size=(300, 300))
        self.panel = wx.Panel(self, size=(300, 300))

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.recipieBox = wx.ListBox(self.panel, style=wx.ALIGN_RIGHT, size=(260, 230))

        self.vbox.AddSpacer(20)
        self.vbox.Add(self.recipieBox)
        self.vbox.AddSpacer(20)

        self.hbox.AddSpacer(20)
        self.hbox.Add(self.vbox)
        self.hbox.AddSpacer(20)

        self.panel.SetSizer(self.hbox)


class chooseMealWindow(wx.Frame):

    def __init__(self, parent, title):
        super(chooseMealWindow, self).__init__(parent, title=title, size=(340, 75))
        self.panel = wx.Panel(self, size=(440, 40))

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.recipieBox = wx.TextCtrl(self.panel, style=wx.ALIGN_LEFT, size=(200, 30))
        self.buttonGO = wx.Button(self.panel, id=wx.ID_ANY, label='GO', size=(30, 30))
        self.buttonNEXT = wx.Button(self.panel, id=wx.ID_ANY, label='NXT', size=(30, 30))
        self.buttonPREVIOUS = wx.Button(self.panel, id=wx.ID_ANY, label='PRE', size=(30, 30))

        self.hbox.AddSpacer(10)
        self.hbox.Add(self.recipieBox, 1)
        self.hbox.AddSpacer(10)
        self.hbox.Add(self.buttonGO, 0, wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
        self.hbox.AddSpacer(10)
        self.hbox.Add(self.buttonNEXT, 0, wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
        self.hbox.AddSpacer(10)
        self.hbox.Add(self.buttonPREVIOUS, 0, wx.RESERVE_SPACE_EVEN_IF_HIDDEN)

        self.vbox.AddSpacer(10)
        self.vbox.Add(self.hbox)
        self.vbox.AddSpacer(10)

        self.panel.SetSizer(self.vbox)

        self.index = -1
        self.buttonPREVIOUS.Hide()

        # callbacks
        self.buttonNEXT.Bind(wx.EVT_BUTTON, self.nextDish)
        self.buttonPREVIOUS.Bind(wx.EVT_BUTTON, self.previousDish)
        self.buttonGO.Bind(wx.EVT_BUTTON, self.chooseDish)

    def chooseDish(self, event):
        menuItem = self.recipieBox.GetValue()
        selection = mywin.menuBox.GetSelection()
        mywin.menuBox.SetString(selection, mywin.menuBox.GetString(selection) + menuItem)
        mywin.dishes.append(menuItem)
        self.Hide()
        mywin.recordMenuSelect()

    def nextDish(self, event):
        self.index = self.index + 1
        self.recipieBox.ChangeValue(mywin.Recipies[self.index].split(" ")[0])
        if self.index >= 1:
            self.buttonPREVIOUS.Show()
            self.hbox.Layout()
        if self.index == len(mywin.Recipies) - 1:
            self.buttonNEXT.Hide()

    def previousDish(self, event):
        self.index = self.index - 1
        self.recipieBox.ChangeValue(mywin.Recipies[self.index].split(" ")[0])
        if self.index < 1:
            self.buttonPREVIOUS.Hide()
        if self.index < len(mywin.Recipies) - 1:
            self.buttonNEXT.Show()
            self.hbox.Layout()


app = wx.App()
mywin = Example(None, title='BoxSizer demo')
app.MainLoop()
