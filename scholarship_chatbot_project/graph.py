import pandas as pd
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Sample scholarship dataset
data = {
    'Name': ['Scholarship A', 'Scholarship B', 'Scholarship C', 'Scholarship D'],
    'Income Eligibility': [200000, 300000, 150000, 500000],
    'Minimum Qualification': ['UG', 'UG', 'PG', 'UG'],
    'Category': ['SC', 'OBC', 'ST', 'General'],
    'Qualification': ['UG', 'UG', 'PG', 'UG'],
    'Description': [
        'Merit-based scholarship for SC students pursuing engineering.',
        'Financial aid for OBC category undergraduate science students.',
        'Support for ST category postgraduates in social sciences.',
        'Scholarship for general category students in computer science.'
    ]
}
df = pd.DataFrame(data)

# Simulated user profile
user_profile = {
    'income': 250000,
    'qualification': 'UG',
    'cgpa': 8.0,
    'category': 'OBC',
    'interests': 'undergraduate student interested in science and financial aid'
}

# --- Stage 1: Hard Filtering ---
def hard_filter(row, user):
    return (user['income'] <= row['Income Eligibility']) and \
           (row['Minimum Qualification'] == user['qualification']) and \
           (row['Category'].lower() == user['category'].lower())

filtered_df = df[df.apply(lambda row: hard_filter(row, user_profile), axis=1)].reset_index(drop=True)

# Graph 1: Scholarships before vs after filtering
plt.figure(figsize=(6, 4))
plt.bar(['Before Filtering', 'After Filtering'], [len(df), len(filtered_df)], color=['red', 'green'])
plt.title('Scholarships Before vs After Hard Filtering')
plt.ylabel('Number of Scholarships')
plt.tight_layout()
plt.show()

# --- Stage 2: Semantic Similarity Ranking ---
model = SentenceTransformer('all-MiniLM-L6-v2')

# Prepare text blocks
user_text = user_profile['interests']
scholarship_texts = filtered_df['Description'].tolist()

# Encode and calculate cosine similarity
user_embedding = model.encode(user_text, convert_to_tensor=True)
scholarship_embeddings = model.encode(scholarship_texts, convert_to_tensor=True)
cosine_scores = util.cos_sim(user_embedding, scholarship_embeddings)[0].cpu().tolist()

filtered_df['Similarity Score'] = cosine_scores
filtered_df = filtered_df.sort_values(by='Similarity Score', ascending=False).reset_index(drop=True)

# Enhanced Graph 2: Horizontal bar chart with color and annotations
colors = plt.cm.viridis(np.linspace(0.3, 1, len(filtered_df)))

plt.figure(figsize=(8, 5))
bars = plt.barh(filtered_df['Name'], filtered_df['Similarity Score'], color=colors)
plt.xlabel('Cosine Similarity')
plt.title('Semantic Similarity Between User Profile and Scholarships')
plt.xlim(0, 1)
plt.gca().invert_yaxis()

# Annotate each bar with score
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.02, bar.get_y() + bar.get_height()/2,
             f'{width:.2f}', va='center', fontsize=9, weight='bold')

plt.tight_layout()
plt.show()
