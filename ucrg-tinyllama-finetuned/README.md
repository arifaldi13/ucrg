---
license: mit
language:
- en
---

# Fine-tuned TinyLlama for Utility Compliance Report Generation (UCRG)

This repository contains the fine-tuned weights for a `TinyLlama-1.1B` model, specialized for generating natural-language compliance reports from structured JSON data.

This model is the AI core of the **Utility Compliance Report Generator (UCRG)**, a full-stack proof-of-concept project demonstrating an end-to-end AI application workflow.

<br>

▶️ **[Live Demo](https://rifukawa-ucrg.vercel.app/)**  |  📖 **[GitHub Repository](https://github.com/arifaldi13/ucrg**

---

## 🚀 Project Overview

The UCRG project showcases the entire lifecycle of a modern AI application:

1.  **Problem Definition:** Automating the tedious task of writing compliance summaries from raw incident data.
2.  **Data Curation:** Creating a custom, high-quality dataset for a specialized task.
3.  **Model Fine-tuning:** Taking a powerful base model and adapting it to understand the specific domain language and format.
4.  **API Development:** Building a robust Flask backend to serve the model's predictions.
5.  **Frontend & Deployment:** Creating an intuitive React UI and deploying the full system to the cloud.

This model was trained to translate JSON objects describing utility incidents (like power outages or gas leaks) into clear, concise, human-readable summaries suitable for internal reporting or regulatory review.

## 💡 Model Details

*   **Base Model:** [`TinyLlama/TinyLlama-1.1B-Chat-v1.0`](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)
*   **Fine-tuning Technique:** Low-Rank Adaptation (LoRA) using the `peft` and `trl` libraries.
*   **Training Data:** A custom-generated dataset of 50+ examples mapping JSON incident data to natural-language reports. The data was structured in an instruction format to optimize for the `instruct` base model.

### Prompt Format

The model was trained using a specific instruction-following prompt format. To get the best results, your input should follow this structure:

```
### Instruction:
Generate a compliance report summary from the following structured data.

### Input:
{ "incident_type": "Power Outage", "duration": "3 hours", "location": "Zone 4", "resolved": true }

### Response:
```

## 🛠️ How to Use This Model

This model is served via a public Flask API as part of the full application. The easiest way to use it is through the **[live demo](https://rifukawa-ucrg.vercel.app/)**.

For programmatic use, you can load the base model and apply this LoRA adapter:

```python
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Define model paths
base_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
adapter_path = "rifukawa/ucrg-tinyllama-finetuned"

# Load tokenizer and base model
tokenizer = AutoTokenizer.from_pretrained(base_model_name)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype=torch.float16,
    device_map="auto",
)

# Load the LoRA adapter
model = PeftModel.from_pretrained(base_model, adapter_path)

# Create a text-generation pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Prepare the prompt
prompt = """### Instruction:
Generate a compliance report summary from the following structured data.

### Input:
{ "incident_type": "Gas Leak", "duration": "45 minutes", "location": "Substation B", "resolved": true }

### Response:
"""

# Generate the report
result = generator(prompt, max_new_tokens=100, do_sample=False)
print(result[0]['generated_text'].split("### Response:")[1].strip())

# Expected output:
# A gas leak occurred at Substation B. The event lasted for 45 minutes. The issue has been resolved.
```

## Limitations and Considerations

This model is a proof-of-concept and was trained on a small, simulated dataset.

*   **Factuality:** The model may "hallucinate" or fail to accurately represent all fields from the input JSON, especially for complex or unseen data structures. For example, it may incorrectly state an issue is resolved.
*   **Scalability:** For a production environment, this model would require a much larger and more diverse training dataset, along with a rigorous validation framework to ensure factual accuracy.

Despite these limitations, it effectively demonstrates the viability of using fine-tuned smaller LLMs for specialized, high-value automation tasks.