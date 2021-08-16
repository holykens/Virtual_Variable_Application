import sqlite3
import pandas
import csv
import re

class Database:

    def __init__(self):                      #Function to create SQL database                                  
        self.conn=sqlite3.connect("lite.db")         #Establish self.connection to lite.db
        self.cur=self.conn.cursor()                       #Create self.cursor object in dataase
        self.cur.execute("CREATE TABLE IF NOT EXISTS calculation (ID INTEGER PRIMARY KEY,Station_ID INTEGER,Variable TEXT,\
                        Variable_ID INTEGER,Unit_ID INTEGER,Formula TEXT,RoC_Active INTEGER,RoC_Precision INTEGER,\
                        RoC_Period_Value INTEGER,RoC_Period_Type INTEGER,RoC_Unit_Value INTEGER,RoC_Unit_Type INTEGER,\
                        Datum_Variable_ID INTEGER,Datum_Timestamp TEXT,Datum_Information TEXT,Constants TEXT)")         #Create SQL table if it does not exist
        self.conn.commit()                   #Commit changes in database

    def calculate(self, Building_callsign, AllPrisms, NW_Prism, NE_Prism, SW_Prism, SE_Prism, NS_Distance, WE_Distance, Station_ID, Variable_ID):  #Function to calculate deformations and displacements
        VVListofLists=[]                            #Assign an empty list to VVListofLists
        VVList=[]                                   #Assign an empty list to VVList
        Tassgloname=Building_callsign + "Tass_Glo"  #Assign Tassgloname to the name of Tassement Global variable with corresponding to building's name
        ListAllPrisms=AllPrisms.split("+")          #Create a list with all Prisms in AllPrisms input box
        TasGLO="("+AllPrisms+")"+"/"+str(len(ListAllPrisms))        #Assign TasGLO as the calculation for Tassement Global
        VVList=[Station_ID,Tassgloname,Variable_ID,42,TasGLO]       #Put Station_ID,Tassgloname,Variable_ID,42,TasGLO into VVList of self.current input
        VVListofLists.append(VVList)                #Append VVList to VVListofLists

        if (NW_Prism!="" and SW_Prism!="") or (NE_Prism!="" and SE_Prism!=""):      #Conditional for Tassement differentiel NS calculation is possible
            TasDifNSname=Building_callsign + "Tass_Diff_NS"                         #Assign TasDifNSname to the name of Tassement differentiel NS variable with corresponding to building's name
            
            if NW_Prism!="" and SW_Prism!="" and NE_Prism!="" and SE_Prism!="":     #Conditional for all prisms inputs are not empty
                TasDifNS="("+"("+"Z"+str(NW_Prism)+"+"+"Z"+str(NE_Prism)+")"+"/"+"2"+"-"+"("+"Z"+str(SW_Prism)+"+"+"Z"+str(SE_Prism)+")"+"/"+"2"+")"+"/"+str(NS_Distance)  #Assign TasDifNS as the calculation for Tassement Differentiel NS

            elif NW_Prism!="" and SW_Prism!="" and NE_Prism!="" and SE_Prism=="":       #Conditional for SE_Prism input box is empty
                TasDifNS="("+"("+"Z"+str(NW_Prism)+"+"+"Z"+str(NE_Prism)+")"+"/"+"2"+"-"+"Z"+str(SW_Prism)+")"+"/"+str(NS_Distance) #Assign TasDifNS as the calculation for Tassement Differentiel NS

            elif NW_Prism!="" and SW_Prism!="" and NE_Prism=="" and SE_Prism!="":       #Conditional for NE_Prism input box is empty
                TasDifNS="("+"Z"+str(NW_Prism)+"-"+"("+"Z"+str(SW_Prism)+"+"+"Z"+str(SE_Prism)+")"+"/"+"2"+")"+"/"+str(NS_Distance)     #Assign TasDifNS as the calculation for Tassement Differentiel NS     
            
            elif NW_Prism!="" and SW_Prism=="" and NE_Prism!="" and SE_Prism!="":       #Conditional for SW_Prism input box is empty
                TasDifNS="("+"("+"Z"+str(NW_Prism)+"+"+"Z"+str(NE_Prism)+")"+"/"+"2"+"-"+"Z"+str(SE_Prism)+")"+"/"+str(NS_Distance)     #Assign TasDifNS as the calculation for Tassement Differentiel NS
            
            elif NW_Prism=="" and SW_Prism!="" and NE_Prism!="" and SE_Prism!="":       #Conditional for NW_Prism input box is empty
                TasDifNS="("+"Z"+str(NE_Prism)+"-"+"("+"Z"+str(SW_Prism)+"+"+"Z"+str(SE_Prism)+")"+"/"+"2"+")"+"/"+str(NS_Distance)     #Assign TasDifNS as the calculation for Tassement Differentiel NS

            elif NW_Prism!="" and SW_Prism!="" and NE_Prism=="" and SE_Prism=="":       #Conditional for NE_Prism and SE_Prism input boxes are empty
                TasDifNS="("+"Z"+str(NW_Prism)+"-"+"Z"+str(SW_Prism)+")"+"/"+str(NS_Distance)       #Assign TasDifNS as the calculation for Tassement Differentiel NS
            
            elif NW_Prism=="" and SW_Prism=="" and NE_Prism!="" and SE_Prism!="":       #Conditional for NW_Prism and SW_Prism input boxes are empty
                TasDifNS="("+"Z"+str(NE_Prism)+"-"+"Z"+str(SE_Prism)+")"+"/"+str(NS_Distance)       #Assign TasDifNS as the calculation for Tassement Differentiel NS
            
            VVList=[Station_ID,TasDifNSname,Variable_ID,101,TasDifNS]           #Put Station_ID,TasDifNSname,Variable_ID,101,TasDifNS into VVList of self.current input
            VVListofLists.append(VVList)                #Append VVList to VVListofLists

        else:                   #Conditional for Tassement differentiel NS calculation is not possible
            TasDifNS=""         #Set TasDifNS as blank
            TasDifNSname=""     #Set TasDifNSname as blank

        if (NW_Prism!="" and NE_Prism!="") or (SW_Prism!="" and SE_Prism!=""):      #Conditional for Tassement differentiel OE calculation is possible
            TasDifOEname=Building_callsign + "Tass_Diff_OE"                         #Assign TasDifOEname to the name of Tassement differentiel OE variable with corresponding to building's name
            
            if NW_Prism!="" and SW_Prism!="" and NE_Prism!="" and SE_Prism!="":     #Conditional for all prisms inputs are not empty
                TasDifOE="("+"("+"Z"+str(NW_Prism)+"+"+"Z"+str(SW_Prism)+")"+"/"+"2"+"-"+"("+"Z"+str(NE_Prism)+"+"+"Z"+str(SE_Prism)+")"+"/"+"2"+")"+"/"+str(WE_Distance)   #Assign TasDifOE as the calculation for Tassement Differentiel OE

            elif NW_Prism!="" and SW_Prism!="" and NE_Prism!="" and SE_Prism=="":   #Conditional for SE_Prism input box is empty
                TasDifOE="("+"("+"Z"+str(NW_Prism)+"+"+"Z"+str(SW_Prism)+")"+"/"+"2"+"-"+"Z"+str(NE_Prism)+")"+"/"+str(WE_Distance)     #Assign TasDifOE as the calculation for Tassement Differentiel OE

            elif NW_Prism!="" and SW_Prism!="" and NE_Prism=="" and SE_Prism!="":   #Conditional for NE_Prism input box is empty
                TasDifOE="("+"("+"Z"+str(SW_Prism)+"+"+"Z"+str(NW_Prism)+")"+"/"+"2"+"-"+"Z"+str(SE_Prism)+")"+"/"+str(WE_Distance)     #Assign TasDifOE as the calculation for Tassement Differentiel OE
            
            elif NW_Prism!="" and SW_Prism=="" and NE_Prism!="" and SE_Prism!="":   #Conditional for SW_Prism input box is empty
                TasDifOE="("+"Z"+str(NW_Prism)+"-"+"("+"Z"+str(SE_Prism)+"+"+"Z"+str(NE_Prism)+")"+"/"+"2"+")"+"/"+str(WE_Distance)     #Assign TasDifOE as the calculation for Tassement Differentiel OE
            
            elif NW_Prism=="" and SW_Prism!="" and NE_Prism!="" and SE_Prism!="":   #Conditional for NW_Prism input box is empty
                TasDifOE="("+"Z"+str(SW_Prism)+"-"+"("+"Z"+str(NE_Prism)+"+"+"Z"+str(SE_Prism)+")"+"/"+"2"+")"+"/"+str(WE_Distance)     #Assign TasDifOE as the calculation for Tassement Differentiel OE

            elif NW_Prism!="" and NE_Prism!="" and SW_Prism=="" and SE_Prism=="":   #Conditional for SW_Prism and SE_Prism input boxes are empty
                TasDifOE="("+"Z"+str(NW_Prism)+"-"+"Z"+str(NE_Prism)+")"+"/"+str(WE_Distance)       #Assign TasDifOE as the calculation for Tassement Differentiel OE
            
            elif NW_Prism=="" and NE_Prism=="" and SW_Prism!="" and SE_Prism!="":   #Conditional for NW_Prism and NE_Prism input boxes are empty
                TasDifOE="("+"Z"+str(SW_Prism)+"-"+"Z"+str(SE_Prism)+")"+"/"+str(WE_Distance)       #Assign TasDifOE as the calculation for Tassement Differentiel OE

            VVList=[Station_ID,TasDifOEname,Variable_ID,101,TasDifOE]           #Put Station_ID,TasDifOEname,Variable_ID,101,TasDifOE into VVList of self.current input
            VVListofLists.append(VVList)                #Append VVList to VVListofLists
            
        else:               #Conditional for Tassement differentiel OE calculation is not possible
            TasDifOE=""         #Set TasDifOE as blank
            TasDifOEname=""     #Set TasDifOEname as blank

        if (NW_Prism!="" and NE_Prism!="") or (SW_Prism!="" and SE_Prism!=""):          #Conditional for Deformation Horizontal NS calculation is possible
            DEHNSname=Building_callsign + "DEH_NS"                  #Assign DEHNSname to the name of Deformation Horizontal NS variable with corresponding to building's name
            
            if NW_Prism!="" and SW_Prism!="" and NE_Prism!="" and SE_Prism!="":         #Conditional for all prisms inputs are not empty
                DEHNS="("+"("+"Y"+str(NW_Prism)+"+"+"Y"+str(SW_Prism)+")"+"/"+"2"+"-"+"("+"Y"+str(NE_Prism)+"+"+"Y"+str(SE_Prism)+")"+"/"+"2"+")"+"/"+str(NS_Distance)      #Assign DEHNS as the calculation for Deformation Horizontal NS

            elif NW_Prism!="" and SW_Prism!="" and NE_Prism!="" and SE_Prism=="":       #Conditional for SE_Prism input box is empty       
                DEHNS="("+"("+"Y"+str(NW_Prism)+"+"+"Y"+str(SW_Prism)+")"+"/"+"2"+"-"+"Y"+str(NE_Prism)+")"+"/"+str(NS_Distance)    #Assign DEHNS as the calculation for Deformation Horizontal NS

            elif NW_Prism!="" and SW_Prism!="" and NE_Prism=="" and SE_Prism!="":       #Conditional for NE_Prism input box is empty
                DEHNS="("+"("+"Y"+str(SW_Prism)+"+"+"Y"+str(NW_Prism)+")"+"/"+"2"+"-"+"Y"+str(SE_Prism)+")"+"/"+str(NS_Distance)    #Assign DEHNS as the calculation for Deformation Horizontal NS
            
            elif NW_Prism!="" and SW_Prism=="" and NE_Prism!="" and SE_Prism!="":       #Conditional for SW_Prism input box is empty
                DEHNS="("+"Y"+str(NW_Prism)+"-"+"("+"Y"+str(SE_Prism)+"+"+"Y"+str(NE_Prism)+")"+"/"+"2"+")"+"/"+str(NS_Distance)    #Assign DEHNS as the calculation for Deformation Horizontal NS
            
            elif NW_Prism=="" and SW_Prism!="" and NE_Prism!="" and SE_Prism!="":       #Conditional for NW_Prism input box is empty
                DEHNS="("+"Y"+str(SW_Prism)+"-"+"("+"Y"+str(NE_Prism)+"+"+"Y"+str(SE_Prism)+")"+"/"+"2"+")"+"/"+str(NS_Distance)    #Assign DEHNS as the calculation for Deformation Horizontal NS

            elif NW_Prism!="" and NE_Prism!="" and SW_Prism=="" and SE_Prism=="":       #Conditional for SW_Prism and SE_Prism input boxes are empty
                DEHNS="("+"Y"+str(NW_Prism)+"-"+"Y"+str(NE_Prism)+")"+"/"+str(NS_Distance)  #Assign DEHNS as the calculation for Deformation Horizontal NS
            
            elif NW_Prism=="" and NE_Prism=="" and SW_Prism!="" and SE_Prism!="":       #Conditional for NW_Prism and NE_Prism input boxes are empty
                DEHNS="("+"Y"+str(SW_Prism)+"-"+"Y"+str(SE_Prism)+")"+"/"+str(NS_Distance)  #Assign DEHNS as the calculation for Deformation Horizontal NS

            VVList=[Station_ID,DEHNSname,Variable_ID,101,DEHNS]         #Put Station_ID,DEHNSname,Variable_ID,101,DEHNS into VVList of self.current input
            VVListofLists.append(VVList)                                #Append VVList to VVListofLists

        else:                       #Conditional for Deformation Horizontal NS calculation is not possible
            DEHNS=""            #Set DEHNS as blank
            DEHNSname=""        #Set DEHNSname as blank

        if (NW_Prism!="" and SW_Prism!="") or (NE_Prism!="" and SE_Prism!=""):          #Conditional for Deformation Horizontal OE calculation is possible
            DEHOEname=Building_callsign + "DEH_OE"                                      #Assign DEHOEname to the name of Deformation Horizontal OE variable with corresponding to building's name
            
            if NW_Prism!="" and SW_Prism!="" and NE_Prism!="" and SE_Prism!="":         #Conditional for all prisms inputs are not empty
                DEHOE="("+"("+"X"+str(NW_Prism)+"+"+"X"+str(NE_Prism)+")"+"/"+"2"+"-"+"("+"X"+str(SW_Prism)+"+"+"X"+str(SE_Prism)+")"+"/"+"2"+")"+"/"+str(WE_Distance)      #Assign DEHOE as the calculation for Deformation Horizontal OE

            elif NW_Prism!="" and SW_Prism!="" and NE_Prism!="" and SE_Prism=="":       #Conditional for SE_Prism input box is empty
                DEHOE="("+"("+"X"+str(NW_Prism)+"+"+"X"+str(NE_Prism)+")"+"/"+"2"+"-"+"X"+str(SW_Prism)+")"+"/"+str(WE_Distance)        #Assign DEHOE as the calculation for Deformation Horizontal OE

            elif NW_Prism!="" and SW_Prism!="" and NE_Prism=="" and SE_Prism!="":       #Conditional for NE_Prism input box is empty
                DEHOE="("+"X"+str(NW_Prism)+"-"+"("+"X"+str(SW_Prism)+"+"+"X"+str(SE_Prism)+")"+"/"+"2"+")"+"/"+str(WE_Distance)        #Assign DEHOE as the calculation for Deformation Horizontal OE
            
            elif NW_Prism!="" and SW_Prism=="" and NE_Prism!="" and SE_Prism!="":       #Conditional for SW_Prism input box is empty
                DEHOE="("+"("+"X"+str(NW_Prism)+"+"+"X"+str(NE_Prism)+")"+"/"+"2"+"-"+"X"+str(SE_Prism)+")"+"/"+str(WE_Distance)        #Assign DEHOE as the calculation for Deformation Horizontal OE
            
            elif NW_Prism=="" and SW_Prism!="" and NE_Prism!="" and SE_Prism!="":       #Conditional for NW_Prism input box is empty
                DEHOE="("+"X"+str(NE_Prism)+"-"+"("+"X"+str(SW_Prism)+"+"+"X"+str(SE_Prism)+")"+"/"+"2"+")"+"/"+str(WE_Distance)        #Assign DEHOE as the calculation for Deformation Horizontal OE

            elif NW_Prism!="" and SW_Prism!="" and NE_Prism=="" and SE_Prism=="":       #Conditional for NE_Prism and SE_Prism input boxes are empty
                DEHOE="("+"X"+str(NW_Prism)+"-"+"X"+str(SW_Prism)+")"+"/"+str(WE_Distance)      #Assign DEHOE as the calculation for Deformation Horizontal OE
            
            elif NW_Prism=="" and SW_Prism=="" and NE_Prism!="" and SE_Prism!="":       #Conditional for NW_Prism and SW_Prism input boxes are empty
                DEHOE="("+"X"+str(NE_Prism)+"-"+"X"+str(SE_Prism)+")"+"/"+str(WE_Distance)      #Assign DEHOE as the calculation for Deformation Horizontal OE

            VVList=[Station_ID,DEHOEname,Variable_ID,101,DEHOE]         #Put Station_ID,DEHOEname,Variable_ID,101,DEHOE into VVList of self.current input
            VVListofLists.append(VVList)                                #Append VVList to VVListofLists
            
        else:                   #Conditional for Deformation Horizontal OE calculation is not possible
            DEHOE=""            #Set DEHOE as blank
            DEHOEname=""        #Set DEHOEname as blank    

        for a_list in VVListofLists:     #Loop for each list in VVListofLists
            self.insert(*a_list)              #Call the insert function with arguments based of items in a_list   

        
        return TasGLO, Tassgloname, TasDifNS, TasDifNSname, TasDifOE, TasDifOEname, DEHNS, DEHNSname, DEHOE, DEHOEname

    def insert(self, Station_ID, Virtual_Variable, Variable_ID, Unit_ID,Formula):
        self.cur.execute("INSERT INTO calculation VALUES(NULL,?,?,?,?,?,0,0,1,3600,1,3600,0,\"0000-00-00 00:00:00\",0,\"\")",(Station_ID,Virtual_Variable,Variable_ID,Unit_ID,Formula))
        self.conn.commit()


    def view(self):
        self.cur.execute("SELECT * FROM calculation")
        rows=self.cur.fetchall()
        return rows

    def drop(self):
        self.cur.execute("DROP TABLE calculation")

    def Search(self,Virtual_Variable):
        self.cur.execute("SELECT * FROM calculation WHERE Variable LIKE ?",(Virtual_Variable+"%",))
        rows=self.cur.fetchall()
        return rows

    def delete(self, id):
        placeholders = ', '.join('?'*len(id))
        sql = f"DELETE FROM calculation WHERE id IN ({placeholders})"
        self.cur.execute(sql,id)
        self.conn.commit()

    """export method query explanation
    ||: concatenate the value in Variable column
    COALESCE(column, '') to return the value in the corresponding column"""
    def export(self):
        sql = """
        SELECT
        Station_ID,
        '"' || COALESCE(Variable, '') || '"' Variable,
        Variable_ID,
        Unit_ID,
        '"' || COALESCE(Formula, '') || '"' Formula,
        RoC_Active,
        RoC_Precision,
        RoC_Period_Value,
        RoC_Period_Type,
        RoC_Unit_Value,
        RoC_Unit_Type,
        Datum_Variable_ID,
        '"' || COALESCE(Datum_Timestamp, '') || '"' Datum_Timestamp,
        '"' || COALESCE(Datum_Information, '') || '"' Datum_Information,
        '"' || COALESCE(Constants, '') || '"' Constants
        FROM calculation 
        """
        self.cur.execute(sql)
        rows=self.cur.fetchall()
        csv_path = "output.csv"
        with open(csv_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=";", quotechar='', quoting=csv.QUOTE_NONE)
            # Write headers.
            csv_writer.writerow([i[0] for i in self.cur.description])       #self.cur.description returns a tuple of tuples the first value in each tuple is the column label
            # Write data.
            csv_writer.writerows(rows)

    def update(self, id, Station_ID, Virtual_Variable, Formula):
        self.cur.execute("UPDATE calculation SET Station_ID=?, Variable=?, Formula=? WHERE id=?",(Station_ID,Virtual_Variable,Formula,id))
        self.conn.commit()

    def match(self,filepath):
        sql = """
        SELECT
        Station_ID,
        '"' || COALESCE(Variable, '') || '"' Variable,
        Variable_ID,
        Unit_ID,
        '"' || COALESCE(Formula, '') || '"' Formula,
        RoC_Active,
        RoC_Precision,
        RoC_Period_Value,
        RoC_Period_Type,
        RoC_Unit_Value,
        RoC_Unit_Type,
        Datum_Variable_ID,
        '"' || COALESCE(Datum_Timestamp, '') || '"' Datum_Timestamp,
        '"' || COALESCE(Datum_Information, '') || '"' Datum_Information,
        '"' || COALESCE(Constants, '') || '"' Constants
        FROM calculation 
        """
        self.cur.execute(sql)
        rows=self.cur.fetchall()

        newrow = [["Station_ID;Variable;Variable_ID;Unit_ID;Formula;RoC_Active;RoC_Precision;RoC_Period_Value;RoC_Period_Type;RoC_Unit_Value;RoC_Unit_Type;Datum_Variable_ID;Datum_Timestamp;Datum_Information;Constants"]]
        df = pandas.read_csv(filepath)
        # df1=df.loc[:,["Variable ID","Modified_prism_name"]]

        """prism_dict explanation
        df1["Variable ID"].values returns an array of values in Variable ID column
        prism_dict would be a dictionary with keys as values of Variable ID column and values as Modified_prism_name's values"""
        prisms_dict = pandas.Series(df["Variable ID"].values,index=df["Modified_prism_name"]).to_dict()

        """Regex explanation
        (?<=[(+-]) - a positive lookbehind that matches a location that is immediately preceded with "(" or "+" or "-" 
        [XYZ] - X, Y or Z
        \d\d\d - three digits
        (?=[)+-]) - a positive lookahead that makes sure there is ")" or "+" or "-" immediately to the right of the current location."""
        prism_callsign=re.compile(r"(?<=[(+-])([XYZ]\d\d\d)(?=[)+-])")
        #row=rows[1]
        #test=row[4]
        for row in rows:
            row_converted=list(row)
            variables = prism_callsign.findall(row_converted[4])
            variable_values = [prisms_dict[x] for x in variables]

            #replace user input with prism's id in the vista-data-vision's database
            for variable,prism_value in zip(variables,variable_values):
                row_converted[4] = row_converted[4].replace(variable,prism_value)
            newrow.append(row_converted)
            #print(variable,prism_value)
        with open("matched_output.csv", "w", newline="") as f:
            writer = csv.writer(f, delimiter=";", quotechar='', quoting=csv.QUOTE_NONE, escapechar="\\")
            writer.writerows(newrow)

    #Method below would be executed when the object is destroyed - close the connection to database when we exit the app
    def __del__(self):
        self.conn.close()

#drop()
#self.connect()
#insert(1669,"93007AX0025_01_M_DEH_NS","",42,"($278333$-($277292$+$278339$)/2)/1.75")
#print(view())