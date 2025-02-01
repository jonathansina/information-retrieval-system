# Information Retrieval System for Digikala’s FAQ

This project develops an Information Retrieval System for Digikala’s FAQ section using TF-IDF and LaBSE-based embeddings, with ranking via cosine similarity, Jaccard similarity, and a custom metric. It supports Persian text processing with Hazm and Parsivar, focusing on data collection, augmentation, and evaluation.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project aims to provide an efficient Information Retrieval System for Digikala’s FAQ section. It leverages various text processing techniques and ranking algorithms to enhance the search experience for Persian text.

## Features

- **Text Processing**: Utilizes Hazm and Parsivar for Persian text processing.
- **Embeddings**: Uses TF-IDF and LaBSE-based embeddings.
- **Ranking Algorithms**: Supports cosine similarity, Jaccard similarity, and a custom metric for ranking.
- **Data Augmentation**: Focuses on data collection and augmentation to improve retrieval performance.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/jonathansina/information-retrieval-system.git
    cd information-retrieval-system
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To use the Information Retrieval System, follow these steps:

1. Prepare your dataset and place it in the `data` directory.
2. Run the Jupyter notebooks in the `notebooks` directory to preprocess the data and train the models.
3. Use the provided scripts in the `scripts` directory to evaluate and test the models.

## Project Structure

- `data/`: Directory to store datasets.
- `dev/`: Jupyter notebooks for preprocessing, training, and evaluation.
- `src/`: Python scripts for running the models and evaluating performance.
- `requirements.txt`: List of required Python packages.
- `README.md`: Project documentation.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
