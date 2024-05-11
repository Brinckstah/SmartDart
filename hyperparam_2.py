import optuna
import torch
from ultralytics import YOLO
import os

def objective(trial):
    # Define hyperparameters using trial object
    lr = trial.suggest_loguniform('lr', 1e-5, 1e-1)
    optimizer_name = trial.suggest_categorical('optimizer', ['Adam', 'SGD', 'AdamW'])
    batch_size = trial.suggest_categorical('batch_size', [8, 16, 32])

    # Model setup
    model = YOLO('yolov8s.yaml')
    model.to('cuda')

    # Training setup
    optimizer = getattr(torch.optim, optimizer_name)(model.parameters(), lr=lr)
    data_path = r"C:\Users\tbmor\BachelorData\SmartDart\YoloV8\dartV1.yaml"

    # Dummy training function
    loss = model.train(data=data_path, epochs=10, batch=batch_size, optimizer=optimizer)
    
    return loss  # Objective: minimize loss

def main():
    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=20)

    print("Best hyperparameters: ", study.best_trial.params)

if __name__ == '__main__':
    main()