import io
# Import the BAML client and types
from baml_client import b 
# We only import these to construct the request, not to hold state
from baml_client.types import GameState, Fighter, InventoryItem, ActionType

class GameEngine:
    def __init__(self):
        # 1. USE STANDARD PYTHON DICTIONARIES FOR MUTABLE STATE
        self.player = {
            "name": "Hero",
            "hp": 100,
            "max_hp": 100,
            "inventory": [{"name": "Potion", "quantity": 2, "effect_value": 30}]
        }
        
        self.opponent = {
            "name": "Dark Knight",
            "hp": 120,
            "max_hp": 120,
            "inventory": [{"name": "Dark Elixir", "quantity": 1, "effect_value": 50}]
        }
        
        self.last_player_move = None

    # Helper to convert Dict -> BAML Type just for the API call
    def get_baml_state(self):
        return GameState(
            player=Fighter(
                name=self.player["name"],
                hp=self.player["hp"],
                max_hp=self.player["max_hp"],
                inventory=[InventoryItem(**item) for item in self.player["inventory"]]
            ),
            opponent=Fighter(
                name=self.opponent["name"],
                hp=self.opponent["hp"],
                max_hp=self.opponent["max_hp"],
                inventory=[InventoryItem(**item) for item in self.opponent["inventory"]]
            ),
            last_player_move=self.last_player_move
        )

    def print_status(self):
        p_potions = self.player["inventory"][0]["quantity"]
        o_potions = self.opponent["inventory"][0]["quantity"]
        
        print("\n" + "="*40)
        print(f"🛡️  {self.player['name']}: {self.player['hp']}/{self.player['max_hp']} HP | Potions: {p_potions}")
        print(f"💀 {self.opponent['name']}: {self.opponent['hp']}/{self.opponent['max_hp']} HP | Potions: {o_potions}")
        print("="*40 + "\n")

    def process_damage(self, defender_dict, is_defending):
        damage = 15 if not is_defending else 5
        defender_dict["hp"] = max(0, defender_dict["hp"] - damage)
        return damage

    def process_heal(self, char_dict):
        # Find potion in the list
        potion = next((i for i in char_dict["inventory"] if i["name"] in ["Potion", "Dark Elixir"]), None)
        
        if potion and potion["quantity"] > 0:
            heal_amt = potion["effect_value"]
            char_dict["hp"] = min(char_dict["max_hp"], char_dict["hp"] + heal_amt)
            potion["quantity"] -= 1
            return heal_amt
        return 0


def main():
    game = GameEngine()
    print("⚔️  BATTLE STARTED: HERO vs DARK KNIGHT ⚔️")

    while game.player["hp"] > 0 and game.opponent["hp"] > 0:
        game.print_status()

        # --- 1. Player Turn ---
        print("Choose Action: [1] Attack  [2] Heal  [3] Defend")
        choice = input(">> ")
        
        player_action = "WAIT"
        player_defending = False

        if choice == "1":
            # Pass the DICTIONARY, not the BAML object
            dmg = game.process_damage(game.opponent, False) 
            print(f"👊 You attacked for {dmg} damage!")
            player_action = "ATTACK"
        elif choice == "2":
            amt = game.process_heal(game.player)
            if amt > 0:
                print(f"✨ You healed for {amt} HP.")
                player_action = "HEAL"
            else:
                print("❌ No potions left!")
                player_action = "FAILED_HEAL"
        elif choice == "3":
            print("🛡️ You brace yourself.")
            player_defending = True
            player_action = "DEFEND"
        else:
            print("Invalid move, you stumble!")

        game.last_player_move = player_action

        # Check win condition immediately after player move
        if game.opponent["hp"] <= 0:
            break

        # --- 2. Opponent Turn ---
        print("\n🤔 The Dark Knight is thinking...")
        
        # CONVERT STATE TO BAML TYPES HERE
        current_baml_state = game.get_baml_state()

        # Call LLM
        bot_move = b.DecideOpponentMove(state=current_baml_state)

        print(f"\n🗣️  Dark Knight: \"{bot_move.shout}\"")

        if bot_move.action == ActionType.ATTACK:
            dmg = game.process_damage(game.player, player_defending)
            print(f"🔥 Opponent attacks you for {dmg} damage!")
        
        elif bot_move.action == ActionType.HEAL:
            amt = game.process_heal(game.opponent)
            if amt > 0:
                print(f"💚 Opponent used a potion and recovered {amt} HP!")
            else:
                print("😤 Opponent tried to heal but failed (Logic Error check!).")
        
        elif bot_move.action == ActionType.DEFEND:
            print("🛡️ Opponent raises their shield.")
            
        elif bot_move.action == ActionType.TAUNT:
            print("😒 The opponent is mocking you.")

    if game.player["hp"] > 0:
        print("\n🎉 VICTORY! The Dark Knight has fallen.")
    else:
        print("\n💀 DEFEAT! You have been vanquished.")

if __name__ == "__main__":
    main()