from database.schema import (
    Algorithm,
    DataType,
    AlgorithmDataType,
    TrainedModel,
    TrainModelDatatype,
    ModelVersion,
    Function,
    Parameter,
    FunctionParameter,
)
from loguru import logger
import random


def insert_data():
    logger.info("Inserting dummy data")
    # Create Algorithms
    algorithms = [
        {
            "name": "RandomForestClassifier",
            "description": "A random forest classifier",
            "default_loss_function": "gini",
        },
        {
            "name": "MLPClassifier",
            "description": "Multi-layer Perceptron classifier",
            "default_loss_function": "log_loss",
        },
        {
            "name": "SVC",
            "description": "C-Support Vector Classification",
            "default_loss_function": "hinge",
        },
        {
            "name": "LogisticRegression",
            "description": "Logistic Regression classifier",
            "default_loss_function": "log_loss",
        },
    ]

    algo_objs = []
    for algo in algorithms:
        algo_objs.append(Algorithm.create(**algo))

    # Create DataTypes
    data_types = [
        {"type": "integer", "is_categorical": False},
        {"type": "float", "is_categorical": False},
        {"type": "string", "is_categorical": True},
        {"type": "boolean", "is_categorical": True},
        {"type": "image", "is_categorical": False},
    ]

    dtype_objs = []
    for dt in data_types:
        dtype_objs.append(DataType.create(**dt))

    # Create AlgorithmDataType relationships
    for algo in algo_objs:
        # Randomly assign 2-4 data types to each algorithm
        num_types = random.randint(2, 4)
        selected_types = random.sample(dtype_objs, num_types)
        for dtype in selected_types:
            AlgorithmDataType.create(algorithm=algo, datatype=dtype)

    # Create TrainedModels
    trained_models = [
        {
            "name": "Image Classifier",
            "dataset_name": "CIFAR-10",
            "size": "50MB",
            "input_shape": "(32,32,3)",
            "algorithm": algo_objs[1],  # MLPClassifier
        },
        {
            "name": "Fraud Detector",
            "dataset_name": "Credit Card Fraud",
            "size": "5MB",
            "input_shape": "(30,)",
            "algorithm": algo_objs[0],  # RandomForestClassifier
        },
        {
            "name": "Sentiment Analyzer",
            "dataset_name": "IMDB Reviews",
            "size": "15MB",
            "input_shape": "(1000,)",
            "algorithm": algo_objs[3],  # LogisticRegression
        },
        {
            "name": "Object Detector",
            "dataset_name": "COCO",
            "size": "120MB",
            "input_shape": "(256,256,3)",
            "algorithm": algo_objs[1],  # MLPClassifier
        },
    ]

    model_objs = []
    for model in trained_models:
        model_objs.append(TrainedModel.create(**model))

    # Create TrainModelDatatype features
    feature_names = [
        "age",
        "income",
        "color",
        "height",
        "weight",
        "pixel",
        "text",
        "label",
        "score",
    ]
    feature_types = ["continuous", "categorical", "primary_key", "group_index"]
    for model in model_objs:
        num_features = random.randint(3, 7)
        for i in range(num_features):
            TrainModelDatatype.create(
                feature_name=f"{random.choice(feature_names)}_{i}",
                feature_position=i,
                feature_size=1,
                feature_type=random.choice(feature_types),
                datatype=random.choice(dtype_objs),
                trained_model=model,
            )

    # Create ModelVersions
    for model in model_objs:
        for v in range(1, random.randint(2, 4)):
            ModelVersion.create(
                version_name=f"v{v}.0",
                image_path=f"/models/{model.name.replace(' ', '_')}_v{v}.pkl",
                loss_function=model.algorithm.default_loss_function,
                train_loss=random.uniform(0.1, 1.0),
                val_loss=random.uniform(0.1, 1.0),
                train_samples=random.randint(1000, 10000),
                val_samples=random.randint(200, 2000),
                trained_model=model,
            )

    # Create Functions (now using scikit-learn functions)
    functions = [
        {
            "name": "StandardScaler",
            "description": "Standardize features by removing the mean and scaling to unit variance",
            "function_reference": "sklearn.preprocessing.StandardScaler",
        },
        {
            "name": "CountVectorizer",
            "description": "Convert a collection of text documents to a matrix of token counts",
            "function_reference": "sklearn.feature_extraction.text.CountVectorizer",
        },
        {
            "name": "MinMaxScaler",
            "description": "Transforms features by scaling each feature to a given range",
            "function_reference": "sklearn.preprocessing.MinMaxScaler",
        },
        {
            "name": "OneHotEncoder",
            "description": "Encode categorical features as a one-hot numeric array",
            "function_reference": "sklearn.preprocessing.OneHotEncoder",
        },
    ]

    func_objs = []
    for func in functions:
        func_objs.append(Function.create(**func))

    # Create Parameters (real parameters from scikit-learn functions)
    parameters = [
        {"name": "with_mean", "value": "True", "parameter_type": "bool"},
        {"name": "with_std", "value": "True", "parameter_type": "bool"},
        {"name": "max_features", "value": "1000", "parameter_type": "int"},
        {"name": "ngram_range", "value": "(1,1)", "parameter_type": "tuple"},
        {"name": "feature_range", "value": "(0,1)", "parameter_type": "tuple"},
        {"name": "categories", "value": "auto", "parameter_type": "str"},
        {"name": "handle_unknown", "value": "error", "parameter_type": "str"},
    ]

    param_objs = []
    for param in parameters:
        param_objs.append(Parameter.create(**param))

    # Create FunctionParameter relationships
    FunctionParameter.create(
        function=func_objs[0], parameter=param_objs[0]
    )  # StandardScaler - with_mean
    FunctionParameter.create(
        function=func_objs[0], parameter=param_objs[1]
    )  # StandardScaler - with_std
    FunctionParameter.create(
        function=func_objs[1], parameter=param_objs[2]
    )  # CountVectorizer - max_features
    FunctionParameter.create(
        function=func_objs[1], parameter=param_objs[3]
    )  # CountVectorizer - ngram_range
    FunctionParameter.create(
        function=func_objs[2], parameter=param_objs[4]
    )  # MinMaxScaler - feature_range
    FunctionParameter.create(
        function=func_objs[3], parameter=param_objs[5]
    )  # OneHotEncoder - categories
    FunctionParameter.create(
        function=func_objs[3], parameter=param_objs[6]
    )  # OneHotEncoder - handle_unknown
