import json
from sentence_transformers import SentenceTransformer
import pickle


# -----------------------------
# Load Telani project JSON
# -----------------------------
with open("JsonExport.json", encoding="utf-8-sig") as jsonfile:
    project = json.load(jsonfile)


sentences = []
metadata = []  # keeps track of what each embedding belongs to


# -----------------------------
# Zones → sentences
# -----------------------------
for zone in project.get("Zones", []):
    sentence = (
        f"Zone '{zone['Name']}' is located on floor {zone['Geschoss']}. "
        f"Description: {zone['Beschreibung']}. "
        f"Displayed with color {zone['Farbe']}."
    )
    sentences.append(sentence)
    metadata.append({
        "type": "zone",
        "name": zone["Name"]
    })


# -----------------------------
# Systems → sentences
# -----------------------------
for system in project.get("Systems", []):
    sentence = (
        f"System '{system.get('BeautifulName')}' "
        f"is part of '{system.get('NameOfSuperSystem')}'. "
        f"{'It is a subsystem.' if system.get('IsSubSystem') else 'It is a main system.'}"
    )
    sentences.append(sentence)
    metadata.append({
        "type": "system",
        "system_id": system.get("SystemId")
    })


actuator_types = {
    at["Identifier"]: at
    for at in  project.get("Actuator_Types", [])
}

actuators = project.get("Actuators", [])
# -----------------------------
# Actuators → sentences
# -----------------------------
for actuator in actuators:
    actuator_type = actuator_types.get(actuator["TypeIdentifier"])
    sentence = (
        f"Actuator '{actuator['Name']}' of type '{actuator_type['Name']}' and category '{actuator_type['Category']}'. "
        f"located at '{actuator['Location']}' on floor {actuator['Geschoss']}. "
        f"It belongs to '{actuator['Anlage']}', "
        f"zone '{actuator['Auslösebereich']}', "
        f"alarm state '{actuator['Alarmzustand']}', "
        f"with transmission path '{actuator['Übertragungsweg']}'."
    )
    sentences.append(sentence)
    metadata.append({
        "type": "actuator",
        "name": actuator["Name"],
        "export_id": actuator.get("ExportId")
    })

actuator_dict = {
    at["ExportId"]: at
    for at in  actuators
}

sensor_types = {
    st["Identifier"]: st
    for st in  project.get("Sensor_Types", [])
}

# -----------------------------
# Sensors → sentences
# -----------------------------
for sensor in project.get("Sensors", []):
    sensor_type = sensor_types.get(sensor["TypeIdentifier"])
    sentence = (
        f"Sensor '{sensor['Name']}' of type '{sensor_type['Name']}' "
        f"located at '{sensor['Location']}' on floor {sensor['Geschoss']}. "
        f"It belongs to system '{sensor['Anlage']}', "
        f"zone '{sensor['Auslösebereich']}', "
        f"with alarm state '{sensor['Alarmzustand']}'. "
        f"Connection type '{sensor['Aufschaltung']}'. "
        f"with transmission path '{sensor['Übertragungsweg']}',"
        f"Detector type is '{sensor['Melderart']}',"
        f"and is related to '{ [ actuator_dict.get(expId)['Name'] for expId in sensor['RelatedElements']]}' actuators"
    )
    sentences.append(sentence)
    metadata.append({
        "type": "sensor",
        "name": sensor["Name"],
        "export_id": sensor.get("ExportId")
    })




# -----------------------------
# Load embedding model
# -----------------------------
model_name = "sentence-transformers/all-MiniLM-L12-v2"
model = SentenceTransformer(model_name)


# -----------------------------
# Create embeddings
# -----------------------------
embeddings = model.encode(
    sentences,
    convert_to_numpy=True,
    normalize_embeddings=True
)

print(f"Embedded {len(embeddings)} items")
print(f"Vector dimension: {embeddings.shape[1]}")


# -----------------------------
# Save embeddings + metadata
# -----------------------------
with open("telani_embeddings.pkl", "wb") as f:
    pickle.dump(
        {
            "model_name": model_name,
            "sentences": sentences,
            "metadata": metadata,
            "embeddings": embeddings,
        },
        f
    )

print("Saved embeddings to telani_embeddings.pkl")