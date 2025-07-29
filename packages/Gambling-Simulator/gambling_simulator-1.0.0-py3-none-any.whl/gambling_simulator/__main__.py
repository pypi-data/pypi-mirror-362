import customtkinter
import subprocess
import random
import time
import datetime
import dill
import os
from typing import Dict, Callable

app = customtkinter.CTk()

scaling_factor = 0.95

def update_window_size():
    """Update window size based on current scaling_factor"""
    global app, scaling_factor
    width = app.winfo_screenwidth() * scaling_factor
    height = app.winfo_screenheight() * scaling_factor
    print(f"Updating window size: {width}x{height} (scaling factor: {scaling_factor})")
    app.geometry(f"{int(width)}x{int(height)}")

# Set initial window size
update_window_size()
app.title("Gambling Simulator")


# Save game when window is closed
def on_window_close():
    save_game_state()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_window_close)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

current_frame = None
current_title = None
current_bet_frame = None
current_balance_label = None
balance = 1000
current_bet = 0
game_active = False
sidebar_expanded = False
bank_tabview_ref = None  # Reference to bank tabview for tracking inner tab changes
lost = None

inventory: Dict[str, int] = {}
shop_items = {
    "🍎": {"name": "Lucky Apple", "base_price": 50, "price": 50, "volatility": 0.15, "trend": 0.0, "description": "Brings good luck!"},
    "💎": {"name": "Diamond Ring", "base_price": 500, "price": 500, "volatility": 0.25, "trend": 0.02, "description": "Shiny and valuable"},
    "🎩": {"name": "Top Hat", "base_price": 200, "price": 200, "volatility": 0.10, "trend": 0.01, "description": "Classy headwear"},
    "🕶️": {"name": "Cool Sunglasses", "base_price": 150, "price": 150, "volatility": 0.20, "trend": -0.01, "description": "Look cool while gambling"},
    "🎲": {"name": "Lucky Dice", "base_price": 100, "price": 100, "volatility": 0.12, "trend": 0.005, "description": "Roll your way to fortune"},
    "🪙": {"name": "Golden Coin", "base_price": 75, "price": 75, "volatility": 0.30, "trend": 0.03, "description": "A collector's item"},
    "🎯": {"name": "Dart Set", "base_price": 120, "price": 120, "volatility": 0.08, "trend": 0.0, "description": "For precise betting"},
    "🃏": {"name": "Magic Cards", "base_price": 300, "price": 300, "volatility": 0.18, "trend": 0.015, "description": "May help with card games"},
    "🎰": {"name": "Mini Slot Machine", "base_price": 800, "price": 800, "volatility": 0.22, "trend": 0.025, "description": "Your own personal slots"},
    "🏆": {"name": "Trophy", "base_price": 1000, "price": 1000, "volatility": 0.35, "trend": 0.04, "description": "Symbol of victory"}
}

# Price update system
last_price_update = time.time()
price_update_interval = 30  # Update prices every 30 seconds

def update_market_prices():
    """Update item prices based on market volatility and trends"""
    global shop_items, last_price_update
    
    current_time = time.time()
    if current_time - last_price_update < price_update_interval:
        return
    
    last_price_update = current_time
    
    for emoji, item in shop_items.items():
        # Random market fluctuation
        volatility_change = random.uniform(-item["volatility"], item["volatility"])
        
        # Long-term trend (some items gain value, others lose)
        trend_change = item["trend"]
        
        # Occasionally shift trends (5% chance per update)
        if random.random() < 0.05:
            item["trend"] = random.uniform(-0.02, 0.04)  # New trend between -2% and +4%
        
        # Market events (1% chance for significant price movement)
        market_event_multiplier = 1.0
        if random.random() < 0.01:
            market_event_multiplier = random.choice([0.7, 0.8, 1.2, 1.3])  # Market crash or boom
        
        # Total price change (as percentage)
        total_change = (volatility_change + trend_change) * market_event_multiplier
        
        # Apply change to current price
        new_price = item["price"] * (1 + total_change)
        
        # Keep prices within reasonable bounds (20% to 300% of base price)
        min_price = item["base_price"] * 0.2
        max_price = item["base_price"] * 3.0
        
        item["price"] = max(min_price, min(max_price, int(new_price)))

def get_price_trend_emoji(emoji):
    """Get trend emoji based on current vs base price"""
    item = shop_items[emoji]
    current_ratio = item["price"] / item["base_price"]
    
    if current_ratio >= 1.2:
        return "📈"  # Significantly up
    elif current_ratio >= 1.05:
        return "📊"  # Slightly up
    elif current_ratio <= 0.8:
        return "📉"  # Significantly down
    elif current_ratio <= 0.95:
        return "📋"  # Slightly down
    else:
        return "➡️"  # Stable

def get_price_change_color(emoji):
    """Get color based on price change"""
    item = shop_items[emoji]
    current_ratio = item["price"] / item["base_price"]
    
    if current_ratio >= 1.05:
        return ("#27AE60", "#2ECC71")  # Green for gains
    elif current_ratio <= 0.95:
        return ("#E74C3C", "#C0392B")  # Red for losses
    else:
        return ("#F39C12", "#E67E22")  # Orange for stable

transaction_history = []  # List of transactions: {"type": "income/expense", "amount": int, "description": str, "timestamp": str}
loan_info = {"amount": 0, "interest_rate": 0.0, "monthly_payment": 0, "remaining_payments": 0}
credit_limit = 5000

# Save file path
SAVE_FILE = "gambling_simulator_save.dill"

# Variables to exclude from automatic snapshot (UI elements and non-serializable objects)
EXCLUDED_VARS = {
    # Python modules and imports
    'customtkinter', 'subprocess', 'random', 'time', 'datetime', 'dill', 'os', 'Dict', 'Callable',
    'SAVE_FILE', 'EXCLUDED_VARS',
    # Tkinter/UI objects that can't be serialized
    'app', 'main_frame', 'current_frame', 'current_title', 'current_bet_frame', 'current_balance_label',
    # Core functions that get recreated on load
    'update_market_prices', 'get_price_trend_emoji', 'get_price_change_color', 'add_transaction',
    'save_game_state', 'load_game_state', 'auto_save', 'reload', 'on_window_close', 'track_ui_change',
    'capture_deep_state', 'restore_ui_state',
    'show_casino', 'show_number_guesser', 'show_roulette', 'show_blackjack', 'show_dice_roll', 'show_slot_machine',
    'show_bank', 'show_shop', 'show_settings', 'create_sidebar', 'update_bank_display', 'scaling_factor', 'update_window_size',
    # Timer and async IDs
    'pending_save_id',
    # Module level variables that shouldn't be saved
    '__name__', '__doc__', '__file__', '__package__', '__builtins__', '__cached__', '__spec__'
}

# Track which UI function is currently active
current_ui_state = {
    'active_function': 'show_casino',  # Default starting function
    'ui_elements': {},  # Store references to current UI elements
    'bank_active_tab': '📊 Dashboard',  # Track which bank sub-tab is active
    'last_update': None
}

def is_serializable(obj):
    """Check if an object can be serialized with dill"""
    try:
        # Quick check for common non-serializable types
        if hasattr(obj, 'winfo_exists'):  # Tkinter widget
            return False
        if hasattr(obj, '__module__') and obj.__module__ == 'tkinter':
            return False
        if str(type(obj)) in ['<class \'_tkinter.tkapp\'>', '<class \'tkinter.Tk\'>', '<class \'customtkinter.CTk\'>']:
            return False
        if callable(obj) and hasattr(obj, '__name__'):  # Functions
            return False
        
        # Try a quick dill test
        dill.dumps(obj)
        return True
    except:
        return False

def capture_deep_state():
    """Capture a comprehensive but safe snapshot of serializable game state"""
    try:
        # Get current global namespace
        current_globals = globals().copy()
        
        # Create game state snapshot
        game_state = {}
        saved_vars = []
        failed_vars = []
        
        # Save ALL serializable global variables
        for var_name, var_value in current_globals.items():
            # Skip excluded variables
            if var_name in EXCLUDED_VARS:
                continue
                
            # Skip private variables (starting with _) except our important ones
            if var_name.startswith('_') and var_name not in ['_save_metadata']:
                continue
            
            # Check if the object is serializable
            if is_serializable(var_value):
                try:
                    # Double-check by actually trying to serialize
                    test_data = dill.dumps(var_value)
                    game_state[var_name] = var_value
                    saved_vars.append(var_name)
                except Exception as e:
                    failed_vars.append((var_name, str(e)))
            else:
                # For non-serializable objects, save metadata about them
                try:
                    metadata = {
                        'type': str(type(var_value)),
                        'repr': str(var_value)[:100] if hasattr(var_value, '__repr__') else 'No repr',
                        'serializable': False
                    }
                    game_state[f'{var_name}_META'] = metadata
                    saved_vars.append(f'{var_name}_META')
                except:
                    failed_vars.append((var_name, 'Could not create metadata'))
        
        # Capture current UI state in a serializable way
        ui_state_snapshot = {
            'current_ui_state': current_ui_state.copy(),
            'active_elements': {},
            'window_info': {}
        }
        
        # Skip window size information - we don't want to save/restore window geometry
        try:
            if 'app' in current_globals:
                app_obj = current_globals['app']
                if hasattr(app_obj, 'winfo_exists') and app_obj.winfo_exists():
                    ui_state_snapshot['window_info'] = {
                        'title': app_obj.title()
                        # Geometry, size and position removed - use default values instead
                    }
        except Exception as e:
            ui_state_snapshot['window_info']['error'] = str(e)
        
        # Add comprehensive metadata
        game_state['_save_metadata'] = {
            'timestamp': datetime.datetime.now().isoformat(),
            'saved_variables': saved_vars,
            'failed_variables': failed_vars,
            'variable_count': len(saved_vars),
            'ui_state': ui_state_snapshot,
            'save_type': 'safe_deep_snapshot'
        }
        
        return game_state, saved_vars, failed_vars
        
    except Exception as e:
        print(f"Error capturing deep state: {e}")
        return {}, [], [(f"global_error", str(e))]

def save_game_state():
    """Save a complete safe snapshot of serializable application state using dill"""
    try:
        game_state, saved_vars, failed_vars = capture_deep_state()
        
        if not game_state:
            print("Failed to capture game state")
            return
        
        # Save to file
        with open(SAVE_FILE, 'wb') as f:
            dill.dump(game_state, f)
            
        print(f"Safe deep snapshot saved: {len(saved_vars)} variables at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Show summary of saved variables
        important_vars = [v for v in saved_vars if not v.endswith('_META')]
        if len(important_vars) <= 10:
            print(f"Saved: {', '.join(sorted(important_vars))}")
        else:
            print(f"Saved: {', '.join(sorted(important_vars)[:8])}... (+{len(important_vars)-8} more)")
        
        # Show failed variables (if any)
        if failed_vars:
            print(f"Could not save {len(failed_vars)} variables: {', '.join([v[0] for v in failed_vars[:3]])}{'...' if len(failed_vars) > 3 else ''}")
        
        # Note: Window size/geometry is intentionally not saved
        print("Window size not saved - will use default size on restart")
        
    except Exception as e:
        print(f"Error saving safe deep state: {e}")

def restore_ui_state(ui_state_snapshot):
    """Attempt to restore UI state after loading"""
    try:
        current_ui = ui_state_snapshot.get('current_ui_state', {})
        active_function = current_ui.get('active_function', 'show_casino')
        
        # Update current UI state
        global current_ui_state
        current_ui_state.update(current_ui)
        
        print(f"Restoring UI state: {active_function}")
        if current_ui.get('bank_active_tab'):
            print(f"Will restore bank tab: {current_ui['bank_active_tab']}")
        
        # Try to restore the active UI function
        if active_function in globals() and callable(globals()[active_function]):
            # Schedule UI restoration after main loop starts
            if 'app' in globals():
                globals()['app'].after(100, lambda: globals()[active_function]())
                
        # Window size is determined by initial scaling_factor only - not saved/restored
                
        # Restore only window title, not size/position
        window_info = ui_state_snapshot.get('window_info', {})
        if window_info and 'app' in globals():
            try:
                # Only restore title, skip geometry/size/position
                if 'title' in window_info:
                    globals()['app'].title(window_info['title'])
            except Exception as e:
                print(f"Could not restore window title: {e}")
        
        return True
        
    except Exception as e:
        print(f"Could not restore UI state: {e}")
        return False

def load_game_state():
    """Load the complete safe game state snapshot from file using dill"""
    if not os.path.exists(SAVE_FILE):
        print("No save file found, starting with default values")
        return False
    
    try:
        with open(SAVE_FILE, 'rb') as f:
            game_state = dill.load(f)
        
        # Get metadata if available
        metadata = game_state.get('_save_metadata', {})
        saved_vars = metadata.get('saved_variables', [])
        failed_vars = metadata.get('failed_variables', [])
        save_timestamp = metadata.get('timestamp', 'Unknown')
        save_type = metadata.get('save_type', 'basic')
        
        # Get current globals to update
        current_globals = globals()
        loaded_vars = []
        
        # Restore all saved variables to global namespace
        for var_name, var_value in game_state.items():
            if var_name == '_save_metadata':
                continue  # Skip metadata
                
            # Handle metadata entries (skip them for actual loading)
            if var_name.endswith('_META'):
                continue
                
            # Update global variable
            current_globals[var_name] = var_value
            loaded_vars.append(var_name)
        
        print(f"Safe deep snapshot loaded: {len(loaded_vars)} variables from {save_timestamp}")
        
        # Show summary
        if len(loaded_vars) <= 10:
            print(f"Loaded: {', '.join(sorted(loaded_vars))}")
        else:
            print(f"Loaded: {', '.join(sorted(loaded_vars)[:8])}... (+{len(loaded_vars)-8} more)")
        
        if failed_vars:
            print(f"{len(failed_vars)} variables were not saved in original session")
        
        # Restore UI state if available
        ui_state = metadata.get('ui_state')
        if ui_state:
            restore_ui_state(ui_state)
        
        return True
        
    except Exception as e:
        print(f"Error loading safe deep state: {e}")
        print("Starting with default values")
        return False

def track_bank_tab_change():
    """Track when bank inner tab changes"""
    global current_ui_state, bank_tabview_ref
    if 'bank_tabview_ref' in globals() and bank_tabview_ref is not None:
        try:
            active_tab = bank_tabview_ref.get()
            current_ui_state['bank_active_tab'] = active_tab
            current_ui_state['last_update'] = datetime.datetime.now().isoformat()
            print(f"Bank tab changed to: {active_tab}")
            
            # Trigger save after tab change
            if 'app' in globals():
                try:
                    globals()['app'].after_cancel(globals().get('pending_save_id', ''))
                except:
                    pass
                globals()['pending_save_id'] = globals()['app'].after(2000, save_game_state)  # Save after 2 seconds
        except Exception as e:
            print(f"Could not track bank tab change: {e}")

def track_ui_change(function_name):
    """Track when UI state changes"""
    global current_ui_state
    current_ui_state['active_function'] = function_name
    current_ui_state['last_update'] = datetime.datetime.now().isoformat()
    
    # Auto-save after UI changes (but not too frequently)
    if 'app' in globals():
        # Cancel any pending save and schedule a new one
        try:
            globals()['app'].after_cancel(globals().get('pending_save_id', ''))
        except:
            pass
        globals()['pending_save_id'] = globals()['app'].after(2000, save_game_state)  # Save after 2 seconds
        # Cancel any pending save and schedule a new one
        try:
            globals()['app'].after_cancel(globals().get('pending_save_id', ''))
        except:
            pass
        globals()['pending_save_id'] = globals()['app'].after(2000, save_game_state)  # Save 2 seconds after UI change

def auto_save():
    """Automatically save the game state and schedule the next auto-save"""
    if lost == False:
        save_game_state()

        if 'app' in globals():
            app.after(30000, auto_save)
        

def add_transaction(transaction_type: str, amount: int, description: str) -> None:
    """Add a transaction to the history for banking tracking"""
    global transaction_history
    transaction_history.append({
        "type": transaction_type,
        "amount": amount,
        "description": description,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    if len(transaction_history) > 50:
        transaction_history = transaction_history[-50:]
    
    # Auto-save after each transaction
    save_game_state()

def reload() -> None:
    save_game_state()  # Save before reloading
    app.quit()
    app.destroy()
    subprocess.run(["python", r".\ui.py"], shell=True)
    exit(0)

def show_casino() -> None:
    if lost == True:
        return
    
    track_ui_change('show_casino')  # Track UI state change
    global current_frame, current_title, current_bet_frame, current_balance_label, balance, current_bet, game_active
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🎰 Coin Flip Casino", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    current_frame = customtkinter.CTkFrame(master=main_frame, 
                                         corner_radius=20,
                                         fg_color=("#2B2B2B", "#1C1C1C"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
    
    coin_label = customtkinter.CTkLabel(master=current_frame, text="🪙", font=("Arial", 100))
    coin_label.pack(pady=60)
    
    result_label = customtkinter.CTkLabel(master=current_frame, text="Click 'Bet' to flip!", 
                                        font=("Arial", 26, "italic"),
                                        text_color=("#E0E0E0", "#E0E0E0"))
    result_label.pack(pady=15)

    current_bet_frame = customtkinter.CTkFrame(master=main_frame,
                                             corner_radius=15,
                                             fg_color=("#333333", "#2A2A2A"))
    current_bet_frame.pack(fill="x", padx=30, pady=(0, 30))
    
    button_container = customtkinter.CTkFrame(master=current_bet_frame, fg_color="transparent")
    button_container.pack(pady=25)
    
    minus_10_btn = customtkinter.CTkButton(master=button_container, text="-10", 
                                         width=60, height=40,
                                         font=("Arial", 14, "bold"),
                                         fg_color=("#FF6B6B", "#FF4757"),
                                         hover_color=("#FF5252", "#FF3742"),
                                         command=lambda: adjust_bet(-10))
    minus_10_btn.pack(side="left", padx=8)
    
    minus_1_btn = customtkinter.CTkButton(master=button_container, text="-1", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#FF6B6B", "#FF4757"),
                                        hover_color=("#FF5252", "#FF3742"),
                                        command=lambda: adjust_bet(-1))
    minus_1_btn.pack(side="left", padx=8)
    
    bet_entry = customtkinter.CTkEntry(master=button_container, 
                                     placeholder_text="💵 Bet amount", 
                                     width=180, height=40,
                                     font=("Arial", 16, "bold"),
                                     corner_radius=10)
    bet_entry.pack(side="left", padx=15)
    bet_entry.insert(0, "0")
    
    plus_1_btn = customtkinter.CTkButton(master=button_container, text="+1", 
                                       width=60, height=40,
                                       font=("Arial", 14, "bold"),
                                       fg_color=("#4ECDC4", "#26D0CE"),
                                       hover_color=("#45B7B8", "#22A3B8"),
                                       command=lambda: adjust_bet(1))
    plus_1_btn.pack(side="left", padx=8)
    
    plus_10_btn = customtkinter.CTkButton(master=button_container, text="+10", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#4ECDC4", "#26D0CE"),
                                        hover_color=("#45B7B8", "#22A3B8"),
                                        command=lambda: adjust_bet(10))
    plus_10_btn.pack(side="left", padx=8)

    bet_submit_button = customtkinter.CTkButton(master=button_container, text="🎲 FLIP COIN", 
                                              width=140, height=40,
                                              font=("Arial", 16, "bold"),
                                              fg_color=("#FFD700", "#FFA500"),
                                              hover_color=("#FFB347", "#FF8C00"),
                                              text_color=("#000000", "#000000"),
                                              command=lambda: start_coinflip())
    bet_submit_button.pack(side="left", padx=15)
    
    win_frame = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    
    double_button = customtkinter.CTkButton(master=win_frame, text="🎲 Double or Nothing", 
                                          command=lambda: double_bet(), 
                                          width=180, height=50,
                                          font=("Arial", 16, "bold"),
                                          fg_color=("#FF6B6B", "#FF4757"),
                                          hover_color=("#FF5252", "#FF3742"))
    cash_out_button = customtkinter.CTkButton(master=win_frame, text="💰 Cash Out", 
                                            command=lambda: cash_out(),
                                            width=180, height=50,
                                            font=("Arial", 16, "bold"),
                                            fg_color=("#00FF7F", "#32CD32"),
                                            hover_color=("#00FA54", "#28B428"),
                                            text_color=("#000000", "#000000"))
    
    def adjust_bet(amount: int) -> None:
        global current_bet
        try:
            current_value = int(bet_entry.get() or 0)
            new_value = max(0, min(balance, current_value + amount))
            bet_entry.delete(0, "end")
            bet_entry.insert(0, str(new_value))
            current_bet = new_value
        except ValueError:
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
            current_bet = 0
    
    def start_coinflip() -> None:
        global balance, current_bet, game_active
        try:
            bet_amount = int(bet_entry.get() or 0)
            if bet_amount <= 0:
                result_label.configure(text="Please enter a valid bet!")
                return
            if bet_amount > balance:
                result_label.configure(text="Insufficient balance!")
                return
            
            current_bet = bet_amount
            balance -= bet_amount
            add_transaction("expense", bet_amount, "Coin Flip Bet")
            if 'update_bank_display' in globals():
                update_bank_display()
            game_active = True
            current_balance_label.configure(text=f"Balance: ${balance}")
            bet_submit_button.configure(state="disabled")
            animate_coin(coin_label, result_label, 0)
        except ValueError:
            result_label.configure(text="Please enter a valid number!")
    
    def animate_coin(coin_label: customtkinter.CTkLabel, result_label: customtkinter.CTkLabel, count: int) -> None:
        if count < 10:
            symbols = ["🪙", "⚪", "🟡", "🔵"]
            coin_label.configure(text=symbols[count % len(symbols)])
            result_label.configure(text="Flipping...")
            app.after(100, lambda: animate_coin(coin_label, result_label, count + 1))
        else:
            result = random.choice(["Heads", "Tails"])
            coin_symbol = "👑" if result == "Heads" else "🐍"
            coin_label.configure(text=coin_symbol)
            
            if result == "Heads":
                result_label.configure(text=f"You won ${current_bet * 2}!")
                show_win_options()
            else:
                result_label.configure(text=f"You lost ${current_bet}!")
                reset_game()
    
    def show_win_options() -> None:
        win_frame.pack(pady=30)
        double_button.pack(side="left", padx=20)
        cash_out_button.pack(side="left", padx=20)
    
    def double_bet() -> None:
        global current_bet
        current_bet *= 2
        win_frame.pack_forget()
        result_label.configure(text=f"Double or Nothing: ${current_bet}")
        coin_label.configure(text="🪙")
        animate_coin(coin_label, result_label, 0)
    
    def cash_out() -> None:
        global balance, current_bet, game_active
        winnings = current_bet * 2
        balance += winnings
        add_transaction("income", winnings, "Coin Flip Win")
        if 'update_bank_display' in globals():
            update_bank_display()
        current_balance_label.configure(text=f"Balance: ${balance}")
        result_label.configure(text=f"Cashed out ${winnings}!")
        reset_game()
    
    def reset_game() -> None:
        global current_bet, game_active
        current_bet = 0
        game_active = False
        try:
            bet_submit_button.configure(state="normal")
            win_frame.pack_forget()
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
        except:
            pass  # UI elements destroyed

def show_number_guesser() -> None:
    track_ui_change('show_number_guesser')  # Track UI state change
    global current_frame, current_title, current_bet_frame, current_balance_label, balance, current_bet, game_active
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🔢 Number Guesser", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    current_frame = customtkinter.CTkFrame(master=main_frame,
                                         corner_radius=20,
                                         fg_color=("#2B2B2B", "#1C1C1C"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
    
    center_container = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    center_container.pack(expand=True, fill="both")
    center_container.grid_rowconfigure(0, weight=1)
    center_container.grid_columnconfigure(0, weight=1)
    
    content_frame = customtkinter.CTkFrame(master=center_container, 
                                          fg_color="transparent")
    content_frame.grid(row=0, column=0)
    
    instruction_label = customtkinter.CTkLabel(master=content_frame, 
                                             text="🎯 Guess a number between 1-49", 
                                             font=("Arial", 24, "bold"),
                                             text_color=("#E0E0E0", "#E0E0E0"))
    instruction_label.pack(pady=15)
    
    odds_label = customtkinter.CTkLabel(master=content_frame, 
                                       text="💎 Win 49x your bet!", 
                                       font=("Arial", 20, "bold"), 
                                       text_color=("#FFD700", "#FFD700"))
    odds_label.pack(pady=15)
    
    number_entry = customtkinter.CTkEntry(master=content_frame, 
                                        placeholder_text="🔢 Your guess (1-49)", 
                                        width=250, height=50,
                                        font=("Arial", 18, "bold"),
                                        corner_radius=15)
    number_entry.pack(pady=25)
    
    result_label = customtkinter.CTkLabel(master=content_frame, text="", 
                                        font=("Arial", 20, "bold"))
    result_label.pack(pady=15)

    current_bet_frame = customtkinter.CTkFrame(master=main_frame,
                                             corner_radius=15,
                                             fg_color=("#333333", "#2A2A2A"))
    current_bet_frame.pack(fill="x", padx=30, pady=(0, 30))
    
    button_container = customtkinter.CTkFrame(master=current_bet_frame, fg_color="transparent")
    button_container.pack(pady=25)
    
    minus_10_btn = customtkinter.CTkButton(master=button_container, text="-10", 
                                         width=60, height=40,
                                         font=("Arial", 14, "bold"),
                                         fg_color=("#FF6B6B", "#FF4757"),
                                         hover_color=("#FF5252", "#FF3742"),
                                         command=lambda: adjust_bet(-10))
    minus_10_btn.pack(side="left", padx=8)
    
    minus_1_btn = customtkinter.CTkButton(master=button_container, text="-1", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#FF6B6B", "#FF4757"),
                                        hover_color=("#FF5252", "#FF3742"),
                                        command=lambda: adjust_bet(-1))
    minus_1_btn.pack(side="left", padx=8)
    
    bet_entry = customtkinter.CTkEntry(master=button_container, 
                                     placeholder_text="💵 Bet amount", 
                                     width=180, height=40,
                                     font=("Arial", 16, "bold"),
                                     corner_radius=10)
    bet_entry.pack(side="left", padx=15)
    bet_entry.insert(0, "0")
    
    plus_1_btn = customtkinter.CTkButton(master=button_container, text="+1", 
                                       width=60, height=40,
                                       font=("Arial", 14, "bold"),
                                       fg_color=("#4ECDC4", "#26D0CE"),
                                       hover_color=("#45B7B8", "#22A3B8"),
                                       command=lambda: adjust_bet(1))
    plus_1_btn.pack(side="left", padx=8)
    
    plus_10_btn = customtkinter.CTkButton(master=button_container, text="+10", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#4ECDC4", "#26D0CE"),
                                        hover_color=("#45B7B8", "#22A3B8"),
                                        command=lambda: adjust_bet(10))
    plus_10_btn.pack(side="left", padx=8)

    bet_submit_button = customtkinter.CTkButton(master=button_container, text="🔮 GUESS", 
                                              width=140, height=40,
                                              font=("Arial", 16, "bold"),
                                              fg_color=("#9B59B6", "#8E44AD"),
                                              hover_color=("#8E44AD", "#7D3C98"),
                                              command=lambda: start_number_game())
    bet_submit_button.pack(side="left", padx=15)
    
    def adjust_bet(amount: int) -> None:
        global current_bet
        try:
            current_value = int(bet_entry.get() or 0)
            new_value = max(0, min(balance, current_value + amount))
            bet_entry.delete(0, "end")
            bet_entry.insert(0, str(new_value))
            current_bet = new_value
        except ValueError:
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
            current_bet = 0
    
    def start_number_game() -> None:
        global balance, current_bet, game_active
        try:
            bet_amount = int(bet_entry.get() or 0)
            guess = int(number_entry.get() or 0)
            
            if bet_amount <= 0:
                result_label.configure(text="Please enter a valid bet!")
                return
            if bet_amount > balance:
                result_label.configure(text="Insufficient balance!")
                return
            if guess < 1 or guess > 49:
                result_label.configure(text="Please guess a number between 1-49!")
                return
            
            current_bet = bet_amount
            balance -= bet_amount
            add_transaction("expense", bet_amount, "Number Guesser Bet")
            if 'update_bank_display' in globals():
                update_bank_display()
            current_balance_label.configure(text=f"Balance: ${balance}")
            bet_submit_button.configure(state="disabled")
            
            winning_number = random.randint(1, 49)
            
            if guess == winning_number:
                winnings = current_bet * 49
                balance += winnings
                add_transaction("income", winnings, "Number Guesser Win")
                if 'update_bank_display' in globals():
                    update_bank_display()
                try:
                    current_balance_label.configure(text=f"Balance: ${balance}")
                    result_label.configure(text=f"🎉 YOU WON! Number was {winning_number}. Won ${winnings}!", text_color="green")
                except:
                    pass  # UI elements destroyed
            else:
                try:
                    result_label.configure(text=f"😞 You lost! Number was {winning_number}. Your guess: {guess}", text_color="red")
                except:
                    pass  # UI elements destroyed
            
            try:
                bet_submit_button.configure(state="normal")
                bet_entry.delete(0, "end")
                bet_entry.insert(0, "0")
                number_entry.delete(0, "end")
            except:
                pass  # UI elements destroyed
            
        except ValueError:
            result_label.configure(text="Please enter valid numbers!")

def show_roulette() -> None:
    track_ui_change('show_roulette')  # Track UI state change
    global current_frame, current_title, current_bet_frame, current_balance_label, balance, current_bet, game_active
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🎯 Roulette", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    current_frame = customtkinter.CTkFrame(master=main_frame,
                                         corner_radius=20,
                                         fg_color=("#2B2B2B", "#1C1C1C"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
    
    wheel_label = customtkinter.CTkLabel(master=current_frame, text="🎰", font=("Arial", 100))
    wheel_label.pack(pady=30)

    bet_options_frame = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    bet_options_frame.pack(pady=20)
    
    selected_bet_type = customtkinter.StringVar(value="red")
    
    red_radio = customtkinter.CTkRadioButton(master=bet_options_frame, text="🔴 Red (2x)", 
                                           variable=selected_bet_type, value="red",
                                           font=("Arial", 16, "bold"))
    red_radio.pack(side="left", padx=20)
    
    black_radio = customtkinter.CTkRadioButton(master=bet_options_frame, text="⚫ Black (2x)", 
                                             variable=selected_bet_type, value="black",
                                             font=("Arial", 16, "bold"))
    black_radio.pack(side="left", padx=20)
    
    green_radio = customtkinter.CTkRadioButton(master=bet_options_frame, text="🟢 Green (36x)", 
                                             variable=selected_bet_type, value="green",
                                             font=("Arial", 16, "bold"))
    green_radio.pack(side="left", padx=20)
    
    result_label = customtkinter.CTkLabel(master=current_frame, text="Place your bet and spin!", 
                                        font=("Arial", 20, "bold"),
                                        text_color=("#E0E0E0", "#E0E0E0"))
    result_label.pack(pady=20)

    current_bet_frame = customtkinter.CTkFrame(master=main_frame,
                                             corner_radius=15,
                                             fg_color=("#333333", "#2A2A2A"))
    current_bet_frame.pack(fill="x", padx=30, pady=(0, 30))
    
    button_container = customtkinter.CTkFrame(master=current_bet_frame, fg_color="transparent")
    button_container.pack(pady=25)

    minus_10_btn = customtkinter.CTkButton(master=button_container, text="-10", 
                                         width=60, height=40,
                                         font=("Arial", 14, "bold"),
                                         fg_color=("#FF6B6B", "#FF4757"),
                                         hover_color=("#FF5252", "#FF3742"),
                                         command=lambda: adjust_bet(-10))
    minus_10_btn.pack(side="left", padx=8)
    
    minus_1_btn = customtkinter.CTkButton(master=button_container, text="-1", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#FF6B6B", "#FF4757"),
                                        hover_color=("#FF5252", "#FF3742"),
                                        command=lambda: adjust_bet(-1))
    minus_1_btn.pack(side="left", padx=8)
    
    bet_entry = customtkinter.CTkEntry(master=button_container, 
                                     placeholder_text="💵 Bet amount", 
                                     width=180, height=40,
                                     font=("Arial", 16, "bold"),
                                     corner_radius=10)
    bet_entry.pack(side="left", padx=15)
    bet_entry.insert(0, "0")
    
    plus_1_btn = customtkinter.CTkButton(master=button_container, text="+1", 
                                       width=60, height=40,
                                       font=("Arial", 14, "bold"),
                                       fg_color=("#4ECDC4", "#26D0CE"),
                                       hover_color=("#45B7B8", "#22A3B8"),
                                       command=lambda: adjust_bet(1))
    plus_1_btn.pack(side="left", padx=8)
    
    plus_10_btn = customtkinter.CTkButton(master=button_container, text="+10", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#4ECDC4", "#26D0CE"),
                                        hover_color=("#45B7B8", "#22A3B8"),
                                        command=lambda: adjust_bet(10))
    plus_10_btn.pack(side="left", padx=8)

    spin_button = customtkinter.CTkButton(master=button_container, text="🎯 SPIN", 
                                        width=140, height=40,
                                        font=("Arial", 16, "bold"),
                                        fg_color=("#E74C3C", "#C0392B"),
                                        hover_color=("#CB4335", "#A93226"),
                                        command=lambda: start_roulette())
    spin_button.pack(side="left", padx=15)
    
    def adjust_bet(amount: int) -> None:
        global current_bet
        try:
            current_value = int(bet_entry.get() or 0)
            new_value = max(0, min(balance, current_value + amount))
            bet_entry.delete(0, "end")
            bet_entry.insert(0, str(new_value))
            current_bet = new_value
        except ValueError:
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
            current_bet = 0
    
    def start_roulette() -> None:
        global balance, current_bet, game_active
        try:
            bet_amount = int(bet_entry.get() or 0)
            if bet_amount <= 0:
                result_label.configure(text="Please enter a valid bet!")
                return
            if bet_amount > balance:
                result_label.configure(text="Insufficient balance!")
                return
            
            current_bet = bet_amount
            balance -= bet_amount
            add_transaction("expense", bet_amount, "Roulette Bet")
            if 'update_bank_display' in globals():
                update_bank_display()
            current_balance_label.configure(text=f"Balance: ${balance}")
            spin_button.configure(state="disabled")
            animate_roulette_wheel(wheel_label, result_label, 0, selected_bet_type.get())
        except ValueError:
            result_label.configure(text="Please enter a valid number!")
    
    def animate_roulette_wheel(wheel_label: customtkinter.CTkLabel, result_label: customtkinter.CTkLabel, count: int, bet_type: str) -> None:
        global balance
        if count < 15:
            symbols = ["🎰", "🔴", "⚫", "🟢", "🎯", "⭕"]
            wheel_label.configure(text=symbols[count % len(symbols)])
            result_label.configure(text="Spinning...")
            app.after(100, lambda: animate_roulette_wheel(wheel_label, result_label, count + 1, bet_type))
        else:
            number = random.randint(0, 36)
            if number == 0:
                color = "green"
                symbol = "🟢"
            elif number in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
                color = "red"
                symbol = "🔴"
            else:
                color = "black"
                symbol = "⚫"
            
            wheel_label.configure(text=symbol)
            
            if bet_type == color:
                if color == "green":
                    winnings = current_bet * 36
                else:
                    winnings = current_bet * 2
                balance += winnings
                add_transaction("income", winnings, "Roulette Win")
                if 'update_bank_display' in globals():
                    update_bank_display()
                try:
                    current_balance_label.configure(text=f"Balance: ${balance}")
                    result_label.configure(text=f"🎉 Winner! Number {number} ({color}). Won ${winnings}!", text_color="green")
                except:
                    pass  # UI elements destroyed
            else:
                try:
                    result_label.configure(text=f"😞 Number {number} ({color}). Better luck next time!", text_color="red")
                except:
                    pass  # UI elements destroyed
            
            try:
                spin_button.configure(state="normal")
                bet_entry.delete(0, "end")
                bet_entry.insert(0, "0")
            except:
                pass  # UI elements destroyed

def show_blackjack() -> None:
    track_ui_change('show_blackjack')  # Track UI state change
    global current_frame, current_title, current_bet_frame, current_balance_label, balance, current_bet, game_active
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🃏 Blackjack", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    current_frame = customtkinter.CTkFrame(master=main_frame,
                                         corner_radius=20,
                                         fg_color=("#2B2B2B", "#1C1C1C"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    player_cards = []
    dealer_cards = []
    game_over = False
    
    dealer_label = customtkinter.CTkLabel(master=current_frame, text="Dealer: 🂠 🂠", 
                                        font=("Arial", 20, "bold"))
    dealer_label.pack(pady=20)
    
    dealer_score_label = customtkinter.CTkLabel(master=current_frame, text="Dealer: ?", 
                                              font=("Arial", 16))
    dealer_score_label.pack()
    
    player_label = customtkinter.CTkLabel(master=current_frame, text="You: 🂠 🂠", 
                                        font=("Arial", 20, "bold"))
    player_label.pack(pady=20)
    
    player_score_label = customtkinter.CTkLabel(master=current_frame, text="You: 0", 
                                               font=("Arial", 16))
    player_score_label.pack()
    
    result_label = customtkinter.CTkLabel(master=current_frame, text="Place your bet to start!", 
                                        font=("Arial", 18, "bold"))
    result_label.pack(pady=20)

    game_buttons_frame = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    game_buttons_frame.pack(pady=20)
    
    hit_button = customtkinter.CTkButton(master=game_buttons_frame, text="🃏 Hit", 
                                       width=100, height=40,
                                       font=("Arial", 14, "bold"),
                                       state="disabled",
                                       command=lambda: hit_card())
    hit_button.pack(side="left", padx=10)
    
    stand_button = customtkinter.CTkButton(master=game_buttons_frame, text="✋ Stand", 
                                         width=100, height=40,
                                         font=("Arial", 14, "bold"),
                                         state="disabled",
                                         command=lambda: stand())
    stand_button.pack(side="left", padx=10)

    current_bet_frame = customtkinter.CTkFrame(master=main_frame,
                                             corner_radius=15,
                                             fg_color=("#333333", "#2A2A2A"))
    current_bet_frame.pack(fill="x", padx=30, pady=(0, 30))
    
    button_container = customtkinter.CTkFrame(master=current_bet_frame, fg_color="transparent")
    button_container.pack(pady=25)

    minus_10_btn = customtkinter.CTkButton(master=button_container, text="-10", 
                                         width=60, height=40,
                                         font=("Arial", 14, "bold"),
                                         fg_color=("#FF6B6B", "#FF4757"),
                                         hover_color=("#FF5252", "#FF3742"),
                                         command=lambda: adjust_bet(-10))
    minus_10_btn.pack(side="left", padx=8)
    
    minus_1_btn = customtkinter.CTkButton(master=button_container, text="-1", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#FF6B6B", "#FF4757"),
                                        hover_color=("#FF5252", "#FF3742"),
                                        command=lambda: adjust_bet(-1))
    minus_1_btn.pack(side="left", padx=8)
    
    bet_entry = customtkinter.CTkEntry(master=button_container, 
                                     placeholder_text="💵 Bet amount", 
                                     width=180, height=40,
                                     font=("Arial", 16, "bold"),
                                     corner_radius=10)
    bet_entry.pack(side="left", padx=15)
    bet_entry.insert(0, "0")
    
    plus_1_btn = customtkinter.CTkButton(master=button_container, text="+1", 
                                       width=60, height=40,
                                       font=("Arial", 14, "bold"),
                                       fg_color=("#4ECDC4", "#26D0CE"),
                                       hover_color=("#45B7B8", "#22A3B8"),
                                       command=lambda: adjust_bet(1))
    plus_1_btn.pack(side="left", padx=8)
    
    plus_10_btn = customtkinter.CTkButton(master=button_container, text="+10", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#4ECDC4", "#26D0CE"),
                                        hover_color=("#45B7B8", "#22A3B8"),
                                        command=lambda: adjust_bet(10))
    plus_10_btn.pack(side="left", padx=8)

    deal_button = customtkinter.CTkButton(master=button_container, text="🃏 DEAL", 
                                        width=140, height=40,
                                        font=("Arial", 16, "bold"),
                                        fg_color=("#2ECC71", "#27AE60"),
                                        hover_color=("#58D68D", "#2ECC71"),
                                        command=lambda: start_blackjack())
    deal_button.pack(side="left", padx=15)
    
    def adjust_bet(amount: int) -> None:
        global current_bet
        try:
            current_value = int(bet_entry.get() or 0)
            new_value = max(0, min(balance, current_value + amount))
            bet_entry.delete(0, "end")
            bet_entry.insert(0, str(new_value))
            current_bet = new_value
        except ValueError:
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
            current_bet = 0
    
    def get_card_value(card: int) -> int:
        if card > 10:
            return 10
        return card
    
    def calculate_score(cards: list) -> int:
        score = sum(get_card_value(card) for card in cards)
        aces = cards.count(1)
        while score <= 11 and aces > 0:
            score += 10
            aces -= 1
        return score
    
    def start_blackjack() -> None:
        nonlocal player_cards, dealer_cards, game_over
        global balance, current_bet
        try:
            bet_amount = int(bet_entry.get() or 0)
            if bet_amount <= 0:
                result_label.configure(text="Please enter a valid bet!")
                return
            if bet_amount > balance:
                result_label.configure(text="Insufficient balance!")
                return
            
            current_bet = bet_amount
            balance -= bet_amount
            add_transaction("expense", bet_amount, "Blackjack Bet")
            if 'update_bank_display' in globals():
                update_bank_display()
            current_balance_label.configure(text=f"Balance: ${balance}")

            # Deal initial cards
            player_cards = [random.randint(1, 13), random.randint(1, 13)]
            dealer_cards = [random.randint(1, 13), random.randint(1, 13)]
            game_over = False
            
            update_display()
            
            if calculate_score(player_cards) == 21:
                try:
                    result_label.configure(text="🎉 Blackjack! You win!", text_color="green")
                    current_balance_label.configure(text=f"Balance: ${balance}")
                except:
                    pass  # UI elements destroyed
                balance += int(current_bet * 2.5)
                add_transaction("income", int(current_bet * 2.5), "Blackjack Win")
                if 'update_bank_display' in globals():
                    update_bank_display()
                game_over = True
            else:
                try:
                    hit_button.configure(state="normal")
                    stand_button.configure(state="normal")
                    deal_button.configure(state="disabled")
                    result_label.configure(text="Hit or Stand?")
                except:
                    pass  # UI elements destroyed
                
        except ValueError:
            result_label.configure(text="Please enter a valid number!")
    
    def update_display() -> None:
        player_score = calculate_score(player_cards)
        dealer_score = calculate_score(dealer_cards)

        player_cards_text = " ".join(["🂠"] * len(player_cards))
        player_label.configure(text=f"You: {player_cards_text}")
        player_score_label.configure(text=f"You: {player_score}")

        if game_over:
            dealer_cards_text = " ".join(["🂠"] * len(dealer_cards))
            dealer_label.configure(text=f"Dealer: {dealer_cards_text}")
            dealer_score_label.configure(text=f"Dealer: {dealer_score}")
        else:
            dealer_label.configure(text=f"Dealer: 🂠 🂭")
            dealer_score_label.configure(text="Dealer: ?")
    
    def hit_card() -> None:
        nonlocal player_cards, game_over
        player_cards.append(random.randint(1, 13))
        player_score = calculate_score(player_cards)
        update_display()
        
        if player_score > 21:
            try:
                result_label.configure(text=f"😞 Bust! You lose ${current_bet}!", text_color="red")
                hit_button.configure(state="disabled")
                stand_button.configure(state="disabled")
                deal_button.configure(state="normal")
            except:
                pass  # UI elements destroyed
            game_over = True
    
    def stand() -> None:
        nonlocal dealer_cards, game_over
        global balance

        while calculate_score(dealer_cards) < 17:
            dealer_cards.append(random.randint(1, 13))
        
        player_score = calculate_score(player_cards)
        dealer_score = calculate_score(dealer_cards)
        game_over = True
        update_display()
        
        if dealer_score > 21:
            try:
                result_label.configure(text=f"🎉 Dealer busts! You win ${current_bet * 2}!", text_color="green")
            except:
                pass  # UI elements destroyed
            balance += current_bet * 2
            add_transaction("income", current_bet * 2, "Blackjack Win")
        elif player_score > dealer_score:
            try:
                result_label.configure(text=f"🎉 You win ${current_bet * 2}!", text_color="green")
            except:
                pass  # UI elements destroyed
            balance += current_bet * 2
            add_transaction("income", current_bet * 2, "Blackjack Win")
        elif player_score == dealer_score:
            try:
                result_label.configure(text="🤝 Push! Bet returned.", text_color="yellow")
            except:
                pass  # UI elements destroyed
            balance += current_bet
            add_transaction("income", current_bet, "Blackjack Push")
        else:
            try:
                result_label.configure(text=f"😞 Dealer wins! You lose ${current_bet}!", text_color="red")
            except:
                pass  # UI elements destroyed
        
        if 'update_bank_display' in globals():
            update_bank_display()
        try:
            current_balance_label.configure(text=f"Balance: ${balance}")
            hit_button.configure(state="disabled")
            stand_button.configure(state="disabled")
            deal_button.configure(state="normal")
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
        except:
            pass  # UI elements destroyed

def show_dice_roll() -> None:
    track_ui_change('show_dice_roll')  # Track UI state change
    global current_frame, current_title, current_bet_frame, current_balance_label, balance, current_bet, game_active
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🎲 Dice Roll", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    current_frame = customtkinter.CTkFrame(master=main_frame,
                                         corner_radius=20,
                                         fg_color=("#2B2B2B", "#1C1C1C"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
    
    dice_frame = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    dice_frame.pack(pady=40)
    
    dice1_label = customtkinter.CTkLabel(master=dice_frame, text="🎲", font=("Arial", 80))
    dice1_label.pack(side="left", padx=20)
    
    dice2_label = customtkinter.CTkLabel(master=dice_frame, text="🎲", font=("Arial", 80))
    dice2_label.pack(side="left", padx=20)
    
    result_label = customtkinter.CTkLabel(master=current_frame, text="Choose your bet and roll!", 
                                        font=("Arial", 20, "bold"))
    result_label.pack(pady=20)

    bet_options_frame = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    bet_options_frame.pack(pady=20)
    
    selected_bet_type = customtkinter.StringVar(value="over7")
    
    over7_radio = customtkinter.CTkRadioButton(master=bet_options_frame, text="🔺 Over 7 (2x)", 
                                             variable=selected_bet_type, value="over7",
                                             font=("Arial", 16, "bold"))
    over7_radio.pack(side="left", padx=20)
    
    exactly7_radio = customtkinter.CTkRadioButton(master=bet_options_frame, text="🎯 Exactly 7 (4x)", 
                                                variable=selected_bet_type, value="exactly7",
                                                font=("Arial", 16, "bold"))
    exactly7_radio.pack(side="left", padx=20)
    
    under7_radio = customtkinter.CTkRadioButton(master=bet_options_frame, text="🔻 Under 7 (2x)", 
                                              variable=selected_bet_type, value="under7",
                                              font=("Arial", 16, "bold"))
    under7_radio.pack(side="left", padx=20)

    current_bet_frame = customtkinter.CTkFrame(master=main_frame,
                                             corner_radius=15,
                                             fg_color=("#333333", "#2A2A2A"))
    current_bet_frame.pack(fill="x", padx=30, pady=(0, 30))
    
    button_container = customtkinter.CTkFrame(master=current_bet_frame, fg_color="transparent")
    button_container.pack(pady=25)
    
    minus_10_btn = customtkinter.CTkButton(master=button_container, text="-10", 
                                         width=60, height=40,
                                         font=("Arial", 14, "bold"),
                                         fg_color=("#FF6B6B", "#FF4757"),
                                         hover_color=("#FF5252", "#FF3742"),
                                         command=lambda: adjust_bet(-10))
    minus_10_btn.pack(side="left", padx=8)
    
    minus_1_btn = customtkinter.CTkButton(master=button_container, text="-1", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#FF6B6B", "#FF4757"),
                                        hover_color=("#FF5252", "#FF3742"),
                                        command=lambda: adjust_bet(-1))
    minus_1_btn.pack(side="left", padx=8)
    
    bet_entry = customtkinter.CTkEntry(master=button_container, 
                                     placeholder_text="💵 Bet amount", 
                                     width=180, height=40,
                                     font=("Arial", 16, "bold"),
                                     corner_radius=10)
    bet_entry.pack(side="left", padx=15)
    bet_entry.insert(0, "0")
    
    plus_1_btn = customtkinter.CTkButton(master=button_container, text="+1", 
                                       width=60, height=40,
                                       font=("Arial", 14, "bold"),
                                       fg_color=("#4ECDC4", "#26D0CE"),
                                       hover_color=("#45B7B8", "#22A3B8"),
                                       command=lambda: adjust_bet(1))
    plus_1_btn.pack(side="left", padx=8)
    
    plus_10_btn = customtkinter.CTkButton(master=button_container, text="+10", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#4ECDC4", "#26D0CE"),
                                        hover_color=("#45B7B8", "#22A3B8"),
                                        command=lambda: adjust_bet(10))
    plus_10_btn.pack(side="left", padx=8)

    roll_button = customtkinter.CTkButton(master=button_container, text="🎲 ROLL", 
                                        width=140, height=40,
                                        font=("Arial", 16, "bold"),
                                        fg_color=("#3498DB", "#2980B9"),
                                        hover_color=("#5DADE2", "#3498DB"),
                                        command=lambda: start_dice_roll())
    roll_button.pack(side="left", padx=15)
    
    def adjust_bet(amount: int) -> None:
        global current_bet
        try:
            current_value = int(bet_entry.get() or 0)
            new_value = max(0, min(balance, current_value + amount))
            bet_entry.delete(0, "end")
            bet_entry.insert(0, str(new_value))
            current_bet = new_value
        except ValueError:
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
            current_bet = 0
    
    def start_dice_roll() -> None:
        global balance, current_bet
        try:
            bet_amount = int(bet_entry.get() or 0)
            if bet_amount <= 0:
                result_label.configure(text="Please enter a valid bet!")
                return
            if bet_amount > balance:
                result_label.configure(text="Insufficient balance!")
                return
            
            current_bet = bet_amount
            balance -= bet_amount
            add_transaction("expense", bet_amount, "Dice Roll Bet")
            if 'update_bank_display' in globals():
                try:
                    update_bank_display()
                except:
                    pass  # Bank UI elements may not exist
            try:
                current_balance_label.configure(text=f"Balance: ${balance}")
                roll_button.configure(state="disabled")
            except:
                pass  # UI elements destroyed
            animate_dice(dice1_label, dice2_label, result_label, 0, selected_bet_type.get())
        except ValueError:
            result_label.configure(text="Please enter a valid number!")
    
    def animate_dice(dice1_label: customtkinter.CTkLabel, dice2_label: customtkinter.CTkLabel, 
                   result_label: customtkinter.CTkLabel, count: int, bet_type: str) -> None:
        global balance
        if count < 10:
            dice_symbols = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
            try:
                dice1_label.configure(text=random.choice(dice_symbols))
                dice2_label.configure(text=random.choice(dice_symbols))
                result_label.configure(text="Rolling...")
                app.after(100, lambda: animate_dice(dice1_label, dice2_label, result_label, count + 1, bet_type))
            except:
                # UI elements have been destroyed, stop animation
                return
        else:
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            total = dice1 + dice2
            
            dice_symbols = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
            try:
                dice1_label.configure(text=dice_symbols[dice1-1])
                dice2_label.configure(text=dice_symbols[dice2-1])
            except:
                # UI elements have been destroyed, stop processing
                return
            
            won = False
            multiplier = 0
            
            if bet_type == "over7" and total > 7:
                won = True
                multiplier = 2
            elif bet_type == "exactly7" and total == 7:
                won = True
                multiplier = 4
            elif bet_type == "under7" and total < 7:
                won = True
                multiplier = 2
            
            if won:
                winnings = current_bet * multiplier
                balance += winnings
                add_transaction("income", winnings, "Dice Roll Win")
                if 'update_bank_display' in globals():
                    update_bank_display()
                try:
                    current_balance_label.configure(text=f"Balance: ${balance}")
                    result_label.configure(text=f"🎉 You won ${winnings}! (Total: {total})", text_color="green")
                except:
                    pass  # UI elements destroyed
            else:
                try:
                    result_label.configure(text=f"😞 You lost! (Total: {total})", text_color="red")
                except:
                    pass  # UI elements destroyed
            
            try:
                roll_button.configure(state="normal")
                bet_entry.delete(0, "end")
                bet_entry.insert(0, "0")
            except:
                pass  # UI elements destroyed

def show_slot_machine() -> None:
    track_ui_change('show_slot_machine')  # Track UI state change
    global current_frame, current_title, current_bet_frame, current_balance_label, balance, current_bet, game_active
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🎰 Slot Machine", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    current_frame = customtkinter.CTkFrame(master=main_frame,
                                         corner_radius=20,
                                         fg_color=("#2B2B2B", "#1C1C1C"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    slot_frame = customtkinter.CTkFrame(master=current_frame, 
                                       corner_radius=15,
                                       fg_color=("#1A1A1A", "#0F0F0F"))
    slot_frame.pack(pady=40)
    
    slots_container = customtkinter.CTkFrame(master=slot_frame, fg_color="transparent")
    slots_container.pack(padx=40, pady=30)
    
    slot1_label = customtkinter.CTkLabel(master=slots_container, text="🍒", 
                                       font=("Arial", 80),
                                       fg_color=("#333333", "#2A2A2A"),
                                       corner_radius=10,
                                       width=100, height=100)
    slot1_label.pack(side="left", padx=10)
    
    slot2_label = customtkinter.CTkLabel(master=slots_container, text="🍒", 
                                       font=("Arial", 80),
                                       fg_color=("#333333", "#2A2A2A"),
                                       corner_radius=10,
                                       width=100, height=100)
    slot2_label.pack(side="left", padx=10)
    
    slot3_label = customtkinter.CTkLabel(master=slots_container, text="🍒", 
                                       font=("Arial", 80),
                                       fg_color=("#333333", "#2A2A2A"),
                                       corner_radius=10,
                                       width=100, height=100)
    slot3_label.pack(side="left", padx=10)

    paytable_frame = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    paytable_frame.pack(pady=20)
    
    paytable_label = customtkinter.CTkLabel(master=paytable_frame, 
                                          text="💎💎💎 = 50x | 🍒🍒🍒 = 10x | 🔔🔔🔔 = 5x | Any 2 = 2x", 
                                          font=("Arial", 14, "bold"),
                                          text_color=("#E0E0E0", "#E0E0E0"))
    paytable_label.pack()
    
    result_label = customtkinter.CTkLabel(master=current_frame, text="Pull the lever to play!", 
                                        font=("Arial", 20, "bold"))
    result_label.pack(pady=20)

    current_bet_frame = customtkinter.CTkFrame(master=main_frame,
                                             corner_radius=15,
                                             fg_color=("#333333", "#2A2A2A"))
    current_bet_frame.pack(fill="x", padx=30, pady=(0, 30))
    
    button_container = customtkinter.CTkFrame(master=current_bet_frame, fg_color="transparent")
    button_container.pack(pady=25)
    
    minus_10_btn = customtkinter.CTkButton(master=button_container, text="-10", 
                                         width=60, height=40,
                                         font=("Arial", 14, "bold"),
                                         fg_color=("#FF6B6B", "#FF4757"),
                                         hover_color=("#FF5252", "#FF3742"),
                                         command=lambda: adjust_bet(-10))
    minus_10_btn.pack(side="left", padx=8)
    
    minus_1_btn = customtkinter.CTkButton(master=button_container, text="-1", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#FF6B6B", "#FF4757"),
                                        hover_color=("#FF5252", "#FF3742"),
                                        command=lambda: adjust_bet(-1))
    minus_1_btn.pack(side="left", padx=8)
    
    bet_entry = customtkinter.CTkEntry(master=button_container, 
                                     placeholder_text="💵 Bet amount", 
                                     width=180, height=40,
                                     font=("Arial", 16, "bold"),
                                     corner_radius=10)
    bet_entry.pack(side="left", padx=15)
    bet_entry.insert(0, "0")
    
    plus_1_btn = customtkinter.CTkButton(master=button_container, text="+1", 
                                       width=60, height=40,
                                       font=("Arial", 14, "bold"),
                                       fg_color=("#4ECDC4", "#26D0CE"),
                                       hover_color=("#45B7B8", "#22A3B8"),
                                       command=lambda: adjust_bet(1))
    plus_1_btn.pack(side="left", padx=8)
    
    plus_10_btn = customtkinter.CTkButton(master=button_container, text="+10", 
                                        width=60, height=40,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#4ECDC4", "#26D0CE"),
                                        hover_color=("#45B7B8", "#22A3B8"),
                                        command=lambda: adjust_bet(10))
    plus_10_btn.pack(side="left", padx=8)

    spin_button = customtkinter.CTkButton(master=button_container, text="🎰 SPIN", 
                                        width=140, height=40,
                                        font=("Arial", 16, "bold"),
                                        fg_color=("#F39C12", "#E67E22"),
                                        hover_color=("#F4D03F", "#F39C12"),
                                        command=lambda: start_slot_spin())
    spin_button.pack(side="left", padx=15)
    
    def adjust_bet(amount: int) -> None:
        global current_bet
        try:
            current_value = int(bet_entry.get() or 0)
            new_value = max(0, min(balance, current_value + amount))
            bet_entry.delete(0, "end")
            bet_entry.insert(0, str(new_value))
            current_bet = new_value
        except ValueError:
            bet_entry.delete(0, "end")
            bet_entry.insert(0, "0")
            current_bet = 0
    
    def start_slot_spin() -> None:
        global balance, current_bet
        try:
            bet_amount = int(bet_entry.get() or 0)
            if bet_amount <= 0:
                result_label.configure(text="Please enter a valid bet!")
                return
            if bet_amount > balance:
                result_label.configure(text="Insufficient balance!")
                return
            
            current_bet = bet_amount
            balance -= bet_amount
            current_balance_label.configure(text=f"Balance: ${balance}")
            spin_button.configure(state="disabled")
            animate_slots(slot1_label, slot2_label, slot3_label, result_label, 0)
        except ValueError:
            result_label.configure(text="Please enter a valid number!")
    
    def animate_slots(slot1_label: customtkinter.CTkLabel, slot2_label: customtkinter.CTkLabel, 
                     slot3_label: customtkinter.CTkLabel, result_label: customtkinter.CTkLabel, count: int) -> None:
        global balance
        if count < 20:
            symbols = ["🍒", "🔔", "🍋", "🍊", "🍇", "💎", "7"]
            slot1_label.configure(text=random.choice(symbols))
            slot2_label.configure(text=random.choice(symbols))
            slot3_label.configure(text=random.choice(symbols))
            result_label.configure(text="Spinning...")
            app.after(100, lambda: animate_slots(slot1_label, slot2_label, slot3_label, result_label, count + 1))
        else:
            symbols = ["🍒", "🍒", "🍒", "🔔", "🔔", "🍋", "🍊", "🍇", "💎", "7"]
            
            final1 = random.choice(symbols)
            final2 = random.choice(symbols)
            final3 = random.choice(symbols)
            
            slot1_label.configure(text=final1)
            slot2_label.configure(text=final2)
            slot3_label.configure(text=final3)

            if final1 == final2 == final3:
                if final1 == "💎":
                    multiplier = 50
                elif final1 == "🍒":
                    multiplier = 10
                elif final1 == "🔔":
                    multiplier = 5
                else:
                    multiplier = 3
                winnings = current_bet * multiplier
                balance += winnings
                try:
                    current_balance_label.configure(text=f"Balance: ${balance}")
                    result_label.configure(text=f"🎉 JACKPOT! Won ${winnings}!", text_color="green")
                except:
                    pass  # UI elements destroyed
            elif final1 == final2 or final2 == final3 or final1 == final3:
                winnings = current_bet * 2
                balance += winnings
                try:
                    current_balance_label.configure(text=f"Balance: ${balance}")
                    result_label.configure(text=f"🎊 Pair! Won ${winnings}!", text_color="green")
                except:
                    pass  # UI elements destroyed
            else:
                try:
                    result_label.configure(text="😞 No match. Try again!", text_color="red")
                except:
                    pass  # UI elements destroyed
            
            try:
                spin_button.configure(state="normal")
                bet_entry.delete(0, "end")
                bet_entry.insert(0, "0")
            except:
                pass  # UI elements destroyed

def show_shop() -> None:
    track_ui_change('show_shop')  # Track UI state change
    global current_frame, current_title, current_bet_frame, current_balance_label, balance
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🛍️ Shop", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    current_frame = customtkinter.CTkFrame(master=main_frame,
                                          corner_radius=20,
                                          fg_color=("#2B2B2B", "#1C1C1C"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    tab_frame = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    tab_frame.pack(fill="x", padx=20, pady=20)
    
    shop_tab_btn = customtkinter.CTkButton(master=tab_frame, text="🛒 Shop", 
                                         width=150, height=40,
                                         font=("Arial", 16, "bold"),
                                         fg_color=("#4ECDC4", "#26D0CE"),
                                         hover_color=("#45B7B8", "#22A3B8"),
                                         command=lambda: switch_to_shop_tab())
    shop_tab_btn.pack(side="left", padx=10)
    
    inventory_tab_btn = customtkinter.CTkButton(master=tab_frame, text="🎒 Inventory", 
                                              width=150, height=40,
                                              font=("Arial", 16, "bold"),
                                              fg_color=("#9B59B6", "#8E44AD"),
                                              hover_color=("#8E44AD", "#7D3C98"),
                                              command=lambda: switch_to_inventory_tab())
    inventory_tab_btn.pack(side="left", padx=10)

    content_frame = customtkinter.CTkScrollableFrame(master=current_frame,
                                                   corner_radius=15,
                                                   fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    # Store reference to status label for auto-refresh
    status_label_ref = None
    
    def switch_to_shop_tab():
        nonlocal status_label_ref
        # Update market prices before displaying
        update_market_prices()
        
        try:
            # Check if content_frame still exists before trying to access its children
            if content_frame.winfo_exists():
                for widget in content_frame.winfo_children():
                    widget.destroy()
            else:
                return  # Exit if the frame no longer exists
        except:
            return  # Exit if there's an error accessing the frame
        
        try:
            shop_tab_btn.configure(fg_color=("#4ECDC4", "#26D0CE"))
            inventory_tab_btn.configure(fg_color=("#555555", "#404040"))
        except:
            return  # Exit if button widgets don't exist
        
        # Auto-refresh mechanism for shop prices
        def auto_refresh_shop():
            try:
                # Check if widgets still exist and we're still on the shop tab
                if (content_frame.winfo_exists() and 
                    shop_tab_btn.winfo_exists() and 
                    shop_tab_btn.cget("fg_color") == ("#4ECDC4", "#26D0CE")):
                    
                    old_prices = {emoji: item["price"] for emoji, item in shop_items.items()}
                    update_market_prices()
                    
                    # Check if any prices changed
                    prices_changed = any(shop_items[emoji]["price"] != old_prices[emoji] for emoji in old_prices)
                    
                    if prices_changed:
                        # Refresh the shop display
                        switch_to_shop_tab()
                    else:
                        # Just update the countdown timer
                        try:
                            if status_label_ref and status_label_ref.winfo_exists():
                                next_update = int(price_update_interval - (time.time() - last_price_update))
                                status_label_ref.configure(text=f"⏰ Next price update in: {max(0, next_update)}s")
                        except:
                            pass
                    
                    # Schedule next check in 1 second
                    app.after(1000, auto_refresh_shop)
            except:
                # Widget has been destroyed, stop the auto-refresh
                pass
        
        # Start auto-refresh
        app.after(1000, auto_refresh_shop)
        
        # Enhanced header with market info
        header_frame = customtkinter.CTkFrame(master=content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=20)
        
        shop_header = customtkinter.CTkLabel(master=header_frame, 
                                           text="🛍️ Dynamic Marketplace", 
                                           font=("Arial", 24, "bold"),
                                           text_color=("#FFD700", "#FFD700"))
        shop_header.pack()
        
        market_info = customtkinter.CTkLabel(master=header_frame, 
                                           text="📊 Prices update every 30 seconds based on market trends\n💡 Buy low, sell high to maximize profit!", 
                                           font=("Arial", 12),
                                           text_color=("#95A5A6", "#7F8C8D"))
        market_info.pack(pady=(5, 0))
        
        # Market status indicator
        next_update = int(price_update_interval - (time.time() - last_price_update))
        status_label_ref = customtkinter.CTkLabel(master=header_frame, 
                                            text=f"⏰ Next price update in: {max(0, next_update)}s", 
                                            font=("Arial", 10),
                                            text_color=("#3498DB", "#2980B9"))
        status_label_ref.pack()
        
        for emoji, item_data in shop_items.items():
            item_frame = customtkinter.CTkFrame(master=content_frame,
                                              corner_radius=12,
                                              fg_color=("#333333", "#2A2A2A"),
                                              border_width=2,
                                              border_color=get_price_change_color(emoji))
            item_frame.pack(fill="x", padx=20, pady=10)
            
            item_info_frame = customtkinter.CTkFrame(master=item_frame, fg_color="transparent")
            item_info_frame.pack(fill="x", padx=20, pady=15)
            
            icon_name_frame = customtkinter.CTkFrame(master=item_info_frame, fg_color="transparent")
            icon_name_frame.pack(side="left", fill="x", expand=True)
            
            item_icon = customtkinter.CTkLabel(master=icon_name_frame, text=emoji, 
                                             font=("Arial", 40))
            item_icon.pack(side="left", padx=(0, 15))
            
            item_details = customtkinter.CTkFrame(master=icon_name_frame, fg_color="transparent")
            item_details.pack(side="left", fill="x", expand=True)
            
            item_name = customtkinter.CTkLabel(master=item_details, 
                                             text=item_data["name"], 
                                             font=("Arial", 18, "bold"),
                                             anchor="w")
            item_name.pack(anchor="w")
            
            item_desc = customtkinter.CTkLabel(master=item_details, 
                                             text=item_data["description"], 
                                             font=("Arial", 14),
                                             text_color=("#B0B0B0", "#B0B0B0"),
                                             anchor="w")
            item_desc.pack(anchor="w")
            
            # Price change indicator
            price_change_percent = ((item_data["price"] - item_data["base_price"]) / item_data["base_price"]) * 100
            trend_emoji = get_price_trend_emoji(emoji)
            
            price_change_text = f"{trend_emoji} {price_change_percent:+.1f}% from base price"
            price_change_color = get_price_change_color(emoji)
            
            price_change_label = customtkinter.CTkLabel(master=item_details, 
                                                      text=price_change_text, 
                                                      font=("Arial", 11, "bold"),
                                                      text_color=price_change_color,
                                                      anchor="w")
            price_change_label.pack(anchor="w")

            price_buy_frame = customtkinter.CTkFrame(master=item_info_frame, fg_color="transparent")
            price_buy_frame.pack(side="right")
            
            # Enhanced price display
            price_frame = customtkinter.CTkFrame(master=price_buy_frame, fg_color="transparent")
            price_frame.pack(pady=(0, 5))
            
            current_price_label = customtkinter.CTkLabel(master=price_frame, 
                                                       text=f"${item_data['price']:,}", 
                                                       font=("Arial", 18, "bold"),
                                                       text_color=price_change_color)
            current_price_label.pack()
            
            base_price_label = customtkinter.CTkLabel(master=price_frame, 
                                                    text=f"(Base: ${item_data['base_price']:,})", 
                                                    font=("Arial", 10),
                                                    text_color=("#888888", "#888888"))
            base_price_label.pack()
            
            buy_btn = customtkinter.CTkButton(master=price_buy_frame, text="Buy", 
                                            width=80, height=35,
                                            font=("Arial", 14, "bold"),
                                            fg_color=("#4ECDC4", "#26D0CE"),
                                            hover_color=("#45B7B8", "#22A3B8"),
                                            command=lambda e=emoji, data=item_data: buy_item(e, data))
            buy_btn.pack()
    
    def switch_to_inventory_tab():
        try:
            # Check if content_frame still exists before trying to access its children
            if content_frame.winfo_exists():
                for widget in content_frame.winfo_children():
                    widget.destroy()
            else:
                return  # Exit if the frame no longer exists
        except:
            return  # Exit if there's an error accessing the frame
        
        try:
            shop_tab_btn.configure(fg_color=("#555555", "#404040"))
            inventory_tab_btn.configure(fg_color=("#9B59B6", "#8E44AD"))
        except:
            return  # Exit if button widgets don't exist
        
        inv_header = customtkinter.CTkLabel(master=content_frame, 
                                          text="🎒 Your Inventory", 
                                          font=("Arial", 24, "bold"),
                                          text_color=("#9B59B6", "#8E44AD"))
        inv_header.pack(pady=20)
        
        if not inventory:
            empty_label = customtkinter.CTkLabel(master=content_frame, 
                                               text="Your inventory is empty!\nVisit the shop to buy some items.", 
                                               font=("Arial", 16),
                                               text_color=("#B0B0B0", "#B0B0B0"))
            empty_label.pack(pady=50)
        else:
            for emoji, quantity in inventory.items():
                if quantity > 0:
                    item_data = shop_items[emoji]
                    sell_price = int(item_data["price"] * 0.7)
                    
                    item_frame = customtkinter.CTkFrame(master=content_frame,
                                                      corner_radius=12,
                                                      fg_color=("#333333", "#2A2A2A"))
                    item_frame.pack(fill="x", padx=20, pady=10)
                    
                    item_info_frame = customtkinter.CTkFrame(master=item_frame, fg_color="transparent")
                    item_info_frame.pack(fill="x", padx=20, pady=15)
                    
                    icon_name_frame = customtkinter.CTkFrame(master=item_info_frame, fg_color="transparent")
                    icon_name_frame.pack(side="left", fill="x", expand=True)
                    
                    item_icon = customtkinter.CTkLabel(master=icon_name_frame, text=emoji, 
                                                     font=("Arial", 40))
                    item_icon.pack(side="left", padx=(0, 15))
                    
                    item_details = customtkinter.CTkFrame(master=icon_name_frame, fg_color="transparent")
                    item_details.pack(side="left", fill="x", expand=True)
                    
                    item_name = customtkinter.CTkLabel(master=item_details, 
                                                     text=f"{item_data['name']} x{quantity}", 
                                                     font=("Arial", 18, "bold"),
                                                     anchor="w")
                    item_name.pack(anchor="w")
                    
                    item_desc = customtkinter.CTkLabel(master=item_details, 
                                                     text=item_data["description"], 
                                                     font=("Arial", 14),
                                                     text_color=("#B0B0B0", "#B0B0B0"),
                                                     anchor="w")
                    item_desc.pack(anchor="w")
                    
                    # Add market value information
                    price_change_percent = ((item_data["price"] - item_data["base_price"]) / item_data["base_price"]) * 100
                    trend_emoji = get_price_trend_emoji(emoji)
                    market_value_text = f"{trend_emoji} Market Value: ${item_data['price']:,} ({price_change_percent:+.1f}%)"
                    market_value_color = get_price_change_color(emoji)
                    
                    market_value_label = customtkinter.CTkLabel(master=item_details, 
                                                              text=market_value_text, 
                                                              font=("Arial", 11, "bold"),
                                                              text_color=market_value_color,
                                                              anchor="w")
                    market_value_label.pack(anchor="w")
                    
                    sell_frame = customtkinter.CTkFrame(master=item_info_frame, fg_color="transparent")
                    sell_frame.pack(side="right")
                    
                    # Enhanced sell price display
                    sell_price_frame = customtkinter.CTkFrame(master=sell_frame, fg_color="transparent")
                    sell_price_frame.pack(pady=(0, 5))
                    
                    sell_price_label = customtkinter.CTkLabel(master=sell_price_frame, 
                                                            text=f"Sell: ${sell_price:,}", 
                                                            font=("Arial", 16, "bold"),
                                                            text_color=("#FF6B6B", "#FF4757"))
                    sell_price_label.pack()
                    
                    sell_note_label = customtkinter.CTkLabel(master=sell_price_frame, 
                                                           text="(70% of market value)", 
                                                           font=("Arial", 9),
                                                           text_color=("#888888", "#888888"))
                    sell_note_label.pack()
                    
                    sell_btn = customtkinter.CTkButton(master=sell_frame, text="Sell", 
                                                     width=80, height=35,
                                                     font=("Arial", 14, "bold"),
                                                     fg_color=("#E74C3C", "#C0392B"),
                                                     hover_color=("#C0392B", "#A93226"),
                                                     command=lambda e=emoji, price=sell_price: sell_item(e, price))
                    sell_btn.pack()
    
    def buy_item(emoji: str, item_data: Dict[str, any]):
        global balance
        price = item_data["price"]
        
        if balance >= price:
            balance -= price
            add_transaction("expense", price, f"Shop: {item_data['name']}")
            if 'update_bank_display' in globals():
                update_bank_display()
            current_balance_label.configure(text=f"Balance: ${balance}")
            
            if emoji in inventory:
                inventory[emoji] += 1
            else:
                inventory[emoji] = 1
            
            success_window = customtkinter.CTkToplevel(app)
            success_window.title("Purchase Successful")
            success_window.geometry("400x200")
            success_window.transient(app)
            success_window.grab_set()
            
            success_label = customtkinter.CTkLabel(master=success_window, 
                                                 text=f"✅ Successfully bought {item_data['name']}!\n\n{emoji} Added to inventory", 
                                                 font=("Arial", 16, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
            success_label.pack(pady=50)
            
            ok_btn = customtkinter.CTkButton(master=success_window, text="OK", 
                                           width=100, height=35,
                                           command=success_window.destroy)
            ok_btn.pack(pady=20)
            
        else:
            error_window = customtkinter.CTkToplevel(app)
            error_window.title("Insufficient Funds")
            error_window.geometry("400x200")
            error_window.transient(app)
            error_window.grab_set()
            
            error_label = customtkinter.CTkLabel(master=error_window, 
                                               text=f"❌ Not enough money!\n\nYou need ${price} but only have ${balance}", 
                                               font=("Arial", 16, "bold"),
                                               text_color=("#FF6B6B", "#FF4757"))
            error_label.pack(pady=50)
            
            ok_btn = customtkinter.CTkButton(master=error_window, text="OK", 
                                           width=100, height=35,
                                           command=error_window.destroy)
            ok_btn.pack(pady=20)
    
    def sell_item(emoji: str, sell_price: int):
        global balance
        
        if emoji in inventory and inventory[emoji] > 0:
            item_name = shop_items[emoji]["name"]
            balance += sell_price
            add_transaction("income", sell_price, f"Sold: {item_name}")
            if 'update_bank_display' in globals():
                update_bank_display()
            current_balance_label.configure(text=f"Balance: ${balance}")
            inventory[emoji] -= 1
            
            success_window = customtkinter.CTkToplevel(app)
            success_window.title("Sale Successful")
            success_window.geometry("400x200")
            success_window.transient(app)
            success_window.grab_set()
            
            item_name = shop_items[emoji]["name"]
            success_label = customtkinter.CTkLabel(master=success_window, 
                                                 text=f"💰 Successfully sold {item_name}!\n\n+${sell_price} added to balance", 
                                                 font=("Arial", 16, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
            success_label.pack(pady=50)
            
            ok_btn = customtkinter.CTkButton(master=success_window, text="OK", 
                                           width=100, height=35,
                                           command=lambda: [success_window.destroy(), switch_to_inventory_tab()])
            ok_btn.pack(pady=20)
    

    switch_to_shop_tab()

def show_settings() -> None:
    track_ui_change('show_settings')  # Track UI state change
    global current_frame, current_title, current_bet_frame, current_balance_label
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="⚙️ Settings & Save Game", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_frame = customtkinter.CTkFrame(master=main_frame,
                                         corner_radius=20,
                                         fg_color=("#2B2B2B", "#1C1C1C"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
    
    # Game State Info
    info_frame = customtkinter.CTkFrame(master=current_frame,
                                       corner_radius=15,
                                       fg_color=("#333333", "#2A2A2A"))
    info_frame.pack(fill="x", padx=30, pady=30)
    
    info_title = customtkinter.CTkLabel(master=info_frame, 
                                       text="📊 Current Game State", 
                                       font=("Arial", 20, "bold"),
                                       text_color=("#E0E0E0", "#E0E0E0"))
    info_title.pack(pady=(20, 10))
    
    balance_info = customtkinter.CTkLabel(master=info_frame, 
                                         text=f"💰 Balance: ${balance}", 
                                         font=("Arial", 16),
                                         text_color=("#00FF7F", "#00FF7F"))
    balance_info.pack(pady=5)
    
    inventory_count = len(inventory)
    inventory_info = customtkinter.CTkLabel(master=info_frame, 
                                           text=f"🎒 Inventory Items: {inventory_count}", 
                                           font=("Arial", 16))
    inventory_info.pack(pady=5)
    
    transactions_count = len(transaction_history)
    transaction_info = customtkinter.CTkLabel(master=info_frame, 
                                             text=f"📋 Transactions: {transactions_count}", 
                                             font=("Arial", 16))
    transaction_info.pack(pady=(5, 20))
    
    # Save/Load Buttons
    buttons_frame = customtkinter.CTkFrame(master=current_frame, fg_color="transparent")
    buttons_frame.pack(pady=30)
    
    manual_save_btn = customtkinter.CTkButton(master=buttons_frame, 
                                             text="💾 Manual Save", 
                                             width=180, height=50,
                                             font=("Arial", 16, "bold"),
                                             fg_color=("#2ECC71", "#27AE60"),
                                             hover_color=("#58D68D", "#2ECC71"),
                                             command=lambda: manual_save_callback())
    manual_save_btn.pack(side="left", padx=15)
    
    reset_save_btn = customtkinter.CTkButton(master=buttons_frame, 
                                            text="🗑️ Reset Game", 
                                            width=180, height=50,
                                            font=("Arial", 16, "bold"),
                                            fg_color=("#E74C3C", "#C0392B"),
                                            hover_color=("#CB4335", "#A93226"),
                                            command=lambda: reset_game_callback())
    reset_save_btn.pack(side="left", padx=15)
    
    # Auto-save info
    auto_save_info = customtkinter.CTkLabel(master=current_frame, 
                                           text="🔄 Auto-save is enabled (every 60 seconds)\n💾 Game automatically saves after each transaction", 
                                           font=("Arial", 14),
                                           text_color=("#A0A0A0", "#A0A0A0"))
    auto_save_info.pack(pady=20)
    
    def manual_save_callback():
        save_game_state()
        # Show success message
        success_window = customtkinter.CTkToplevel(app)
        success_window.title("Save Successful")
        success_window.geometry("300x150")
        success_window.transient(app)
        success_window.grab_set()
        
        success_label = customtkinter.CTkLabel(master=success_window, 
                                             text="✅ Game saved successfully!", 
                                             font=("Arial", 16, "bold"),
                                             text_color=("#00FF7F", "#00FF7F"))
        success_label.pack(pady=50)
        
        close_btn = customtkinter.CTkButton(master=success_window, 
                                           text="OK", 
                                           command=success_window.destroy)
        close_btn.pack()
    
    def reset_game_callback():
        # Confirmation dialog
        confirm_window = customtkinter.CTkToplevel(app)
        confirm_window.title("Reset Game")
        confirm_window.geometry("400x200")
        confirm_window.transient(app)
        confirm_window.grab_set()
        
        confirm_label = customtkinter.CTkLabel(master=confirm_window, 
                                              text="⚠️ Are you sure you want to reset?\nThis will delete all progress!", 
                                              font=("Arial", 16, "bold"),
                                              text_color=("#E74C3C", "#C0392B"))
        confirm_label.pack(pady=30)
        
        button_frame = customtkinter.CTkFrame(master=confirm_window, fg_color="transparent")
        button_frame.pack(pady=20)
        
        yes_btn = customtkinter.CTkButton(master=button_frame, 
                                         text="Yes, Reset", 
                                         fg_color=("#E74C3C", "#C0392B"),
                                         command=lambda: perform_reset())
        yes_btn.pack(side="left", padx=10)
        
        no_btn = customtkinter.CTkButton(master=button_frame, 
                                        text="Cancel", 
                                        command=confirm_window.destroy)
        no_btn.pack(side="left", padx=10)
        
        def perform_reset():
            global balance, inventory, transaction_history, loan_info, credit_limit
            balance = 1000
            inventory = {}
            transaction_history = []
            loan_info = {"amount": 0, "interest_rate": 0.0, "monthly_payment": 0, "remaining_payments": 0}
            credit_limit = 5000
            
            # Reset shop items to default prices
            for emoji, item in shop_items.items():
                item["price"] = item["base_price"]
                item["trend"] = 0.0
            
            save_game_state()
            confirm_window.destroy()
            show_settings()  # Refresh the settings view

def create_sidebar(buttons: Dict[str, Callable[[], None]]) -> None:
    global sidebar_expanded
    sidebar = customtkinter.CTkFrame(master=app, 
                                   width=250, 
                                   corner_radius=0,
                                   fg_color=("#1E1E1E", "#0D1117"))
    sidebar.pack(side="left", fill="y")

    # Casino Games Section
    casino_frame = customtkinter.CTkFrame(master=sidebar, fg_color="transparent")
    casino_frame.pack(fill="x", padx=15, pady=(15, 10))
    
    casino_button = customtkinter.CTkButton(master=casino_frame, text="🎰 Casino Games ▼", 
                                          command=lambda: toggle_casino_menu(),
                                          font=("Arial", 16, "bold"),
                                          height=50,
                                          fg_color=("#FFD700", "#FFA500"),
                                          hover_color=("#FFB347", "#FF8C00"),
                                          text_color=("#000000", "#000000"),
                                          corner_radius=15)
    casino_button.pack(fill="x")
    
    # Compact 2-column submenu layout
    casino_submenu = customtkinter.CTkFrame(master=casino_frame, 
                                          fg_color=("#2B2B2B", "#1C1C1C"),
                                          corner_radius=12)
    
    # Row 1: Coin Flip + Number Guesser
    row1_frame = customtkinter.CTkFrame(master=casino_submenu, fg_color="transparent")
    row1_frame.pack(fill="x", padx=8, pady=6)
    
    coinflip_btn = customtkinter.CTkButton(master=row1_frame, 
                                         text="🪙 Coin Flip", 
                                         command=show_casino,
                                         font=("Arial", 12, "bold"),
                                         height=40,
                                         fg_color="transparent",
                                         hover_color=("#4ECDC4", "#26D0CE"),
                                         corner_radius=8)
    coinflip_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
    
    number_btn = customtkinter.CTkButton(master=row1_frame, 
                                       text="🔢 Number", 
                                       command=show_number_guesser,
                                       font=("Arial", 12, "bold"),
                                       height=40,
                                       fg_color="transparent",
                                       hover_color=("#9B59B6", "#8E44AD"),
                                       corner_radius=8)
    number_btn.pack(side="right", fill="x", expand=True, padx=(4, 0))
    
    # Row 2: Roulette + Blackjack
    row2_frame = customtkinter.CTkFrame(master=casino_submenu, fg_color="transparent")
    row2_frame.pack(fill="x", padx=8, pady=6)
    
    roulette_btn = customtkinter.CTkButton(master=row2_frame, 
                                         text="🎯 Roulette", 
                                         command=show_roulette,
                                         font=("Arial", 12, "bold"),
                                         height=40,
                                         fg_color="transparent",
                                         hover_color=("#E74C3C", "#C0392B"),
                                         corner_radius=8)
    roulette_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
    
    blackjack_btn = customtkinter.CTkButton(master=row2_frame, 
                                          text="🃏 Blackjack", 
                                          command=show_blackjack,
                                          font=("Arial", 12, "bold"),
                                          height=40,
                                          fg_color="transparent",
                                          hover_color=("#2ECC71", "#27AE60"),
                                          corner_radius=8)
    blackjack_btn.pack(side="right", fill="x", expand=True, padx=(4, 0))
    
    # Row 3: Dice Roll + Slot Machine
    row3_frame = customtkinter.CTkFrame(master=casino_submenu, fg_color="transparent")
    row3_frame.pack(fill="x", padx=8, pady=(6, 8))
    
    dice_btn = customtkinter.CTkButton(master=row3_frame, 
                                     text="🎲 Dice Roll", 
                                     command=show_dice_roll,
                                     font=("Arial", 12, "bold"),
                                     height=40,
                                     fg_color="transparent",
                                     hover_color=("#3498DB", "#2980B9"),
                                     corner_radius=8)
    dice_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
    
    slot_btn = customtkinter.CTkButton(master=row3_frame, 
                                     text="🎰 Slots", 
                                     command=show_slot_machine,
                                     font=("Arial", 12, "bold"),
                                     height=40,
                                     fg_color="transparent",
                                     hover_color=("#F39C12", "#E67E22"),
                                     corner_radius=8)
    slot_btn.pack(side="right", fill="x", expand=True, padx=(4, 0))
    
    def toggle_casino_menu():
        global sidebar_expanded
        if sidebar_expanded:
            casino_submenu.pack_forget()
            casino_button.configure(text="🎰 Casino Games ▼")
            sidebar_expanded = False
        else:
            casino_submenu.pack(fill="x", pady=(8, 0))
            casino_button.configure(text="🎰 Casino Games ▲")
            sidebar_expanded = True
    
    # Compact separator
    separator_line = customtkinter.CTkFrame(master=sidebar, 
                                          height=2, 
                                          fg_color=("#FFD700", "#FFA500"),
                                          corner_radius=1)
    separator_line.pack(fill="x", padx=30, pady=(15, 10))
    
    # Main navigation buttons with reduced spacing
    for button in buttons:
        if button == "Bank":
            icon = "🏦"
        elif button == "Shop":
            icon = "🛍️"
        elif button == "Settings":
            icon = "⚙"
        elif button == "Reload":
            icon = "🔄"
        else:
            icon = "📋"
        
        btn = customtkinter.CTkButton(master=sidebar, 
                                    text=f"{icon} {button}", 
                                    command=buttons[button],
                                    height=50,
                                    font=("Arial", 15, "bold"),
                                    fg_color=("#333333", "#2A2A2A"),
                                    hover_color=("#555555", "#404040"),
                                    corner_radius=15)
        btn.pack(pady=8, padx=15, fill="x")

    separator = customtkinter.CTkFrame(master=app, 
                                     width=3, 
                                     fg_color=("#FFD700", "#FFA500"))
    separator.pack(side="left", fill="y")

def show_bank() -> None:
    track_ui_change('show_bank')  # Track UI state change
    global current_frame, current_title, current_bet_frame, current_balance_label, balance, transaction_history, loan_info, bank_tabview_ref
    if current_frame:
        current_frame.destroy()
    if current_title:
        current_title.destroy()
    if current_bet_frame:
        current_bet_frame.destroy()
    if current_balance_label:
        current_balance_label.destroy()
    
    current_title = customtkinter.CTkLabel(master=main_frame, text="🏦 Digital Banking Center", 
                                          font=("Arial", 32, "bold"),
                                          text_color=("#FFD700", "#FFD700"))
    current_title.pack(pady=(30, 15))
    
    current_balance_label = customtkinter.CTkLabel(master=main_frame, 
                                                 text=f"💰 Account Balance: ${balance}", 
                                                 font=("Arial", 20, "bold"),
                                                 text_color=("#00FF7F", "#00FF7F"))
    current_balance_label.pack(pady=(0, 20))
    
    # Main container with gradient-like effect
    current_frame = customtkinter.CTkFrame(master=main_frame,
                                         corner_radius=25,
                                         fg_color=("#2B2B2B", "#1C1C1C"),
                                         border_width=2,
                                         border_color=("#FFD700", "#FFA500"))
    current_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
    
    # Modern tab view with enhanced styling
    bank_tabview = customtkinter.CTkTabview(master=current_frame,
                                          corner_radius=20,
                                          fg_color=("#1A1A1A", "#0F0F0F"),
                                          segmented_button_fg_color=("#2C3E50", "#34495E"),
                                          segmented_button_selected_color=("#FFD700", "#FFA500"),
                                          segmented_button_selected_hover_color=("#F39C12", "#E67E22"),
                                          segmented_button_unselected_color=("#34495E", "#2C3E50"),
                                          segmented_button_unselected_hover_color=("#3498DB", "#2980B9"),
                                          text_color=("#FFFFFF", "#FFFFFF"),
                                          text_color_disabled=("#7F8C8D", "#7F8C8D"),
                                          command=track_bank_tab_change)  # Track tab changes
    bank_tabview.pack(fill="both", expand=True, padx=25, pady=25)
    
    # Store reference for tracking tab changes
    bank_tabview_ref = bank_tabview
    
    # Create modern tabs with icons
    overview_tab = bank_tabview.add("📊 Dashboard")
    analytics_tab = bank_tabview.add("📈 Analytics") 
    loans_tab = bank_tabview.add("💳 Credit")
    history_tab = bank_tabview.add("📋 Transactions")
    
    # Restore previously selected tab if available
    if current_ui_state.get('bank_active_tab'):
        try:
            bank_tabview.set(current_ui_state['bank_active_tab'])
            print(f"Restored bank tab: {current_ui_state['bank_active_tab']}")
        except Exception as e:
            print(f"Could not restore bank tab, using default: {e}")
            bank_tabview.set("📊 Dashboard")
    else:
        # Set default tab
        bank_tabview.set("📊 Dashboard")
        current_ui_state['bank_active_tab'] = "📊 Dashboard"
    
    # =================== OVERVIEW TAB ===================
    
    # Top KPI Cards Row
    kpi_frame = customtkinter.CTkFrame(master=overview_tab,
                                     corner_radius=15,
                                     fg_color="transparent")
    kpi_frame.pack(fill="x", pady=(10, 20))
    
    # Calculate key metrics
    total_income = sum(t["amount"] for t in transaction_history if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in transaction_history if t["type"] == "expense")
    net_profit = total_income - total_expenses
    debt_amount = loan_info["amount"] if loan_info["amount"] > 0 else 0
    
    # Modern Balance Card with gradient effect
    balance_card = customtkinter.CTkFrame(master=kpi_frame,
                                        corner_radius=20,
                                        fg_color=("#27AE60", "#2ECC71"),
                                        border_width=3,
                                        border_color=("#2ECC71", "#27AE60"),
                                        width=200, height=140)
    balance_card.pack(side="left", fill="x", expand=True, padx=(0, 15))
    
    # Icon and title row with proper alignment
    balance_header = customtkinter.CTkFrame(master=balance_card, fg_color="transparent")
    balance_header.pack(fill="x", padx=20, pady=(20, 5))
    
    balance_icon = customtkinter.CTkLabel(master=balance_header,
                                        text="💰",
                                        font=("Arial", 28),
                                        text_color=("white", "white"))
    balance_icon.pack(side="left", anchor="w")
    
    balance_title = customtkinter.CTkLabel(master=balance_header,
                                         text="Balance",
                                         font=("Arial", 14, "bold"),
                                         text_color=("white", "white"))
    balance_title.pack(side="right", anchor="e")
    
    current_balance_stat = customtkinter.CTkLabel(master=balance_card,
                                                text=f"${balance:,}",
                                                font=("Arial", 24, "bold"),
                                                text_color=("white", "white"))
    current_balance_stat.pack(pady=(5, 20))
    
    # Modern Income Card
    income_card = customtkinter.CTkFrame(master=kpi_frame,
                                       corner_radius=20,
                                       fg_color=("#3498DB", "#2980B9"),
                                       border_width=3,
                                       border_color=("#2980B9", "#3498DB"),
                                       width=200, height=140)
    income_card.pack(side="left", fill="x", expand=True, padx=(0, 15))
    
    # Icon and title row with proper alignment
    income_header = customtkinter.CTkFrame(master=income_card, fg_color="transparent")
    income_header.pack(fill="x", padx=20, pady=(20, 5))
    
    income_icon = customtkinter.CTkLabel(master=income_header,
                                       text="📈",
                                       font=("Arial", 28),
                                       text_color=("white", "white"))
    income_icon.pack(side="left", anchor="w")
    
    income_title = customtkinter.CTkLabel(master=income_header,
                                        text="Income",
                                        font=("Arial", 14, "bold"),
                                        text_color=("white", "white"))
    income_title.pack(side="right", anchor="e")
    
    total_income_stat = customtkinter.CTkLabel(master=income_card,
                                             text=f"${total_income:,}",
                                             font=("Arial", 24, "bold"),
                                             text_color=("white", "white"))
    total_income_stat.pack(pady=(5, 20))
    
    # Modern Expenses Card
    expenses_card = customtkinter.CTkFrame(master=kpi_frame,
                                         corner_radius=20,
                                         fg_color=("#E74C3C", "#C0392B"),
                                         border_width=3,
                                         border_color=("#C0392B", "#E74C3C"),
                                         width=200, height=140)
    expenses_card.pack(side="left", fill="x", expand=True, padx=(0, 15))
    
    # Icon and title row with proper alignment
    expenses_header = customtkinter.CTkFrame(master=expenses_card, fg_color="transparent")
    expenses_header.pack(fill="x", padx=20, pady=(20, 5))
    
    expenses_icon = customtkinter.CTkLabel(master=expenses_header,
                                         text="📉",
                                         font=("Arial", 28),
                                         text_color=("white", "white"))
    expenses_icon.pack(side="left", anchor="w")
    
    expenses_title = customtkinter.CTkLabel(master=expenses_header,
                                          text="Expenses",
                                          font=("Arial", 14, "bold"),
                                          text_color=("white", "white"))
    expenses_title.pack(side="right", anchor="e")
    
    total_expenses_stat = customtkinter.CTkLabel(master=expenses_card,
                                               text=f"${total_expenses:,}",
                                               font=("Arial", 24, "bold"),
                                               text_color=("white", "white"))
    total_expenses_stat.pack(pady=(5, 20))
    
    # Modern Net Profit Card
    profit_color = ("#27AE60", "#2ECC71") if net_profit >= 0 else ("#E74C3C", "#C0392B")
    border_color = ("#2ECC71", "#27AE60") if net_profit >= 0 else ("#C0392B", "#E74C3C")
    profit_card = customtkinter.CTkFrame(master=kpi_frame,
                                       corner_radius=20,
                                       fg_color=profit_color,
                                       border_width=3,
                                       border_color=border_color,
                                       width=200, height=140)
    profit_card.pack(side="left", fill="x", expand=True)
    
    # Icon and title row with proper alignment
    profit_header = customtkinter.CTkFrame(master=profit_card, fg_color="transparent")
    profit_header.pack(fill="x", padx=20, pady=(20, 5))
    
    profit_icon = customtkinter.CTkLabel(master=profit_header,
                                       text="💹" if net_profit >= 0 else "💔",
                                       font=("Arial", 28),
                                       text_color=("white", "white"))
    profit_icon.pack(side="left", anchor="w")
    
    profit_title = customtkinter.CTkLabel(master=profit_header,
                                        text="Net Profit",
                                        font=("Arial", 14, "bold"),
                                        text_color=("white", "white"))
    profit_title.pack(side="right", anchor="e")
    
    net_profit_stat = customtkinter.CTkLabel(master=profit_card,
                                           text=f"${net_profit:,}",
                                           font=("Arial", 24, "bold"),
                                           text_color=("white", "white"))
    net_profit_stat.pack(pady=(5, 20))
    
    # Modern Financial Health Dashboard
    trend_frame = customtkinter.CTkFrame(master=overview_tab,
                                       corner_radius=20,
                                       fg_color=("#1A1A1A", "#0F0F0F"),
                                       border_width=2,
                                       border_color=("#3498DB", "#2980B9"))
    trend_frame.pack(fill="both", expand=True, pady=(20, 10))
    
    trend_title = customtkinter.CTkLabel(master=trend_frame,
                                       text="📊 Financial Health Dashboard",
                                       font=("Arial", 20, "bold"),
                                       text_color=("#FFD700", "#FFD700"))
    trend_title.pack(pady=(25, 20))
    
    # Create modern visual chart using progress bars
    chart_container = customtkinter.CTkFrame(master=trend_frame, 
                                           fg_color="transparent")
    chart_container.pack(fill="both", expand=True, padx=30, pady=(0, 25))
    
    # Modern Financial Health Score
    health_score = calculate_financial_health(balance, net_profit, debt_amount)
    
    health_frame = customtkinter.CTkFrame(master=chart_container, 
                                        corner_radius=15,
                                        fg_color=("#2C3E50", "#34495E"),
                                        border_width=2,
                                        border_color=get_health_color(health_score))
    health_frame.pack(fill="x", pady=(0, 25))
    
    health_title = customtkinter.CTkLabel(master=health_frame,
                                        text="💚 Financial Health Score",
                                        font=("Arial", 18, "bold"),
                                        text_color=("#FFFFFF", "#FFFFFF"))
    health_title.pack(pady=(20, 10))
    
    health_progress = customtkinter.CTkProgressBar(master=health_frame,
                                                 width=600, height=30,
                                                 progress_color=get_health_color(health_score),
                                                 fg_color=("#555555", "#444444"),
                                                 corner_radius=15)
    health_progress.pack(pady=(0, 10))
    health_progress.set(health_score / 100)
    
    health_value = customtkinter.CTkLabel(master=health_frame,
                                        text=f"{health_score:.0f}/100 - {get_health_status(health_score)} {get_health_emoji(health_score)}",
                                        font=("Arial", 16, "bold"),
                                        text_color=get_health_color(health_score))
    health_value.pack(pady=(0, 20))
    
    # Modern Income vs Expenses Visual Comparison
    comparison_frame = customtkinter.CTkFrame(master=chart_container, 
                                            corner_radius=15,
                                            fg_color=("#2C3E50", "#34495E"),
                                            border_width=2,
                                            border_color=("#95A5A6", "#7F8C8D"))
    comparison_frame.pack(fill="x", pady=10)
    
    comparison_title = customtkinter.CTkLabel(master=comparison_frame,
                                            text="💰 Income vs Expenses Analysis",
                                            font=("Arial", 18, "bold"),
                                            text_color=("#FFFFFF", "#FFFFFF"))
    comparison_title.pack(pady=(20, 15))
    
    max_amount = max(total_income, total_expenses, 1)
    
    # Modern Income bar with better alignment
    income_row = customtkinter.CTkFrame(master=comparison_frame, fg_color="transparent")
    income_row.pack(fill="x", padx=25, pady=(0, 15))
    
    income_info = customtkinter.CTkFrame(master=income_row, fg_color="transparent")
    income_info.pack(fill="x", pady=(0, 8))
    
    # Create a horizontal layout for emoji and text
    income_left = customtkinter.CTkFrame(master=income_info, fg_color="transparent")
    income_left.pack(side="left", anchor="w")
    
    income_emoji = customtkinter.CTkLabel(master=income_left,
                                        text="💚",
                                        font=("Arial", 18),
                                        text_color=("#2ECC71", "#27AE60"))
    income_emoji.pack(side="left", padx=(0, 8), anchor="w")
    
    income_bar_label = customtkinter.CTkLabel(master=income_left,
                                            text="Total Income",
                                            font=("Arial", 16, "bold"),
                                            text_color=("#2ECC71", "#27AE60"))
    income_bar_label.pack(side="left", anchor="w")
    
    income_value = customtkinter.CTkLabel(master=income_info,
                                        text=f"${total_income:,}",
                                        font=("Arial", 16, "bold"),
                                        text_color=("#2ECC71", "#27AE60"))
    income_value.pack(side="right", anchor="e")
    
    income_bar = customtkinter.CTkProgressBar(master=income_row,
                                            width=400, height=25,
                                            progress_color=("#2ECC71", "#27AE60"),
                                            fg_color=("#555555", "#444444"),
                                            corner_radius=12)
    income_bar.pack(fill="x")
    income_bar.set(total_income / max_amount if max_amount > 0 else 0)
    
    # Modern Expenses bar with better alignment
    expenses_row = customtkinter.CTkFrame(master=comparison_frame, fg_color="transparent")
    expenses_row.pack(fill="x", padx=25, pady=(0, 20))
    
    expenses_info = customtkinter.CTkFrame(master=expenses_row, fg_color="transparent")
    expenses_info.pack(fill="x", pady=(0, 8))
    
    # Create a horizontal layout for emoji and text
    expenses_left = customtkinter.CTkFrame(master=expenses_info, fg_color="transparent")
    expenses_left.pack(side="left", anchor="w")
    
    expenses_emoji = customtkinter.CTkLabel(master=expenses_left,
                                          text="🔴",
                                          font=("Arial", 18),
                                          text_color=("#E74C3C", "#C0392B"))
    expenses_emoji.pack(side="left", padx=(0, 8), anchor="w")
    
    expenses_bar_label = customtkinter.CTkLabel(master=expenses_left,
                                              text="Total Expenses",
                                              font=("Arial", 16, "bold"),
                                              text_color=("#E74C3C", "#C0392B"))
    expenses_bar_label.pack(side="left", anchor="w")
    
    expenses_value = customtkinter.CTkLabel(master=expenses_info,
                                          text=f"${total_expenses:,}",
                                          font=("Arial", 16, "bold"),
                                          text_color=("#E74C3C", "#C0392B"))
    expenses_value.pack(side="right", anchor="e")
    
    expenses_bar = customtkinter.CTkProgressBar(master=expenses_row,
                                              width=400, height=25,
                                              progress_color=("#E74C3C", "#C0392B"),
                                              fg_color=("#555555", "#444444"),
                                              corner_radius=12)
    expenses_bar.pack(fill="x")
    expenses_bar.set(total_expenses / max_amount if max_amount > 0 else 0)
    
    # =================== ANALYTICS TAB ===================
    
    analytics_title = customtkinter.CTkLabel(master=analytics_tab,
                                            text="📈 Advanced Financial Analytics",
                                            font=("Arial", 20, "bold"),
                                            text_color=("#FFD700", "#FFD700"))
    analytics_title.pack(pady=(20, 15))
    
    # Transaction Frequency Chart
    freq_frame = customtkinter.CTkFrame(master=analytics_tab,
                                      corner_radius=15,
                                      fg_color=("#1A1A1A", "#0F0F0F"),
                                      border_width=2,
                                      border_color=("#3498DB", "#2980B9"))
    freq_frame.pack(fill="x", pady=(0, 15), padx=20)
    
    freq_title = customtkinter.CTkLabel(master=freq_frame,
                                      text="📊 Recent Transaction Activity",
                                      font=("Arial", 18, "bold"),
                                      text_color=("#3498DB", "#2980B9"))
    freq_title.pack(pady=(15, 5))
    
    # Detailed description
    description_label = customtkinter.CTkLabel(master=freq_frame,
                                             text="📈 Visual overview of your last 10 transactions\n" +
                                                  "🟢 Green bars = Money earned (winnings, loans)\n" +
                                                  "🔴 Red bars = Money spent (bets, payments)\n" +
                                                  "📏 Bar length shows relative transaction amounts",
                                             font=("Arial", 12),
                                             text_color=("#CCCCCC", "#CCCCCC"),
                                             justify="left")
    description_label.pack(pady=(0, 15))
    
    # Create visual transaction frequency bars
    if transaction_history:
        recent_transactions = transaction_history[-10:]
        create_enhanced_transaction_chart(freq_frame, recent_transactions)
    else:
        no_data_frame = customtkinter.CTkFrame(master=freq_frame, 
                                             fg_color=("#2C3E50", "#34495E"),
                                             corner_radius=10)
        no_data_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        no_data_label = customtkinter.CTkLabel(master=no_data_frame,
                                             text="🔍 No transaction data available yet\n" +
                                                  "💡 Start playing games to see your activity here!\n" +
                                                  "🎮 Every bet, win, and transaction will appear in this chart",
                                             font=("Arial", 14),
                                             text_color=("#95A5A6", "#7F8C8D"))
        no_data_label.pack(pady=30)
    
    # Spending Categories
    categories_frame = customtkinter.CTkFrame(master=analytics_tab,
                                            corner_radius=15,
                                            fg_color=("#1A1A1A", "#0F0F0F"))
    categories_frame.pack(fill="both", expand=True, padx=20)
    
    cat_title = customtkinter.CTkLabel(master=categories_frame,
                                     text="🎯 Spending Categories",
                                     font=("Arial", 16, "bold"))
    cat_title.pack(pady=(15, 10))
    
    create_spending_category_chart(categories_frame, transaction_history)
    
    # =================== LOANS TAB ===================
    
    # Scrollable container for the entire loans tab
    loans_scroll_frame = customtkinter.CTkScrollableFrame(master=loans_tab,
                                                        corner_radius=15,
                                                        fg_color="transparent")
    loans_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Title - centered
    loan_title = customtkinter.CTkLabel(master=loans_scroll_frame,
                                      text="💳 Loan Management Center",
                                      font=("Arial", 22, "bold"),
                                      text_color=("#FF6B6B", "#FF4757"))
    loan_title.pack(pady=(10, 20))
    
    # Loan Status Card - compact design
    loan_status_card = customtkinter.CTkFrame(master=loans_scroll_frame,
                                            corner_radius=15,
                                            fg_color=("#1A1A1A", "#0F0F0F"),
                                            border_width=2,
                                            border_color=("#FF6B6B", "#FF4757"))
    loan_status_card.pack(pady=(0, 15), padx=20, fill="x")
    
    if loan_info["amount"] > 0:
        create_active_loan_display(loan_status_card, loan_info)
    else:
        create_no_loan_display(loan_status_card)
    
    # Loan Controls - compact card
    loan_controls_frame = customtkinter.CTkFrame(master=loans_scroll_frame,
                                               corner_radius=15,
                                               fg_color=("#1A1A1A", "#0F0F0F"),
                                               border_width=2,
                                               border_color=("#3498DB", "#2980B9"))
    loan_controls_frame.pack(pady=(0, 15), padx=20, fill="x")
    
    controls_title = customtkinter.CTkLabel(master=loan_controls_frame,
                                          text="💰 Loan Operations",
                                          font=("Arial", 16, "bold"),
                                          text_color=("#3498DB", "#2980B9"))
    controls_title.pack(pady=(15, 10))
    
    # Compact input field
    loan_amount_entry = customtkinter.CTkEntry(master=loan_controls_frame,
                                             placeholder_text="💵 Enter loan amount (max $5,000)",
                                             width=250, height=40,
                                             font=("Arial", 14),
                                             corner_radius=10,
                                             border_width=2,
                                             border_color=("#3498DB", "#2980B9"))
    loan_amount_entry.pack(pady=(0, 15))
    
    # Compact buttons frame
    buttons_frame = customtkinter.CTkFrame(master=loan_controls_frame, fg_color="transparent")
    buttons_frame.pack(pady=(0, 10))
    
    # Result label for feedback - compact
    loan_result_label = customtkinter.CTkLabel(master=loan_controls_frame,
                                             text="💡 Enter amount and click 'Take Loan' to get started",
                                             font=("Arial", 12, "bold"),
                                             text_color=("#888888", "#888888"))
    loan_result_label.pack(pady=(0, 15))
    
    def take_loan():
        global balance, loan_info, current_balance_label
        try:
            loan_amount = int(loan_amount_entry.get() or 0)
            
            if loan_info["amount"] > 0:
                loan_result_label.configure(text="❌ You already have an active loan!", 
                                          text_color=("#FF6B6B", "#FF4757"))
                return
            
            if loan_amount <= 0:
                loan_result_label.configure(text="❌ Please enter a valid amount!", 
                                          text_color=("#FF6B6B", "#FF4757"))
                return
                
            if loan_amount > credit_limit:
                loan_result_label.configure(text=f"❌ Maximum loan amount is ${credit_limit:,}!", 
                                          text_color=("#FF6B6B", "#FF4757"))
                return
            
            # Random interest rate between 5% and 15%
            interest_rate = random.uniform(5.0, 15.0)
            
            # Calculate monthly payment
            total_with_interest = loan_amount * (1 + interest_rate / 100)
            monthly_payment = int(total_with_interest / 12)
            
            # Update loan info
            loan_info["amount"] = int(total_with_interest)
            loan_info["interest_rate"] = interest_rate
            loan_info["monthly_payment"] = monthly_payment
            loan_info["remaining_payments"] = 12
            
            # Add money to balance
            balance += loan_amount
            if current_balance_label:
                current_balance_label.configure(text=f"💰 Account Balance: ${balance}")
            
            # Record transaction
            add_transaction("income", loan_amount, f"Bank Loan ({interest_rate:.2f}%)")
            
            loan_result_label.configure(text=f"✅ Loan approved! ${loan_amount:,} added to balance", 
                                      text_color=("#00FF7F", "#00FF7F"))
            loan_amount_entry.delete(0, "end")
            
            # Refresh the bank display completely
            show_bank()
            
        except ValueError:
            loan_result_label.configure(text="❌ Please enter a valid number!", 
                                      text_color=("#FF6B6B", "#FF4757"))
    
    def pay_loan():
        global balance, loan_info, current_balance_label
        
        if loan_info["amount"] <= 0:
            loan_result_label.configure(text="❌ No active loan to pay!", 
                                      text_color=("#FF6B6B", "#FF4757"))
            return
        
        payment = loan_info["monthly_payment"]
        
        if balance < payment:
            loan_result_label.configure(text=f"❌ Insufficient funds! Need ${payment:,}", 
                                      text_color=("#FF6B6B", "#FF4757"))
            return
        
        balance -= payment
        loan_info["amount"] -= payment
        loan_info["remaining_payments"] -= 1
        
        if current_balance_label:
            current_balance_label.configure(text=f"💰 Account Balance: ${balance}")

        add_transaction("expense", payment, "Loan Payment")
        
        if loan_info["remaining_payments"] <= 0:
            loan_info = {"amount": 0, "interest_rate": 0.0, "monthly_payment": 0, "remaining_payments": 0}
            loan_result_label.configure(text="🎉 Loan fully paid off! Congratulations!", 
                                      text_color=("#00FF7F", "#00FF7F"))
        else:
            loan_result_label.configure(text=f"✅ Payment successful! {loan_info['remaining_payments']} payments remaining", 
                                      text_color=("#00FF7F", "#00FF7F"))
        
        # Refresh the bank display completely  
        show_bank()
    
    def pay_full_loan():
        global balance, loan_info, current_balance_label
        
        if loan_info["amount"] <= 0:
            loan_result_label.configure(text="❌ No active loan to pay!", 
                                      text_color=("#FF6B6B", "#FF4757"))
            return
        
        full_payment = loan_info["amount"]
        
        if balance < full_payment:
            loan_result_label.configure(text=f"❌ Insufficient funds! Need ${full_payment:,} to pay off loan", 
                                      text_color=("#FF6B6B", "#FF4757"))
            return
        
        balance -= full_payment
        
        if current_balance_label:
            current_balance_label.configure(text=f"💰 Account Balance: ${balance}")

        add_transaction("expense", full_payment, "Full Loan Payment")
        
        # Reset loan info completely
        loan_info = {"amount": 0, "interest_rate": 0.0, "monthly_payment": 0, "remaining_payments": 0}
        loan_result_label.configure(text="🎉 Loan fully paid off! Congratulations!", 
                                  text_color=("#00FF7F", "#00FF7F"))
        
        # Refresh the bank display completely  
        show_bank()
    
    
    take_loan_btn = customtkinter.CTkButton(master=buttons_frame,
                                          text="💳 Take Loan",
                                          command=take_loan,
                                          width=110, height=40,
                                          font=("Arial", 13, "bold"),
                                          corner_radius=10,
                                          fg_color=("#E74C3C", "#C0392B"),
                                          hover_color=("#CB4335", "#A93226"))
    take_loan_btn.pack(side="left", padx=(0, 8))
    
    pay_loan_btn = customtkinter.CTkButton(master=buttons_frame,
                                         text="💰 Pay Monthly",
                                         command=pay_loan,
                                         width=110, height=40,
                                         font=("Arial", 13, "bold"),
                                         corner_radius=10,
                                         fg_color=("#27AE60", "#229954"),
                                         hover_color=("#2ECC71", "#27AE60"))
    pay_loan_btn.pack(side="left", padx=(0, 8))
    
    pay_full_loan_btn = customtkinter.CTkButton(master=buttons_frame,
                                              text="💸 Pay Full",
                                              command=pay_full_loan,
                                              width=110, height=40,
                                              font=("Arial", 13, "bold"),
                                              corner_radius=10,
                                              fg_color=("#8E44AD", "#7D3C98"),
                                              hover_color=("#9B59B6", "#8E44AD"))
    pay_full_loan_btn.pack(side="left")
    
    # =================== HISTORY TAB ===================
    
    history_title = customtkinter.CTkLabel(master=history_tab,
                                         text="📋 Complete Transaction History",
                                         font=("Arial", 20, "bold"),
                                         text_color=("#3498DB", "#2980B9"))
    history_title.pack(pady=(20, 15))
    
    # Create scrollable transaction list with better formatting
    create_transaction_history_display(history_tab, transaction_history)
    
    # Global update function for all tabs
    def update_all_bank_data():
        global balance, transaction_history, loan_info
        
        # Recalculate all metrics
        total_income = sum(t["amount"] for t in transaction_history if t["type"] == "income")
        total_expenses = sum(t["amount"] for t in transaction_history if t["type"] == "expense")
        net_profit = total_income - total_expenses
        debt_amount = loan_info["amount"] if loan_info["amount"] > 0 else 0
        
        # Update all displays - wrap in try/except to handle destroyed widgets
        try:
            current_balance_stat.configure(text=f"${balance:,}")
            current_balance_label.configure(text=f"💰 Account Balance: ${balance:,}")
            total_income_stat.configure(text=f"${total_income:,}")
            total_expenses_stat.configure(text=f"${total_expenses:,}")
            net_profit_stat.configure(text=f"${net_profit:,}")
        except:
            pass  # Bank UI elements don't exist or have been destroyed
        
        # Update progress bars
        try:
            health_score = calculate_financial_health(balance, net_profit, debt_amount)
            health_progress.configure(progress_color=get_health_color(health_score))
            health_progress.set(health_score / 100)
            health_value.configure(text=f"{health_score:.0f}/100 - {get_health_status(health_score)}",
                                  text_color=get_health_color(health_score))
        except:
            pass  # Health UI elements don't exist
        
        # Update comparison bars
        try:
            max_amount = max(total_income, total_expenses, 1)
            income_bar.set(total_income / max_amount if max_amount > 0 else 0)
            expenses_bar.set(total_expenses / max_amount if max_amount > 0 else 0)
            income_value.configure(text=f"${total_income:,}")
            expenses_value.configure(text=f"${total_expenses:,}")
        except:
            pass  # Comparison UI elements don't exist
        
        # Update card colors
        try:
            profit_color = ("#2ECC71", "#27AE60") if net_profit >= 0 else ("#E74C3C", "#C0392B")
            profit_card.configure(fg_color=profit_color)
            profit_icon.configure(text="💹" if net_profit >= 0 else "💔")
        except:
            pass  # Card UI elements don't exist
    
    # Add refresh button
    refresh_frame = customtkinter.CTkFrame(master=overview_tab, fg_color="transparent")
    refresh_frame.pack(fill="x", pady=10)
    
    refresh_btn = customtkinter.CTkButton(master=refresh_frame,
                                        text="🔄 Refresh All Data",
                                        command=update_all_bank_data,
                                        width=150, height=35,
                                        font=("Arial", 14, "bold"),
                                        fg_color=("#3498DB", "#2980B9"),
                                        hover_color=("#5DADE2", "#3498DB"))
    refresh_btn.pack()
    
    # Store update function globally so other functions can call it
    global update_bank_display
    update_bank_display = update_all_bank_data
    
    # Initial update
    update_all_bank_data()


# Helper functions for bank display
def calculate_financial_health(balance, net_profit, debt):
    """Calculate financial health score (0-100)"""
    score = 50  # Base score
    if balance > 0:
        score += min(25, balance / 100)
    if net_profit > 0:
        score += min(25, net_profit / 200)
    if debt == 0:
        score += 25
    else:
        score -= min(25, debt / 200)
    return max(0, min(100, score))

def get_health_color(score):
    """Get color based on health score"""
    if score >= 75:
        return ("#2ECC71", "#27AE60")
    elif score >= 50:
        return ("#F39C12", "#E67E22")
    elif score >= 25:
        return ("#FF9500", "#FF8C00")
    else:
        return ("#E74C3C", "#C0392B")

def get_health_status(score):
    """Get status text based on health score"""
    if score >= 75:
        return "Excellent"
    elif score >= 50:
        return "Good"
    elif score >= 25:
        return "Fair"
    else:
        return "Poor"

def get_health_emoji(score):
    """Get emoji based on health score"""
    if score >= 75:
        return "🟢"
    elif score >= 50:
        return "🟡"
    elif score >= 25:
        return "🟠"
    else:
        return "🔴"

def create_enhanced_transaction_chart(parent, transactions):
    """Create enhanced visual chart for recent transactions with detailed information"""
    
    # Main chart container with enhanced styling
    chart_container = customtkinter.CTkFrame(master=parent, 
                                           fg_color=("#2C3E50", "#34495E"),
                                           corner_radius=12,
                                           border_width=1,
                                           border_color=("#3498DB", "#2980B9"))
    chart_container.pack(fill="x", padx=20, pady=(0, 20))
    
    # Chart header with summary stats
    header_frame = customtkinter.CTkFrame(master=chart_container, fg_color="transparent")
    header_frame.pack(fill="x", padx=15, pady=(15, 10))
    
    total_in = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_out = sum(t["amount"] for t in transactions if t["type"] == "expense")
    net_change = total_in - total_out
    
    stats_text = f"💰 Last {len(transactions)} transactions: +${total_in} in, -${total_out} out, Net: "
    net_text = f"{'📈' if net_change >= 0 else '📉'} ${abs(net_change):,}"
    net_color = ("#2ECC71", "#27AE60") if net_change >= 0 else ("#E74C3C", "#C0392B")
    
    stats_label = customtkinter.CTkLabel(master=header_frame,
                                       text=stats_text,
                                       font=("Arial", 12, "bold"),
                                       text_color=("#FFFFFF", "#FFFFFF"))
    stats_label.pack(side="left")
    
    net_label = customtkinter.CTkLabel(master=header_frame,
                                     text=net_text,
                                     font=("Arial", 12, "bold"),
                                     text_color=net_color)
    net_label.pack(side="left")
    
    # Transactions list with enhanced display
    if not transactions:
        return
    
    max_amount = max(abs(t["amount"]) for t in transactions)
    
    # Scrollable frame for transactions
    trans_scroll = customtkinter.CTkScrollableFrame(master=chart_container,
                                                  height=200,
                                                  fg_color="transparent")
    trans_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 15))
    
    for i, transaction in enumerate(reversed(transactions)):  # Most recent first
        row_frame = customtkinter.CTkFrame(master=trans_scroll, 
                                         fg_color=("#34495E", "#2C3E50"),
                                         corner_radius=8,
                                         border_width=1,
                                         border_color=("#555555", "#444444"))
        row_frame.pack(fill="x", pady=2, padx=5)
        
        # Transaction row content
        content_frame = customtkinter.CTkFrame(master=row_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=10, pady=8)
        
        # Left side: Type indicator and description
        left_frame = customtkinter.CTkFrame(master=content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="x", expand=True)
        
        # Transaction type with enhanced emoji
        type_emoji = "�" if transaction["type"] == "income" else "�"
        type_color = ("#2ECC71", "#27AE60") if transaction["type"] == "income" else ("#E74C3C", "#C0392B")
        
        type_label = customtkinter.CTkLabel(master=left_frame,
                                          text=type_emoji,
                                          font=("Arial", 16),
                                          text_color=type_color)
        type_label.pack(side="left", padx=(0, 8))
        
        # Description with category detection
        description = transaction['description']
        if len(description) > 20:
            description = description[:17] + "..."
            
        desc_label = customtkinter.CTkLabel(master=left_frame,
                                          text=description,
                                          font=("Arial", 11, "bold"),
                                          text_color=("#FFFFFF", "#FFFFFF"),
                                          width=150,
                                          anchor="w")
        desc_label.pack(side="left", padx=(0, 10))
        
        # Timestamp (if available)
        if "timestamp" in transaction:
            time_text = transaction["timestamp"].split(" ")[1]  # Just the time part
            time_label = customtkinter.CTkLabel(master=left_frame,
                                              text=f"🕐 {time_text}",
                                              font=("Arial", 9),
                                              text_color=("#95A5A6", "#7F8C8D"))
            time_label.pack(side="left")
        
        # Right side: Visual bar and amount
        right_frame = customtkinter.CTkFrame(master=content_frame, fg_color="transparent")
        right_frame.pack(side="right")
        
        # Visual progress bar showing relative amount
        bar_width = int((transaction["amount"] / max_amount) * 120) if max_amount > 0 else 5
        bar_width = max(bar_width, 10)  # Minimum width for visibility
        
        bar = customtkinter.CTkProgressBar(master=right_frame,
                                         width=bar_width, height=12,
                                         progress_color=type_color,
                                         fg_color=("#555555", "#444444"),
                                         corner_radius=6)
        bar.pack(side="left", padx=(0, 10))
        bar.set(1.0)  # Always full since width represents the amount
        
        # Amount with proper formatting
        amount_text = f"${transaction['amount']:,}"
        if transaction["type"] == "income":
            amount_text = f"+{amount_text}"
        else:
            amount_text = f"-{amount_text}"
            
        amount_label = customtkinter.CTkLabel(master=right_frame,
                                            text=amount_text,
                                            font=("Arial", 11, "bold"),
                                            text_color=type_color,
                                            width=80)
        amount_label.pack(side="right")

def create_transaction_visual_chart(parent, transactions):
    """Legacy function - kept for compatibility, redirects to enhanced version"""
    create_enhanced_transaction_chart(parent, transactions)

def create_spending_category_chart(parent, transactions):
    """Create spending category visualization"""
    if not transactions:
        no_data = customtkinter.CTkLabel(master=parent,
                                       text="📊 No spending data available",
                                       font=("Arial", 14))
        no_data.pack(pady=30)
        return
    
    # Categorize expenses with emojis
    categories = {
        "🎮 Gaming": 0,
        "🛍️ Shopping": 0, 
        "💳 Loans": 0,
        "📦 Other": 0
    }
    
    for t in transactions:
        if t["type"] == "expense":
            desc = t["description"].lower()
            if any(game in desc for game in ["flip", "guess", "roulette", "blackjack", "dice", "slot"]):
                categories["🎮 Gaming"] += t["amount"]
            elif "shop" in desc or "buy" in desc or "sell" in desc:
                categories["🛍️ Shopping"] += t["amount"]
            elif "loan" in desc:
                categories["💳 Loans"] += t["amount"]
            else:
                categories["📦 Other"] += t["amount"]
    
    total_expenses = sum(categories.values())
    if total_expenses == 0:
        return
    
    colors = [
        ("#E74C3C", "#C0392B"),   # Gaming - Red
        ("#9B59B6", "#8E44AD"),   # Shopping - Purple  
        ("#F39C12", "#E67E22"),   # Loans - Orange
        ("#95A5A6", "#7F8C8D")    # Other - Gray
    ]
    
    chart_container = customtkinter.CTkFrame(master=parent, fg_color="transparent")
    chart_container.pack(fill="x", padx=20, pady=(0, 15))
    
    for i, (category, amount) in enumerate(categories.items()):
        if amount > 0:
            row = customtkinter.CTkFrame(master=chart_container, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            # Left side with aligned emoji and text
            left_side = customtkinter.CTkFrame(master=row, fg_color="transparent")
            left_side.pack(side="left", padx=(0, 20))
            
            # Category label with emoji and text properly aligned
            cat_label = customtkinter.CTkLabel(master=left_side,
                                             text=category,
                                             font=("Arial", 14, "bold"),
                                             width=120)
            cat_label.pack(side="left")
            
            # Progress bar
            percentage = amount / total_expenses
            progress = customtkinter.CTkProgressBar(master=row,
                                                  width=250, height=20,
                                                  progress_color=colors[i],
                                                  fg_color=("#555555", "#444444"))
            progress.pack(side="left", padx=(0, 15))
            progress.set(percentage)
            
            # Amount and percentage
            stats_label = customtkinter.CTkLabel(master=row,
                                                text=f"${amount:,} ({percentage*100:.1f}%)",
                                                font=("Arial", 12, "bold"),
                                                text_color=colors[i])
            stats_label.pack(side="left")

def create_active_loan_display(parent, loan_info):
    """Create display for active loan"""
    loan_frame = customtkinter.CTkFrame(master=parent, fg_color="transparent")
    loan_frame.pack(fill="x", padx=15, pady=10)
    
    # Loan details with progress bar - compact
    details_frame = customtkinter.CTkFrame(master=loan_frame,
                                         corner_radius=10,
                                         fg_color=("#FF6B6B", "#FF4757"))
    details_frame.pack(fill="x", pady=(0, 10))
    
    loan_amount_label = customtkinter.CTkLabel(master=details_frame,
                                             text=f"💳 Outstanding Loan: ${loan_info['amount']:,}",
                                             font=("Arial", 14, "bold"),
                                             text_color=("white", "white"))
    loan_amount_label.pack(pady=(10, 5))
    
    # Payment progress - compact
    progress = (12 - loan_info["remaining_payments"]) / 12
    
    progress_bar = customtkinter.CTkProgressBar(master=details_frame,
                                              width=250, height=12,
                                              progress_color=("#FFFFFF", "#FFFFFF"),
                                              fg_color=("#AA0000", "#880000"))
    progress_bar.pack(pady=5)
    progress_bar.set(progress)
    
    progress_label = customtkinter.CTkLabel(master=details_frame,
                                          text=f"Payments: {12 - loan_info['remaining_payments']}/12 completed",
                                          font=("Arial", 11),
                                          text_color=("white", "white"))
    progress_label.pack(pady=(0, 10))

def create_no_loan_display(parent):
    """Create display when no loan is active"""
    no_loan_frame = customtkinter.CTkFrame(master=parent,
                                         corner_radius=10,
                                         fg_color=("#2ECC71", "#27AE60"))
    no_loan_frame.pack(fill="x", padx=15, pady=10)
    
    status_label = customtkinter.CTkLabel(master=no_loan_frame,
                                        text="✅ No Active Loans - Debt Free!",
                                        font=("Arial", 14, "bold"),
                                        text_color=("white", "white"))
    status_label.pack(pady=10)
    
    credit_label = customtkinter.CTkLabel(master=no_loan_frame,
                                        text=f"💡 Available Credit: ${credit_limit:,}",
                                        font=("Arial", 12),
                                        text_color=("white", "white"))
    credit_label.pack(pady=(0, 10))

def create_transaction_history_display(parent, transactions):
    """Create enhanced transaction history display"""
    if not transactions:
        no_history = customtkinter.CTkLabel(master=parent,
                                          text="📝 No transaction history available\nStart playing games to build your history!",
                                          font=("Arial", 16))
        no_history.pack(pady=50)
        return
    
    # Scrollable frame for transactions
    history_scroll = customtkinter.CTkScrollableFrame(master=parent,
                                                    corner_radius=15,
                                                    fg_color=("#1A1A1A", "#0F0F0F"))
    history_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    # Header
    header_frame = customtkinter.CTkFrame(master=history_scroll,
                                        corner_radius=10,
                                        fg_color=("#3498DB", "#2980B9"))
    header_frame.pack(fill="x", pady=(10, 5))
    
    header_row = customtkinter.CTkFrame(master=header_frame, fg_color="transparent")
    header_row.pack(fill="x", padx=15, pady=10)
    
    headers = ["Date & Time", "Type", "Amount", "Description"]
    for header in headers:
        label = customtkinter.CTkLabel(master=header_row,
                                     text=header,
                                     font=("Arial", 12, "bold"),
                                     text_color=("white", "white"),
                                     width=120)
        label.pack(side="left", padx=10)
    
    # Transaction rows
    for transaction in reversed(transactions[-25:]):  # Show last 25
        row_frame = customtkinter.CTkFrame(master=history_scroll,
                                         corner_radius=5,
                                         fg_color=("#333333", "#2A2A2A"))
        row_frame.pack(fill="x", pady=2)
        
        row_content = customtkinter.CTkFrame(master=row_frame, fg_color="transparent")
        row_content.pack(fill="x", padx=15, pady=8)
        
        # Date
        date_label = customtkinter.CTkLabel(master=row_content,
                                          text=transaction["timestamp"],
                                          font=("Arial", 11),
                                          width=120)
        date_label.pack(side="left", padx=10)
        
        # Type with icon
        type_icon = "🟢" if transaction["type"] == "income" else "🔴"
        type_label = customtkinter.CTkLabel(master=row_content,
                                          text=f"{type_icon} {transaction['type'].title()}",
                                          font=("Arial", 11),
                                          width=120)
        type_label.pack(side="left", padx=10)
        
        # Amount
        amount_text = f"+${transaction['amount']}" if transaction["type"] == "income" else f"-${transaction['amount']}"
        amount_color = ("#2ECC71", "#27AE60") if transaction["type"] == "income" else ("#E74C3C", "#C0392B")
        amount_label = customtkinter.CTkLabel(master=row_content,
                                            text=amount_text,
                                            font=("Arial", 11, "bold"),
                                            text_color=amount_color,
                                            width=120)
        amount_label.pack(side="left", padx=10)
        
        # Description
        desc_label = customtkinter.CTkLabel(master=row_content,
                                          text=transaction["description"],
                                          font=("Arial", 11),
                                          width=200)
        desc_label.pack(side="left", padx=10)


# Global update function for live bank updates
def update_bank_display():
    """Update bank data without switching tabs"""
    global balance, transaction_history, loan_info
    
    # Only update the current balance label if it exists and we're not in the bank
    if current_balance_label:
        try:
            current_balance_label.configure(text=f"💰 Balance: ${balance}")
        except:
            pass  # UI element destroyed
    
    # No tab switching - just update data silently


buttons: Dict[str, Callable[[], None]] = {"Bank": show_bank, "Shop": show_shop, "Settings": show_settings, "Reload": reload}

# Load saved game state at startup
load_game_state()

create_sidebar(buttons)

main_frame = customtkinter.CTkFrame(master=app,
                                   fg_color=("#F0F0F0", "#1A1A1A"),
                                   corner_radius=0)
main_frame.pack(side="left", fill="both", expand=True)

def auto_lose():
    global balance, current_balance_label, loan_info, inventory, game_active

    # Only check for lose condition if balance is 0 or negative
    if balance <= 0:
        # Check if player still has a loan available (not already taken)
        can_take_loan = loan_info["amount"] == 0 and loan_info["remaining_payments"] == 0
        
        # Check if player has inventory items to sell
        has_inventory_items = any(inventory.get(key, 0) > 0 for key in inventory.keys()) if inventory else False
        
        # Player can still play if they can take a loan OR have inventory items
        if can_take_loan or has_inventory_items:
            # Game continues - player still has options
            pass
        else:
            # Game over - player has no money, no loan option, and no inventory
            game_active = False
            
            # Clear the save file permanently
            try:
                os.remove("gambling_simulator_save.dill")
            except:
                pass
            
            # Clear the entire UI
            try:
                for widget in app.winfo_children():
                    widget.destroy()
            except:
                pass
            
            # Create lose screen
            lose_frame = customtkinter.CTkFrame(master=app,
                                               fg_color=("#F0F0F0", "#1A1A1A"),
                                               corner_radius=0)
            lose_frame.pack(fill="both", expand=True)

            # Game Over title
            game_over_title = customtkinter.CTkLabel(master=lose_frame, 
                                                    text="🎰 GAME OVER! 🎰", 
                                                    font=("Arial", 48, "bold"),
                                                    text_color=("#E74C3C", "#C0392B"))
            game_over_title.pack(pady=(100, 30))
            
            # Lose message
            lose_message = customtkinter.CTkLabel(master=lose_frame, 
                                                 text="💸 You ran out of money with no way to recover!\n\n" +
                                                      "❌ No loan available (already used)\n" +
                                                      "❌ No inventory items to sell\n" +
                                                      "❌ No money left to play\n\n" +
                                                      "💡 Tips for next time:\n" +
                                                      "• Don't use your loan too early\n" +
                                                      "• Buy items from the shop as backup\n" +
                                                      "• Don't bet everything at once!\n\n" +
                                                      "🔄 Click below to start a new game!", 
                                                 font=("Arial", 16),
                                                 text_color=("#FFFFFF", "#FFFFFF"),
                                                 justify="center")
            lose_message.pack(pady=(0, 40))
            
            # New Game button
            new_game_btn = customtkinter.CTkButton(master=lose_frame, 
                                                  text="🎮 Start New Game", 
                                                  width=200, height=50,
                                                  font=("Arial", 18, "bold"),
                                                  fg_color=("#2ECC71", "#27AE60"),
                                                  hover_color=("#58D68D", "#2ECC71"),
                                                  command=restart_game)
            new_game_btn.pack(pady=20)
            
            # Don't continue the auto_lose loop
            return
    
    # Continue checking if game is still active
    if 'app' in globals() and game_active:
        app.after(1500, auto_lose)

def restart_game():
    """Restart the game with fresh state"""
    global balance, inventory, loan_info, transaction_history, game_active
    
    # Reset all game state
    balance = 1000
    inventory = {}
    loan_info = {"amount": 0, "interest_rate": 0.0, "monthly_payment": 0, "remaining_payments": 0}
    transaction_history = []
    game_active = True
    
    # Clear save file
    try:
        os.remove("gambling_simulator_save.dill")
    except:
        pass
    
    # Clear the UI
    try:
        for widget in app.winfo_children():
            widget.destroy()
    except:
        pass
    
    # Recreate the main UI
    create_sidebar(buttons)
    
    global main_frame
    main_frame = customtkinter.CTkFrame(master=app,
                                       fg_color=("#F0F0F0", "#1A1A1A"),
                                       corner_radius=0)
    main_frame.pack(side="left", fill="both", expand=True)
    
    # Show casino and restart auto functions
    show_casino()
    auto_lose()
    auto_save()

show_casino()

auto_lose()

auto_save()

app.mainloop()