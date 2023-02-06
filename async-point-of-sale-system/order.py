from inventory import Inventory
import asyncio


class Order:
    def __init__(self, inventory):
        self.categories = ["Burgers", "Sides", "Drinks"]
        self.items = {"Combos": [], "Burgers": [], "Sides": [], "Drinks": []}
        self.inventory = inventory
        self.combo_discount = 0.15
        self.tax_rate = 0.05

    async def add_item(self, item_id):
        stock, item = await asyncio.gather(self.inventory.get_stock(item_id),
                                           self.inventory.get_item(item_id)
                                           )
        if stock > 0:
            success = await self.inventory.decrement_stock(item_id)
            # This may not be successful because in the time we waited
            # to get the stock and item the stock level may have decreased.
            if not success:
                return False, item

            self.items[item['category']].append(item)

            return True, item

        else:
            return False, item

    def prepare_combos(self):
        for category in self.items.keys():
            self.items[category].sort(key=lambda x: x['price'], reverse=True)
        while min(len(self.items["Burgers"]), len(self.items["Sides"]), len(self.items["Drinks"])) > 0:
            combo = []
            for category in self.categories:
                combo.append(self.items[category].pop(0))
            self.items["Combos"].append(combo)

    def get_combo_price(self, combo):
        return (1-self.combo_discount) * \
            (sum(map(lambda x: x["price"], combo)))

    def print_name(self, item):
        if item.get("name") is not None:
            return item['name']
        else:
            return f"{item['size']} {item['subcategory']}"

    def display_order(self):
        self.compute_prices()

        print("\n")
        print("Here is a summary of your order:")
        print("\n")
        for combo in self.items["Combos"]:
            combo_price = self.get_combo_price(combo)
            print(f"${round(combo_price,2)} Burger Combo")
            for el in combo:
                print(f"  {self.print_name(el)}")

        for category in self.categories:
            for el in self.items[category]:
                print(f"${round(el['price'],2)} {self.print_name(el)}")

        print("\n")
        print("-------")
        print(f"Subtotal: ${round(self.subtotal,2)}")
        print(f"Tax: ${round((self.tax), 2)}")
        print(f"Total: ${round(self.total, 2)}")
        print("-------")

    def compute_prices(self):
        self.subtotal = sum(
            map(lambda x: self.get_combo_price(x), self.items["Combos"])) + sum(el["price"] for category in self.categories for el in self.items[category])
        self.tax = self.subtotal * (self.tax_rate)
        self.total = self.subtotal * (1+self.tax_rate)

    def clear(self):
        self.items = []
