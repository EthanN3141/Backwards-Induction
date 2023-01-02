from IndTree import IndTree


BInduction = IndTree("samplegame.txt")

ID = input("Input the index of your starting node: ")

while ID != "-1":
    try:
        BInduction.equilibrate(int(ID))
    except ValueError:
        print("Invalid input! Please only input integers")

    ID = input("Input the index of your starting node: ")


print("Thanks for playing! Have a nice day!")