import copy
import pickle
flask_results_fname="flask_results.pickle"
default_step1_template = """A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: {instruction} ASSISTANT:"""
def doc_to_text(doc):
    template = default_step1_template
    return template.replace('{instruction}', doc['instruction'])
def doc_to_target(doc):
    return ""
def process_results(doc,generations):
    try:
        with open(flask_results_fname, 'rb') as handle:
            flask_results = pickle.load(handle)
    except:
        flask_results = dict()
    key = doc['idx']
    flask_results[key] = generations[0]
    with open(flask_results_fname, 'wb') as handle:
        pickle.dump(flask_results, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return {'acc':0}
