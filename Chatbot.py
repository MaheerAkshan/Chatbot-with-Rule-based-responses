import tkinter as tk
from tkinter import scrolledtext
import random
from datetime import datetime

class BuddyChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("buddy")
        self.root.geometry("600x700")
        self.root.configure(bg='#f5f5f5')
        
        # Configure fonts
        self.title_font = ("Arial", 16, "bold")
        self.user_font = ("Segoe UI", 11)
        self.bot_font = ("Georgia", 11)
        self.button_font = ("Arial", 10)
        
        # Weather data
        self.weather_data = {
            "chennai": {"temp": "72°F", "condition": "Sunny"},
            "london": {"temp": "58°F", "condition": "Cloudy"},
            "dubai": {"temp": "65°F", "condition": "Rainy"},
            "delhi": {"temp": "78°F", "condition": "Clear"},
            "paris": {"temp": "62°F", "condition": "Partly Cloudy"}
        }
        
        # Movie database
        self.movies = {
            "action": ["The Dark Knight", "Mad Max: Fury Road", "John Wick", "Inception", "The Matrix"],
            "comedy": ["Superbad", "The Hangover", "Step Brothers", "Bridesmaids", "Anchorman"],
            "drama": ["The Shawshank Redemption", "Forrest Gump", "The Godfather", "Schindler's List", "Fight Club"],
            "sci-fi": ["Interstellar", "Blade Runner 2049", "Arrival", "The Martian", "Ex Machina"],
            "horror": ["Get Out", "Hereditary", "The Conjuring", "A Quiet Place", "It Follows"]
        }
        
        # Conversation history
        self.chat_history = []
        self.bot_name = "buddy"
        self.typing_speed = random.uniform(0.05, 0.15)
        
        self.create_widgets()
        self.add_bot_message(self.get_random_greeting())
    
    def create_widgets(self):
        """Create all GUI elements"""
        main_frame = tk.Frame(self.root, bg='#f5f5f5')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(main_frame, bg='#f5f5f5')
        header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            header,
            text=f"Chat with {self.bot_name}",
            font=self.title_font,
            bg='#f5f5f5',
            fg='#333'
        ).pack(side=tk.LEFT)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=60,
            height=25,
            font=self.user_font,
            bg='white',
            fg='#333',
            padx=15,
            pady=15,
            relief=tk.FLAT
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.tag_config('user', foreground='#1a73e8', font=self.user_font)
        self.chat_display.tag_config('bot', foreground='#202124', font=self.bot_font)
        self.chat_display.tag_config('time', foreground='#666', font=("Arial", 8))
        self.chat_display.config(state=tk.DISABLED)
        
        # Input area
        input_frame = tk.Frame(main_frame, bg='#f5f5f5')
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.user_input = tk.Entry(
            input_frame,
            font=self.user_font,
            bg='white',
            relief=tk.FLAT,
            width=50
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.user_input.bind("<Return>", lambda e: self.process_input())
        
        tk.Button(
            input_frame,
            text="Send",
            command=self.process_input,
            font=self.button_font,
            bg='#4CAF50',
            fg='white',
            relief=tk.FLAT
        ).pack(side=tk.RIGHT)
        
        # Typing indicator
        self.typing_label = tk.Label(
            main_frame,
            text="",
            font=("Arial", 9, "italic"),
            bg='#f5f5f5',
            fg='#666'
        )
        self.typing_label.pack()
        self.typing_label.pack_forget()
    
    def get_random_greeting(self):
        """Return a random friendly greeting"""
        greetings = [
            "Hey there! What's up?",
            "Yo! How can I help you today?",
            "Hi friend! What's on your mind?",
            "Hey buddy! Need some help?",
            "Hello! How's it going?"
        ]
        return random.choice(greetings)
    
    def show_typing(self):
        """Show typing indicator"""
        self.typing_label.config(text=f"{self.bot_name} is typing...")
        self.typing_label.pack()
        self.root.update()
    
    def hide_typing(self):
        """Hide typing indicator"""
        self.typing_label.pack_forget()
    
    def process_input(self):
        """Process user input"""
        user_text = self.user_input.get().strip()
        if not user_text:
            return
        
        self.add_user_message(user_text)
        self.user_input.delete(0, tk.END)
        
        self.show_typing()
        delay = max(1, len(user_text) * self.typing_speed)
        self.root.after(int(delay * 1000), lambda: self.generate_response(user_text))
    
    def generate_response(self, user_input):
        """Generate a helpful response"""
        self.hide_typing()
        
        user_input = user_input.lower()
        response = ""
        
        # Weather queries
        if "weather" in user_input:
            city = self.extract_city(user_input)
            if city in self.weather_data:
                weather = self.weather_data[city]
                response = f"The weather in {city.title()} is {weather['condition']} with a temperature of {weather['temp']}"
            else:
                response = f"I don't have weather data for {city}. I know about: {', '.join(self.weather_data.keys())}"
        
        # Movie suggestions
        elif any(word in user_input for word in ["movie", "film", "suggest"]):
            genre = self.extract_genre(user_input)
            if genre in self.movies:
                movie = random.choice(self.movies[genre])
                response = f"I recommend watching '{movie}' (a great {genre} movie!)"
            else:
                response = (f"I don't recognize that genre. I can suggest movies from these genres: "
                          f"{', '.join(self.movies.keys())}. Try 'suggest a comedy movie'")
        
        # Time questions
        elif any(word in user_input for word in ["time", "clock"]):
            current_time = datetime.now().strftime("%I:%M %p")
            responses = [
                f"Right now it's {current_time}",
                f"My watch says {current_time}",
                f"Looks like it's about {current_time}"
            ]
            response = random.choice(responses)
        
        # Date questions
        elif any(word in user_input for word in ["date", "today"]):
            current_date = datetime.now().strftime("%B %d, %Y")
            responses = [
                f"Today is {current_date}",
                f"It's {current_date} today",
                f"The date is {current_date}"
            ]
            response = random.choice(responses)
        
        # Help requests
        elif any(word in user_input for word in ["help", "support"]):
            response = ("I can help with:\n"
                       "- Weather information (try 'weather in London')\n"
                       "- Movie suggestions (try 'suggest a comedy movie')\n"
                       "- Time and date information\n"
                       "- General conversation")
        
        # Greetings
        elif any(word in user_input for word in ["hi", "hello", "hey"]):
            response = self.get_random_greeting()
        
        # Farewells
        elif any(word in user_input for word in ["bye", "thanks"]):
            responses = ["See you later!", "Bye! Come back anytime", "Take care!"]
            response = random.choice(responses)
        
        # Default response
        else:
            responses = [
                "I'm not sure I understand. Can you explain?",
                "Could you rephrase that?",
                "I didn't quite get that. Ask me something else?"
            ]
            response = random.choice(responses)
        
        self.add_bot_message(response)
    
    def extract_city(self, text):
        """Extract city name from weather queries"""
        for city in self.weather_data.keys():
            if city in text:
                return city
        return text.replace("weather", "").replace("in", "").strip() or "unknown"
    
    def extract_genre(self, text):
        """Extract genre from movie queries"""
        for genre in self.movies.keys():
            if genre in text:
                return genre
        return text.replace("movie", "").replace("film", "").replace("suggest", "").strip() or "unknown"
    
    def add_user_message(self, text):
        """Add user message to chat"""
        timestamp = datetime.now().strftime("%I:%M %p")
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'time')
        self.chat_display.insert(tk.END, f"You: {text}\n\n", 'user')
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        self.chat_history.append(('user', text))
    
    def add_bot_message(self, text):
        """Add bot message to chat"""
        timestamp = datetime.now().strftime("%I:%M %p")
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'time')
        self.chat_display.insert(tk.END, f"{self.bot_name}: {text}\n\n", 'bot')
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        self.chat_history.append(('bot', text))

if __name__ == "__main__":
    root = tk.Tk()
    app = BuddyChatbot(root)
    root.mainloop()
