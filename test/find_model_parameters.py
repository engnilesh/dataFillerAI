from transformers import AutoModelForCausalLM

# Load deepset/roberta-base-squad2 model
model = AutoModelForCausalLM.from_pretrained("deepset/roberta-base-squad2")

# Count total parameters
total_params = sum(p.numel() for p in model.parameters())

print(f"Total Parameters: {total_params:,}")  # Prints in a human-readable format

trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Trainable Parameters: {trainable_params:,}")

