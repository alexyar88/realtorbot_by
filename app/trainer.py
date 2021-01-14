import os
import pickle

import dataset
import pipeline


def run_training(csv_dir, model_dir):
    X, y = dataset.get_X_y(csv_dir)
    training_pipeline = pipeline.build()
    training_pipeline.fit(X, y)

    with open(os.path.join(model_dir, 'pipeline.pkl'), 'wb') as file:
        pickle.dump(training_pipeline, file)


if __name__ == "__main__":
    print(os.path.abspath(os.getcwd()))
    run_training('../../mounted/data', '../../mounted/model')
    # raise NotImplementedError()
