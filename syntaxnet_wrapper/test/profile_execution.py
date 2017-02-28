from syntaxnet_wrapper.wrapper import SyntaxNetWrapper

from time import time
from prettytable import PrettyTable

def profile_exec(niter, action, keep_wrapper):
    t = time()
    sentence = 'une phrase de test'

    for i in range(niter):
	if keep_wrapper == False or i == 0:
	    sn_wrapper = SyntaxNetWrapper('French')
	
	if action == 'morpho':
	    sn_wrapper.morpho_sentence(sentence)
	elif action == 'tagger':
	    sn_wrapper.tag_sentence(sentence)
	elif action == 'parser':
	    sn_wrapper.parse_sentence(sentence)

    del sn_wrapper
    return time() - t
          

x = PrettyTable(['Action', 'niter', 'keep wrapper', 'execution_time'])

# Describe test case
test_cases = [
	{'action': 'morpho', 'niter': 1, 'keep_wrapper': False},
	{'action': 'morpho', 'niter': 10, 'keep_wrapper': True},
	#{'action': 'morpho', 'niter': 100, 'keep_wrapper': True},
	#{'action': 'morpho', 'niter': 1000, 'keep_wrapper': True},
	{'action': 'tagger', 'niter': 1, 'keep_wrapper': True},
	#{'action': 'tagger', 'niter': 10, 'keep_wrapper': True},
	#{'action': 'tagger', 'niter': 100, 'keep_wrapper': True},
	#{'action': 'tagger', 'niter': 1000, 'keep_wrapper': True},
	{'action': 'parser', 'niter': 1, 'keep_wrapper': True},
	#{'action': 'parser', 'niter': 10, 'keep_wrapper': True},
	#{'action': 'parser', 'niter': 100, 'keep_wrapper': True},
	#{'action': 'parser', 'niter': 1000, 'keep_wrapper': True},
	{'action': 'morpho', 'niter': 1, 'keep_wrapper': False},
	#{'action': 'morpho', 'niter': 10, 'keep_wrapper': False},
	#{'action': 'morpho', 'niter': 100, 'keep_wrapper': False},
	#{'action': 'morpho', 'niter': 1000, 'keep_wrapper': False},
	{'action': 'tagger', 'niter': 1, 'keep_wrapper': False},
	#{'action': 'tagger', 'niter': 10, 'keep_wrapper': False},
	#{'action': 'tagger', 'niter': 100, 'keep_wrapper': False},
	#{'action': 'tagger', 'niter': 1000, 'keep_wrapper': False},
	{'action': 'parser', 'niter': 1, 'keep_wrapper': False},
	#{'action': 'parser', 'niter': 10, 'keep_wrapper': False},
	#{'action': 'parser', 'niter': 100, 'keep_wrapper': False},
	#{'action': 'parser', 'niter': 1000, 'keep_wrapper': False},
]

for test_case in test_cases:
    exec_time = profile_exec(**test_case)
    x.add_row([test_case['action'],
	       test_case['niter'],
               test_case['keep_wrapper'],
               exec_time])
with open('output_profiling.txt', 'wb') as file_:
    file_.write(x.get_string())


