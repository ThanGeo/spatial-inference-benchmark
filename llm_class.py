import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

class bcolors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    PURPLE = '\033[35m'
    MAGENTA = '\033[35m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

# Base LLM class
class LLM:
    llm_modelid = ""
    # default bnb quantization config - none
    bnb_config = BitsAndBytesConfig()
    model = None
    terminators = None
    tokenizer = None
    system_role = []

    def getSystemRole(self):
            return self.system_role
    
    def generateSystemRole(self):
        self.system_role = [{"role": "system", "content": "You are a bot that answers spatial reasoning questions."}]

    def loadModel(self):        
        # Load LLM
        self.tokenizer = AutoTokenizer.from_pretrained(self.llm_modelid)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.llm_modelid,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            quantization_config=self.bnb_config
            )
        # terminators
        self.terminators = []
        if self.tokenizer.eos_token_id is not None:
            self.terminators.append(self.tokenizer.eos_token_id)
        try:
            eot_id = self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
            if eot_id is not None:
                self.terminators.append(eot_id)
        except Exception:
            pass

    def generateAndDecode(self, messages):
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.model.device)
        outputs = self.model.generate(
            input_ids,
            max_new_tokens=4096,
            do_sample=True,
            eos_token_id=self.terminators,
            temperature=0.7,
            top_p=0.9,
        )
        response = outputs[0][input_ids.shape[-1]:]
        decoded_response = self.tokenizer.decode(response, skip_special_tokens=True)
        return decoded_response

    def generate(self, messages):
        # add the system role
        messages = self.getSystemRole() + messages
        return self.generateAndDecode(messages)

    # def __init__(self, llm_modelid):
    #     self.llm_modelid = llm_modelid
    #     self.loadModel()
    #     self.generateSystemRole()

# Plain LLM
class PlainLLM(LLM):
    def generate(self, prompt, k=0):
        messages = [{"role": "user", "content": "Question: " + prompt+"\n"}]
        return super().generate(messages)
    
    def __init__(self, llm_modelid, quantize_bits=None):
        # model id
        self.llm_modelid = llm_modelid
        # set quantization
        if quantize_bits == 4:
            self.bnb_config = BitsAndBytesConfig(load_in_4bit=True)
        elif quantize_bits == 8:
            self.bnb_config = BitsAndBytesConfig(
                load_in_8bit=True,
                # bnb_4bit_quant_type="nf4",  # or "fp4"
                # bnb_4bit_compute_dtype=torch.float16,
                # bnb_4bit_use_double_quant=True
            )   
        else:
            self.bnb_config = BitsAndBytesConfig()
        # load model (TE and LLM)
        self.loadModel()
        # set system role
        self.generateSystemRole()
