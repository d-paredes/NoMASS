def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)

# global enums
typeOfClass = enum("BUILDING", "BUILDING_ZONES", "BUILDING_ZONE", "BUILDING_OCCUPANTS", "BUILDING_OCCUPANT", "BUILDING_OCCUPANTTEMPLATE", "MODELS", "MODEL_PRESENCE", "MODEL_WINDOWS", "MODEL_WINDOW", "MODEL_SHADES", "MODEL_SHADE", "MODEL_LIGHTS", "MODEL_AGENTHEATGAINS", "MODEL_HEATING", "N_A")
typeOfMessage = enum("ERROR", "INFO", "WARNING")
typeOfAppStatus = enum("IDLE", "SIMULATING", "WRITING", "PROCESSING_DATA")
