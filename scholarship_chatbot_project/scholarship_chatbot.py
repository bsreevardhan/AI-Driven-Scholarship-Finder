import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load your dataset
df = pd.read_csv(r'd:\miniproj\scholarship_chatbot_project\structured_scholarships wo Desired.csv')

print("Available columns:", df.columns.tolist())

# Fun fallback responses
fallback_jokes_facts = [
    "Did you know? The first computer bug was an actual moth stuck in a Harvard Mark II computer in 1947.",
    "Fun fact: Honey never spoils. Archaeologists have found 3,000-year-old honey in Egyptian tombs that’s still edible!",
    "Joke: Why don’t scientists trust atoms? Because they make up everything!",
    "Did you know? Bananas are berries, but strawberries aren’t.",
    "Joke: Why was the math book sad? Because it had too many problems."
]

def get_random_joke_or_fact():
    return random.choice(fallback_jokes_facts)

# Prepare TF-IDF once at startup
vectorizer = TfidfVectorizer(stop_words='english')
vectors = vectorizer.fit_transform(df['Name'].astype(str))

# Main chatbot function
def chatbot(query):
    query_lower = query.lower().strip()

    # Check for greetings
    greetings = ['hi', 'hello', 'how are you', 'hey', 'good morning', 'good evening']
    if query_lower in greetings:
        return "Hi there! I’m your scholarship assistant bot. Ask me about deadlines, awards, income eligibility, qualifications, and more."

    # Check similarity to scholarship names
    query_vector = vectorizer.transform([query])
    cosine_sim = cosine_similarity(query_vector, vectors)
    idx = cosine_sim.argmax()
    score = cosine_sim[0, idx]

    # Threshold to consider a valid match
    if score < 0.1:
        return f"That’s an interesting question! But I’m focused on scholarships. Here’s something fun instead:\n\n{get_random_joke_or_fact()}"

    matched_scholarship = df.iloc[idx]

    # Scholarship-related keywords
    if 'deadline' in query_lower or 'last date' in query_lower:
        return f"Deadline for '{matched_scholarship['Name']}' is: {matched_scholarship['Application Deadline']}"
    elif 'award' in query_lower or 'amount' in query_lower or 'how much' in query_lower:
        return f"Award amount for '{matched_scholarship['Name']}' is: {matched_scholarship['Award Amount']}"
    elif 'income' in query_lower or 'family income' in query_lower:
        return f"Income eligibility for '{matched_scholarship['Name']}' is: {matched_scholarship['Income Eligibility']}"
    elif 'qualification' in query_lower or 'requirement' in query_lower:
        return f"Qualification required for '{matched_scholarship['Name']}' is: {matched_scholarship['Qualification']}"
    elif 'state' in query_lower:
        return f"Eligible states for '{matched_scholarship['Name']}' are: {matched_scholarship['State']}"
    elif 'category' in query_lower:
        return f"Category for '{matched_scholarship['Name']}' is: {matched_scholarship.get('Category', 'Not available')}"
    elif 'registration' in query_lower or 'link' in query_lower or 'apply' in query_lower:
        return f"Registration link for '{matched_scholarship['Name']}' is: {matched_scholarship['Registration Link']}"
    else:
        # Default summary if no specific keyword but matched
        return (
            f"Here's what I found about '{matched_scholarship['Name']}':\n"
            f"- Description: {matched_scholarship['Description']}\n"
            f"- Income Eligibility: {matched_scholarship['Income Eligibility']}\n"
            f"- Qualification: {matched_scholarship['Qualification']}\n"
            f"- Deadline: {matched_scholarship['Application Deadline']}\n"
            f"- Registration Link: {matched_scholarship['Registration Link']}"
        )

# Main chatbot loop
if __name__ == "__main__":
    print("Welcome to the Scholarship Chatbot! Type 'exit' to end.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Bot: Goodbye! Best of luck with your scholarship applications!")
            break
        response = chatbot(user_input)
        print(f"Bot: {response}\n")
