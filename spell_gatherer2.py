from bs4 import BeautifulSoup
import requests
import csv

def gather_spell_info(spell_page):

    # Initiate spell dictionary
    spell_attributes = {"Description":       "NONE",
                        "Range":             "NONE",
                        "Components":        "NONE",
                        "Material":          "NONE",
                        "Duration":          "NONE",
                        "Casting time":      "NONE",
                        "Level":             "NONE",
                        "School":            "NONE",
                        "Class":             "NONE",
                        "Ritual":            "NONE",
                        "Save":              "NONE",
                        "Damage":            "NONE",
                        "Damage type":       "NONE",
                        "Damage progression":"NONE"}

    # Make the soup
    soup = BeautifulSoup(spell_page,'html.parser')

    # Marking the tanble location
    table = soup.table.find_all('tr')

    # Grabbing the description
    description = soup.find('div',class_='pagecontent').text.replace("\n"," ")

    #Looping over table to pull out desired information
    for entry in table:
        try:
            if entry['data-attribkey'] == "Range":
                spell_attributes['Range'] = entry.td.text.strip()
            elif entry['data-attribkey'] == "Components":
                spell_attributes['Components'] = entry.td.text.strip()
            elif entry['data-attribkey'] == "Material":
                spell_attributes['Material'] = entry.td.text.replace("\n"," ").replace("%27","'").replace("%28","(").replace("%29",")")
            elif entry['data-attribkey'] == "Duration":
                spell_attributes['Duration']  = entry.td.text.strip()
            elif entry['data-attribkey'] == "Casting Time":
                spell_attributes['Casting time'] = entry.td.text.strip()
            elif entry['data-attribkey'] == "Level":
                spell_attributes['Level'] = entry.td.text.strip()
            elif entry['data-attribkey'] == "School":
                spell_attributes['School'] = entry.td.text.strip()
            elif entry['data-attribkey'] == "Classes":
                spell_attributes['Class'] = entry.td.text.split(",")
            elif entry['data-attribkey'] == "Save":
                spell_attributes['Save'] = entry.td.text.strip()
            elif entry['data-attribkey'] == "Damage":
                spell_attributes['Damage'] = entry.td.text.strip()
            elif entry['data-attribkey'] == "Damage Type":
                spell_attributes['Damage type'] = entry.td.text.strip()
            elif entry['data-attribkey'] == "Damage Progression":
                spell_attributes['Damage progression'] = entry.td.text.strip()
            elif entry['data-attribkey'] == "Ritual":
                spell_attributes['Ritual'] = entry.td.text.strip()
            else:
                pass
        except:
            pass

    # Return spell dictionary
    return spell_attributes

if __name__=="__main__":

    # Site with the information
    url = "https://roll20.net/compendium/dnd5e/Rules:Spells%20by%20Level#content"
    # Site basic url for use later
    base_url = "https://roll20.net"
    res = requests.get(url)
    
    # Make the soup
    soup = BeautifulSoup(res.text,'html.parser')

    # Loop to grab all the spell links into the list 'sLinks'
    sLinks = []
    for link in soup.find_all('a'):
        try:
            # If "Spells" is in the href of link grab it
            if "Spells" in link['href']:
                # Take the href and prepend it with the base_url
                sLinks.append("".join((base_url,link['href'])))
        except:
            pass
        
    # Inititate file and csv
    outputFile = open("DnD_spells.csv",'w',encoding='utf-8')

    # Create header for the csv file
    header = ["Name",
              "Description",
              "Range",
              "Components",
              "Material",
              "Duration",
              "Casting time",
              "Level",
              "School",
              "Class",
              "Ritual",
              "Save",
              "Damage",
              "Damage type",
              "Damage progression"]
             
    csvW = csv.DictWriter(outputFile, fieldnames=header ,dialect='unix')
    csvW.writeheader()

    # Gather spell information and write to csv
    for s in sLinks:
        # Get spell name
        sName = s.split("-")[1].replace("%20"," ")
        # Get the site for the spell
        res = requests.get(s)
        # Gather a spells information
        s_attributes = gather_spell_info(res.text)
        # Add spell name to dictionary
        s_attributes["Name"] = sName

        # 
        class_ = s_attributes['Class']

        # Write out information in csv
        if len(class_) == 1:
            # Put single class back in dictionary
            s_attributes['Class'] = class_[0].strip()
            csvW.writerow(s_attributes)
        else:
            # If a spell has more than one class output a line for each class
            # looping over each class
            for c in class_:
                s_attributes['Class'] = c.strip()
                csvW.writerow(s_attributes)

    outputFile.close()
