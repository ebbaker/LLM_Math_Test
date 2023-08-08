from src.theorems.file_parser import Theorem_Wrapper
from src.proof_check.check_lean import try_proof
import json
import openai
import re
from lean_dojo import *
from src.theorems.csv_out import *

#This class is used as a catch all for the lean chat 
#Probably better to initiate this with __begin__ and __end__.  Also maybe split into more sub-classes, it's a bit bulky
class lean_chat:
    def __init__(self, thm:Theorem_Wrapper, examples, model, output_folder):
        self.thm=thm
        self.model=model
        self.hints = []
        self.num_hints=0
        self.whole_proof = False
        self.output_file = open(output_folder+self.thm.thm_name+".txt","w")
        self.proof_finished = False
        self.messages=[]
        self.add_message("system", "You are a lean theorem proving assistant.")
        self.add_message("user", "Help me complete the proofs of the following theorems, beginning the lean code with ```lean and ending with ```.  Also please provide the theorem statement for all lean code.")
        self.add_message("assistant","Sure, I would be happy to.")
        for ex in examples:
            theorem_msg = "Here is the statement of the theorem and the first 0 lines of the correct proof:\n```lean\n"+ex.thm_statement+"\n```\n Please attempt to solve this theorem in Lean."
            self.add_message("user", theorem_msg)
            proof_msg = "Certainly! Here is the completed proof:\n```lean\n"+ex.full_thm+"```"
            self.add_message("assistant", proof_msg)
        try:
            self.ld_thm = Theorem(thm.repo, thm.path, thm.thm_name)
        except:
            print(f"Error: no theorem named {self.thm_name}\n")
            self.ld_thm = None
    # Add message to messages and write to file.  Might need to include this in gpt_api.py if using with Llamma too, will be more general 
    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.messages.append(message)
        self.pp_file(message)
    # Request from gpt api, in retrospect this belongs in gpt_api.py
    def gpt_request(self, message, temperature=.6):
        self.add_message("user",message)
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=temperature,
        )
        message=response["choices"][0]["message"]["content"]
        self.add_message("assistant", message)
        return message
    # Give a certain number of lines of the correct proof 
    def populate_hints(self, num_hints):
        self.hints = []
        self.num_hints = num_hints
        proof=self.thm.proof
        if num_hints <= len(proof):
            self.hints = [f"  {hint}" for hint in proof[:num_hints]]
        else:
            self.hints = [f"  {hint}" for hint in proof]
            self.whole_proof = True
    # Generate partial proof for message
    def partial_proof(self, num_hints):
        self.populate_hints(num_hints)
        partial_proof = self.thm.thm_statement+" :=\nbegin\n"
        partial_proof += "\n".join(self.hints)
        message=""
        if num_hints>0:
            message += "I'm sorry, that is still not correct. "
        message += f"Here is the statement of the theorem and the first {self.num_hints} lines of the correct proof:\n```lean\n"
        message += partial_proof
        message += "\n```\n Please attempt to solve this theorem in Lean."
        return message 
    # Isolate proof from chat output and check it, returning feedback
    def compile_feedback(self,dojo,s0,gpt_output):
        status=0
        for i in range(3):
            attempt, status = self.isolate_proof(gpt_output)
            if status==1:
                break
            gpt_output=self.gpt_request(attempt)
        if status==0:
            print("Could not obtain unambiguous proof from output\n")
            return "Please write the theorem in the standard lean format starting with \"theorem (theorem_name)\" and ending with \"end\""
        message_out, self.proof_finished = try_proof(dojo,s0,attempt)
        return message_out
    # Pretty Print to file
    def pp_file(self, message):
        self.output_file.write(message["role"]+":\n")
        self.output_file.write(message["content"]+"\n\n")
        self.output_file.flush()
    # Close output_file (should be in __end__)    
    def close_output_file(self):
        self.output_file.close()
    def write_to_csv(self, file_name, num_compiles, notes):
        thm=self.thm
        add_new_csv_line(file_name, thm.thm_name, thm.num_tactics, self.proof_finished, self.num_hints, num_compiles, notes)  
    # Isolate proof from chat output
    def isolate_proof(self,gpt_output):
        lean_index = gpt_output.find("```lean")
        text_after_lean = gpt_output[lean_index:]
        if lean_index == -1:
            return "Please start all lean code with ```lean", 0 
        thm_index = text_after_lean.find(self.thm.thm_name)
        if thm_index == -1:
            return "Theorem name not found after \"```lean\". Please write the theorem in the standard lean format starting with \"theorem (theorem_name)\" and ending with \"end\"", 0
        begin_index = text_after_lean.find("begin")
        if begin_index == -1:
            return "Begin statement not found after theorem name. Please write the full theorem in the standard lean format."
        tquote_index = text_after_lean.find("```", begin_index+7)
        if tquote_index == -1:
            return "\"```\" not found after \"```lean\".",0
        full_thm = text_after_lean[:tquote_index]
        lines = full_thm[begin_index:].split("\n")
        previous_line = lines[len(lines)-2].strip()
        if previous_line.find("end")==-1:
            return "Lean code must end with end statment.",0    
        filtered_lines = [line.strip() for line in lines[1:len(lines)-2] if not line.startswith('--')]
        attempt = filtered_lines
        return attempt, 1
    