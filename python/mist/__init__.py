import saliweb.backend
import os
import subprocess
import re
import copy
import math
from operator import itemgetter 
import logging



class MyInputError(Exception):
    """Exception raised if something was wrong with the input file."""
    def __init__(self, msg):
        self.keyword = "input_error"
        self.msg = msg
    #def __str__(self):
    #    return repr(self.msg)
    pass


class InputFileCheck:

    def fileCheck(self,fileName):
		"""Check if input file is OK"""
		data = open(fileName,'rU')
		Lines = [i.strip().split('\t') for i in data.readlines()]
		data.close()


		# --- check lenghts
		Checker = True
		ErrorMessage = "\n"
		Lengths = [len(i) for i in Lines]
		if len(set(Lengths)) == 1: pass #print "Line lengths:      OK"
		else:
			L = len(Lines[0])
			for x,l in enumerate(Lines):
				if len(l) != L: 
					ErrorMessage += "\tLine %i disagrees with #Exp (%i)!\n" % (x+1,L)
					Checker = False

		# --- check if values
		Mistakes = []
		for x,l in enumerate(Lines):
			if x<3: continue
			for y,i in enumerate(l):
				if y==0 or y==1 or y==3: continue
				try: V = float(i)
				except ValueError: Mistakes.append((x+1,y+1))

		if len(Mistakes)==0: pass #print "Values in lines:   OK"
		else:
			for m in Mistakes:
				ErrorMessage += "\tElement in line %i, row %i is not a value!\n" % m		
				Checker = False

		# --- check experiment uniqueness
		if len(Lines[0][3:]) == len(set(Lines[0][3:])): pass #print "Experiments:       OK"
		else:
			for i in set(Lines[0][3:]):
				if Lines[0][3:].count(i)>1: 
					ErrorMessage += "\tExperiment %s repeated!\n" % i
					Checker = False
		
		# --- check prey uniqueness
		Preys = [i[0] for i in Lines[3:]]
		if len(Preys) == len(set(Preys)): pass #print "Preys:             OK"
		else:
			for i in set(Preys):
				if Preys.count(i)>1: 
					ErrorMessage += "\tPrey %s repeated!\n" % i
					Checker = False

		return (Checker, ErrorMessage)


class Job(saliweb.backend.Job):

	runnercls = saliweb.backend.SaliSGERunner


	def run(self):
		""" Run MiST on input file """
	
		paramsFile = open('param.txt','r')
                inputFile = 'input.txt'

                self.logger.setLevel(logging.INFO)

                self.logger.info("Beginning preprocess() for job %s " %self.name)


                Checker = InputFileCheck()
                inputStatus,errorMessage = Checker.fileCheck(inputFile)
                if inputStatus == True:
                    # input file is OK
                    self.logger.info("Input file is OK.")

		    trainingMode, filteringMode = [i.strip() for i in paramsFile.readlines()]
		    trainingM  = 0
		    filteringM = 0
		    if trainingMode == 'training': trainingM = 1
		    if filteringMode=='filtering': filteringM = 1
		    paramsFile.close()

		    script = """
module load mist
MiST.py %s output %i %i

sleep 17

""" % (inputFile, filteringM, trainingM)

		    r = self.runnercls(script)
        	    r.set_sge_options('-l o64=true -l diva1=1G')

        	    return r

                elif inputStatus == False:
                    # input file is NOT OK
                    self.logger.info("Input File not OK: %s" % errorMessage)
                    
                    script = '''python -c "print 1"'''

                    r = self.runnercls(script)
                    r.set_sge_options('-l o64=true -l diva1=1G')

                    return r
            


	def postprocess(self):
	        """Combine the three files"""

        	try:
			data1 = open('output.log','r')
      			data2 = open('output_metrics.out','r')
        		data3 = open('output_mist.out','r')
		except IOError: return 0


        	D1 = data1.readlines()
        	D2 = data2.readlines()
        	D3 = data3.readlines()

        	data1.close(); data2.close(); data3.close()

        	newOutput = open('MistOutput.txt','w')

        	for d in D1: newOutput.write('# ' + d)

        	Ints = {}
        	for d in D2[1:]:
        	        b,p,r,a,s = d.strip().split('\t')
        	        Ints[(b,p)] = [r,a,s]
        	for d in D3[1:]:
        	        b,p,m = d.strip().split('\t')
        	        if (b,p) in Ints: Ints[(b,p)].append(m)

        	interactions = [tuple(list(i)+Ints[i]) for i in Ints if len(Ints[i])==4]
        	ints = sorted(interactions,key=itemgetter(5),reverse=True)
        	newOutput.write('\n#'+'\t'.join(['Bait','Prey','Reproducibility','Abundance','Specificity','MiST'])+'\n')
        	for i in ints: newOutput.write('\t'.join(list(i))+'\n')
        	newOutput.close()



def get_web_service(config_file):
    db = saliweb.backend.Database(Job)
    config = saliweb.backend.Config(config_file)
    return saliweb.backend.WebService(config, db)
	

		
		
		






