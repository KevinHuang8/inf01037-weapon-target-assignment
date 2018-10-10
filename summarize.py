import os
import statistics

results = os.listdir('results')

def summarize(instance, results):
    if instance <= 4:
        max_iterations = 20
    elif instance <= 8:
        max_iterations = 125
    else:
        max_iterations = 200

    solutions = []
    for result in results:
        params = {}
        for pair in [p for p in result[:-4].split('-')]:
            k, v = pair.split('=')
            params[k] = v

        if int(params['max_iterations']) == max_iterations and params['instance_file'] == 'data_WTA'+str(instance) and int(params['seed']) <= 4 and params['population_size'] == str(instance*250) and params['mutation_probability'] == '0.5':
            with open('results/'+result) as file:
                solutions.append(-float(file.readline()))

    return solutions

for instance in range(1, 13):
    solutions = summarize(instance, results)
    mean = statistics.mean(solutions)
    stdev = statistics.stdev(solutions)
    m = min(solutions)
    M = max(solutions)
    print instance, mean, stdev, M, m
