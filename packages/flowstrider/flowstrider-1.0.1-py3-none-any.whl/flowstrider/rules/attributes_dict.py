# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

from flowstrider import settings

attributes = {}


def init_attributes():
    _ = settings.lang_out.gettext

    # Dictionary containing all attributes of entities with corresponding accepted
    # ... values. Currently has all attributes relevant to the BSI collection.
    global attributes
    attributes = {
        # Attribute pattern:
        # Name: [
        #    display name,
        #    explanation,
        #    [Entity types the attribute is important for],
        #    [accepted values the attribute can take on]
        # ]
        "auth_factors": [
            _("Authentication factors"),
            _(
                "If authentication is required, which factors will be needed for "
                "authentication. Examples: ['PIN', 'Chip Card', 'OTP'] or "
                "['Digital Certificate', 'Biometric Data']."
            ),
            ["Node: DataStore", "Node: Process"],
            [
                "PIN",
                "OTP",
                "Biometric Data",
                "Digital Certificate",
                "Chip Card",
                "Security Token",
            ],
        ],
        "auth_protocol": [
            _("Authentication protocol"),
            _(
                "Which authentication protocol will be used to ensure integrity. "
                "Examples: 'DH_CHAP' or 'FCPAP'"
            ),
            ["Node: DataStore"],
            [
                "DH_CHAP",
                "FCAP",
                "FCPAP",
            ],
        ],
        "auth_req": [
            _("Requires authentication"),
            _("Whether any form of authentication is required to access the entity."),
            ["Node: DataStore", "Node: Process"],
            [True, False],
        ],
        "encryption_method": [
            _("Encryption method"),
            _(
                "Which method of encryption will be used to encrypt the data. "
                "Examples: 'AES_128' or 'AES_256'"
            ),
            ["Node: DataStore"],
            ["AES_128", "AES_192", "AES_256"],
        ],
        "given_permissions": [
            _("Given permissions"),
            _("Actions the actor is priviliged to perform."),
            ["Node: Process", "Node: Interactor"],
            [],
        ],
        "handles_confidential_data": [
            _("Handles confidential data"),
            _("Whether the entity handles confidential data."),
            ["Node: DataStore", "Node: Process", "Edge: Dataflow"],
            [True, False],
        ],
        "handles_logs": [
            _("Handles logs"),
            _("Whether the DataStore handles protocol logging data."),
            ["Node: DataStore"],
            [True, False],
        ],
        "hash_function": [
            _("Hash function"),
            _(
                "Which function will be used to store hashed data. Examples: "
                "'SHA3_256' or 'SHA_512_256'."
            ),
            ["Node: DataStore"],
            [
                "SHA3_256",
                "SHA3_384",
                "SHA3_512",
                "SHA_256",
                "SHA_384",
                "SHA_512",
                "SHA_512_256",
            ],
        ],
        "http_header": [
            _("HTTP header"),
            _(
                "If applicable, which http headers are set. Example: ['Content Type', "
                "'Cache Control']."
            ),
            ["Edge: Dataflow"],
            [
                "Content Security Policy",
                "Strict Transport Security",
                "Content Type",
                "X Content Options",
                "Cache Control",
            ],
        ],
        "is_san_fabric": [
            _("Is SAN fabric"),
            _(
                "Defines, if the entity is part of the fabric layer of a storage area "
                "network."
            ),
            ["Node: DataStore"],
            [True, False],
        ],
        "input_data": [
            _("Input data"),
            _("All types of handled data. Example: ['Session IDs', 'User Requests']."),
            ["Node: Process"],
            [],
        ],
        "input_validation": [
            _("Input validation"),
            _("Defines, if the input data is validated."),
            ["Node: Process"],
            [True, False],
        ],
        "integrity_check": [
            _("Integrity check"),
            _(
                "If an integrity check (such as a check sum) is used, this should "
                "note the specific check. Examples: 'check sum' or 'digital "
                "certificate'."
            ),
            ["Edge: Dataflow"],
            ["check sum", "digital certificate", "ECDSA"],
        ],
        "proxy": [
            _("Uses proxy"),
            _("Whether the dataflow is routed through a TLS-proxy"),
            ["Edge: Dataflow"],
            [True, False],
        ],
        "req_permissions": [
            _("Required permissions"),
            _("Which priviliges are required to interact with the process."),
            ["Node: Process", "Node: Interactor"],
            [],
        ],
        "signature_scheme": [
            _("Signature scheme"),
            _(
                "If a signature scheme is used, this should note the specific scheme. "
                "Examples:'RSA' or 'ECDSA' or 'LMS'."
            ),
            ["Edge: Dataflow", "Node: DataStore"],
            [
                "DSA",
                "ECDSA",
                "ECGDSA",
                "ECKDSA",
                "LMS",
                "RSA",
                "XMSS",
            ],
        ],
        "stores_credentials": [
            _("Stores credentials"),
            _(
                "Whether the DataStore stores Login Credentials or other "
                "authentication data."
            ),
            ["Node: DataStore"],
            [True, False],
        ],
        "transport_protocol": [
            _("Transport protocol"),
            _("Which transport protocol the dataflow uses."),
            ["Edge: Dataflow"],
            ["HTTPS", "TLS 1.2", "TLS 1.3"],
        ],
    }


# Metadata relevant to Threat Dragon but not currently used in rules:
"""
metadata_keys = {
    "Node: Interactor": {
        # "providesAuthentication",
    },
    "Node: DataStore": {
        # "isALog",
        # "isEncrypted",
        # "isSigned",
        # "storesInventory",
    },
    "Node: Process": {
        # "handlesCardPayment",
        # "handlesGoodsOrServices",
        # "isWebApplication",
        # "privilegeLevel",
    },
    "Edge: Dataflow": {
        # "isEncrypted",
        # "isPublicNetwork",
    },
    "Trust Boundary": {},
}
"""
