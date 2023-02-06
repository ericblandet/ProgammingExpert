import asyncio
from inventory import Inventory
from order import Order


def display_catalogue(catalogue):
    burgers = catalogue["Burgers"]
    sides = catalogue["Sides"]
    drinks = catalogue["Drinks"]

    print("--------- Burgers -----------\n")
    for burger in burgers:
        item_id = burger["id"]
        name = burger["name"]
        price = burger["price"]
        print(f"{item_id}. {name} ${price}")

    print("\n---------- Sides ------------")
    for side in sides:
        sizes = sides[side]

        print(f"\n{side}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n---------- Drinks ------------")
    for beverage in drinks:
        sizes = drinks[beverage]

        print(f"\n{beverage}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n------------------------------\n")


async def get_order(inventory, number_of_items):
    order = Order(inventory)
    tasks = []

    print("Please enter the number of items that you would like to add to your order. Enter q to complete your order.")
    while True:
        item_id = input("Enter an item number: ").lower()
        if item_id == "q":
            break
        elif not item_id.isdigit():
            print("Invalid input")
            continue
        elif int(item_id) > number_of_items:
            print(f"Maximum item is {number_of_items}")
            continue
        else:
            task = asyncio.create_task(order.add_item(int(item_id)))
            tasks.append(task)

    print("Placing order...")

    for task in tasks:
        stock, item = await task
        if not stock:
            print(
                f"Unfortunately item number {item['id']} is out of stock and has been removed from your order. Sorry!")

    return order


async def main():
    inventory = Inventory()
    task_1 = asyncio.create_task(inventory.get_number_of_items())
    print("Welcome to the ProgrammingExpert Burger Bar!")
    display_catalogue(inventory.catalogue)
    number_of_items = await task_1
    new_order = "yes"

    while new_order in ["yes", "y"]:

        order = await get_order(inventory, number_of_items)
        order.prepare_combos()
        order.display_order()

        while True:
            confirm = input(
                f"Would you like to purchase this order for ${round(order.total,2)} (yes/no)? ").lower()
            if confirm in ["yes", "y"]:
                print("Thank you for your order!")
                break
            elif confirm in ["no", "n"]:
                # cancel order !
                break
            else:
                print("invalid input!")
                continue

        new_order = input(
            "Would you like to make another order(yes/no)? ").lower()

    print("Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())
