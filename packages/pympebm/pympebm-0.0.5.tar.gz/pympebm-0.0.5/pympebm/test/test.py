from pympebm import run_ebm
from pympebm.data import get_sample_data_path, get_params_path
from pympebm.utils.runners import extract_fname
import os
import json 
import numpy as np 

cwd = os.getcwd()
print("Current Working Directory:", cwd)
data_dir = f"{cwd}/pympebm/test/my_data"
data_files = os.listdir(data_dir) 

OUTPUT_DIR = 'algo_results'

with open(f"{cwd}/pympebm/test/true_order_and_stages.json", "r") as f:
    true_order_and_stages = json.load(f)

# for algorithm in ['hard_kmeans', 'mle', 'conjugate_priors', 'em', 'kde']:
for algorithm in ['conjugate_priors']:
    for data_file in data_files:
        fname = data_file.replace('.csv', '')
        true_order_dict = true_order_and_stages[fname]['true_order']
        true_stages = true_order_and_stages[fname]['true_stages']
        try:
            order_array = true_order_and_stages[fname]['ordering_array']
        except:
            print('No order_array')
        
        rng = np.random.default_rng(53)
        random_num = rng.integers(5, 8)  # generate a random int between 5 and 7
        real_order = sorted(true_order_dict, key=lambda k: true_order_dict.get(k))
        order_array = [real_order[:random_num+1], real_order[random_num-1:]]

        results = run_ebm(
            order_array=order_array,
            data_file= os.path.join(data_dir, data_file),
            algorithm=algorithm,
            output_dir=OUTPUT_DIR,
            n_iter=200,
            n_shuffle=2,
            burn_in=10,
            thinning=1,
            true_order_dict=true_order_dict,
            true_stages = true_stages,
            skip_heatmap=False,
            skip_traceplot=False,
            mp_method='PL',
            seed = 53
        )