import pickle
import os
import random

def loadGame(filename = "map.pickle"):
    with open(filename, 'rb') as f:
        character = pickle.load(f)
    return character

def saveGame(character, filename = "map.pickle"):
    with open(filename, 'wb') as f:
        pickle.dump(character, f)

class Character:
    def loadCharacter(self):
        tempCharacter = loadGame()
        self.area = tempCharacter.area
        self.x = tempCharacter.x
        self.y = tempCharacter.y
        self.inventory = tempCharacter.inventory
        self.items = tempCharacter.items
        self.lore = tempCharacter.lore
        self.currentRoom = tempCharacter.currentRoom
        self.roomsLeft = tempCharacter.roomsLeft
        self.unlocked = tempCharacter.unlocked
    def __init__(self,room=[[[[]]]],x=5,y=3,inventory=[['dust','does nothing']],currentRoom = 0,roomsLeft=6):
        self.area = room
        self.x = x - 1
        self.y = y - 1
        self.inventory = inventory
        self.items = [
["Power Cell", "Looks like it needs to be connected to some bank"],
["Power Bank", "It's empty, it might need some source of power"],
["Power Cord", "It needs to be attached to some center to work"],
["Power Housing Center", "Only useful with a cord"]
]
        self.lore = [
"Day 45: I think i'm close to finding the perfect combination of materials, so my life's work will be complete.. You decide to stop reading, it's hurting your head.",
"Day 10: hopeful but with a bit of skepticism",
"Day 37: hope is gone",
"Day 1: hopeful text",
"Day 24: slightly more worrying text",
"Day 56: Oh god what have I done"
]
        self.currentRoom = currentRoom
        self.roomsLeft = roomsLeft
        self.unlocked = False
        self.update()
    def __str__(self):
        return f"{self.x} {self.y} {self.items} {self.lore} {self.currentRoom} {self.roomsLeft}"
    def stringMap(self):
        j = 0
        i = 0
        rep = ""
        while j < len(self.area[self.currentRoom]):
            if self.x == i and self.y == j:
                rep += "C"
            elif self.area[self.currentRoom][j][i][1] == 'F':
                rep += self.area[self.currentRoom][j][i][0]
            else:
                rep += " "
            if i == len(self.area[self.currentRoom][0])-1:
                i = -1
                j += 1
                rep += "\n"
            i += 1
        return rep
    def stringInventory(self):
        rep = "Inventory: "
        for item in self.inventory:
            rep += item[0]
            rep += ", "
        return rep.strip(", ")
    def generateRoom(self,direction):
        self.roomsLeft -= 1
        newCurrentRoom = len(self.area)
        oldCurrentRoom = self.currentRoom
        self.currentRoom = newCurrentRoom
        room = [
[['/','N'],['-','N'],['-','N'],['-','N'],['-','N'],['-','N'],['-','N'],['-','N'],['\\','N']],
[['|','N'],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['|','N']],
[['|','N'],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['|','N']],
[['|','N'],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['|','N']],
[['\\','N'],['-','N'],['-','N'],['-','N'],['-','N'],['-','N'],['-','N'],['-','N'],['/','N',-1,-1,-1,-1]]]
        self.area.append(room)
        if direction == "up":
            self.area[oldCurrentRoom][-1][-1][4] = newCurrentRoom
            self.area[self.currentRoom][-1][-1][5] = oldCurrentRoom 
            self.area[self.currentRoom][len(self.area[self.currentRoom])-1][self.x][0] = "+"
        elif direction == "down":
            self.area[oldCurrentRoom][-1][-1][5] = newCurrentRoom
            self.area[self.currentRoom][-1][-1][4] = oldCurrentRoom
            self.area[self.currentRoom][0][self.x][0] = "+"
        elif direction == "left":
            self.area[oldCurrentRoom][-1][-1][2] = newCurrentRoom
            self.area[self.currentRoom][-1][-1][3] = oldCurrentRoom
            self.area[self.currentRoom][self.y][len(self.area[self.currentRoom][0]) - 1][0] = "+"
        elif direction == "right":
            self.area[oldCurrentRoom][-1][-1][3] = newCurrentRoom
            self.area[self.currentRoom][-1][-1][2] = oldCurrentRoom
            self.area[self.currentRoom][self.y][0][0] = "+"
        if self.roomsLeft > 0:
            i = random.randint(1,4)
            if i == 1 and self.area[self.currentRoom][0][4][0] != "+":
                self.area[self.currentRoom][0][4] = ['+','N']
            elif i == 2 and self.area[self.currentRoom][2][0][0] != "+":
                self.area[self.currentRoom][2][0] = ['+','N']
            elif i == 3 and self.area[self.currentRoom][2][8][0] != "+":
                self.area[self.currentRoom][2][8] = ['+','N']
            elif i == 4 and self.area[self.currentRoom][4][4][0] != "+":
                self.area[self.currentRoom][4][4] = ['+','N']  
            else:
                self.roomsLeft += 1
            i = random.randint(1,1*self.roomsLeft)
            if i in (1,2) and len(self.items) != 0:
                randomItem = self.items[random.randint(0,len(self.items)-1)]
                self.items.remove(randomItem)
                self.area[self.currentRoom][random.randint(1,3)][random.randint(1,7)] = ['?','N',randomItem]
            i = random.randint(1,4)
            if i == 1:
                randomLore = self.lore[random.randint(0,len(self.lore)-1)]
                self.lore.remove(randomLore)
                randx = random.randint(1,3)
                randy = random.randint(1,7)
                while self.area[self.currentRoom][randx][randy][0] == '?':
                    randx = random.randint(1,3)
                    randy = random.randint(1,7)
                self.area[self.currentRoom][randx][randy] = ['S', 'N',randomLore]
        if self.roomsLeft == 0:
            if self.area[self.currentRoom][2][8][0] != "+":
                self.area[self.currentRoom][2][8] = ['E','F']
                self.area[self.currentRoom][1][8][1] = 'F'
                self.area[self.currentRoom][3][8][1] = 'F'
                self.area[self.currentRoom][2][7][1] = 'F' 
            else:
                self.area[self.currentRoom][2][0] = ['E','F']
                self.area[self.currentRoom][2][1][1] = 'F'
                self.area[self.currentRoom][1][0][1] = 'F'
                self.area[self.currentRoom][3][0][1] = 'F' 
        self.update()
    def options(self):
        rep = "You can move: "
        if ".+?SE".find(self.area[self.currentRoom][self.y+1][self.x][0]) != -1:
            rep += "south, "
        if ".+?SE".find(self.area[self.currentRoom][self.y-1][self.x][0]) != -1:
            rep += "north, "
        if ".+?SE".find(self.area[self.currentRoom][self.y][self.x+1][0]) != -1:
            rep += "east, "
        if ".+?SE".find(self.area[self.currentRoom][self.y][self.x-1][0]) != -1:
            rep += "west, "
        rep = rep.strip(", ")
        rep += "\nYou can also: save, load, quit, mapKey (shows the key for the map), inspect, use, "
        if "?".find(self.area[self.currentRoom][self.y][self.x][0]) != -1:
            rep += "grab"
        return rep.strip(", ")
    def update(self):
        if self.area[self.currentRoom][self.y][self.x][0] == "+":
            direction = ""
            if self.x == 0:
                newCurrentRoom = self.area[self.currentRoom][-1][-1][2]
                self.x = len(self.area[self.currentRoom][0]) - 2
                direction = "left"
            elif self.x == len(self.area[self.currentRoom][0]) - 1:
                newCurrentRoom = self.area[self.currentRoom][-1][-1][3]
                self.x = 1
                direction = "right"
            elif self.y == 0:
                newCurrentRoom = self.area[self.currentRoom][-1][-1][4]
                self.y = len(self.area[self.currentRoom]) - 2
                direction = "up"
            elif self.y == len(self.area[self.currentRoom]) - 1:
                newCurrentRoom = self.area[self.currentRoom][-1][-1][5]
                self.y = 1
                direction = "down"
            if newCurrentRoom == -1:
                self.generateRoom(direction)
                return
            self.currentRoom = newCurrentRoom
        if self.area[self.currentRoom][self.y][self.x][0] == "E":
            if self.unlocked:
                return
            else:
                if self.x == len(self.area[self.currentRoom][0])-1:
                    print("The door is locked")
                    self.x -= 1
                else:
                    print("The door is locked")
                    self.x += 1
        self.area[self.currentRoom][self.y+1][self.x][1] = 'F'
        self.area[self.currentRoom][self.y+1][self.x+1][1] = 'F'
        self.area[self.currentRoom][self.y+1][self.x-1][1] = 'F'
        self.area[self.currentRoom][self.y-1][self.x+1][1] = 'F'
        self.area[self.currentRoom][self.y-1][self.x-1][1] = 'F'
        self.area[self.currentRoom][self.y-1][self.x][1] = 'F'
        self.area[self.currentRoom][self.y][self.x+1][1] = 'F'
        self.area[self.currentRoom][self.y][self.x-1][1] = 'F'
        self.area[self.currentRoom][self.y][self.x][1] = 'F'
    def response(self,choice):
        rep = ""
        if choice == "sayintro":
            rep += "Map Key:\n|-:Wall\nS:Sign\n?:Item\n.:Empty\nC:Character\n+:Door\nE:Escape\n"
            rep += "You wake up in a strange room, no reminders of your past, find out where to go!"
        elif choice == "mapKey":
            rep += "Map Key:\n|-/\\:Wall\nS:Sign\n?:Item\n.:Empty\nC:Character\n+:Door\nE:Escape\n"
        elif c.options().find(choice.lower()) != -1 and choice.lower() == "south":
            self.y += 1
            rep += "You move south"
        elif c.options().find(choice.lower()) != -1 and choice.lower() == "north":
            self.y -= 1
            rep += "You move north"
        elif c.options().find(choice.lower()) != -1 and choice.lower() == "east":
            self.x += 1
            rep += "You move east"
        elif c.options().find(choice.lower()) != -1 and choice.lower() == "west":
            self.x -= 1
            rep += "You move west"
        elif choice.lower() == "grab" and self.area[self.currentRoom][self.y][self.x][0] == "?":
            rep += f"You grab a {self.area[self.currentRoom][self.y][self.x][2][0]}"
            if self.inventory[0][0] == "dust":
                self.inventory.pop()
            self.inventory.append(self.area[self.currentRoom][self.y][self.x][2])
            self.area[self.currentRoom][self.y][self.x] = [".","F"]
        elif choice.lower() == "save":
            saveGame(self)
            rep += "Game Saved!"
        elif choice.lower() == "load":
            self.loadCharacter()
            rep += "Game Loaded!"
        elif choice.lower() == "inspect":
            print(self.stringInventory())
            item = input("What item?\n")
            i = 0
            rep += "Not found"
            while i < len(self.inventory):
                if item.lower() == self.inventory[i][0].lower():
                    rep = rep.strip("Not found")
                    rep += str(self.inventory[i][1])
                    break
                i += 1
            os.system('clear')
        elif choice.lower() == "use":
            print(self.stringInventory())
            item = input("What item?\n").lower()
            i = 0
            rep += "Not found"
            while i < len(self.inventory):
                if item == self.inventory[i][0].lower():
                    rep = rep.strip("Not found")
                    break
                i += 1
            if rep.find("Not found") == -1 and item != "complete power housing unit":
                item2 = input("Use with?\n").lower()
                i = 0
                rep += "Not found"
                while i < len(self.inventory):
                    if item == self.inventory[i][0].lower():
                        rep = rep.strip("Not found")
                        break
                    i += 1
            if rep.find("Not found") == -1 and item != "complete power housing unit":
                if (item == "power bank" and item2 == "power cell") or (item == "power cell" and item2 == "power bank"):
                    rep += "Items Combined!\nYou've made a Filled Power Bank"
                    self.inventory.remove(["Power Bank", "It's empty, it might need some source of power"])
                    self.inventory.remove(["Power Cell", "Looks like it needs to be connected to some bank"])
                    self.inventory.append(["Filled Power Bank", "Just needs a connector"])
                elif (item == "power cord" and item2 == "power housing center") or (item == "power housing center" and item2 == "power cord"):
                    rep += "Items Combined!\nYou've made a Power Connector"
                    self.inventory.remove(["Power Cord", "It needs to be attached to some center to work"])
                    self.inventory.remove(["Power Housing Center", "Only useful with a cord"])
                    self.inventory.append(["Power Connector", "Just needs a source of power"])
                elif (item == "power connector" and item2 == "filled power bank") or (item == "filled power bank" and item2 == "power connector"):
                    rep += "Items Combined!\nYou've made a Complete Power Housing Unit"
                    self.inventory.remove(["Power Connector", "Just needs a source of power"])
                    self.inventory.remove(["Filled Power Bank", "Just needs a connector"])
                    self.inventory.append(["Complete Power Housing Unit", "Looks like it'd fit in some escape door"])
                else:
                    rep += "Those Items Don't Connect"
            if item == "complete power housing unit":
                if self.area[self.currentRoom][self.y+1][self.x][0] == "E" or self.area[self.currentRoom][self.y-1][self.x][0] == "E" or self.area[self.currentRoom][self.y][self.x+1][0] == "E" or self.area[self.currentRoom][self.y][self.x-1][0] == "E":
                    rep += "Item slotted into the door, It's Now Unlocked ESCAPE!"
                    self.unlocked = True
                    self.inventory.remove(["Complete Power Housing Unit", "Looks like it'd fit in some escape door"])
                else:
                    rep += "Can't use that here"
            os.system('clear')
        else:
            rep += "not a valid option"
        if self.area[self.currentRoom][self.y][self.x][0] == "?" and choice.lower() != "grab":
            rep += f"\nYou find a {self.area[self.currentRoom][self.y][self.x][2][0]}"
        if self.area[self.currentRoom][self.y][self.x][0] == "S":
            rep += f"\nYou read the sign, it says:\n"
            rep += self.area[self.currentRoom][self.y][self.x][2]
        self.update()
        return rep


#main         
choice = "sayintro"
area = [
[[['/','N'],['-','N'],['-','N'],['-','N'],['+','N'],['-','N'],['-','N'],['-','N'],['\\','N']],
[['|','N'],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['|','N']],
[['+','N'],['.','N'],['?','N',["Magic Skull","Who's is this??"]],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['+','N']],
[['|','N'],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['.','N'],['S','N',"Good Luck"],['|','N']],
[['\\','N'],['-','N'],['-','N'],['-','N'],['+','N'],['-','N'],['-','N'],['-','N'],['/','N',-1,-1,-1,-1]]]
]
c = Character(area)
while choice.lower() != "quit":
    os.system('clear')        
    print(c.response(choice))
    if (c.area[c.currentRoom][c.y][c.x][0] == "E"):
        os.system('clear')
        print("YOU ESCAPED!!")
        print("Map Key:\n,:Grass\nC:You\n")
        print("...|,,,,,\n...|,,,,,\n...+C,,,,\n...|,,,,,\n...|,,,,,")
        break
    print(c.stringMap())
    print(c.stringInventory())
    print(c.options())
    choice = input("What would you like to do?\n")
    
        
