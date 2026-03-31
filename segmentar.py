# Cabeçalho do programa
# Equipe: Os Laplacianos
# Integrantes:
# Matheus Foresto Moselli - RA: 11202320707
# Marcos Vinicius Medeiros da Silva - RA:
# Karl Eloy Marques Henrique - RA:
# Data: 30/03/2026
# Programa: segmentar.py
# Descrição: SPV para contagem automática de comprimidos via webcam/imagem.
from pathlib import Path
import numpy as np
import cv2

MODO_FUNDO       = 'escuro'
KERNEL_MORPH     = 5    # Kernel morfológico
ITER_OPEN        = 2    # Iterações da abertura (remove ruído)
ITER_CLOSE       = 2    # Iterações do fechamento (preenche buracos)
MIN_AREA_FRAC    = 0.001  # Mín. 0.1% da área da imagem
MAX_AREA_FRAC    = 0.05   # Máx. 5% da área da imagem
MIN_CIRCULARIDADE = 0.55  # 0=qualquer forma, 1=círculo perfeito
PASTA_ENTRADA = Path("images")
PASTA_SAIDA = Path("segmented")
PASTA_SAIDA.mkdir(exist_ok=True)

def segmentar(cinza_blur):
    """
    Segmenta comprimidos: Otsu → Morfologia → Watershed → filtro área/circularidade.

    Retorna:
        labels        : mapa de rótulos do Watershed
        mascara_bin   : máscara binária pós-morfologia
        contornos_val : lista de (contorno, área, circularidade) válidos
        n             : quantidade de comprimidos detectados
    """
    h, w = cinza_blur.shape
    min_area = (h * w) * MIN_AREA_FRAC
    max_area = (h * w) * MAX_AREA_FRAC

    # Binarização Otsu
    flag = cv2.THRESH_BINARY if MODO_FUNDO == 'escuro' else cv2.THRESH_BINARY_INV
    _, mascara = cv2.threshold(cinza_blur, 0, 255, flag + cv2.THRESH_OTSU)

    # Operadores Morfológicos
    kernel = np.ones((KERNEL_MORPH, KERNEL_MORPH), np.uint8)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN,  kernel, iterations=ITER_OPEN)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel, iterations=ITER_CLOSE)
    mascara_bin = mascara.copy()

    # Watershed
    dist = cv2.distanceTransform(mascara, cv2.DIST_L2, 5)
    _, frente = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)
    frente = np.uint8(frente)
    fundo = cv2.dilate(mascara, kernel, iterations=3)
    desconhecido = cv2.subtract(fundo, frente)
    _, marcadores = cv2.connectedComponents(frente)
    marcadores = marcadores + 1
    marcadores[desconhecido == 255] = 0
    labels = cv2.watershed(cv2.cvtColor(cinza_blur, cv2.COLOR_GRAY2BGR), marcadores)

    # Filtrar regiões por área e circularidade
    contornos_val = []
    for rid in np.unique(labels):
        if rid <= 1:
            continue
        mask_r = np.uint8(labels == rid) * 255
        cnts, _ = cv2.findContours(mask_r, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not cnts:
            continue
        c = cnts[0]
        area = cv2.contourArea(c)
        if not (min_area <= area <= max_area):
            continue
        perim = cv2.arcLength(c, True)
        if perim == 0:
            continue
        circ = 4 * np.pi * area / (perim ** 2)
        if circ >= MIN_CIRCULARIDADE:
            contornos_val.append((c, area, circ))

    return labels, mascara_bin, contornos_val, len(contornos_val)