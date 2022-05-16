# -*- coding: utf-8 -*-

# importing modules useds in this program
from ssl import RAND_add
import pandas as pd
import random
import glob
import math
import time
from datetime import datetime

class Interactions:
    """
    Class Interactions: this class is used for mapping each parameters in one interecation, this informations coming to cvs' files.
        
    """

    # atributes of this class
    idinteracao=0
    nome_interacao=""
    min_valor=0
    max_valor=0
    context=""
    observable=None
    readonly=None
    idconcept_context=0
    idconcept_unit_measurement=0
    formula=""

    idconcept=0
    idontology=0
    concept=""

    idontology=0
    url=""
    shortname=""
    unit_of_measurement=""


    df_idconcept = None
    df_idinteracao = None
    df_idontology = None
    df_idvirtual_thing = None
    df_idvt_interacao = None

    def __init__(self) -> None:  # It's a constructor of this class 
        # In below line is calling methods for read csv's files and 
        # choice interaction randomly
        self.read_csv() 
        self.random_choice_interaction()

    def read_csv(self) -> None: # read csv's files to create one intereaction
        cont = 0
        dfs = []
        # run about all csv's files and get your names and store them in one list
        for files in glob.glob("*.csv"):
            dfs.append(pd.read_csv(files))
            """ df_idconcept 
                df_idinteracao 
                df_idontology 
                df_idvirtual_thing
                df_idvt_interacao
            """
        # This loop store each data in your match dataframe    
        for df in dfs:
            if 'idconcept' == df.columns[1]:
                self.df_idconcept = df
            elif 'idinteracao' == df.columns[1]:
                self.df_idinteracao = df
            elif 'idontology' == df.columns[1]:
                self.df_idontology = df
            #elif 'idvirtual_thing' == df.columns[1]:    
            #    self.df_idvirtual_thing = df
            #elif 'idvt_interacao' == df.columns[1]:
            #    self.df_idvt_interacao = df

    # This method choose one interaction using random module         
    def random_choice_interaction(self):
        # randomic choice interaction
        df = self.df_idinteracao
        random_number = random.randint(0, df.shape[0]-1)
        # get interaction using the filter with id randomic choiced
        df_interacao = df.query("id ==  + {}".format(random_number))
        # get concepts using the filter with intecraction's idconcept 
        df_concept = self.df_idconcept
        idconcept = int(df_interacao.idconcept_context.iloc[0])
        df_concept = df_concept.query("idconcept ==  + {}".format(idconcept))
        # get ontologies using the filter with concept's idontology 
        df_ontology = self.df_idontology
        idontology = int(df_concept.idontology.iloc[0])
        df_ontology = df_ontology.query("idontology ==  + {}".format(idontology))  
        # get concepts using the filter with intecraction's idconcept_unit_measurement 
        df_concept = self.df_idconcept
        idconcept_unit_measurement = int(df_interacao.idconcept_unit_measurement.iloc[0])
        df_concept_unit_measurement = df_concept.query("idconcept ==  + {}".format(idconcept_unit_measurement))

        # mounting interaction
        self.idinteracao=df_interacao.idinteracao.iloc[0]
        self.nome_interacao=df_interacao.nome_interacao.iloc[0]
        self.min_valor=df_interacao.min_valor.iloc[0]
        self.max_valor=df_interacao.max_valor.iloc[0]
        self.context=df_interacao.context.iloc[0]
        self.observable=df_interacao.observable.iloc[0]
        self.readonly=df_interacao.readonly.iloc[0]
        self.idconcept_context=df_interacao.idconcept_context.iloc[0]
        self.idconcept_unit_measurement=df_interacao.idconcept_unit_measurement.iloc[0]
        self.formula=df_interacao.formula.iloc[0]
        # mounting concepts
        self.idconcept=df_concept.idconcept.iloc[0]
        self.idontology=df_concept.idontology.iloc[0]
        self.concept=df_concept.concept.iloc[0]
        # mounting ontologies
        self.idontology=df_ontology.idontology.iloc[0]
        self.url=df_ontology.url.iloc[0]
        self.shortname=df_ontology.shortname.iloc[0]
        # mounting the unit of measurement
        self.unit_of_measurement=df_concept_unit_measurement.concept.iloc[0]

class VirtualThingFileGenerator:
    """
    Class VirtualThingFileGenerator: this class is used for create the thing.
    
    """
    # atributes of this class
    vt_thing = ""
    WoT_produce = ""
    then = ""
    list_interactions = None
    thing_name = ""
    run_time = 0

    def __init__(self, number_of_interactions) -> None: # It's a constructor of this class 
        self.run_time = time.time()# start count time to make log file
        # In below line is calling methods for create and produce the thing  
        self.WoT_produce_create(number_of_interactions)
        self.then_create()
        self.create_thing()
    
    def WoT_produce_create(self, number_of_interactions) -> None: # This method create json of thing
        # create interactions
        self.list_interactions = [Interactions() for i in range(number_of_interactions)]       
        TITLE = ''.join(chr(random.randrange(65,90)) for i in range(20))
        self.thing_name = TITLE
        DESCRIPTION = "VirtualThingFileGenerator: 1.0"
        SUPPORT = "git://github.com/eclipse/thingweb.node-wot.git"
        # including context
        CONTEXT = "iot: \"http://example.org/iot\"" 
        cont = 0
        element_context = ""
        for c in self.list_interactions:
            if not str(c.context)=="nan":
                element_context += " " + (c.context.split(":",1)[0] + ":" + "\"" + c.context.split(":",1)[1] + "\"") + "," 
            cont += 1   

        if cont != 0:
           CONTEXT += "," + element_context

        CONTEXT = CONTEXT[:-1]
        INTERACTIONS = []
        ACTIONS = []
        for c in self.list_interactions:
            # \"""" + str(c.unit_of_measurement) + """\"
            # \"""" + str(c.concept) + """\"
            INTERACTIONS.append(
                """\t\t\t"""+str(c.nome_interacao) + """: {
                type: "integer",
                description: \"null\",
                unit: \"%\",
                observable: """ + str(c.observable).lower() + """,
                readOnly: """ + str(c.readonly).lower() + """,
                writeOnly: false,
            }""")
        
        for c in self.list_interactions:
            ACTIONS.append("""
                keep_""" + str(c.nome_interacao) + """ : {
                description: "Action """ + str(c.nome_interacao) + """",
            }""") 

        self.WoT_produce = """
    function checkPropertyWrite(expected, actual) { 
        var output = "Property " + expected + " written with " + actual;
        if (expected === actual) { 
            console.info("PASS: " + output);
        }
        else {
            throw new Error("FAIL: " + output);
        }
    }
    function checkActionInvocation(name, expected, actual) {
        var output = "Action " + name + " invoked with " + actual;
        if (expected === actual) {
            console.info("PASS: " + output);
        }
        else {
            throw new Error("FAIL: " + output);
        }
    }    
    WoT.produce({
        title: \"""" + TITLE + """\",
        description: \"""" + DESCRIPTION + """\",
        support: \"""" + SUPPORT + """\",
        "@context": [
            "https://www.w3.org/2019/wot/td/v1",
            "https://www.w3.org/2022/wot/td/v1.1",
            { """ + CONTEXT + """ },
        ],
        properties: {\n """+"\n".join(str(i) + "," for i in INTERACTIONS)+ """

        },
        actions: { """ + "".join(str(a) + "," for a in ACTIONS)+ """

        },
    })"""
        self.vt_thing += self.WoT_produce

    def then_create(self) -> None: # create the thing's operation 

        SET_PROPERTY_HANDLERS = []

        for c in self.list_interactions:
            SET_PROPERTY_HANDLERS.append("""thing.setPropertyReadHandler(\"""" + c.nome_interacao + """\", async () => 0.0);""")

        SET_ACTIONS_HANDLERS = []    
        for c in self.list_interactions:
            str_actions ="\nthing.setPropertyReadHandler(\"" + c.nome_interacao + "\", () => {\n"
            str_actions +="  \t\t\treturn new Promise(function (resolve, reject) {\n"
            str_actions +="		\t\tconsole.log(\"" + c.nome_interacao + "\");\n"
            str_actions +="		\t\tresolve(" + c.formula + ");\n"
            str_actions +="	\t\t});\n"
            str_actions +="\t\t});"

            str_actions=str_actions.replace("MAX", str(c.max_valor))
            str_actions=str_actions.replace("MIN", str(c.min_valor))
            SET_ACTIONS_HANDLERS.append(str_actions)

        self.then = """
    .then((thing) => {
        console.log(\"Produced \" + thing.getThingDescription().title);

        // set property handlers (using async-await) 
        """ + "\n".join(str(p) for p in SET_PROPERTY_HANDLERS) + """

        // set action handlers (using async-await)
        """ + "\n".join(str(p) for p in SET_ACTIONS_HANDLERS) + """

        // expose the thing
        thing.expose().then(() => {
            console.info(thing.getThingDescription().title + " ready");
        });
    })
    .catch((e) => {
        console.log(e);
    });
    """
        self.vt_thing += self.then;

    def create_thing(self) -> float:
        # open file for save JS file
        f = open("things/THING_" + self.thing_name + ".js", "w")
        # write in folder
        f.write(self.vt_thing)
        # close file
        f.close()
        # print("THING_{}.js was generated in folder thing in this root directory!".format(self.thing_name))
        # open file for save JS file
        f = open("log/LOG_" + self.thing_name + "_" +datetime.now().strftime("%H-%M-%S") + ".txt", "a")
        # calculate time of execution
        self.run_time = time.time() - self.run_time
        # write in folder
        f.write("log/LOG_" + self.thing_name + "_" +datetime.now().strftime("%H:%M:%S") + " - creation time: " + str(self.run_time) + " seconds")
        # close file
        f.close()

if __name__ == "__main__":
    f = open("log/ALL_" +datetime.now().strftime("%H-%M-%S") + ".txt", "a")
    run_time = time.time()
    # number of instances
    q = 1000
    for i in range(q):
        vtc = VirtualThingFileGenerator(2)
    # write in folder
    f.write("Number of instances: " + str(q) + " - Creation time: " + str(time.time() - run_time) + " seconds")
    # close file
    f.close()