import tensorflow as tf
import numpy as np
import json
import pandas as pd
import convert_json
import argparse
from sklearn.model_selection import train_test_split


parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', default=100, type=int, help='batch size')
parser.add_argument('--train_steps', default=1000, type=int,
                    help='number of training steps')

def main(argv):
    NUM_CLASSIFICATIONS = 5
    args = parser.parse_args(argv[1:])

    weed_info = convert_json.json_to_pd('effects.json')
    categories = pd.DataFrame(np.random.randint(0, NUM_CLASSIFICATIONS-1, len(weed_info)), index=weed_info.index.values.tolist())
    x_train, x_test, y_train, y_test = train_test_split(weed_info, categories, test_size=.33, random_state=42)

    numeric_columns = list(x_train) # ['Relaxed', 'Hungry', 'Sleepy', 'Creative', 'Energetic', 'Aroused', 'Uplifted', 'Happy', 'Tingly', 'Euphoric', 'Giggly', 'Talkative', 'Focused']
    numeric_featues = [tf.feature_column.numeric_column(key=numeric_column) for numeric_column in numeric_columns]

    # make categorical columns if we had any
    categorical_features = []

    features = numeric_featues + categorical_features

    # using automatic makers of input functions
    # if not pandas object must make directly
    training_input_function = tf.estimator.inputs.pandas_input_fn(
        x=x_train,
        y=y_train,
        batch_size=args.batch_size,
        shuffle=True,
        num_epochs=None
    )
    eval_input_function = tf.estimator.inputs.pandas_input_fn(
        x=x_test,
        y=y_test,
        batch_size=args.batch_size,
        shuffle=False,
        num_epochs=1
    )

    #build the NN
    classifier = tf.estimator.DNNClassifier(
        feature_columns=features,
        # two layers of 10 nodes each
        hidden_units=[10,10],
        # model chooses between 5 classifications
        n_classes=NUM_CLASSIFICATIONS,
        model_dir="simple_nn"
    )
    classifier.train(
        input_fn=training_input_function,
        steps=args.train_steps
    )
    loss = classifier.evaluate(
        input_fn=eval_input_function
    )
    print('loss is {}'.format(loss))

    # predictions = classifier.predict(input_fn=eval_input_function)
    # predictions = [p['predictions'][0] for p in predictions]

if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)