# if every sentences has these anotated words then label anotation with 0
NOT_ANNOTATED = ["no", "not", "normal", "without", "negative for", "stable", "intact", "unchanged", "no evidence", "no acute", "no suspicious", "clear", "free of", "removal", "removed"]

NOT_FOUND = ["no indexing", "technical quality of image unsatisfactory"]
# annotations: text
# look for that key and also synonyms
# "/" look for first then second part
SYNONYMS = {
        "middle lobe": "midlobe/mid lobe",
        "pulmonary disease, chronic obstructive": "copd",
        "thoracic vertebrae": "thoracic spine",
        "cardiomegaly": "large heart/heart size is enlarged",
        "lingula": "left lung",
        "hyperdistention": "large lung volume/hyperexpanded",
        "hypoinflation": "low lung volume",
        "markings": "crowding",
        "cicatrix": "scar/scaring",
        "bilateral": "both", # search for both then for mid if it is there search for lobe
        "atherosclerosis": "atherosclerotic/ectasia",
        "nodule": "nodules",
        "multiple": "bilateral",
        "mild": "minimal",
        "abdomen": "upper quadrant",
        "surgical instruments": "clips/surgical clips/valve replacement",
        "bone diseases, metabolic": "osteopenic",
        "foreign bodies": "nipple ring",
        "hilum": "hilar",
        "pleural effusion": "residual effusion",
        "catheters, indwelling": "picc line"
    }