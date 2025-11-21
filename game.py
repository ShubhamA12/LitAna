# player_inventory = ['health potion', 'wooden sword', 'water bottle']
# player_health = 100

# def show_inventory():
#     if not player_inventory:
#         print("Your inventory is empty.")
#     else:
#         print("You have the following items in your inventory:")
#         for item in player_inventory:
#             print(f"- {item}")

# def show_status():
#     print(f"Your current health is: {player_health}")

# def start_game():
#     print("Welcome to the Simple Adventure Game!")
#     show_status()
#     print("You find yourself at the entrance of a mysterious forest.")
#     print("Do you want to 'enter' the forest or 'turn back'?")
#     print("You can also type 'inventory' to check your items or 'status' to check your health at any time.")

#     choice = ""
#     while choice not in ["enter", "turn back"]:
#         choice = input("> ").lower()
#         if choice == "inventory":
#             show_inventory()
#         elif choice == "status":
#             show_status()
#         elif choice == "enter":
#             forest_path()
#         elif choice == "turn back":
#             print("You decide to turn back and return home. The adventure ends here.")
#         else:
#             print("Invalid choice. Please type 'enter' or 'turn back'.")


# def forest_path():
#     print("\nYou enter the forest. The trees are tall and the path is narrow.")
#     print("You see a 'glowing object' in the distance or you can 'follow' the path deeper.")

#     choice = ""
#     while choice not in ["glowing object", "follow"]:
#         choice = input("> ").lower()
#         if choice == "inventory":
#             show_inventory()
#         elif choice == "status":
#             show_status()
#         elif choice == "glowing object":
#             glowing_object_encounter()
#         elif choice == "follow":
#             deep_forest_path()
#         else:
#             print("Invalid choice. Please type 'glowing object' or 'follow'.")


# def glowing_object_encounter():
#     print("\nYou approach the glowing object and find it's a magical amulet!")
#     print("Do you 'take' the amulet or 'leave' it?")

#     choice = ""
#     while choice not in ["take", "leave"]:
#         choice = input("> ").lower()
#         if choice == "inventory":
#             show_inventory()
#         elif choice == "status":
#             show_status()
#         elif choice == "take":
#             print("You take the amulet. It hums with power. You feel a surge of energy!")
#             player_inventory.append("magical amulet")
#             # After taking the amulet, let's continue the journey
#             deep_forest_path()
#         elif choice == "leave":
#             print("You decide to leave the amulet untouched and continue your journey.")
#             deep_forest_path()
#         else:
#             print("Invalid choice. Please type 'take' or 'leave'.")


# def deep_forest_path():
#     global player_health
#     print("\nYou follow the path deeper into the forest. It gets darker and more eerie.")
#     print("Suddenly, you encounter a 'friendly squirrel' or a 'growling beast'.")

#     choice = ""
#     while choice not in ["friendly squirrel", "growling beast"]:
#         choice = input("> ").lower()
#         if choice == "inventory":
#             show_inventory()
#         elif choice == "status":
#             show_status()
#         elif choice == "friendly squirrel":
#             print("The squirrel offers you a nut. You feel a sense of calm.")
#             print("The adventure continues another day.")
#         elif choice == "growling beast":
#             if "magical amulet" in player_inventory:
#                 print("The beast sees the magical amulet and whimpers, backing away into the shadows.")
#                 print("Your amulet protected you!")
#             else:
#                 print("The beast lunges at you! You manage to escape, but not unharmed.")
#                 player_health -= 50
#                 show_status()
#                 if player_health <= 0:
#                     print("You have taken too much damage. You collapse. The adventure is over.")
#                 else:
#                     print("You are wounded, but you can continue.")

#         else:
#             print("Invalid choice. Please type 'friendly squirrel' or 'growling beast'.")

# # Start the game
# if __name__ == "__main__":
#     start_game()