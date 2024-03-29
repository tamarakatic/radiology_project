# if every sentences has these anotated words then label anotation with 0
# NOT_ANNOTATED = ["not", "no", "normal", "without", "negative for", "stable", "intact", "unchanged", "no evidence", "no acute", "no suspicious", "clear", "free of", "removal", "removed"]
NOT_ANNOTATED = ["not", "negative for", "no evidence", "no suspicious", "free of", "removal", "removed"]

NOT_FOUND = ["no indexing", "technical quality of image unsatisfactory"]
# annotations: text
# look for that key and also synonyms
# "/" look for first then second part
SYNONYMS = {
        "middle lobe": "midlobe/mid lobe",  # search for both then for mid if it is there search for lobe
        "middle": "mid",
        "lobe": "lung",
        "lung": "lobe",
        "pulmonary disease, chronic obstructive": "copd",
        "thoracic vertebrae": "thoracic spine/thoracic vertebral/spine",
        "cardiomegaly": "large heart/heart size is enlarged/heart size/cardiac",
        "lingula": "left lung",
        "hyperdistention": "large lung volume/hyperexpanded/hyperinflation/hyperaerated",
        "hypoinflation": "hypoinflated/low lung volume",
        "markings": "crowding/stripe/lines",
        "cicatrix": "scar/scaring/scarring/change",
        "bilateral": "both",
        "atherosclerosis": "atherosclerotic/ectasia",
        "sclerosis": "sclerotic",
        "nodule": "nodular",
        "multiple": "bilateral/numerous",
        "adipose tissue": "fat",
        "osteophyte": "spur",
        "mild": "minimal",
        "abdomen": "upper quadrant",
        "surgical instruments": "surgical clips/valve replacement/clips",
        "bone diseases, metabolic": "osteopeni/demineralization",
        "foreign bodies": "nipple ring/shrapnel/bullet/device",
        "hilum": "hilar",
        "pleural effusion": "residual effusion",
        "catheters, indwelling": "picc line/tip",
        "funnel chest": "pectus excavatum",
        "scoliosis": "spine curvature/scoliotic",
        "opacity": "opacities", # remove
        "cardiac shadow": "cardiac contour/cardiomediastinal silhouette",
        "calcinosis": "calcifi", # remove
        "diaphragm": "hemidiaphragm",
        "density": "densities/hyperdense", # remove
        "airspace disease": "airspace consolidation",
        "medical device": "spinal stimulator",
        "implanted medical device": "stimulator/pacemaker/prosthesis/generator/septal occluder/valve/icd",
        "diaphragmatic": "hemidiaphragm",
        "cervical vertebrae": "cervical spine",
        "diaphragmatic eventration": "diaphragm eventration",
        "pneumothorax": "pleural",
        "lymph node": "adenopathy",
        "disease": "finding/infection",
        "humerus": "humeral",
        "cysts": "lucent",
        "shoulder": "acromioclavicular",
        "aorta": "aortic",
        "deformity": "shortening/degenerative/abnormal",
        "fractures": "fracture", # remove
        "dislocations": "retrolisthesis",
        "pulmonary": "lung/cardiopulmonary",
        "pneumomediastinum": "mediastinal emphysema", 
        "lung": "pulmonary",
        "blood vessels": "pulmonary vasculature",
        "mediastinum": "mediastinal",
        "arthritis": "arthritic",
        "lymph nodes": "adenopathy",
        "granulomatous disease": "granulomatous infection",
        "pulmonary congestion": "edema/lung vascularity",
        "pulmonary atelectasis": "collapse of the lung",
        "lucency": "lucent",
        "osteophyte": "spurring",
        "pneumonia": "pneumonitis"
    }