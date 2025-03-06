from transformers import AutoConfig

# Load the config of a pre-trained deepset/roberta-base-squad2 model
config = AutoConfig.from_pretrained("deepset/roberta-base-squad2")

# Print the configuration details
print(config)
