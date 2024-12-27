import pandas as pd
import requests
import time

import unicodedata

# Load the test set
test_set_path = "test_set.xlsx"  # Replace with your test set path
test_set = pd.read_excel(test_set_path)
test_set_1 = test_set[:25000]
test_set_2= test_set[25000:]
def remove_vietnamese_tones(text):
    text=str(text)
    tmp = ''.join(
        char for char in unicodedata.normalize('NFD', text)
        if unicodedata.category(char) != 'Mn'
    )
    tmp =tmp.replace("đ","d")
    return tmp

test_set_2['Query'] = test_set_2['Query'].apply(remove_vietnamese_tones)
combined_test_set = pd.concat([test_set_1, test_set_2])

# URL of your search API
api_url = "http://127.0.0.1:5000/search"  # Replace with your deployed API URL

# Function to test the search API and calculate metrics
def test_search_api(test_set, top_k_values=[1, 5, 10]):
    results = []
    total_queries = len(test_set)  # Total number of queries
    reciprocal_ranks = []  # For MRR calculation
    top_k_accuracies = {k: [] for k in top_k_values}  # To track Top-K accuracy for different values of K

    for i, row in test_set.iterrows():
        title = row['Title']
        query = row['Query']
        start_time = time.time()
        response = requests.get(api_url, params={'query': query, 'size': max(top_k_values)})  # Fetch results for max K
        elapsed_time = time.time() - start_time

        matched = False  # Default to no match
        returned_titles = []  # To store titles from the search results

        if response.status_code == 200:
            search_results = response.json()
            returned_titles = [result['title'] for result in search_results]  # Extract titles
            # Calculate if the correct title is within Top-K results
            for k in top_k_values:
                matched_k = any(result['title'] == title for result in search_results[:k])
                top_k_accuracies[k].append(1 if matched_k else 0)

            # Check if the correct title is matched in any result
            matched = any(result['title'] == title for result in search_results)

            # Calculate Reciprocal Rank (1/rank of the correct result, or 0 if not found)
            rank = next((idx + 1 for idx, result in enumerate(search_results) if result['title'] == title), None)
            reciprocal_rank = 1 / rank if rank else 0
            reciprocal_ranks.append(reciprocal_rank)
        else:
            # Handle failed requests
            for k in top_k_values:
                top_k_accuracies[k].append(0)
            reciprocal_ranks.append(0)

        results.append({
            'Title': title,
            'Query': query,
            'Matched': matched,
            'Returned Titles': returned_titles,
            'Time (s)': elapsed_time
        })
        print(f"Query {i + 1}/{total_queries}: '{query}' -> Matched: {matched} (Time: {elapsed_time:.2f} seconds)")

    # Calculate overall metrics
    top_k_accuracy_scores = {k: sum(top_k_accuracies[k]) / total_queries for k in top_k_values}
    mean_reciprocal_rank = sum(reciprocal_ranks) / total_queries

    print("\nMetrics Summary:")
    for k, score in top_k_accuracy_scores.items():
        print(f"Top-{k} Accuracy: {score:.2f}")
    print(f"Mean Reciprocal Rank (MRR): {mean_reciprocal_rank:.2f}")

    return pd.DataFrame(results), top_k_accuracy_scores, mean_reciprocal_rank

# Run the tests
test_results, top_k_accuracy_scores, mean_reciprocal_rank = test_search_api(combined_test_set, top_k_values=[1, 5, 10])


