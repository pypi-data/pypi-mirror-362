# Easy Edge

[![PyPI](https://img.shields.io/pypi/v/easy-edge.svg)](https://pypi.org/project/easy-edge/)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A simple Ollama-like tool for running Large Language Models (LLMs) locally using llama.cpp under the hood.

## Features

- 🚀 **Local LLM Inference**: Run models locally using llama.cpp
- 📥 **Automatic Downloads**: Download models from URLs or Hugging Face
- 💬 **Interactive Chat**: Chat with models in an interactive terminal
- 📋 **Model Management**: List, download, and remove models
- ⚙️ **Configurable**: Customize model parameters and settings

## Installation

Install Easy Edge from PyPI:

```bash
pip install easy-edge
```

Or, to install the latest version from source:

```bash
git clone https://github.com/criminact/easy-edge.git
cd easy-edge
pip install .
```

## Usage

After installation, use the `easy-edge` command from your terminal:

### Download a Model

```bash
easy-edge pull --repo-id TheBloke/Llama-2-7B-Chat-GGUF --filename llama-2-7b-chat.Q4_K_M.gguf
```

Or download from a Hugging Face URL:

```bash
easy-edge pull --url https://huggingface.co/google/gemma-3-1b-it-qat-q4_0-gguf/resolve/main/gemma-3-1b-it-q4_0.gguf
```

### Run the Model

**Single prompt:**
```bash
easy-edge run gemma-3-1b-it-qat-q4_0-gguf --prompt "Hello, how are you?"
```

**Interactive chat:**
```bash
easy-edge run gemma-3-1b-it-qat-q4_0-gguf --interactive
```

### List Installed Models
```bash
easy-edge list
```

### Remove a Model
```bash
easy-edge remove gemma-3-1b-it-qat-q4_0-gguf
```

## Configuration

The tool stores configuration in `models/config.json`. You can modify settings like:

- `max_tokens`: Maximum tokens to generate (default: 2048)
- `temperature`: Sampling temperature (default: 0.7)
- `top_p`: Top-p sampling parameter (default: 0.9)

## Requirements

- Python 3.11+
- 8GB+ RAM (for 7B models)
- 16GB+ RAM (for 13B models)
- 4GB+ free disk space per model

## Troubleshooting

### Common Issues

1. **"llama-cpp-python not installed"**
   ```bash
   pip install llama-cpp-python
   ```

2. **Out of memory errors**
   - Try smaller models (7B instead of 13B)
   - Use more quantized models (Q4_K_M instead of Q8_0)
   - Close other applications to free up RAM

3. **Slow inference**
   - The tool uses all CPU cores by default
   - For better performance, consider using GPU acceleration (requires CUDA)

### GPU Acceleration (Optional)

For faster inference with NVIDIA GPUs:

```bash
pip uninstall llama-cpp-python
pip install llama-cpp-python --force-reinstall --index-url=https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/AVX2/cu118
```

## Finetuning Your Own Model

Easy Edge supports finetuning LLMs using a Modelfile (Ollama-style) and Hugging Face Trainer. This allows you to create custom models for your own data and use them locally.

### 1. Create a Modelfile

A Modelfile describes the base model, training parameters, and example messages for finetuning. Example:

```
HF_TOKEN <your_huggingface_token>
FROM meta-llama/Llama-3.2-1B-Instruct

PARAMETER device cpu
PARAMETER max_length 64
PARAMETER learning_rate 3e-5
PARAMETER epochs 4
PARAMETER batch_size 1
PARAMETER lora true
PARAMETER lora_r 8
PARAMETER lora_alpha 32
PARAMETER lora_dropout 0.05
PARAMETER lora_target_modules q_proj,v_proj

SYSTEM You are a helpful assistant.
MESSAGE user How can I reset my password?
MESSAGE assistant To reset your password, click on 'Forgot Password' at the login screen and follow the instructions.
```

- `HF_TOKEN` is your Hugging Face access token (required for private models).
- `FROM` specifies the base model to finetune.
- `PARAMETER` lines set training options (see above for examples).
- `SYSTEM` and `MESSAGE` blocks provide training data.

### 2. Run Finetuning

Use the `finetune` command to start training:

```bash
easy-edge finetune --modelfile Modelfile --output my-finetuned-model --epochs 4 --batch-size 1 --learning-rate 3e-5
```

- `--modelfile` is the path to your Modelfile.
- `--output` is where the trained model will be saved.
- You can override epochs, batch size, and learning rate on the command line.

### 3. Convert to GGUF (for llama.cpp)

After training, you will see instructions to convert your model to GGUF format for use with llama.cpp:

```bash
python3 convert_hf_to_gguf.py --in my-finetuned-model --out my-finetuned-model.gguf
```

Upload your GGUF file to Hugging Face or use it locally with Easy Edge.

### Notes
- Finetuning is resource-intensive. For best results, use a machine with a GPU.
- LoRA/PEFT is supported for efficient finetuning.
- See the example Modelfile in the repository for more options.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [llama.cpp](https://github.com/ggerganov/llama.cpp) - The underlying inference engine
- [Ollama](https://ollama.ai/) - Inspiration for the tool design
- [Hugging Face](https://huggingface.co/) - Model hosting and distribution 