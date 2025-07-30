# Federated Learning Client CLI with Supabase Integration

A comprehensive command-line interface for federated learning using scikit-learn MLPClassifier with Supabase Storage and Firebase Authentication.

## 🚀 Features

- **🤖 Train**: Train MLP models locally on CSV datasets using scikit-learn
- **📊 Evaluate**: Comprehensive model evaluation with metrics and comparisons
- **☁️ Supabase Storage**: Secure model storage and retrieval with signed URLs
- **🔐 Firebase Auth**: Secure authentication for protected operations
- **🔄 Sync**: Download/upload models with automatic fallback to HTTP
- **📈 Compare**: Compare multiple models on the same test dataset
- **🎯 Lightweight**: No PyTorch/TensorFlow dependencies, works in <100MB environments

## Installation

### From PyPI (Recommended)
```bash
pip install federated-learning-client
```

### From Source
1. Clone the repository:
```bash
git clone https://github.com/yourusername/federated-learning-client.git
cd federated-learning-client
```

2. Install in development mode:
```bash
pip install -e .
```

## Quick Start

### 1. Train a Model
```bash
fl-client train ./data/sample_diabetes_client1.csv --rounds 10 --model ./models/client1_model.pth
```

### 2. Evaluate the Model
```bash
fl-client evaluate ./models/client1_model.pth ./data/sample_diabetes_test.csv --save
```

### 3. Sync with Server
```bash
fl-client sync https://server.com/global_model.pth --model ./models/global_model.pth
```

### 4. Upload Local Model
```bash
fl-client upload ./models/client1_model.pth https://server.com/upload --round 5
```

## Commands

### `train`
Train an MLP model locally on CSV data.

**Usage:**
```bash
python cli.py train [DATA_PATH] [OPTIONS]
```

**Options:**
- `--model, -m`: Path to save/load model (default: `./models/local_model.pth`)
- `--rounds, -r`: Number of training epochs (default: 10)
- `--batch-size, -b`: Batch size for training (default: 32)
- `--lr`: Learning rate (default: 0.001)
- `--target, -t`: Name of target column (default: last column)
- `--log, -l`: Path to save training log
- `--round-num`: Federated learning round number

**Example:**
```bash
python cli.py train ./data/client1.csv --rounds 15 --batch-size 64 --lr 0.01
```

### `evaluate`
Evaluate a trained model on test data.

**Usage:**
```bash
python cli.py evaluate [MODEL_PATH] [TEST_DATA_PATH] [OPTIONS]
```

**Options:**
- `--target, -t`: Name of target column
- `--batch-size, -b`: Batch size for evaluation (default: 32)
- `--save, -s`: Save evaluation results to file
- `--output, -o`: Path to save results (default: `./results/evaluation_results.txt`)

**Example:**
```bash
python cli.py evaluate ./models/model.pth ./data/test.csv --save --output ./results/eval.txt
```

### `sync`
Download the latest global model from a server URL.

**Usage:**
```bash
python cli.py sync [URL] [OPTIONS]
```

**Options:**
- `--model, -m`: Local path to save downloaded model (default: `./models/global_model.pth`)
- `--client-id, -c`: Client identifier (default: `client_001`)
- `--timeout`: Download timeout in seconds (default: 30)

**Example:**
```bash
python cli.py sync https://federated-server.com/global_model.pth --client-id client_hospital_1
```

### `upload`
Upload local model weights to a server endpoint.

**Usage:**
```bash
python cli.py upload [MODEL_PATH] [SERVER_URL] [OPTIONS]
```

**Options:**
- `--client-id, -c`: Client identifier (default: `client_001`)
- `--round, -r`: Current federated learning round number
- `--timeout`: Upload timeout in seconds (default: 30)

**Example:**
```bash
python cli.py upload ./models/local_model.pth https://server.com/upload --round 3
```

### `full-sync`
Perform complete synchronization with federated learning server.

**Usage:**
```bash
python cli.py full-sync [SERVER_URL] [OPTIONS]
```

**Options:**
- `--model, -m`: Local model path (default: `./models/federated_model.pth`)
- `--client-id, -c`: Client identifier (default: `client_001`)
- `--round, -r`: Current round number
- `--upload-after`: Upload local model after downloading global model

**Example:**
```bash
python cli.py full-sync https://federated-server.com --round 5 --upload-after
```

### `compare`
Compare multiple models on the same test dataset.

**Usage:**
```bash
python cli.py compare [MODEL_PATHS...] --test-data [TEST_DATA_PATH] [OPTIONS]
```

**Options:**
- `--test-data, -d`: Path to test CSV file (required)
- `--target, -t`: Name of target column
- `--batch-size, -b`: Batch size for evaluation (default: 32)

**Example:**
```bash
python cli.py compare model1.pth model2.pth model3.pth --test-data ./data/test.csv
```

### `info`
Display information about the federated learning client.

**Usage:**
```bash
python cli.py info
```

## Data Format

The CLI expects CSV files with the following characteristics:

- **Headers**: First row should contain column names
- **Features**: Numerical or categorical features (categorical will be automatically encoded)
- **Target**: Binary classification target (0/1 or categorical labels)
- **Missing Values**: Will be automatically filled with mean values for numerical columns

### Example CSV Format:
```csv
pregnancies,glucose,blood_pressure,skin_thickness,insulin,bmi,diabetes_pedigree,age,outcome
6,148,72,35,0,33.6,0.627,50,1
1,85,66,29,0,26.6,0.351,31,0
8,183,64,0,0,23.3,0.672,32,1
```

## Model Architecture

The MLP model uses the following architecture:

- **Input Layer**: Matches the number of features in your dataset
- **Hidden Layers**: Configurable (default: [64, 32] neurons)
- **Activation**: ReLU activation functions
- **Regularization**: Dropout (0.2) between layers
- **Output Layer**: 2 neurons for binary classification
- **Initialization**: Xavier uniform weight initialization

## Configuration

You can customize default settings by editing `config.json`:

```json
{
  "federated_learning": {
    "server_base_url": "https://your-server.com",
    "client_id": "your_client_id"
  },
  "model": {
    "hidden_sizes": [128, 64, 32],
    "dropout_rate": 0.3
  },
  "training": {
    "default_epochs": 20,
    "default_batch_size": 64,
    "default_learning_rate": 0.001
  }
}
```

## Logging

Training and evaluation activities are automatically logged to:
- Console output with rich formatting
- Log files (when specified)
- Training history for federated learning rounds

## File Structure

```
client_cli/
├── cli.py              # Main CLI entry point
├── model.py            # MLP model architecture
├── train.py            # Training logic
├── evaluate.py         # Evaluation logic
├── sync.py             # Synchronization with server
├── requirements.txt    # Python dependencies
├── config.json         # Configuration file
├── data/               # Sample data files
│   ├── sample_diabetes_client1.csv
│   └── sample_diabetes_test.csv
├── models/             # Saved models (created automatically)
├── logs/               # Training logs (created automatically)
└── results/            # Evaluation results (created automatically)
```

## Example Workflow

Here's a complete federated learning workflow:

```bash
# 1. Train local model
python cli.py train ./data/sample_diabetes_client1.csv --rounds 10 --log ./logs/round1.log

# 2. Evaluate local model
python cli.py evaluate ./models/local_model.pth ./data/sample_diabetes_test.csv --save

# 3. Download global model from server
python cli.py sync https://federated-server.com/global_model.pth

# 4. Upload local model weights
python cli.py upload ./models/local_model.pth https://federated-server.com/upload --round 1

# 5. Compare models
python cli.py compare ./models/local_model.pth ./models/global_model.pth --test-data ./data/sample_diabetes_test.csv
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

2. **CUDA Issues**: The client automatically detects and uses GPU if available, falls back to CPU

3. **File Not Found**: Ensure data files exist and paths are correct

4. **Model Loading Errors**: Check that model files are valid PyTorch models

5. **Network Issues**: For sync operations, ensure server URLs are accessible

### Getting Help

For detailed help on any command:
```bash
python cli.py [COMMAND] --help
```

For general information:
```bash
python cli.py info
```

## License

This federated learning client is designed for educational and research purposes in healthcare ML applications.
