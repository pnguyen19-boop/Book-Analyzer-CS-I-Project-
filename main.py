"""
Concepts We Are Practicing:
- Functions
- Loops and Menu-Driven Programs
- Lists and Data Filtering
- Dictionaries
- Counter (from collections)

Modules and Libraries:
- API Requests (requests)
- Text Processing (re - regular expressions)
"""

"""
Author: Your Name
GitHub Link: https://github.com/your-username/your-repo
Project: Book Analyzer (CS I Project)
Extra credit: I implemeted a new feature: 
                                            - Added word search feature
                                            - Improved visualization with scaled bar chart
                                            - Implemented advanced error handling for network issues
"""

import requests
import re
from collections import Counter


# -----------------------------
# INITIAL DATA
# -----------------------------

my_library = {
    "Moby Dick": "https://www.gutenberg.org/files/2701/2701-0.txt"
}

# TODO 3: Read stop words from a file instead; this file "EN-Stopwords" contains thousands stop words(2 points)
STOP_WORDS = set()

try:
    with open("EN-Stopwords.txt", "r") as file:
        for line in file:
            word = line.strip().lower()
            if word:
                STOP_WORDS.add(word)
except FileNotFoundError:
    print("Warning: Stopwords file not found. Using empty stopword list.")

# -----------------------------
# FETCH BOOK
# -----------------------------
def fetch_book(url):
    """Download text from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
        return None

    except requests.exceptions.ConnectionError:
        print("Error: No internet connection.")
        return None

    except requests.exceptions.InvalidURL:
        print("Error: Invalid URL.")
        return None

    except requests.exceptions.RequestException:
        print("Error: Could not download book.")
        return None

# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(raw_text):
    """Lowercase text and remove punctuation."""
    text = raw_text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text.split()

# -----------------------------
# ANALYZE TEXT
# -----------------------------
def analyze_text(words):
    """Remove stop words and count frequencies."""
    filtered_words = [] 
    for w in words: 
        if w not in STOP_WORDS and len(w) > 2:   #checking len(w)> 2 to remove tiny words((is, to, at))
            filtered_words.append(w)

    return Counter(filtered_words).most_common(10)



# -----------------------------
# VISUALIZATION (BAR CHART)
# -----------------------------
# TODO 5: Implement the following function (2 points)
# hints: use print() statements to create a horizontal bar chart using the "█" or "*" character.
def plot_results(stats, title):
    """Create a bar chart of word frequencies."""
    short_title = title.split()[0].lower()

    print(f"\n--- Top 10 Words in {short_title} ---\n")

    if not stats:
        print("No words to display.")
        return

    max_count = stats[0][1]

    for word, count in stats:
        bar = "█" * int((count / max_count) * 40)
        print(f"{word:<12} | {bar:<40} ({count})") 


def search_word_in_book(words):
    """Search for a word and count how many times it appears."""
    search_word = input("Enter word to search: ").strip().lower()

    if search_word == "":
        print("Error: Search word cannot be empty.")
        return

    word_counts = Counter(words)
    count = word_counts[search_word]

    print(f"'{search_word}' appears {count} time(s).")


def main():
    while True:
        print("\n--- LIBRARY MANAGER ---")
        print(f"Current Books: {list(my_library.keys())}")
        print("1. Add New Book")
        print("2. Remove Book")
        print("3. Update Book URL")
        print("4. Analyze a Book")
        print("5. Search Word in a Book")
        print("6. Exit")
        choice = input("\nSelect (1-6): ")

        if choice == '1':
            # Add new books to the dictionary (use this website: https://www.gutenberg.org/browse/scores/top)
            # TODO 1.1: Normalize input by removing extra spaces and ignoring case.
                # (e.g., " The Hobbit " (with space) and "the hobbit" should be treated as the same book.) (1 point)
            name = input("Enter Book Title: ").strip()
            url = input("Enter Gutenberg .txt URL: ").strip()

            
            if name == "" or url == "":
                print("Error: Book title or URL cannot be empty.")
                continue

           
            normalized = name.lower()
            for k in my_library:
                if k.lower() == normalized:
                    print(f"Error: '{name}' already exists in the library.")
                    break
            else:
                name = name.title()  # normalize format
                my_library[name] = url
                print(f"'{name}' added.")

        elif choice == '2':
            # Remove books from the dictionary
            #TODO 2.1: Handle missing books—check if the title exists before trying to delete it.(1 point)
            #TODO 2.2: Make the removal case-insensitive so "The Hobbit" matches "the hobbit".(1 point)
            # Hint: Use .strip().lower() to normalize the user's input!
            name = input("Enter title to remove: ").strip().lower()

           
            target_key = None
            for k in my_library:
                if k.lower() == name:
                    target_key = k
                    break

            if target_key:
                del my_library[target_key]
                print(f"'{target_key}' removed.")
            else:
                print("Book not found.")
            
            

        elif choice == '3':
            # UPDATE OPERATION
            name_input = input("Enter the book title to update: ").strip().lower()
            target_key = None  # Start with None in case we don't find it

            for k in my_library:
                if k.lower() == name_input:
                    target_key = k
                    break  # We found it, so stop looking

            if target_key:
                print(f"Current URL: {my_library[target_key]}")
                new_url = input("Enter new URL: ").strip()
                if new_url == "":
                    print("Invalid URL. Update cancelled.")
                else:
                    my_library[target_key] = new_url
                    print(f"'{target_key}' updated successfully.")
            else:
                print("Book not found.")

        elif choice == '4':
            name_input = input("Which book to analyze? ").strip().lower()
            
            target_key = None
            for k in my_library:
                if k.lower() == name_input:
                    target_key = k
                    break

            if target_key:
                url = my_library[target_key]
                print(f"Fetching and analyzing '{target_key}'...")
                raw_text = fetch_book(url)

                if raw_text:
                    words = clean_text(raw_text)
                    stats = analyze_text(words)
                    print(f"Total words in book: {len(words)}")
                    plot_results(stats, target_key)
            else:
                print("Error: Book not found.")

        elif choice == '5':
            name_input = input("Which book to search? ").strip().lower()

            target_key = None
            for k in my_library:
                if k.lower() == name_input:
                    target_key = k
                    break

            if target_key:
                url = my_library[target_key]
                print(f"Downloading and searching {target_key.split()[0].lower()}...")

                raw_text = fetch_book(url)

                if raw_text:
                    words = clean_text(raw_text)
                    search_word_in_book(words)
            else:
                print("Error: Book not found.")

        elif choice == '6':
            print("Goodbye!")
            break



if __name__ == "__main__":
    main()