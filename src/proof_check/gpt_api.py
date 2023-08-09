import os
from src.proof_check.lean_chat import lean_chat
from lean_dojo import *
from src.theorems.file_parser import Theorem_Wrapper
import openai
from src.theorems.csv_out import *

def thm_chat(thm:Theorem_Wrapper, examples, num_lean_compiles, model, long_model, output_folder, csv_file, temperature=.6, lean_version="Lean 3"):
  chat = lean_chat(thm, examples, model, long_model, output_folder, lean_version)
  with Dojo(chat.ld_thm) as (dojo, s0):
    num_hints=0
    for num_hints in range(thm.num_tactics):
      message=chat.partial_proof(num_hints, trim_input=True)
      message=chat.gpt_request(message,temperature=temperature)
      message=chat.compile_feedback(dojo, s0, message)
      for compiles in range(num_lean_compiles):
        if chat.proof_finished:
          break
        message=chat.gpt_request(message,temperature=temperature)
        message=chat.compile_feedback(dojo, s0, message)
      if chat.proof_finished:
        break
  chat.write_to_csv(csv_file,num_lean_compiles,None)
  chat.close_output_file()
  
        
          
        
      
