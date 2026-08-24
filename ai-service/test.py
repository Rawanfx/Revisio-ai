from Services.retrieval import retrieve_context_for_question

result = retrieve_context_for_question("lec_001", "ما هو قانون نيوتن الثاني؟", 5)
print(result)