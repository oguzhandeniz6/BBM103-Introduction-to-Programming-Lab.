# 21946022 - Oğuzhan Deniz

def printFloat(f):
    if f % 1 == 0:
        return str(int(f))  # Delete zeros after dot (x.0)
    else:
        return str(f)


def readFile(filename):
    with open(filename, mode="r", encoding="utf-8") as file:  # mode= Read, encoding= UTF-8 (for Turkish characters)
        lineList = file.read().splitlines()
    file.close()
    return lineList


def controlName(patientList, name):
    for patient in patientList:  # Find and return patient if there is a patient with given name
        if patient[0] == name:
            return patient
    return []


def addPatient(patientList, name, accuracy, disease, incidence, treatment, risk, output):
    if controlName(patientList, name):  # If there is a patient with given name
        output.write("Patient " + name + " cannot be recorded due to duplication.\n")
    else:  # If there is not a patient with given name
        patientList.append([name, accuracy, disease, incidence, treatment, risk])  # Add patient
        output.write("Patient " + name + " is recorded.\n")
    return patientList


def removePatient(patientList, name, output):
    if controlName(patientList, name):  # If there is a patient with given name
        patient = controlName(patientList, name)
        patientList.remove(patient)  # Remove patient
        output.write("Patient " + name + " is removed.\n")
        return patientList

    else:  # If there is not a patient with given name
        output.write("Patient " + name + " cannot be removed due to absence.\n")
        return patientList


def listPatients(patientList, output):
    output.write("Patient\tDiagnosis\tDisease\t\t\tDisease\t\tTreatment\t\tTreatment\n"
                 "Name\tAccuracy\tName\t\t\tIncidence\tName\t\t\tRisk\n"
                 "-------------------------------------------------------------------------\n")
    for patient in patientList:
        outputStr = patient[0]

        if len(patient[0]) < 4:  # Check patient's name length
            outputStr += "\t"

        outputStr += "\t" + format(float(patient[1]) * 100, '.2f') + "%\t\t" + patient[2]

        if len(patient[2]) < 12:  # Check patient's disease name's length
            outputStr += "\t\t"
        else:
            outputStr += "\t"

        outputStr += patient[3] + "\t" + patient[4]

        if len(patient[4]) < 8:  # Check patient's treatment name's length
            outputStr += "\t\t\t"
        elif len(patient[4]) < 12:
            outputStr += "\t\t"
        elif len(patient[4]) < 16:
            outputStr += "\t"

        outputStr += printFloat(float(patient[5]) * 100) + "%\n"
        output.write(outputStr)  # Write to output file


def calcProbability(patientList, name):
    patient = controlName(patientList, name)  # Find patient
    if patient:
        incidence = patient[3].split("/")  # Ocurrence ratio
        realDisease, realNonDisease = int(incidence[0]), (int(incidence[1]) - int(incidence[0]))
        hitAccuracy, missAccuracy = float(patient[1]), (1.0 - float(patient[1]))
        tp = realDisease * hitAccuracy  # True Positive = Real disease ratio * hit accuracy of diagnosis
        fp = realNonDisease * missAccuracy  # False Positive = Real non-disease ratio * miss accuracy of diagnosis
        prob = ((tp / (tp + fp)) * 100.0).__round__(2)  # Probability = True Positive / All Positives (round by 2 digit)
        return prob
    else:
        return -1


def calcRecommendation(patientList, name, output):
    prob = calcProbability(patientList, name)  # Calculate probability of having disease
    if prob == -1:  # Patient is not in system
        output.write("Recommendation for " + subline[0][15:] + " cannot be calculated due to absence.\n")
    else:
        patient = controlName(patientList, name)
        risk = float(patient[5]) * 100
        if risk > prob:  # If Treatment Risk is higher than Probability of True Diagnosis
            output.write("System suggests " + name + " NOT to have the treatment.\n")  # Treatment NOT Suggested
        else:
            output.write("System suggests " + name + " to have the treatment.\n")  # Treatment Suggested


# Main Starts Here

lines = readFile("doctors_aid_inputs.txt")  # Read
output = open("doctors_aid_outputs.txt", mode="w", encoding="utf-8")  # mode= Write, encoding= UTF-8 (for Turkish characters)

patients = []  # Patients List

for line in lines:
    subline = line.split(", ")
    if subline[0].__contains__("create"):  # Add patient
        patients = addPatient(patients, subline[0][7:], subline[1], subline[2], subline[3], subline[4], subline[5], output)
    elif subline[0].__contains__("remove"):  # Remove patient
        patients = removePatient(patients, subline[0][7:], output)
    elif subline[0].__contains__("list"):  # List patients
        listPatients(patients, output)
    elif subline[0].__contains__("probability"):  # Calculate patient's probability of having disease
        probability = calcProbability(patients, subline[0][12:])
        if probability == -1:
            output.write("Probability for " + subline[0][12:] + " cannot be calculated due to absence.\n")
        else:
            patient = controlName(patients, subline[0][12:])
            output.write("Patient " + subline[0][12:] + " has a probability of " + printFloat(probability) + "% of having " + patient[2].lower() + ".\n")
    elif subline[0].__contains__("recommendation"):  # Recommend treatment if necessary
        calcRecommendation(patients, subline[0][15:], output)
    else:
        output.write("Wrong Command!\n")

output.close()
