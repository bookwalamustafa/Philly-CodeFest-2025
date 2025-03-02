import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv3D, MaxPooling3D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split

# Function to load a video and extract a fixed number of frames
def load_video(path, num_frames=16, target_size=(64, 64)):
    cap = cv2.VideoCapture(path)
    frames = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Sample indices uniformly across the video
    frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
    
    frame_id = 0
    grabbed_frames = 0
    while grabbed_frames < num_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_id in frame_indices:
            # Resize frame and convert from BGR (OpenCV default) to RGB
            frame = cv2.resize(frame, target_size)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
            grabbed_frames += 1
        frame_id += 1
    cap.release()
    
    # Ensure we have the desired number of frames
    if len(frames) != num_frames:
        return None
    frames = np.array(frames, dtype=np.float32) / 255.0  # Normalize pixel values
    return frames

# Function to load the dataset based on the directory structure
def load_dataset(dataset_dir, selected_words=None, num_frames=16, target_size=(64, 64)):
    X, y = [], []
    # Get all folder names in the dataset directory
    all_labels = sorted([folder for folder in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, folder))])
    # Filter labels if selected_words is provided
    labels = [label for label in all_labels if (selected_words is None or label in selected_words)]
    label_to_index = {label: index for index, label in enumerate(labels)}
    
    for label in labels:
        folder_path = os.path.join(dataset_dir, label)
        for video_file in os.listdir(folder_path):
            # Skip hidden files or non-video files (like .DS_Store)
            if video_file.startswith('.') or not video_file.lower().endswith(('.mp4', '.avi', '.mov')):
                continue
            video_path = os.path.join(folder_path, video_file)
            video_frames = load_video(video_path, num_frames, target_size)
            if video_frames is not None:
                X.append(video_frames)
                y.append(label_to_index[label])
    return np.array(X), np.array(y), label_to_index

# Set the path to your dataset folder
dataset_dir = "/Users/mustafabookwala/Desktop/Code/Philly-CodeFest-2025/dataset"  # Update this path accordingly

# Load data (for now, try with one or two classes)
X, y, label_to_index = load_dataset(dataset_dir, selected_words=None, num_frames=16, target_size=(64, 64))
print("Dataset loaded. Sample shapes:")
print("X shape:", X.shape)  # Expected shape: (num_samples, 16, 64, 64, 3)
print("y shape:", y.shape)
print("Label mapping:", label_to_index)

# Build a simple 3D CNN model
model = Sequential([
    Conv3D(32, kernel_size=(3, 3, 3), activation='relu', input_shape=(16, 64, 64, 3)),
    MaxPooling3D(pool_size=(1, 2, 2)),
    Conv3D(64, kernel_size=(3, 3, 3), activation='relu'),
    MaxPooling3D(pool_size=(1, 2, 2)),
    Conv3D(128, kernel_size=(3, 3, 3), activation='relu'),
    MaxPooling3D(pool_size=(1, 2, 2)),
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(len(label_to_index), activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

# Split the dataset for training and testing (this is just for demonstration)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model (for a small-scale experiment, epochs and batch_size can be small)
model.fit(X_train, y_train, epochs=10, batch_size=2, validation_data=(X_test, y_test))

loss, accuracy = model.evaluate(X_test, y_test)
print("Test accuracy: ", accuracy)

# Example function to predict the word from a new video clip
def predict_video(model, video_path, num_frames=16, target_size=(64, 64), label_map=None):
    video_frames = load_video(video_path, num_frames, target_size)
    if video_frames is None:
        print("Could not process video:", video_path)
        return None
    video_frames = np.expand_dims(video_frames, axis=0)  # Add batch dimension
    prediction = model.predict(video_frames)
    predicted_index = np.argmax(prediction)
    # Reverse mapping: index to label
    index_to_label = {index: label for label, index in label_map.items()}
    return index_to_label[predicted_index]

# Use the prediction function on a new video sample
new_video_path = "/Users/mustafabookwala/Desktop/Code/Philly-CodeFest-2025/dataset/able/00376.mp4"  # Update this path
predicted_word = predict_video(model, new_video_path, num_frames=16, target_size=(64, 64), label_map=label_to_index)
if predicted_word:
    print("Predicted word:", predicted_word)
