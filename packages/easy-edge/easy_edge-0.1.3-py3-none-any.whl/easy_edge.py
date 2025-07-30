#!/usr/bin/env python3
"""
Easy Edge - A simple Ollama-like tool for running LLMs locally
"""

import os
import sys
import json
import click
import requests
from pathlib import Path
from typing import Optional, Dict, Any
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt
from rich.panel import Panel
from tqdm import tqdm
import huggingface_hub
import re
import tempfile
import shutil
import subprocess
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
import torch
from peft import LoraConfig, get_peft_model, TaskType
import bitsandbytes as bnb
import platform
import sys
import urllib.request
import zipfile

# Try to import llama-cpp-python
try:
    from llama_cpp import Llama
except ImportError:
    print("Error: llama-cpp-python not installed. Run: pip install llama-cpp-python")
    sys.exit(1)

console = Console()

class EasyEdge:
    def __init__(self, models_dir: str = None):
        # Check for Homebrew installation
        if models_dir is None:
            homebrew_models = Path.home() / ".easy-edge-models"
            if homebrew_models.exists():
                models_dir = str(homebrew_models)
            else:
                models_dir = "models"
        
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        self.config_file = self.models_dir / "config.json"
        self.load_config()
        
    def load_config(self):
        """Load or create configuration file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "models": {},
                "default_model": None,
                "settings": {
                    "max_tokens": 2048,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_model_path(self, model_name: str) -> Optional[Path]:
        """Get the local path for a model"""
        if model_name in self.config["models"]:
            model_path = self.models_dir / self.config["models"][model_name]["filename"]
            if model_path.exists():
                return model_path
        return None
    
    def download_model(self, model_url: str) -> Path:
        """Download a model from URL using Hugging Face hub"""
        try:
            # Extract repo_id and filename from URL
            # URL format: https://huggingface.co/google/gemma-3-1b-it-qat-q4_0-gguf/resolve/main/gemma-3-1b-it-q4_0.gguf
            if "huggingface.co" in model_url:
                parts = model_url.split("/")
                repo_id = f"{parts[3]}/{parts[4]}"
                filename_in_repo = parts[-1]
                
                # Extract model name from repo_id (last part)
                model_name = repo_id.split("/")[-1]
                
                console.print(f"Detected Hugging Face repo: {repo_id}, file: {filename_in_repo}")
                console.print(f"Model name: {model_name}")
                
                filename = f"{model_name}.gguf"
                model_path = self.models_dir / filename
                
                if model_path.exists():
                    console.print(f"Model {model_name} already exists at {model_path}")
                    return model_path
                
                # Use Hugging Face download with progress
                with console.status(f"Downloading {model_name} from Hugging Face..."):
                    downloaded_path = huggingface_hub.hf_hub_download(
                        repo_id=repo_id,
                        filename=filename_in_repo,
                        local_dir=self.models_dir,
                        local_dir_use_symlinks=False
                    )
                
                # Rename to our standard format
                if Path(downloaded_path).exists():
                    Path(downloaded_path).rename(model_path)
                
                # Update config
                self.config["models"][model_name] = {
                    "filename": filename,
                    "repo_id": repo_id,
                    "original_filename": filename_in_repo,
                    "size": model_path.stat().st_size
                }
                self.save_config()
                
                console.print(f"✅ Model {model_name} downloaded successfully!")
                return model_path
            else:
                # For non-Hugging Face URLs, fall back to requests
                console.print("Non-Hugging Face URL detected, using direct download...")
                console.print("❌ Please provide a Hugging Face URL for automatic model name extraction")
                raise ValueError("Only Hugging Face URLs are supported for automatic model name extraction")
                
        except Exception as e:
            console.print(f"❌ Error downloading model: {e}")
            raise
    
    def download_from_huggingface(self, repo_id: str, filename: str) -> Path:
        """Download a model from Hugging Face"""
        # Extract model name from repo_id (last part)
        model_name = repo_id.split("/")[-1]
        
        local_filename = f"{model_name}.gguf"
        model_path = self.models_dir / local_filename
        
        if model_path.exists():
            console.print(f"Model {model_name} already exists at {model_path}")
            return model_path
        
        console.print(f"Downloading {model_name} from Hugging Face ({repo_id})...")
        
        try:
            with console.status(f"Downloading {model_name} from Hugging Face..."):
                huggingface_hub.hf_hub_download(
                    repo_id=repo_id,
                    filename=filename,
                    local_dir=self.models_dir,
                    local_dir_use_symlinks=False
                )
            
            # Rename to our standard format
            downloaded_path = self.models_dir / filename
            if downloaded_path.exists():
                downloaded_path.rename(model_path)
            
            # Update config
            self.config["models"][model_name] = {
                "filename": local_filename,
                "repo_id": repo_id,
                "original_filename": filename,
                "size": model_path.stat().st_size
            }
            self.save_config()
            
            console.print(f"✅ Model {model_name} downloaded successfully!")
            return model_path
            
        except Exception as e:
            console.print(f"❌ Error downloading model: {e}")
            raise
    
    def list_models(self):
        """List all available models"""
        if not self.config["models"]:
            console.print("No models installed. Use 'easy-edge pull <model>' to download a model.")
            return
        
        console.print("\n[bold]Installed Models:[/bold]")
        for name, info in self.config["models"].items():
            size_mb = info.get("size", 0) / (1024 * 1024)
            status = "✅" if (self.models_dir / info["filename"]).exists() else "❌"
            console.print(f"  {status} {name} ({size_mb:.1f} MB)")
    
    def run_model(self, model_name: str, prompt: str = None, interactive: bool = False):
        """Run a model for inference"""
        model_path = self.get_model_path(model_name)
        
        if not model_path:
            console.print(f"❌ Model '{model_name}' not found. Use 'easy-edge pull <model>' to download it.")
            return
        
        try:
            console.print(f"Loading model {model_name}...")
            llm = Llama(
                model_path=str(model_path),
                n_ctx=2048,
                n_threads=os.cpu_count()
            )
            
            if interactive:
                self.interactive_chat(llm, model_name)
            else:
                if not prompt:
                    prompt = Prompt.ask("Enter your prompt")
                
                response = llm(
                    prompt,
                    max_tokens=self.config["settings"]["max_tokens"],
                    temperature=self.config["settings"]["temperature"],
                    top_p=self.config["settings"]["top_p"],
                    stop=["User:", "\n\n"]
                )
                
                console.print(Panel(response["choices"][0]["text"], title="Response"))
                
        except Exception as e:
            console.print(f"❌ Error running model: {e}")
    
    def interactive_chat(self, llm, model_name: str):
        """Interactive chat mode"""
        console.print(f"\n[bold]Chat with {model_name}[/bold] (type 'quit' to exit)")
        console.print("=" * 50)
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold blue]You[/bold blue]")
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not user_input.strip():
                    continue
                
                console.print("\n[bold green]Assistant[/bold green]")
                with console.status("Thinking..."):
                    response = llm(
                        user_input,
                        max_tokens=self.config["settings"]["max_tokens"],
                        temperature=self.config["settings"]["temperature"],
                        top_p=self.config["settings"]["top_p"],
                        stop=["User:", "\n\n"]
                    )
                
                console.print(response["choices"][0]["text"])
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                console.print(f"❌ Error: {e}")
        
        console.print("\nGoodbye!")

def parse_modelfile(modelfile_path):
    """Parse a Modelfile and return a dict of its instructions."""
    config = {
        'FROM': None,
        'PARAMETER': {},
        'SYSTEM': None,
        'MESSAGES': [],
        'HF_TOKEN': None,
        'TEMPLATE': None
    }
    with open(modelfile_path, 'r') as f:
        template_lines = []
        in_template = False
        for line in f:
            line = line.rstrip('\n')
            if not line or line.strip().startswith('#'):
                continue
            if line.startswith('FROM '):
                config['FROM'] = line[len('FROM '):].strip()
            elif line.startswith('PARAMETER '):
                param = line[len('PARAMETER '):].strip()
                key, value = param.split(' ', 1)
                config['PARAMETER'][key] = value
            elif line.startswith('SYSTEM '):
                config['SYSTEM'] = line[len('SYSTEM '):].strip()
            elif line.startswith('MESSAGE '):
                m = re.match(r'MESSAGE (\w+) (.+)', line)
                if m:
                    role, content = m.groups()
                    config['MESSAGES'].append({'role': role, 'content': content})
            elif line.startswith('HF_TOKEN '):
                config['HF_TOKEN'] = line[len('HF_TOKEN '):].strip()
            elif line.startswith('TEMPLATE '):
                in_template = True
                template_lines = [line[len('TEMPLATE '):].strip()]
            elif in_template:
                if line.strip() == '"""' or line.strip() == "'''":
                    in_template = False
                    config['TEMPLATE'] = '\n'.join(template_lines)
                else:
                    template_lines.append(line)
        if in_template:
            config['TEMPLATE'] = '\n'.join(template_lines)
    return config

@click.group()
@click.option('--models-dir', default='models', help='Directory to store models')
@click.version_option(version='1.0.0', prog_name='easy-edge')
@click.pass_context
def cli(ctx, models_dir):
    """Easy Edge - Run LLMs locally like Ollama"""
    ctx.ensure_object(dict)
    ctx.obj['easy_edge'] = EasyEdge(models_dir)

@cli.command()
@click.option('--url', help='Hugging Face URL to download the model')
@click.option('--repo-id', help='Hugging Face repository ID')
@click.option('--filename', help='Filename in the repository')
@click.pass_context
def pull(ctx, url, repo_id, filename):
    """Download a model (model name is automatically extracted)"""
    easy_edge = ctx.obj['easy_edge']
    
    if url:
        easy_edge.download_model(url)
    elif repo_id and filename:
        easy_edge.download_from_huggingface(repo_id, filename)
    else:
        console.print("❌ Please provide either --url or both --repo-id and --filename")
        console.print("\nExample:")
        console.print("  easy-edge pull --url https://huggingface.co/google/gemma-3-1b-it-qat-q4_0-gguf/resolve/main/gemma-3-1b-it-q4_0.gguf")
        console.print("  easy-edge pull --repo-id TheBloke/Llama-2-7B-Chat-GGUF --filename llama-2-7b-chat.Q4_K_M.gguf")

@cli.command()
@click.pass_context
def list(ctx):
    """List installed models"""
    easy_edge = ctx.obj['easy_edge']
    easy_edge.list_models()

@cli.command()
@click.argument('model_name')
@click.option('--prompt', '-p', help='Prompt to send to the model')
@click.option('--interactive', '-i', is_flag=True, help='Start interactive chat mode')
@click.pass_context
def run(ctx, model_name, prompt, interactive):
    """Run a model"""
    easy_edge = ctx.obj['easy_edge']
    easy_edge.run_model(model_name, prompt, interactive)

@cli.command()
@click.argument('model_name')
@click.pass_context
def remove(ctx, model_name):
    """Remove a model"""
    easy_edge = ctx.obj['easy_edge']
    
    if model_name not in easy_edge.config["models"]:
        console.print(f"❌ Model '{model_name}' not found")
        return
    
    model_path = easy_edge.get_model_path(model_name)
    if model_path and model_path.exists():
        model_path.unlink()
        console.print(f"✅ Removed model file: {model_path}")
    
    del easy_edge.config["models"][model_name]
    easy_edge.save_config()
    console.print(f"✅ Removed model '{model_name}' from configuration")

@cli.command()
@click.option('--modelfile', required=True, type=click.Path(exists=True), help='Path to the Modelfile')
@click.option('--output', required=True, type=click.Path(), help='Path to save the finetuned model (GGUF)')
@click.option('--name', required=False, type=str, help='Name to register the finetuned model (default: output filename without extension)')
@click.option('--epochs', required=False, type=int, default=3, help='Number of training epochs (default: 3)')
@click.option('--batch-size', required=False, type=int, default=2, help='Batch size (default: 2)')
@click.option('--learning-rate', required=False, type=float, default=2e-5, help='Learning rate (default: 2e-5)')
@click.pass_context
def finetune(ctx, modelfile, output, name, epochs, batch_size, learning_rate):
    """Finetune a model using a Modelfile (Ollama-style, Hugging Face Trainer, GGUF conversion)."""
    console.print(f"[bold green]Parsing Modelfile:[/bold green] {modelfile}")
    config = parse_modelfile(modelfile)
    # Helper to extract and convert parameters (must be defined before use)
    def get_param(key, default, typ):
        val = config['PARAMETER'].get(key, default)
        if typ == bool:
            return str(val).lower() in ['true', '1', 'yes']
        try:
            return typ(val)
        except Exception:
            return default
    models_dir = ctx.obj['easy_edge'].models_dir
    name = name if name else None
    model_name = name if name else Path(output).stem
    repo_id = config['FROM']
    messages = config['MESSAGES']
    hf_token = config.get('HF_TOKEN')
    # LoRA/PEFT parameters
    lora = get_param('lora', False, bool)
    load_in_4bit = get_param('load_in_4bit', False, bool)
    load_in_8bit = get_param('load_in_8bit', False, bool)
    lora_r = get_param('lora_r', 8, int)
    lora_alpha = get_param('lora_alpha', 32, int)
    lora_dropout = get_param('lora_dropout', 0.05, float)
    lora_target_modules = config['PARAMETER'].get('lora_target_modules', 'q_proj,v_proj').split(',')
    # 1. Download base model and tokenizer
    console.print(f"[bold blue]Downloading base model and tokenizer from Hugging Face: {repo_id}[/bold blue]")
    # Device selection
    device_param = config['PARAMETER'].get('device', None)
    if device_param:
        device = device_param.lower()
        if device not in ['cuda', 'cpu']:
            console.print(f"[bold yellow]Unknown device '{device}', defaulting to auto-detect.[/bold yellow]")
            device = None
    else:
        device = None
    if not device:
        if torch.cuda.is_available():
            n_gpus = torch.cuda.device_count()
            device = 'cuda'
            console.print(f"[bold green]GPU detected! Using CUDA with {n_gpus} GPU(s) for finetuning.[/bold green]")
        else:
            device = 'cpu'
            console.print("[bold yellow]No GPU detected. Training will run on CPU (much slower).[/bold yellow]")
    else:
        if device == 'cuda' and not torch.cuda.is_available():
            console.print("[bold yellow]Requested CUDA but no GPU found. Falling back to CPU.[/bold yellow]")
            device = 'cpu'
    # When loading model, move to device if possible
    try:
        tokenizer = AutoTokenizer.from_pretrained(repo_id, token=hf_token)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            console.print("[bold yellow]No pad_token found in tokenizer. Setting pad_token = eos_token.[/bold yellow]")
        model_kwargs = {}
        if lora:
            if load_in_4bit:
                model_kwargs['load_in_4bit'] = True
                model_kwargs['device_map'] = 'auto'
            elif load_in_8bit:
                model_kwargs['load_in_8bit'] = True
                model_kwargs['device_map'] = 'auto'
        model = AutoModelForCausalLM.from_pretrained(repo_id, token=hf_token, **model_kwargs)
        if lora:
            console.print(f"[bold green]LoRA/PEFT enabled. Wrapping model with LoRA adapters (r={lora_r}, alpha={lora_alpha}, dropout={lora_dropout}) targeting modules: {lora_target_modules}[/bold green]")
            lora_config = LoraConfig(
                r=lora_r,
                lora_alpha=lora_alpha,
                target_modules=lora_target_modules,
                lora_dropout=lora_dropout,
                bias='none',
                task_type=TaskType.CAUSAL_LM
            )
            model = get_peft_model(model, lora_config)
        model.to(device)
    except Exception as e:
        console.print(f"[bold red]Error downloading model/tokenizer or applying LoRA: {e}[/bold red]")
        return
    # 2. Create dataset from MESSAGE blocks
    console.print("[bold blue]Preparing dataset from Modelfile messages...[/bold blue]")
    data = []
    for i in range(0, len(messages), 2):
        if i+1 < len(messages) and messages[i]['role'] == 'user' and messages[i+1]['role'] == 'assistant':
            data.append({
                'instruction': messages[i]['content'],
                'output': messages[i+1]['content'],
                'user_message': messages[i],
                'assistant_message': messages[i+1]
            })
    if not data:
        console.print("[bold red]No valid user/assistant message pairs found in Modelfile![/bold red]")
        return
    # 2b. Format dataset using tokenizer.apply_chat_template if available, else use template
    formatted_data = []
    if hasattr(tokenizer, 'apply_chat_template'):
        console.print("[bold blue]Using tokenizer.apply_chat_template for prompt formatting...[/bold blue]")
        for ex in data:
            chat_messages = [
                {"role": "user", "content": ex['instruction']},
                {"role": "assistant", "content": ex['output']}
            ]
            formatted_data.append({'text': tokenizer.apply_chat_template(chat_messages, tokenize=False)})
    else:
        template = config.get('TEMPLATE')
        system_prompt = config.get('SYSTEM')
        if not template:
            template = """{{ .System }}\nUser: {{ .Prompt }}\nAssistant: {{ .Response }}"""
        def render_template(system, prompt, response, template):
            result = template
            if system is not None:
                result = result.replace('{{ .System }}', system)
            else:
                result = result.replace('{{ .System }}\n', '').replace('{{ .System }}', '')
            result = result.replace('{{ .Prompt }}', prompt)
            result = result.replace('{{ .Response }}', response)
            return result
        for ex in data:
            formatted_data.append({'text': render_template(system_prompt, ex['instruction'], ex['output'], template)})
    dataset = Dataset.from_list(formatted_data)
    # 3. Tokenize dataset
    # Use max_length from PARAMETER if present, else default to 2048
    try:
        max_length = int(config['PARAMETER'].get('max_length', 2048))
    except Exception:
        max_length = 2048
    def preprocess(example):
        return tokenizer(example['text'], truncation=True, padding='max_length', max_length=max_length)
    tokenized_dataset = dataset.map(preprocess, batched=False)
    # 4. Training
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = f"{tmpdir}/finetuned_model"
        console.print(f"[bold blue]Starting Hugging Face Trainer finetuning...[/bold blue]")
        # Extract parameters
        max_length = get_param('max_length', 2048, int)
        learning_rate = get_param('learning_rate', 2e-5, float)
        epochs = get_param('epochs', epochs, int)
        batch_size = get_param('batch_size', batch_size, int)
        weight_decay = get_param('weight_decay', 0.0, float)
        warmup_steps = get_param('warmup_steps', 0, int)
        gradient_accumulation_steps = get_param('gradient_accumulation_steps', 1, int)
        fp16 = get_param('fp16', False, bool)
        save_steps = get_param('save_steps', 500, int)
        logging_steps = get_param('logging_steps', 5, int)
        lr_scheduler_type = config['PARAMETER'].get('lr_scheduler_type', 'linear')
        eval_steps = get_param('eval_steps', None, int)
        save_total_limit = get_param('save_total_limit', None, int)
        seed = get_param('seed', None, int)
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            learning_rate=learning_rate,
            weight_decay=weight_decay,
            warmup_steps=warmup_steps,
            gradient_accumulation_steps=gradient_accumulation_steps,
            fp16=fp16,
            save_strategy='steps',
            save_steps=save_steps,
            logging_steps=logging_steps,
            lr_scheduler_type=lr_scheduler_type,
            report_to=[],
            seed=seed if seed is not None else 42,
            eval_steps=eval_steps,
            save_total_limit=save_total_limit,
        )
        data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=data_collator,
            # device_map is handled by model.to(device) above
        )
        try:
            trainer.train()
            trainer.save_model(output_dir)
            if lora:
                console.print("[bold blue]Saving LoRA adapter weights in models/ directory...[/bold blue]")
                adapter_dir = models_dir / f"{model_name}-lora-adapter"
                model.save_pretrained(str(adapter_dir))
                # Do NOT register adapter in config.json
                console.print("[bold blue]Merging LoRA adapters into base model before GGUF conversion...[/bold blue]")
                model = model.merge_and_unload()
                merged_dir = models_dir / f"{model_name}-merged"
                model.save_pretrained(str(merged_dir))
                # Do NOT register merged model in config.json
                # Use merged_dir for GGUF conversion
                output_dir = str(merged_dir)
        except Exception as e:
            console.print(f"[bold red]Error during training: {e}[/bold red]")
            return
        # Remove GGUF conversion and quantization steps
        # After training and saving merged model, print instructions for user
        console.print(f"[bold green]Finetuning complete! Your merged model is saved at: {output_dir}")
        console.print("[bold yellow]To use your model with llama.cpp, convert it to GGUF using convert_hf_to_gguf.py. Example:")
        console.print(f"python3 convert_hf_to_gguf.py --in {output_dir} --out <your-model>.gguf")
        console.print("[bold yellow]Then upload the GGUF file to your Hugging Face repo for easy download and use with llama.cpp![/bold yellow]")
        return

if __name__ == '__main__':
    cli() 