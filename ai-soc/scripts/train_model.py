from ingestion.reader import read_new_logs
from features.feature_engineer import FeatureEngineer
from ml.model import train_and_save

FILE_PATH = "logs.csv"
MODEL_PATH = "models/isolation_forest.pkl"


def main():
    fe = FeatureEngineer()

    # read full dataset
    logs, _ = read_new_logs(FILE_PATH, 0)

    if not logs:
        print("No data found")
        return

    # generate features
    features = fe.process_logs(logs)

    # convert to vectors
    data = []
    for f in features:
        vec = [
            f["request_freq"],
            f["failed_ratio"],
            f["unique_ports"],
            f["off_hour"]
        ]
        data.append(vec)

    # train and save model
    train_and_save(data, path=MODEL_PATH)

    print("Model trained and saved at:", MODEL_PATH)


if __name__ == "__main__":
    main()