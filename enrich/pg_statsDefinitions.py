from enrich.computantions import get_abilityScoresModifiers,gey_abilityRef

class Pg_statsClass:
    def __init__(self,conf):
        self.conf= conf
        self.stats =  conf["stats"]
        self.skills =  conf["skills"]
        self.savingT =  conf["saving_throws"]

        self.proficiency_bonus =  conf["other"]["proficiency_bonus"]

    def makeComputations(self):
        self.computeModifiers()
        return self.conf
    
    def computeModifiers(self):
        statMods = {}

        for statName,value in self.stats.items():
            modifier=get_abilityScoresModifiers(value)
            statMods[statName+"_mod"] = modifier

        self.statMods=statMods
        self.conf["statMods"]=statMods

    def compute_skills(self):
        skillMods = {}

        for skillName,profToken in self.skills.items():
            statName=gey_abilityRef(skillName)
            skillMod=self._compute_modifier(statName,profToken)
            skillMods[statName] = skillMod

        self.skillMods=skillMods
        self.conf["skillMods"]=skillMods

    def compute_saving_throws(self):
        savingMods = {}
        for statName,profToken in self.savingT.items():
            skillMod=self._compute_modifier(statName,profToken)
            savingMods[statName] = skillMod

        self.savingMods=savingMods
        self.conf["savingMods"]=savingMods

    def _compute_modifier(self,name,profToken):
            modifier = self.statMods[ name+"_mod"]
            profModifier = 0
            if profToken == "*" :  profModifier=int(self.proficiency_bonus)
            if profToken == "**":  profModifier=(int(self.proficiency_bonus)*2)
            
            skillMod = modifier + profModifier
            if skillMod >=0 : skillModStr = "+" + str(skillMod) 
            else: skillModStr = str(skillMod)        
