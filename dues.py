
from option_3 import splitTransaction
owed = splitTransaction(8)
def option_2(num: str):
    match num:
        case "1":
            print("Here's Tommy's balance:\n" \
            "Tommy currently owes you $ " + owed)
            
        case "2":
            print("Here's Hiram's balance: \n")
        case "3":
            print("Here's Hazel's balance: \n")
        case "4":
            print("Here's Kyle's balance: \n")
        case "5":
            print("Here's Michael's balance: \n")
        case "6":
            print("Everyone's balances: ")