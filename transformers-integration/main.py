# Due to the size of the model, it won't be integrated in the main code to run locally, optionally you can see a snip below of how it should be.
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "mistralai/Mistral-7B-Instruct-v0.2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")
# Here is where you put your prompt, I won't update this file because I won't download the model in the repository, this is just a test for loading the model locally.
prompt = ""
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)


output = model.generate(**inputs, max_length=200, temperature=0.7, top_p=0.9)

response = tokenizer.decode(output[0], skip_special_tokens=True)

print(response)