import os
from typing import List

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
from optimum.onnxruntime import ORTModelForSeq2SeqLM, ORTModelForCausalLM

PREFIX = "semplifica: "
TOKENIZER_MAX_LENGTH = 1024

MT5_SMALL_MODEL_ID = "VerbACxSS/sempl-it-mt5-small"
UMT5_SMALL_MODEL_ID = "VerbACxSS/sempl-it-umt5-small"
GP2_SMALL_ITALIAN_MODEL_ID = "VerbACxSS/sempl-it-gpt2-small-italian"

class PredictionService:

    def __init__(self):
        self.mt5_small_tokenizer = AutoTokenizer.from_pretrained(MT5_SMALL_MODEL_ID)
        self.umt5_small_tokenizer = AutoTokenizer.from_pretrained(UMT5_SMALL_MODEL_ID)
        self.gpt2_small_italian_tokenizer = AutoTokenizer.from_pretrained(GP2_SMALL_ITALIAN_MODEL_ID)

        self.umt5_small_model = AutoModelForSeq2SeqLM.from_pretrained(UMT5_SMALL_MODEL_ID).eval() # UMT5 is not supported by ONNX

        if os.getenv('USE_ONNX', default = False):
            self.mt5_small_model = ORTModelForSeq2SeqLM.from_pretrained(MT5_SMALL_MODEL_ID, export=True)
            self.gpt2_small_italian_model = ORTModelForCausalLM.from_pretrained(GP2_SMALL_ITALIAN_MODEL_ID, export=True)
        else:
            self.mt5_small_model = AutoModelForSeq2SeqLM.from_pretrained(MT5_SMALL_MODEL_ID).eval()
            self.gpt2_small_italian_model = AutoModelForCausalLM.from_pretrained(GP2_SMALL_ITALIAN_MODEL_ID).eval()

    def predict_mt5_small(self, text: str) -> List[str]:
        prompt = PREFIX + text

        x = self.mt5_small_tokenizer([prompt], max_length=TOKENIZER_MAX_LENGTH, truncation=True, padding=True, return_tensors='pt').input_ids
        y = self.mt5_small_model.generate(input_ids=x, max_new_tokens=TOKENIZER_MAX_LENGTH, num_return_sequences=5, num_beams=5, early_stopping=True)

        return self.mt5_small_tokenizer.batch_decode(y, skip_special_tokens=True, clean_up_tokenization_spaces=True, max_length=TOKENIZER_MAX_LENGTH, truncation=True)


    def predict_umt5_small(self, text: str) -> List[str]:
        prompt = PREFIX + text

        x = self.umt5_small_tokenizer([prompt], max_length=TOKENIZER_MAX_LENGTH, truncation=True, padding=True, return_tensors='pt').input_ids
        y = self.umt5_small_model.generate(input_ids=x, max_new_tokens=TOKENIZER_MAX_LENGTH, num_return_sequences=5, num_beams=5, early_stopping=True)

        return self.umt5_small_tokenizer.batch_decode(y, skip_special_tokens=True, clean_up_tokenization_spaces=True, max_length=TOKENIZER_MAX_LENGTH, truncation=True)


    def predict_gpt2_small_italian(self, text: str) -> List[str]:
        prompt = f'### [Input]:\n{text}\n\n###[Output]:\n'

        x = self.gpt2_small_italian_tokenizer([prompt], max_length=TOKENIZER_MAX_LENGTH, truncation=True, padding=True, return_tensors='pt').input_ids
        y = self.gpt2_small_italian_model.generate(input_ids=x, max_new_tokens=TOKENIZER_MAX_LENGTH, num_return_sequences=5, num_beams=5, early_stopping=True)
        y_decs = self.gpt2_small_italian_tokenizer.batch_decode(y, max_length=TOKENIZER_MAX_LENGTH, truncation=True)

        return [y_dec.split("###[Output]:\n")[1].split('<|endoftext|>')[0].strip() for y_dec in y_decs if "###[Output]:\n" in y_dec]