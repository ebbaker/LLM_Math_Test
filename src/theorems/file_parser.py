from lean_dojo import *

class Theorem_Wrapper:
    
    ld_thm : Theorem
    
    def __init__(self, repo, path):
        self.thm_name = None
        self.thm_statement = None
        self.full_thm = None
        self.proof = None
        self.category = None
        self.num_tactics = None
        self.repo=repo
        self.path=path
    def populate_subfields(self, thm_name, thm_statement, full_thm, proof):
        self.thm_name = thm_name
        self.thm_statement = thm_statement
        self.full_thm = full_thm
        self.proof = proof
        self.num_tactics = len(self.proof)
    def set_category(self,cin:str):
        self.category=cin
    def pp_proof(self):
        seperator="\n  "
        out=" "+seperator.join(self.proof)
        return out       

def parse_lean_file(file_path, repo, path):
    thms = []
    with open(file_path, 'r') as file:
        content = file.read()
        thm_split = content.split("theorem")
        for i in range(1, len(thm_split)):
            thm=Theorem_Wrapper(repo, path)
            sub_split = thm_split[i].split(":=")
            thm_lines = thm_split[i].strip().splitlines()
            thm_name = thm_lines[0].strip().split()[0].strip()
            thm_statement = "theorem " + sub_split[0]
            full_thm = "theorem " + thm_split[i]
            proof_start_index = full_thm.index(":=") + 9
            proof_end_index = len(full_thm) - 6
            proof = full_thm[proof_start_index:proof_end_index].split("\n")
            proof = [line.strip() for line in proof]
            # Split the proof at the "begin" and "end" commands
            if "sorry" in full_thm.lower():
                continue
            thm.populate_subfields(thm_name,thm_statement,full_thm,proof)
            thms.append(thm)
    thm_names = [thm.thm_name for thm in thms]
    return thms, thm_names

