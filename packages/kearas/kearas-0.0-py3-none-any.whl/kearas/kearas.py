
def pro1():
    print(
        '''import numpy as np
        import tensorflow as tf
        import matplotlib.pyplot as plt

        # Create a dataset for the AND logic gate
        data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float32)
        labels = np.array([[0], [0], [0], [1]], dtype=np.float32)

        # Build the perceptron model
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(units=1, activation='sigmoid', input_shape=(2,))
        ])

        # Compile the model
        model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.1),
                    loss='binary_crossentropy',
                    metrics=['accuracy'])

        # Train the model
        model.fit(data, labels, epochs=1000, verbose=0)

        # Evaluate the model
        loss, accuracy = model.evaluate(data, labels, verbose=0)
        print(f'Loss: {loss:.4f}, Accuracy: {accuracy:.4f}')

        # Visualize the decision boundary
        def plot_decision_boundary(model, data, labels):
            x_min, x_max = data[:, 0].min() - 1, data[:, 0].max() + 1
            y_min, y_max = data[:, 1].min() - 1, data[:, 1].max() + 1
            xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))
            grid = np.c_[xx.ravel(), yy.ravel()]
            predictions = model.predict(grid).reshape(xx.shape)

            plt.contourf(xx, yy, predictions, alpha=0.7, levels=[0, 0.5, 1], cmap="coolwarm")
            plt.scatter(data[:, 0], data[:, 1], c=labels[:, 0], edgecolors='k', cmap="coolwarm")
            plt.title("Decision Boundary")
            plt.xlabel("Input 1")
            plt.ylabel("Input 2")
            plt.show()

        plot_decision_boundary(model, data, labels)
        print('this program is powered by')'''
    )

    def pro2():
        print(
        '''import tensorflow as tf
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler


        data = pd.read_csv('data.csv')
        

        X = data.iloc[:, :-1].values
        y = data.iloc[:, -1].values


        y = tf.keras.utils.to_categorical(y)


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)


        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(y.shape[1], activation='softmax')  
        ])


        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


        history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=1)


        loss, accuracy = model.evaluate(X_test, y_test)
        print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")

        plt.plot(history.history['accuracy'], label='Train Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.title('Model Accuracy')
        plt.legend()
        plt.show()


        def visualize_predictions(model, X, y_true, num_samples=5):
            predictions = model.predict(X)
            y_pred = np.argmax(predictions, axis=1)
            y_true = np.argmax(y_true, axis=1)

            for i in range(num_samples):
                print(f"Sample {i+1}")
                print(f"True Label: {y_true[i]}, Predicted Label: {y_pred[i]}")
                print()

        visualize_predictions(model, X_test[:5], y_test[:5])
        print('this program is powered by ')'''

    )
 
    
    def pro3():
        print(
        '''import pandas as pd
        import numpy as np
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense
        import matplotlib.pyplot as plt


        data = pd.read_csv('mnist.csv')  # Replace with your MNIST .csv file path
        X = data.drop('label', axis=1).values  
        y = data['label'].values  

        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


        def create_model(activation_function):
            model = Sequential([
                Dense(128, input_shape=(X_train.shape[1],), activation=activation_function),
                Dense(64, activation=activation_function),
                Dense(10, activation='softmax')  
            ])
            model.compile(optimizer='adam',
                        loss='sparse_categorical_crossentropy',
                        metrics=['accuracy'])
            return model


        activation_functions = ['sigmoid', 'relu', 'tanh']
        results = {}

        for activation in activation_functions:
            print(f"Training model with {activation} activation function...")
            model = create_model(activation)
            history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test), verbose=1)
            results[activation] = history


        plt.figure(figsize=(10, 6))

        for activation in activation_functions:
            history = results[activation]
            plt.plot(history.history['accuracy'], label=f'{activation} - train')
            plt.plot(history.history['val_accuracy'], label=f'{activation} - validation')

        plt.title('Training Performance Comparison')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.show()
        print('this program is powred by  ')''')
    

    def pro4():
        print(
        '''import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
        from tensorflow.keras.optimizers import SGD, Adam, RMSprop
        import matplotlib.pyplot as plt
        import pandas as pd
        import numpy as np
        from sklearn.model_selection import train_test_split


        def load_cifar10_csv(filepath):
            df = pd.read_csv(filepath)
            labels = df['label'].values
            images = df.drop('label', axis=1).values.reshape(-1, 32, 32, 3) / 255.0
            return images, labels


        X, y = load_cifar10_csv('cifar10.csv') # replace 'cifar10.csv' with your actual csv filepath


        y = tf.keras.utils.to_categorical(y, 10)


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        def build_and_train_model(optimizer, epochs=10):
            model = Sequential()
            model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(32, 32, 3)))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Flatten())
            model.add(Dense(128, activation='relu'))
            model.add(Dense(10, activation='softmax'))

            model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
            history = model.fit(X_train, y_train, epochs=epochs, batch_size=32, verbose=1, validation_data=(X_test, y_test))
            return history

        optimizers = {'SGD': SGD(), 'Adam': Adam(), 'RMSprop': RMSprop()}
        histories = {name: build_and_train_model(optimizer) for name, optimizer in optimizers.items()}


        plt.figure(figsize=(12, 8))
        for name in optimizers.keys():
            plt.plot(histories[name].history['accuracy'], label=f'{name} train')
            plt.plot(histories[name].history['val_accuracy'], label=f'{name} val')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.title('Training and Validation Accuracy for Different Optimizers (TensorFlow/Keras)')
        plt.show()


        for name, history in histories.items():
            final_train_acc = history.history['accuracy'][-1]
            final_val_acc = history.history['val_accuracy'][-1]
            print(f"{name} - Train Accuracy: {final_train_acc:.4f}, Validation Accuracy: {final_val_acc:.4f}")
            print('this program is powred by ajay ')'''
    )

def pro5():
    print(
        '''import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
        from tensorflow.keras.optimizers import SGD, Adam, RMSprop
        import matplotlib.pyplot as plt
        import pandas as pd
        import numpy as np
        from sklearn.model_selection import train_test_split


        def load_cifar10_csv(filepath):
            df = pd.read_csv(filepath)
            labels = df['label'].values
            images = df.drop('label', axis=1).values.reshape(-1, 32, 32, 3) / 255.0
            return images, labels


        X, y = load_cifar10_csv('cifar10.csv') # replace 'cifar10.csv' with your actual csv filepath


        y = tf.keras.utils.to_categorical(y, 10)


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        def build_and_train_model(optimizer, epochs=10):
            model = Sequential()
            model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(32, 32, 3)))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Flatten())
            model.add(Dense(128, activation='relu'))
            model.add(Dense(10, activation='softmax'))

            model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
            history = model.fit(X_train, y_train, epochs=epochs, batch_size=32, verbose=1, validation_data=(X_test, y_test))
            return history

        optimizers = {'SGD': SGD(), 'Adam': Adam(), 'RMSprop': RMSprop()}
        histories = {name: build_and_train_model(optimizer) for name, optimizer in optimizers.items()}


        plt.figure(figsize=(12, 8))
        for name in optimizers.keys():
            plt.plot(histories[name].history['accuracy'], label=f'{name} train')
            plt.plot(histories[name].history['val_accuracy'], label=f'{name} val')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.title('Training and Validation Accuracy for Different Optimizers (TensorFlow/Keras)')
        plt.show()


        for name, history in histories.items():
            final_train_acc = history.history['accuracy'][-1]
            final_val_acc = history.history['val_accuracy'][-1]
            print(f"{name} - Train Accuracy: {final_train_acc:.4f}, Validation Accuracy: {final_val_acc:.4f}")
            print('this program is powred by ajay ')'''
    )

def pro6():
    print('''import pandas as pd
        import numpy as np
        import tensorflow as tf
        from tensorflow import keras
        from tensorflow.keras import layers
        import matplotlib.pyplot as plt

        data = pd.read_csv("mnist.csv")  # Replace with your dataset path

        y = data.iloc[:, 0].values  
        X = data.iloc[:, 1:].values 

        X = X / 255.0

        X = X.reshape(-1, 28, 28, 1)

        y = keras.utils.to_categorical(y, num_classes=10)

        model = keras.Sequential([
            layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
            layers.MaxPooling2D((2,2)),
            layers.Conv2D(64, (3,3), activation='relu'),
            layers.MaxPooling2D((2,2)),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dense(10, activation='softmax')
        ])

        model.compile(optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])


        model.fit(X, y, epochs=5, batch_size=32, validation_split=0.2)

        test_loss, test_acc = model.evaluate(X, y)
        print(f"Test Accuracy: {test_acc:.4f}")

        layer_outputs = [layer.output for layer in model.layers if isinstance(layer, layers.Conv2D)]
        activation_model = keras.Model(inputs=model.input, outputs=layer_outputs)

        img = X[0].reshape(1, 28, 28, 1)
        activations = activation_model.predict(img)

        fig, axes = plt.subplots(1, len(activations[0][0, :, :, :]), figsize=(12, 6))
        for i in range(len(activations[0][0, :, :, :])):
            axes[i].imshow(activations[0][0, :, :, i], cmap='viridis')
            axes[i].axis('off')
        plt.show()

        print('this program is powred by  ')'''
        )          
    
def pro7():
    print(
        '''from keras.preprocessing.text import Tokenizer
        from keras.utils import pad_sequences
        from keras import Sequential
        from keras.utils import to_categorical
        from keras.layers import Dense,SimpleRNN,Embedding,Flatten

        import numpy as np
        import pandas as pd

        train_ds = pd.read_csv('8train.csv',encoding='latin1')
        validation_ds = pd.read_csv('8test.csv',encoding='latin1')

        train_ds = train_ds[['text','sentiment']]
        validation_ds = validation_ds[['text','sentiment']]

        train_ds['text'].fillna('',inplace=True)
        validation_ds['text'].fillna('',inplace=True)

        def func(sentiment):
            if sentiment =='positive':
                return 0;
            elif sentiment =='negative':
                return 1;
            else:
                return 2;
        train_ds['sentiment'] = train_ds['sentiment'].apply(func)
        validation_ds['sentiment'] = validation_ds['sentiment'].apply(func)

        x_train = np.array(train_ds['text'].tolist())
        y_train = np.array(train_ds['sentiment'].tolist())
        x_test = np.array(validation_ds['text'].tolist())
        y_test = np.array(validation_ds['sentiment'].tolist())

        x_train
        y_train

        y_train = to_categorical(y_train, 3)
        y_test = to_categorical(y_test, 3)

        y_train
        tokenizer = Tokenizer(num_words=20000)
        tokenizer.fit_on_texts(x_train)
        tokenizer.fit_on_texts(x_test)
        len(tokenizer.word_index)

        x_train = tokenizer.texts_to_sequences(x_train)
        x_test = tokenizer.texts_to_sequences(x_test)

        from keras.utils import pad_sequences
        x_train = pad_sequences(x_train, padding='post', maxlen=35)  # Set maxlen to 35
        x_test = pad_sequences(x_test, padding='post', maxlen=35)

        x_train[0]
        x_train.shape

        model = Sequential()
        model.add(Embedding(input_dim=20000, output_dim=5, input_length=35))
        model.add(SimpleRNN(32,return_sequences=False))
        model.add(Dense(3,activation='softmax'))
        model.summary()

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        history = model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))

        import matplotlib.pyplot as plt
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.show()

        text = "The movie was bad bad bad, i will not recommend this movie to anyone"

        new_text_seq = tokenizer.texts_to_sequences([text])
        new_text_padded = pad_sequences(new_text_seq, padding='post', maxlen=35) 
        predictions = model.predict(new_text_padded)
        predicted_class_index = predictions.argmax(axis=-1)
        if predicted_class_index[0] == 0:
            print("Postive Sentiment");
        elif predicted_class_index[0] == 1:
            print("Negative Sentiment")
        else:
            print("Neutral Sentiment")

        text = "The movie was good, i will recommend this movie to anyone"


        new_text_seq = tokenizer.texts_to_sequences([text])
        new_text_padded = pad_sequences(new_text_seq, padding='post', maxlen=35)  # Use the max_len determined during training
        predictions = model.predict(new_text_padded)
        predicted_class_index = predictions.argmax(axis=-1)
        if predicted_class_index[0] == 0:
            print("Postive Sentiment");
        elif predicted_class_index[0] == 1:
            print("Negative Sentiment")
        else:
            print("Neutral Sentiment")

        print('this code is powered by ')'''
    )

def pro8():
    print(
        '''import numpy as np
        import pandas as pd
        import os
        import numpy
        import glob
        import cv2
        from keras.applications.vgg16 import VGG16
        from keras.models import Sequential
        from keras.layers import Flatten, Dense
        print(os.listdir("../input/flowers-recognition/flowers/flowers"))
        weights = '../input/vgg16/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5'

        folders = glob.glob('../input/flowers/*')
        imagenames_list = []
        for folder in folders:
            for f in glob.glob(folder+'/*.jpg'):
                imagenames_list.append(f)

        def label_img(image):
            word_label = image.split('/')[4]
            if word_label == 'daisy':
                return [1,0,0,0,0]
            elif word_label == 'dandelion':
                return [0,1,0,0,0]
            elif word_label == 'rose':
                return [0,0,1,0,0]
            elif word_label == 'tulip':
                return [0,0,0,1,0]
            else:
                return [0,0,0,0,1]
            
        train = []

        for image in imagenames_list:
            label = label_img(image)
            train.append([np.array(cv2.resize(cv2.imread(image),(224,224))), np.array(label)])
            np.random.shuffle(train)

        X = np.array([i[0] for i in train])
        X = X/255
        Y = np.array([i[1] for i in train])

        model = Sequential()
        model.add(VGG16(include_top = False, weights = weights, input_shape = (224,224,3)))
        model.add(Flatten())
        model.add(Dense(512, activation = 'relu'))
        model.add(Dense(5, activation = 'softmax'))
        model.compile(loss='categorical_crossentropy',
                    optimizer='sgd',
                    metrics=['accuracy'])

        Fit = model.fit(X, Y, epochs = 1, validation_split = 0.30)
        loss, accuracy = model.evaluate(X, Y)
        print(f"Loss: {loss}")
        print(f"Accuracy: {accuracy}")

        import matplotlib.pyplot as plt
        num_images = 5
        random_indices = np.random.choice(len(X), num_images, replace=False)
        selected_images = X[random_indices]
        true_labels = Y[random_indices]

        predictions = model.predict(selected_images)
        predicted_classes = np.argmax(predictions, axis=1)

        flower_names = ['Daisy', 'Dandelion', 'Rose', 'Tulip', 'Sunflower']

        plt.figure(figsize=(12,6))
        for i in range(num_images):
            plt.subplot(1, num_images, i+1)
            plt.imshow(selected_images[i])
            plt.axis('off')
            actual = flower_names[np.argmax(true_labels[i])]
            predicted = flower_names[predicted_classes[i]]
            plt.title(f"Actual: {actual}\nPredicted: {predicted}", fontsize=10)
        plt.show()'''

    )