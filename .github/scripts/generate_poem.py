from transformers import pipeline, set_seed

def generate_poem():
    # Load the GPT-2 model pipeline
    generator = pipeline("text-generation", model="gpt2")
    set_seed(42)  # For reproducibility

    prompt = "Write a short poem about GitHub pull requests."

    print("🎉 Poem Generated:\n")
    poem = generator(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]
    print(poem)

if __name__ == "__main__":
    generate_poem()
