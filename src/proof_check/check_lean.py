from lean_dojo import *
from src.theorems.file_parser import Theorem_Wrapper

def try_proof(dojo, s0, proof_tacs):
    s_new=s0
    message_out=""
    proof_finished=0
    for i in range(len(proof_tacs)):
        s_new = dojo.run_tac(s_new, proof_tacs[i].strip())  
        if isinstance(s_new,TacticError):
            message_out+=f"Tactic Error at line {i} of proof: \n"
            message_out+=s_new.error
            break
        elif isinstance(s_new,TacticState):
            if i==len(proof_tacs)-1:
                message_out+="Proof was not finished, proof state is given by:\n"
                message_out+=s_new.pp
                break
            else:
                continue
        elif isinstance(s_new,ProofFinished):
            message_out+=f"Proof Finished at line {i}: "
            if s_new.message!=None:
                message_out+=s_new.message
            proof_finished=1
            break    
        elif isinstance(s_new,TimeoutError):
            message_out+=f"Timeout Error at line {i}: \n"
            message_out+=s_new.error
            break
        elif isinstance(s_new,ProofGivenUp):
            message_out+=f"Proof given up at line {i}\n"
            break
        else:
            print("Error: did not recognize lean_dojo output")
            break
    return message_out, proof_finished




