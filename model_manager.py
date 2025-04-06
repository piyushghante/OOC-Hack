from typing import Any, Dict, Optional, Tuple
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    PreTrainedTokenizerBase
)

def load_tokenizer(model_name: str) -> PreTrainedTokenizerBase:
    """
    Load and configure the tokenizer for the specified model.
    
    Args:
        model_name: Name or path of the model to load
        
    Returns:
        A configured tokenizer for the model
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Some models require specific configurations
        if tokenizer.pad_token is None:
            # GPT models typically don't have pad_token
            tokenizer.pad_token = tokenizer.eos_token
        
        return tokenizer
    
    except Exception as e:
        raise RuntimeError(f"Failed to load tokenizer for {model_name}: {str(e)}")

def load_model(model_name: str, device: str = "cpu") -> Any:
    """
    Load the language model and place it on the appropriate device.
    
    Args:
        model_name: Name or path of the model to load
        device: Device to place the model on ('cpu' or 'cuda')
        
    Returns:
        The loaded language model
    """
    try:
        # Determine if we need any special loading configurations
        # For Mistral and other large models, we might need to use lower precision
        if "mistral" in model_name.lower():
            # Load in 8-bit precision if on GPU to conserve memory
            if device == "cuda":
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    device_map="auto",
                    load_in_8bit=True,
                    torch_dtype=torch.float16
                )
            else:
                # On CPU, load with reduced precision
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    device_map={"": device},
                    low_cpu_mem_usage=True
                )
        else:
            # Default loading for smaller models
            model = AutoModelForCausalLM.from_pretrained(model_name)
            model = model.to(device)
        
        # Set to evaluation mode
        model.eval()
        
        return model
    
    except Exception as e:
        raise RuntimeError(f"Failed to load model {model_name}: {str(e)}")

def generate_text(
    model: Any,
    tokenizer: PreTrainedTokenizerBase,
    prompt: str,
    max_length: int = 512,
    temperature: float = 0.7,
    num_return_sequences: int = 1,
    device: Optional[str] = None
) -> str:
    """
    Generate text using the language model.
    
    Args:
        model: The language model
        tokenizer: The tokenizer for the model
        prompt: Text prompt to generate from
        max_length: Maximum length of the generated text
        temperature: Temperature for sampling (higher = more random)
        num_return_sequences: Number of sequences to generate
        device: Device to run on (if None, will use model's device)
        
    Returns:
        str: Generated text
    """
    try:
        # Prepare the inputs
        inputs = tokenizer(prompt, return_tensors="pt", padding=True)
        
        # Move to the appropriate device
        if device:
            inputs = {k: v.to(device) for k, v in inputs.items()}
        elif next(model.parameters()).device != torch.device("cpu"):
            inputs = {k: v.to(next(model.parameters()).device) for k, v in inputs.items()}
        
        # Generate text
        with torch.no_grad():
            # Truncate input if it's too long
            max_input_length = 512
            if inputs["input_ids"].shape[1] > max_input_length:
                inputs["input_ids"] = inputs["input_ids"][:, -max_input_length:]
                inputs["attention_mask"] = inputs["attention_mask"][:, -max_input_length:]
            
            output = model.generate(
                **inputs,
                max_new_tokens=128,  # Smaller, safer number of tokens
                temperature=temperature,
                num_return_sequences=num_return_sequences,
                pad_token_id=tokenizer.pad_token_id,
                do_sample=True,
                top_p=0.95,
                top_k=50,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3,
                early_stopping=True
            )
        
        # Decode and return the generated text
        if len(output) > 0 and len(output[0]) > 0:
            generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
            
            # Remove the prompt from the generated text if it appears at the beginning
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            return generated_text
        else:
            raise RuntimeError("No text was generated - the output tensor is empty")
    
    except Exception as e:
        raise RuntimeError(f"Text generation failed: {str(e)}")
