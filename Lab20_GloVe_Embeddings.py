# """
# GLOVE 50D EMBEDDINGS — COMPLETE HANDS-ON DEMO
# ==============================================

# Goal:
#     Learn word embeddings step-by-step and finally build
#     a small semantic FAQ search engine.

# Flow:
#     1. Load GloVe
#     2. Understand word vectors
#     3. Find similar words
#     4. Word analogy
#     5. Create sentence embeddings
#     6. Compare sentences
#     7. Build a semantic FAQ search engine
#     8. Add simple best practices

# Install:
#     pip install gensim numpy scikit-learn
# """

import re

import gensim.downloader as api
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# # ============================================================
# # STEP 1 — LOAD GLOVE
# # ============================================================

print("=" * 60)
print("STEP 1 — LOADING GLOVE")
print("=" * 60)

print("Loading GloVe 50D model...")

model = api.load("glove-wiki-gigaword-50")

print("Model loaded successfully!")
print("Vocabulary size:", len(model.index_to_key))
print("Vector size:", model.vector_size)


# ============================================================
# STEP 2 — WORD → VECTOR
# ============================================================

# print("\n" + "=" * 60)
# print("STEP 2 — WORD EMBEDDING")
# print("=" * 60)

# word = "computer"

# vector = model[word]

# print(f"\nWord: {word}")
# print("Embedding:")
# print(vector)

# print("\nNumber of dimensions:", len(vector))

# """
# A word is converted into a list of numbers.

# Example:

#     computer
#        ↓
#     [0.12, -0.42, 0.71, ...]
#        ↓
#     50 numbers

# This is called a WORD EMBEDDING.
# """


# # ============================================================
# # STEP 3 — SIMILAR WORDS
# # ============================================================

# print("\n" + "=" * 60)
# print("STEP 3 — FIND SIMILAR WORDS")
# print("=" * 60)

# word = "computer"

# print(f"\nWords similar to '{word}':")

# similar_words = model.most_similar(word, topn=5)

# for similar_word, score in similar_words:
#     print(f"{similar_word:15} {score:.4f}")

# """
# GloVe has learned relationships between words.

# For example:

#     computer
#        ↓
#     technology
#     software
#     computers
#     ...
# """


# # ============================================================
# # STEP 4 — WORD ANALOGY
# # ============================================================

# print("\n" + "=" * 60)
# print("STEP 4 — WORD ANALOGY")
# print("=" * 60)

# print("\nking - man + woman ≈ ?")


# results = model.most_similar(
#     positive=["king", "woman"],
#     negative=["man"],
#     topn=3
# )

# king_vector = model["king"]
# woman_vector = model["woman"]
# man_vector = model["man"]
# queen_vector = model["queen"]


# print("king_vector embedding:")
# print(king_vector)
# print()

# print("woman_vector embedding:")
# print(woman_vector)
# print()

# print("man_vector embedding:")
# print(man_vector)
# print()

# print("queen_vector embedding:")
# print(queen_vector)
# print()

# for word, score in results:
#     print(f"{word:15} {score:.4f}")

# """
# The idea:

#     king - man + woman
#             ↓
#           queen

# This shows that embeddings can capture relationships
# between words.
# """


# # ============================================================
# # STEP 5 — CLEAN TEXT
# # ============================================================

# print("\n" + "=" * 60)
# print("STEP 5 — TEXT PREPROCESSING")
# print("=" * 60)


def clean_text(text):
    """
    Basic text cleaning.

    - Convert to lowercase
    - Remove punctuation
    - Keep only words
    """

    text = text.lower()

    # Replace punctuation with spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# text = "How do I reset my Password?"

# print("Original :", text)
# print("Cleaned  :", clean_text(text))


# # ============================================================
# # STEP 6 — SENTENCE → VECTOR
# # ============================================================

# print("\n" + "=" * 60)
# print("STEP 6 — SENTENCE EMBEDDING")
# print("=" * 60)


def sentence_embedding(sentence):
    """
    Convert a sentence into one vector.

    Process:

        Sentence
            ↓
        Words
            ↓
        GloVe vectors
            ↓
        Average
            ↓
        One sentence vector
    """

    sentence = clean_text(sentence)

    words = sentence.split()

    vectors = []

    for word in words:

        if word in model:
            vectors.append(model[word])

    # No known words
    if not vectors:
        return None

    # Average all word vectors
    return np.mean(vectors, axis=0)


# sentence = "I love machine learning"

# vector = sentence_embedding(sentence)

# print("\nSentence:", sentence)
# print("Vector size:", len(vector))
# print("Sentence vector:")
# print(vector)


# # ============================================================
# # STEP 7 — SENTENCE SIMILARITY
# # ============================================================

# print("\n" + "=" * 60)
# print("STEP 7 — SENTENCE SIMILARITY")
# print("=" * 60)


def similarity(vector1, vector2):
    """
    Calculate cosine similarity between two vectors.
    """

    return cosine_similarity(
        [vector1],
        [vector2]
    )[0][0]


# sentence1 = "I love machine learning"
# sentence2 = "Artificial intelligence is amazing"
# sentence3 = "Pizza tastes delicious"

# vector1 = sentence_embedding(sentence1)
# vector2 = sentence_embedding(sentence2)
# vector3 = sentence_embedding(sentence3)

# score12 = similarity(vector1, vector2)
# score13 = similarity(vector1, vector3)

# print(f"\nSentence 1: {sentence1}")
# print(f"Sentence 2: {sentence2}")
# print(f"Similarity: {score12:.4f}")

# print(f"\nSentence 1: {sentence1}")
# print(f"Sentence 3: {sentence3}")
# print(f"Similarity: {score13:.4f}")

# """
# Higher score generally means more similar meaning.

# Example:

#     Sentence A
#          ↓
#       Vector A

#     Sentence B
#          ↓
#       Vector B

#           ↓
#     Cosine Similarity

#           ↓

#     Similarity Score
# """


# # ============================================================
# # STEP 8 — SIMPLE SEMANTIC SEARCH
# # ============================================================

# print("\n" + "=" * 60)
# print("STEP 8 — SEMANTIC SEARCH")
# print("=" * 60)

# documents = [
#     "How do I reset my password?",
#     "How can I track my order?",
#     "What is the refund policy?",
#     "How do I contact customer support?",
#     "How can I update my profile?"
# ]

# query = "I forgot my login password"

# query_vector = sentence_embedding(query)

# best_document = None
# best_score = -1

# for document in documents:

#     document_vector = sentence_embedding(document)

#     score = similarity(query_vector, document_vector)

#     print(f"\n{document}")
#     print(f"Score: {score:.4f}")

#     if score > best_score:
#         best_score = score
#         best_document = document

# print("\nBest Match:")
# print(best_document)
# print("Score:", round(best_score, 4))


# """
# We just created a very basic semantic search engine!

# Instead of searching for exact words:

#     "password"

# we compare the meaning of the complete sentences.
# """


# # ============================================================
# # STEP 9 — REAL-WORLD PROJECT
# #         SEMANTIC FAQ SEARCH ENGINE
# # ============================================================

print("\n" + "=" * 60)
print("STEP 9 — REAL-WORLD FAQ SEARCH ENGINE")
print("=" * 60)


# # ------------------------------------------------------------
# # FAQ DATABASE
# # ------------------------------------------------------------

faq_database = [
    {
        "question": "How do I reset my password?",
        "answer": "Go to Settings > Account > Reset Password."
    },
    {
        "question": "How can I track my order?",
        "answer": "Go to the Orders page and click Track Shipment."
    },
    {
        "question": "What is the refund policy?",
        "answer": "Refunds are available within 30 days of purchase."
    },
    {
        "question": "How do I contact customer support?",
        "answer": "Email support@example.com or call customer care."
    },
    {
        "question": "How can I update my profile?",
        "answer": "Go to Profile Settings and edit your details."
    }
]


# # ------------------------------------------------------------
# # PRECOMPUTE FAQ EMBEDDINGS
# # ------------------------------------------------------------

print("\nCreating FAQ embeddings...")

for faq in faq_database:

    faq["embedding"] = sentence_embedding(
        faq["question"]
    )

print("FAQ embeddings created!")


# # ------------------------------------------------------------
# # SEARCH FUNCTION
# # ------------------------------------------------------------

# def search_faq(user_query, faq_database):
#     """
#     Find the FAQ most semantically similar to the user query.
#     """

#     query_vector = sentence_embedding(user_query)

#     # User query contains no known words
#     if query_vector is None:
#         return None, None

#     best_match = None
#     best_score = -1

#     for faq in faq_database:

#         faq_vector = faq["embedding"]

#         # Safety check
#         if faq_vector is None:
#             continue

#         score = similarity(
#             query_vector,
#             faq_vector
#         )

#         if score > best_score:
#             best_score = score
#             best_match = faq

#     return best_match, best_score


# # ------------------------------------------------------------
# # TEST FAQ SEARCH
# # ------------------------------------------------------------

# test_queries = [
#     "I forgot my login password",
#     "Where is my shipment?",
#     "Can I get my money back?",
#     "I need help from customer service",
#     "I want to edit my account"
# ]

# print("\nTesting FAQ search:")

# for query in test_queries:

#     faq, score = search_faq(
#         query,
#         faq_database
#     )

#     print("\nUser:", query)

#     if faq is None:
#         print("No matching FAQ found.")
#         continue

#     print("Matched FAQ:", faq["question"])
#     print("Answer:", faq["answer"])
#     print("Similarity:", round(score, 4))


# # ============================================================
# # STEP 10 — ADD A MINIMUM SCORE
# # ============================================================

# print("\n" + "=" * 60)
# print("STEP 10 — MINIMUM SIMILARITY THRESHOLD")
# print("=" * 60)


def search_faq(
    user_query,
    faq_database,
    minimum_score=0.45
):
    """
    Search FAQs and reject very weak matches.

    This prevents the system from always returning
    some FAQ even when the question is unrelated.
    """

    query_vector = sentence_embedding(user_query)

    if query_vector is None:
        return None, None

    best_match = None
    best_score = -1

    for faq in faq_database:

        faq_vector = faq["embedding"]

        if faq_vector is None:
            continue

        score = similarity(
            query_vector,
            faq_vector
        )

        if score > best_score:
            best_score = score
            best_match = faq

    # No sufficiently good match
    if best_score < minimum_score:
        return None, best_score

    return best_match, best_score


# # ============================================================
# # STEP 11 — FINAL INTERACTIVE PROJECT
# # ============================================================

print("\n" + "=" * 60)
print("SEMANTIC FAQ SEARCH ENGINE")
print("=" * 60)

print("\nAsk a question.")
print("Type 'exit' to stop.")

while True:

    user_query = input("\nYou: ").strip()

    # Exit
    if user_query.lower() == "exit":
        print("Goodbye!")
        break

    # Empty input
    if not user_query:
        print("Please enter a question.")
        continue

    faq, score = search_faq(
        user_query,
        faq_database
    )

    # No good match
    if faq is None:

        print("\nSorry, I couldn't find a relevant FAQ.")

        if score is not None:
            print(
                "Best similarity:",
                round(score, 4)
            )

        continue

    # Display result
    print("\nBest Match")
    print("-" * 40)
    print("FAQ:", faq["question"])
    print("Answer:", faq["answer"])
    print("Similarity:", round(score, 4))
