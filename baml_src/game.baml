// Define the possible actions
enum ActionType {
  ATTACK
  HEAL
  DEFEND
  TAUNT
}

// Define what an item looks like
class InventoryItem {
  name string
  quantity int
  effect_value int
}

// Define the stats for a character
class Fighter {
  name string
  hp int
  max_hp int
  inventory InventoryItem[]
}

// The full context sent to the LLM
class GameState {
  player Fighter
  opponent Fighter
  last_player_move string?
}

// The structured response we require from the LLM
class OpponentTurn {
  action ActionType
  // The LLM must explain why it chose this (good for debugging/immersion)
//   reasoning string
  // A chat message to the player
  shout string
}

function DecideOpponentMove(state: GameState) -> OpponentTurn {
  // Use a capable model (GPT-4o, Sonnet 3.5, or Haiku)
  client "LocalOllama4" 
  
  prompt #"
    {{_.role('user')}}
    You are a strategic RPG Boss battling a player. 
    Analyze the game state and make a action.
    
    RULES:
    1. You cannot HEAL if you have 0 potions in your inventory.
    2. If your HP is low, prioritize HEAL or DEFEND.
    3. If the player is weak, crush them with ATTACK.
    4. Make your 'shout' menacing and relevant to the action.


    Current Game State:
    {{ state }}

    Output JSON format.
    {{ctx.output_format}}
  "#
}