from itens.itensmerchant.itens_for_sell import get_sellers_items

class Merchant:
    def __init__(self):
        self.name = "Doom HardMob"
        self.items_for_sale = []

    def show_menu(self, player):
        while True:
            print(f"\n--- Bem-vindo(a) à loja do(a) {self.name}! ---")
            print("1) Vender itens")
            print("2) Comprar itens")
            print("0) Sair")
            print(f"Seu dinheiro atual: R$ {player.money}")

            try:
                choice = int(input("\nO que você gostaria de fazer? "))

                if choice == 1:
                    self.sell_items(player)
                elif choice == 2:
                    self.buy_items(player)
                elif choice == 0:
                    print("Até logo!")
                    break
                else:
                    print("Escolha inválida, por favor, tente novamente.")
            except ValueError:
                print("Por favor, digite um número válido.")

    def sell_items(self, player):
        while True:
            if not player.bag:
                print("Você não tem itens para vender.")
                return

            player.show_bag_itens()
            print("0) Cancelar e voltar")

            try:
                choice = int(input("\nQual item você quer vender? ")) - 1

                if choice == -1:
                    return
                
                if choice < 0 or choice >= len(player.bag):
                    print("Número de item inválido!")
                    continue

                item_to_sell = player.bag[choice]
                player.money += item_to_sell.price
                player.remove_item(item_to_sell)
                print(f"Você vendeu {item_to_sell.name} por R$ {item_to_sell.price}.")
                print(f"Seu dinheiro atual: R$ {player.money}")

                sell_more = input("Quer vender mais itens? [s/n]: ").lower()
                if sell_more != 's':
                    break
            except ValueError:
                print("Por favor, digite um número válido.")

    def buy_items(self, player):
        self.items_for_sale = get_sellers_items(player)
        while True:
            print(f"\n--- Itens à venda na {self.name}'s Shop ---")
            for idx, item in enumerate(self.items_for_sale, 1):
                print(f"{idx}) {item}")
            print("0) Cancelar e voltar")
            print(f"Seu dinheiro atual: R$ {player.money}")
            
            try:
                choice = int(input("\nQual item você quer comprar? ")) - 1

                if choice == -1:
                    return

                if choice < 0 or choice >= len(self.items_for_sale):
                    print("Número de item inválido!")
                    continue

                item_to_buy = self.items_for_sale[choice]
                
                if player.money >= item_to_buy.price:
                    player.money -= item_to_buy.price
                    player.add_item(item_to_buy)
                    print(f"Você comprou {item_to_buy.name} por R$ {item_to_buy.price}.")
                    print(f"Seu dinheiro atual: R$ {player.money}")
                else:
                    print("Dinheiro insuficiente para comprar este item.")
                
                buy_more = input("Quer comprar mais itens? [s/n]: ").lower()
                if buy_more != 's':
                    break
            except ValueError:
                print("Por favor, digite um número válido.")