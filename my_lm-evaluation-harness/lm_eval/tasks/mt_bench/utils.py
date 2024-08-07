import copy
import pickle
step_one_results_fname="mt_bench_step1_results.pickle"
step_two_results_fname="mt_bench_step2_results.pickle"
default_step1_template = """A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: {instruction} ASSISTANT:"""
default_step2_template="USER: {instruction} ASSISTANT:"
def doc_to_text1(doc):
    template = default_step1_template
    return template.replace('{instruction}', doc['turns'][0])
def doc_to_target(doc):
    return ""
def process_results1(doc,generations):
    try:
        with open(step_one_results_fname, 'rb') as handle:
            step_one_results = pickle.load(handle)
    except:
        step_one_results = dict()
    key = doc['question_id']
    step_one_results[key] = generations[0]
    with open(step_one_results_fname, 'wb') as handle:
        pickle.dump(step_one_results, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return {'acc':0}

def doc_to_text2(doc):
    try:
        with open(step_one_results_fname, 'rb') as handle:
                step_one_results = pickle.load(handle)
    except:
         raise Exception(f"{step_one_results_fname} was not found.")
    
    template2 = default_step2_template
    step_one_prompt = doc_to_text1(doc)

    key = doc['question_id']
    step_1_result = step_one_results[key]
    step_2_prompt = template2.replace('{instruction}', doc['turns'][1])
    
    return f"{step_one_prompt} {step_1_result} {step_2_prompt}"

def process_results2(doc, generations):
    try:
        with open(step_two_results_fname, 'rb') as handle:
            step_two_results = pickle.load(handle)
    except:
        step_two_results = dict()
    key = doc['question_id']
    step_two_results[key] = generations[0]
    with open(step_two_results_fname, 'wb') as handle:
        pickle.dump(step_two_results, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return {'acc':0}