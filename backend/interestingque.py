import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def ask_question(question, all_data, k, threshold, tfidf_vectorizer, tfidf_matrix):
    query_vect = tfidf_vectorizer.transform([question])
    similarity = cosine_similarity(query_vect, tfidf_matrix)[0]
    sim = [(similarity[i], i) for i in range(len(similarity))]
    sim.sort(reverse=True)
    # Use the top k results
    interesting, difficult = 0, 0
    for max_indices in range(k):
        max_index = sim[max_indices][1]
        max_sim = sim[max_indices][0]
        weight_diff = -1
        weight_interesting = -1
        if all_data.iloc[max_index]['Is the question difficult?'] == 'Yes':
            weight_diff = 1
        if all_data.iloc[max_index]['Is the question interesting?'] == 'Yes':
            weight_interesting = 1
        difficult += weight_diff * max_sim
        interesting += weight_interesting * max_sim

    result = {}

    if difficult >= threshold:
        result["difficulty"] = "Yes"
    else:
        result["difficulty"] = "No"

    if interesting >= threshold:
        result["interesting"] = "Yes"
    else:
        result["interesting"] = "No"

    return result

def interesting_questions(questions, df, tfidf_vectorizer, tfidf_matrix):
    diff, inter = 0, 0
    diffl, interl = [], []
    interesting_questions_list = []
    difficult_questions_list = []
    for question in questions:
        diffl.append(0)
        interl.append(0)
        response = ask_question(question, df, 1, 0, tfidf_vectorizer, tfidf_matrix)
        if response["difficulty"] == "Yes":
            diff += 1
            diffl[-1] = 1
            difficult_questions_list.append(question)
        if response["interesting"] == "Yes":
            inter += 1
            interl[-1] = 1
            interesting_questions_list.append(question)

    print("Interesting questions:")
    for idx, q in enumerate(interesting_questions_list):
        print(f"{idx + 1}. {q}")

    print("\nDifficult questions:")
    for idx, q in enumerate(difficult_questions_list):
        print(f"{idx + 1}. {q}")

    return [diff, inter, diffl, interl]

if __name__ == "__main__":
    # Example usage
    df = pd.DataFrame({
        'Question': ['How to ask question?', 'How to answer question?'],
        'Is the question difficult?': ['Yes', 'No'],
        'Is the question interesting?': ['Yes', 'Yes']
    })
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['Question'])

    questions_to_check = [
        'How to ask a good question?',
        'How to be a good listener?',
        'How to solve a difficult problem?'
    ]

    result = interesting_questions(questions_to_check, df, tfidf_vectorizer, tfidf_matrix)
    print("\nNumber of difficult questions:", result[0])
    print("Number of interesting questions:", result[1])
