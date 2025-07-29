from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import evaluate
import numpy as np
import shutil
import os
import torch
import pandas as pd
import numpy as np
np.random.seed(2025)

def optimize_flan_t5_small(prompts, references, params={}, error_metric='ROUGE-L',
                           number_of_generation = 3, mutation_rate=0.05, population_size=10, random_seed=2025):

  try:
      generation_args = []

      if 'max_length' in params.keys():
          generation_args.append(params['max_length'])
      else:
          generation_args.append([50,100,150,200,250,300])

      if 'temperature' in params.keys():
          generation_args.append(params['temperature'])
      else:
          generation_args.append([0.2,0.4,0.6,0.8])

      if 'top_k' in params.keys():
          generation_args.append(params['top_k'])
      else:
          generation_args.append([10,20,30,40,50])

      if 'top_p' in params.keys():
          generation_args.append(params['top_p'])
      else:
          generation_args.append([0.3,0.5,0.7,0.9])

      obj = optimizer()

      generation_args = obj.best_estimator(prompts, references, generation_args, error_metric, population_size, number_of_generation, mutation_rate, random_seed)

      return generation_args[0]

  except Exception as e:
      print(e)


class optimizer():
    def best_estimator(self, prompts, references, generation_args, error_metric, population_size,
                       number_of_generation, mutation_rate, random_seed):

        # -----------------------------------------   Parameter Assertions   -----------------------------------------

        assert type(prompts) is list, 'x_train must be a List'
        assert type(references) is list, 'x_train must be a List'
        assert type(population_size) is int and population_size > 0, 'Population size must be a positive integer.'
        assert population_size % 2 == 0, 'Population size must be even.'
        assert type(number_of_generation) is int and number_of_generation > 0, \
            'Number of generations must be a non-negative integer.'
        assert type(mutation_rate) is float and 0.0 <= mutation_rate <= 1.0, \
            'Mutation rate must be a float between 0.0 and 1.0.'

        model_name = "google/flan-t5-small"  # or your fine-tuned path
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        model.eval()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)

        inputs = tokenizer(
                  prompts,
                  return_tensors="pt",
                  padding=True,
                  truncation=True,
                  max_length=512
              )

        inputs = {k: v.to(device) for k, v in inputs.items()}

        # --------------------------------------------   Model function   --------------------------------------------
        objective_function = lambda i: self.objective(model_name, i, error_metric, model, inputs, references, random_seed=random_seed)
        # ------------------------------------------------------------------------------------------------------------

        population = pd.DataFrame()
        np.random.seed(random_seed)
        population['max_length'] = np.random.choice(generation_args[0], size=population_size)
        population['temperature'] = np.random.choice(generation_args[1], size=population_size)
        population['top_k'] = np.random.choice(generation_args[2], size=population_size)
        population['top_p'] = np.random.choice(generation_args[3], size=population_size)
        population['score'] = population.apply(objective_function, axis=1)

        for g in range(number_of_generation):
            # Pair the population for breeding
            pairs = self.match(population, random_seed)

            # Generate the children
            children = self.crossover(pairs, random_seed)
            if 'score' in children.columns:
                children.drop('score', axis=1, inplace=True)

            # Generate the mutants
            mutants = self.mutate(children, mutation_rate, generation_args, random_seed)

            # Collect the population removing any duplicates.
            population = pd.concat([population, children]).drop_duplicates(subset=children.columns)
            population = pd.concat([population, mutants]).drop_duplicates(subset=children.columns)

            #population = population.append([children, mutants], ignore_index=True, sort=False).drop_duplicates(subset=children.columns)

            # Score the population, sort it, and terminate the bottom
            population.loc[:, error_metric] = population.apply(objective_function, axis=1)
            population = population.sort_values(by=['score'], ascending=False).iloc[:population_size]

        output_params = population.iloc[0]
        output_params[error_metric] = round(output_params['score'], 2)
        output_params.drop('score', inplace=True)

        return [self.get_generation_args(population.loc[population[error_metric].idxmax()])]

    def match(self, population, random_seed):
        '''
        Samples from population with higher scores having higher probability of selection.
        '''

        np.random.seed(random_seed)
        length = population.shape[0]
        prob = population['score'] / population['score'].sum()

        indices = np.random.choice(np.arange(length), p=prob, size=length)
        return population.iloc[indices]

    def crossover(self, pairs, random_seed):
        '''
        Performs a random crossover with the entire population as an input.
        '''
        np.random.seed(random_seed)
        length, width = pairs.shape
        width -= 1

        # i is an array which maps indices randomly either to themselves or their pair.
        a = np.random.choice((0, 1), size=length * width)
        a[np.arange(1, length * width, 2)] *= -1
        i = np.arange(length * width) + a

        # Convert the population to a list of genes, and map each gene to itself or its pair using i.
        gene_list = np.array(pairs.drop('score', axis=1)).reshape(-1, order='F')
        return pd.DataFrame(gene_list[i].reshape((-1, width), order='F'), columns=pairs.columns[:-1])


    def mutate(self, population, mutation_rate, rf_parameters, random_seed):
        '''
        Mutate the population with a given mutation rate.
        '''

        length, width = population.shape
        np.random.seed(random_seed)

        pop_array = np.array(population).reshape(-1, order='F')

        # List of all the indices in the 1d gene array which should be changed.
        change_indices = np.random.choice(
            np.arange(length * width),
            size=int(mutation_rate * length * width),
            replace=False
        )

        # Get a list new_values that contains random values for the corresponding index in mut_array.
        change_indices.sort()
        c = [np.random.choice(rf_parameters[i], size=np.logical_and
            (i * length <= change_indices, change_indices < (i + 1) * length).sum()) for i in range(width)]
        new_values = np.concatenate(c)

        # Set the values in the population array at the change indices to the new values.
        pop_array[change_indices] = new_values
        mutants = pd.DataFrame(pop_array.reshape((-1, width), order='F'))
        mutants.columns = population.columns

        return mutants

    def get_generation_args(self, row, random_seed = 2025):
        '''
        Return the model specified by the given row.
        '''

        return {
            "max_length": int(row[0]),
            "temperature": row[1],
            "top_k": int(row[2]),
            "top_p": row[3],
            "do_sample": True,       # Enables sampling-based decoding
            "num_beams": 1           # Beam search disabled (greedy/sample)
        }


    def get_mape(self, model, inputs, references, error_metric, generation_args, model_name):
        # ✅ Generate predictions

        with torch.no_grad():
            outputs = model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                **generation_args
            )

        # Decode predictions
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        decoded_preds = tokenizer.batch_decode(outputs, skip_special_tokens=True)

        rouge = evaluate.load("rouge")
        result = rouge.compute(predictions=decoded_preds, references=references, use_stemmer=True)

        if error_metric == 'ROUGE-L':
          mp = round(result['rougeL'] * 100, 2)
          print(mp)

        elif error_metric == 'ROUGE-1':
          mp = round(result['rouge1'] * 100, 2)
          print(mp)

        elif error_metric == 'ROUGE-2':
          mp = round(result['rouge2'] * 100, 2)
          print(mp)

        elif error_metric == 'ROUGE-Lsum':
          mp = round(result['rougeLsum'] * 100, 2)
          print(mp)

        else:
            mp = 0
        return mp

    def objective(self, model_name, row, error_metric, model, inputs, references, random_seed):
        '''
        Returns the inverse of the MAPE of the model described by a row.
        '''

        if 'score' in row and row['score'] == row['score']:  # row[error_metric] == row[error_metric]
            return row['score']  # checks that row[error_metric] is not NaN.

        return self.get_mape(model, inputs, references, error_metric, self.get_generation_args(row, random_seed=random_seed),model_name)
