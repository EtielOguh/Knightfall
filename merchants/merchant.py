from itens.itensmerchant.itens_for_sell import get_sellers_items

class Merchant:
    def __init__(self):
        self.name = "Doom HardMob"
        self.items_for_sale = []

    def show_menu(self, player):
        while True:
            print(f"\n--- Wellcome to the {self.name} store! ---")
            print("1) Sell Itens")
            print("2) Store")
            print("0) Sair")
            print(f"Your actual money: {player.money}")

            try:
                choice = int(input("\n What do you want to do?"))

                if choice == 1:
                    self.sell_items(player)
                elif choice == 2:
                    self.buy_items(player)
                elif choice == 0:
                    print("See you soon!")
                    break
                else:
                    print("Wrong! type again")
            except ValueError:
                print("Please tell me a right answer")

    def sell_items(self, player):
        while True:
            if not player.bag:
                print("You don't have itens to sell\n Sorry!")
                return

            player.show_bag_itens()
            print("0) Cancel and Back")

            try:
                choice = int(input("\nWhich item you want to sell: ")) - 1

                if choice == -1:
                    return
                
                if choice < 0 or choice >= len(player.bag):
                    print("Invalid number! Try again!")
                    continue

                item_to_sell = player.bag[choice]
                player.money += item_to_sell.price
                player.remove_item(item_to_sell)
                print(f"You have been sold a {item_to_sell.name} for: {item_to_sell.price}.")
                print(f"You actual money is: {player.money}")

                sell_more = input("Wanna sell more? [y/n]: ").lower()
                if sell_more != 'y':
                    break
            except ValueError:
                print("Wrong answer, try again!")

    def buy_items(self, player):
        self.items_for_sale = get_sellers_items(player)
        while True:
            print(f"\n--- Itens for sell {self.name}'s Shop ---")
            for idx, item in enumerate(self.items_for_sale, 1):
                print(f"{idx}) {item}")
            print("0) Cancel and Back")
            print(f"You actual money is: {player.money}")
            
            try:
                choice = int(input("\nWhich item you wanna buy: ")) - 1

                if choice == -1:
                    return

                if choice < 0 or choice >= len(self.items_for_sale):
                    print("Wrong number! Try again!")
                    continue

                item_to_buy = self.items_for_sale[choice]
                
                if player.money >= item_to_buy.price:
                    player.money -= item_to_buy.price
                    player.add_item(item_to_buy)
                    print(f"You have bought {item_to_buy.name} for: {item_to_buy.price}.")
                    print(f"You actual money is: {player.money}")
                else:
                    print("You don't have enought money! Why are you here for??!")
                
                buy_more = input("Wanna sell me more itens? [y/n]: ").lower()
                if buy_more != 'y':
                    break
            except ValueError:
                print("Wrong number! Try again")