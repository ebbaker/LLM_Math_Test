import random
from src.theorems.file_parser import Theorem_Wrapper

# Create a class named OrganizedTheorems
class Organized:
    def __init__(self, thms):
        self.categories = {
            "algebra": [],
            "numbertheory": [],
            "amc": [],
            "aime": [],
            "other": []
        }
        self.organize_theorems(thms)
    
    def organize_theorems(self, thms):
        for thm in thms:
            thm_name = thm.thm_name
            if "algebra" in thm_name.lower():
                thm.set_category("algebra")
                self.categories["algebra"].append(thm)
            elif "numbertheory" in thm_name.lower():
                thm.set_category("numbertheory")
                self.categories["numbertheory"].append(thm)
            elif "amc" in thm_name.lower():
                thm.set_category("amc")
                self.categories["amc"].append(thm)
            elif "aime" in thm_name.lower():
                thm.set_category("aime")
                self.categories["aime"].append(thm)
            else:
                thm.set_category("other")
                self.categories["other"].append(thm)
    
    def retrieve_theorem(self, name):
        for category, theorems in self.categories.items():
            for theorem in theorems:
                if theorem.thm_name == name:
                    return theorem
        return None
    
    def count_common_proof_commands(self, proof1, proof2):
        proof1_commands = [line.split()[0] for line in proof1 if line.strip()]
        proof2_commands = [line.split()[0] for line in proof2 if line.strip()]
        count = len(set(proof1_commands) & set(proof2_commands))
        return count

    # Return num_theorems similar theorems or random depending on the value of similarity
    def select_theorems(self, thm_name, num_theorems=1, similarity=True):
      thm_in = self.retrieve_theorem(thm_name)
      category = thm_in.category
      #theorem_set=self.categories[category]
      theorem_set = [x for x in self.categories[category] if x.thm_name!=thm_name and len(x.proof)<10]
      
      if similarity:
          sorted_theorems = sorted(
              theorem_set, 
              key=lambda x: (
                  self.count_common_proof_commands(x.proof, thm_in.proof) 
              ),
              reverse=True
          )
          selected_theorems = sorted_theorems[:num_theorems]
      else:
          selected_theorems = random.sample(theorem_set, num_theorems)
      
      return selected_theorems