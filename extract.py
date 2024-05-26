# import torch
# import transformers
import ast


def load_llm():
    # model_id = "HPAI-BSC/Llama3-Aloe-8B-Alpha"

    # pipeline = transformers.pipeline(
    #     "text-generation",
    #     model=model_id,
    #     model_kwargs={"torch_dtype": torch.bfloat16},
    #     low_cpu_mem_usage=True
    # )

    # Returning the dummy pipeline
    pipeline = "dummy pipeline"
    return pipeline


def setup_prompt(html_block):
    questions = ['What is the name of the product?',
                 'What is the price of that product?',
                 'A brief description about the product?',
                 'is there any image associated with that product?']

    answer_direction = f"Please provide answer of the questions in a json format by analyzing the html content provided. also provide their corresponding CSS selectors.\
                    Don't generate anything else ,not even a character other than the json output staring with a curly brace so that i can access the answer easily."

    example = '''{
        "product-name":{
            "selector": replace with CSS selector,
            "answer": replace with actual name of the product as provided in html content
        },
        "product-price": {
            "selector": replace with CSS selector,
            "answer": replace with price of the product as provided in html content
        },
        "product-description": {
            "selector": replace with CSS selector,
            "answer": replace with product description as provided in html content
        },
        "product-image": {
            "selector": replace with CSS selector,
            "answer": replace with image link if available in html content
        }
    }'''

    messages = [
        {"role": "system", "content": f"You are a expert system at analyzing the hypertext markup langugage and answering question on such context. Here is a small html content{html_block} for you to analyze."},
        {"role": "user", "content": f"Here are multiple questions you need to answer {questions}. {answer_direction} here is an example for you. {example}"},
    ]

    return messages


def generate_output(pipeline, messages):
    # prompt = pipeline.tokenizer.apply_chat_template(
    #     messages,
    #     tokenize=False,
    #     add_generation_prompt=True
    # )

    # terminators = [
    #     pipeline.tokenizer.eos_token_id,
    #     pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    # ]

    # outputs = pipeline(
    #     prompt,
    #     max_new_tokens=256,
    #     eos_token_id=terminators,
    #     do_sample=True,
    #     temperature=0.6,
    #     top_p=0.9
    # )

    # return outputs[0]["generated_text"][len(prompt):]

    # returning the dummy output because this LLM is too big to run locally
    return str({"pipeline": pipeline,
                "messages": messages})


def extract_product_info(html_block, pipeline):

    messages = setup_prompt(html_block)

    result = generate_output(pipeline, messages)

    # you can also try this data to see what happens. when uncommenting this, dont forget to comment the 'data' given below.
    # data = str(result)

    # this is the one of the result generated from the LLM when tested at google colab.
    # you can try to send this data as a response to see if api is working

    data = str({
        "dummy product-name": {
            "selector": ".product-details h2",
            "answer": "907gm Brown Basmati Rice"
        },
        "dummy product-price": {
            "selector": ".product-details p.product-price",
            "answer": "$24.56"
        },
        "dummy product-description": {
            "selector": ".product-details p.product-description",
            "answer": "Long grains, Nice Aroma, Cooks Fast"
        },
        "dummy product-image": {
            "selector": ".product-image img",
            "answer": "https://images-cdn.ubuy.co.in/63402ef469382d3105512dcf-royal-brown-basmati-rice-32-oz.jpg"
        }
    })
    return ast.literal_eval(data)
