__all__ = ['dicionario_poses', 'dicionario_poses_pernas']


dicionario_poses = {
    "cristo_redentor": {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (90 - 30) <= anguloBEC <= (90 + 30) and
            (90 - 30) <= anguloBEB <= (90 + 30) and
            (90 - 30) <= anguloBDC <= (90 + 30) and
            (90 - 30) <= anguloBDB <= (90 + 30)
        )
    },
    "maos_pro_alto": {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (180 - 30) <= anguloBDC <= (180 + 30) and
            (180 - 30) <= anguloBDB <= (180 + 30) and
            (180 - 30) <= anguloBEC <= (180 + 30) and
            (180 - 30) <= anguloBEB <= (180 + 30)
        )
    },
    "maos_pra_baixo": {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (0 - 30) <= anguloBDC <= (0 + 30) and
            (0 - 30) <= anguloBDB <= (0 + 30) and
            (0 - 30) <= anguloBEC <= (0 + 30) and
            (0 - 30) <= anguloBEB <= (0 + 30)
        )
    },
    "esquerda_cima_direita_baixo": {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (180 - 30) <= anguloBEC <= (180 + 30) and
            (180 - 30) <= anguloBEB <= (180 + 30) and
            (0 - 30) <= anguloBDC <= (0 + 30) and
            (0 - 30) <= anguloBDB <= (0 + 30)
        )
    },
    "direita_cima_esquerda_baixo": {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (180 - 30) <= anguloBDC <= (180 + 30) and
            (180 - 30) <= anguloBDB <= (180 + 30) and
            (0 - 30) <= anguloBEC <= (0 + 30) and
            (0 - 30) <= anguloBEB <= (0 + 30)
        )
    },
    "formato_U":
    {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (90 - 30) <= anguloBDC <= (90 + 30) and
            (180 - 30) <= anguloBDB <= (180 + 30) and
            (90 - 30) <= anguloBEC <= (90 + 30) and
            (180 - 30) <= anguloBEB <= (180 + 30)
        )
    },
    "formato_U_invertido":
    {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (90 - 30) <= anguloBDC <= (90 + 30) and
            (0 - 30) <= anguloBDB <= (0 + 30) and
            (90 - 30) <= anguloBEC <= (90 + 30) and
            (0 - 30) <= anguloBEB <= (0 + 30)
        )
    },
    "formato_S":
    {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (90 - 30) <= anguloBDC <= (90 + 30) and
            (0 - 30) <= anguloBDB <= (0 + 30) and
            (90 - 30) <= anguloBEC <= (90 + 30) and
            (180 - 30) <= anguloBEB <= (180 + 30)
        )
    },
    "formato_S_espelhado":
    {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (90 - 30) <= anguloBEC <= (90 + 30) and
            (0 - 30) <= anguloBEB <= (0 + 30) and
            (90 - 30) <= anguloBDC <= (90 + 30) and
            (180 - 30) <= anguloBDB <= (180 + 30)
        )
    },
    "disco_move":
    {
        "condicao": lambda anguloBEC, anguloBEB, anguloBDC, anguloBDB: (
            (45 - 30) <= anguloBEC <= (45 + 30) and
            (45 - 30) <= anguloBEB <= (45 + 30) and
            (135 - 30) <= anguloBDC <= (135 + 30) and
            (135 - 30) <= anguloBDB <= (135 + 30)
        )
    },
    "disco_disco_move":
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
     "maos_na_cabeca":
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
        "condicao": lambda angulo_PEC, angulo_PDC: (
            angulo_PEC <= (10)  and
            angulo_PDC <= (10) 
        )
    },
    "dobra_esquerda": {
        "condicao": lambda angulo_PEC, angulo_PDC: (
            angulo_PEC >= (10)  and
            angulo_PDC <= (10) 
        )
    },
    "dobra_direita": {
        "condicao": lambda angulo_PEC, angulo_PDC: (
            angulo_PEC <= (10)  and
            angulo_PDC >= (10) 
        )
    },
    # "dobradas": {
    #     "condicao": lambda angulo_PEC, angulo_PDC: (
    #         angulo_PEC >= (10)  and
    #         angulo_PDC >= (10) 
    #     )
    # }
}