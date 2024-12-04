__all__ = ['dicionario_poses', 'dicionario_poses_pernas']

dicionario_poses = {
    "cristo redentor": {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (90 - 30) <= anguloBEC <= (90 + 30) and
            (90 - 30) <= anguloBEB <= (90 + 30) and
            (90 - 30) <= anguloBDC <= (90 + 30) and
            (90 - 30) <= anguloBDB <= (90 + 30)
        )
    },
    "maos pro alto": {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (180 - 30) <= anguloBDC <= (180 + 30) and
            (180 - 30) <= anguloBDB <= (180 + 30) and
            (180 - 30) <= anguloBEC <= (180 + 30) and
            (180 - 30) <= anguloBEB <= (180 + 30)
        )
    },
    "maos pra baixo": {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (0 - 30) <= anguloBDC <= (0 + 30) and
            (0 - 30) <= anguloBDB <= (0 + 30) and
            (0 - 30) <= anguloBEC <= (0 + 30) and
            (0 - 30) <= anguloBEB <= (0 + 30)
        )
    },
    "esquerda cima direita baixo": {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (180 - 30) <= anguloBEC <= (180 + 30) and
            (180 - 30) <= anguloBEB <= (180 + 30) and
            (0 - 30) <= anguloBDC <= (0 + 30) and
            (0 - 30) <= anguloBDB <= (0 + 30)
        )
    },
    "direita cima esquerda baixo": {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (180 - 30) <= anguloBDC <= (180 + 30) and
            (180 - 30) <= anguloBDB <= (180 + 30) and
            (0 - 30) <= anguloBEC <= (0 + 30) and
            (0 - 30) <= anguloBEB <= (0 + 30)
        )
    },
    "formato U":
    {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (90 - 30) <= anguloBDC <= (90 + 30) and
            (180 - 30) <= anguloBDB <= (180 + 30) and
            (90 - 30) <= anguloBEC <= (90 + 30) and
            (180 - 30) <= anguloBEB <= (180 + 30)
        )
    },
    "formato U invertido":
    {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (90 - 30) <= anguloBDC <= (90 + 30) and
            (0 - 30) <= anguloBDB <= (0 + 30) and
            (90 - 30) <= anguloBEC <= (90 + 30) and
            (0 - 30) <= anguloBEB <= (0 + 30)
        )
    },
    "formato S":
    {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (90 - 30) <= anguloBDC <= (90 + 30) and
            (0 - 30) <= anguloBDB <= (0 + 30) and
            (90 - 30) <= anguloBEC <= (90 + 30) and
            (180 - 30) <= anguloBEB <= (180 + 30)
        )
    },
    "formato Ƨ":
    {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (90 - 30) <= anguloBEC <= (90 + 30) and
            (0 - 30) <= anguloBEB <= (0 + 30) and
            (90 - 30) <= anguloBDC <= (90 + 30) and
            (180 - 30) <= anguloBDB <= (180 + 30)
        )
    },
    "disco move":
    {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (45 - 30) <= anguloBEC <= (45 + 30) and
            (45 - 30) <= anguloBEB <= (45 + 30) and
            (135 - 30) <= anguloBDC <= (135 + 30) and
            (135 - 30) <= anguloBDB <= (135 + 30)
        )
    },
    "disco-disco move":
    {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (45 - 30) <= anguloBDC <= (45 + 30) and
            (45 - 30) <= anguloBDB <= (45 + 30) and
            (135 - 30) <= anguloBEC <= (135 + 30) and
            (135 - 30) <= anguloBEB <= (135 + 30)
        )
    },
    "uzinho":
    {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (50 - 30) <= anguloBDC <= (50 + 30) and
            (180 - 30) <= anguloBDB <= (180 + 30) and
            (50 - 30) <= anguloBEC <= (50 + 30) and
            (180 - 30) <= anguloBEB <= (180 + 30)
        )
    },
    "v":
    {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (135 - 30) <= anguloBDC <= (135 + 30) and
            (135 - 30) <= anguloBDB <= (135 + 30) and
            (135 - 30) <= anguloBEC <= (135 + 30) and
            (135 - 30) <= anguloBEB <= (135 + 30)
        )
    },
     "maos na cabeca":
    {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (90 - 30) <= anguloBDC <= (90 + 30) and
            (130 - 30) <= anguloBDB <= (130 + 30) and
            (90 - 30) <= anguloBEC <= (90 + 30) and
            (135 - 30) <= anguloBEB <= (130 + 30)
        )
    }, 
}

dicionario_poses_pernas = {
    "retas": {
        "condicao": lambda angulo_PEC, angulo_PEB, angulo_PDC, angulo_PDB: (
            (0 - 30) <= angulo_PEC <= (0 + 30) and
            (0 - 30) <= angulo_PEB <= (0 + 30) and
            (0 - 30) <= angulo_PDC <= (0 + 30) and
            (0 - 30) <= angulo_PDB <= (0 + 30)
        )
    },
    "dobradas": {
        "condicao": lambda angulo_PEC, angulo_PEB, angulo_PDC, angulo_PDB: (
            (90 - 30) <= angulo_PEC <= (90 + 30) and
            (0 - 30) <= angulo_PEB <= (0 + 30) and
            (90 - 30) <= angulo_PDC <= (90 + 30) and
            (0 - 30) <= angulo_PDB <= (0 + 30)
        )
    },
    "chutes": {
        "condicao": lambda angulo_PEC, angulo_PEB, angulo_PDC, angulo_PDB: (
            (90 - 30) <= angulo_PEC <= (90 + 30) and
            (90 - 30) <= angulo_PEB <= (90 + 30) and
            (90 - 30) <= angulo_PDC <= (90 + 30) and
            (90 - 30) <= angulo_PDB <= (90 + 30)
        )
    },
    "chuta esquerdo": {
        "condicao": lambda angulo_PEC, angulo_PEB, angulo_PDC, angulo_PDB: (
            (90 - 30) <= angulo_PEC <= (90 + 30) and
            (90 - 30) <= angulo_PEB <= (90 + 30) and
            (0 - 30) <= angulo_PDC <= (90 + 30) and
            (0 - 30) <= angulo_PDB <= (90 + 30)
        )
    },
    "chuta direito": {
        "condicao": lambda angulo_PEC, angulo_PEB, angulo_PDC, angulo_PDB: (
            (0 - 30) <= angulo_PEC <= (90 + 30) and
            (0 - 30) <= angulo_PEB <= (90 + 30) and
            (90 - 30) <= angulo_PDC <= (90 + 30) and
            (90 - 30) <= angulo_PDB <= (90 + 30)
        )
    },
    "dobra direita": {
        "condicao": lambda angulo_PEC, angulo_PEB, angulo_PDC, angulo_PDB: (
            (90 - 30) <= angulo_PEC <= (90 + 30) and
            (0 - 30) <= angulo_PEB <= (0 + 30) and
            (0 - 30) <= angulo_PDC <= (90 + 30) and
            (0 - 30) <= angulo_PDB <= (0 + 30)
        )
    },
    "dobra esquerda": {
        "condicao": lambda angulo_PEC, angulo_PEB, angulo_PDC, angulo_PDB: (
            (0 - 30) <= angulo_PEC <= (90 + 30) and
            (0 - 30) <= angulo_PEB <= (0 + 30) and
            (90 - 30) <= angulo_PDC <= (90 + 30) and
            (0 - 30) <= angulo_PDB <= (0 + 30)
        )
    },
}