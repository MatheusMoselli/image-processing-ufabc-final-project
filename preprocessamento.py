# Cabeçalho do programa
# Equipe: Os Laplacianos
# Integrantes:
# Matheus Foresto Moselli - RA: 11202320707
# Marcos Vinicius Medeiros da Silva - RA:
# Karl Eloy Marques Henrique - RA:
# Data: 30/03/2026
# Programa: preprocessamento.py
# Descrição: SPV para contagem automática de comprimidos via webcam/imagem.
import matplotlib.pyplot as plt
from pathlib import Path
import cv2

KERNEL_BLUR  = 9      # Tamanho do filtro Gaussiano
CLAHE_CLIP   = 2.0    # Contraste limite do CLAHE
CLAHE_GRID   = (8, 8) # Grade do CLAHE
PASTA_ENTRADA = Path("images")
PASTA_SAIDA = Path("preprocessed")
PASTA_SAIDA.mkdir(exist_ok=True)

def preprocessar(frame):
    """
    Pré-processa um frame BGR.

    Etapas:
        1. Processamento de cores: BGR → LAB
        2. Equalização CLAHE no canal L (melhora contraste local)
        3. Filtro Gaussiano (suavização / remoção de ruído)

    Retorna:
        cinza_blur: imagem suavizada pronta para binarização
        frame_rgb: frame original em RGB (para exibição)
    """
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    # Equalização CLAHE no canal de luminância
    clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP, tileGridSize=CLAHE_GRID)
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])

    cinza = cv2.cvtColor(cv2.cvtColor(lab, cv2.COLOR_LAB2BGR), cv2.COLOR_BGR2GRAY)
    cinza_blur = cv2.GaussianBlur(cinza, (KERNEL_BLUR, KERNEL_BLUR), 0)
    return cinza_blur, frame_rgb


def mostrar_histograma(frame, nome_arquivo):
    """Plota histograma do canal L antes e depois do CLAHE."""
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l_orig = lab[:, :, 0].copy()
    clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP, tileGridSize=CLAHE_GRID)
    l_eq = clahe.apply(l_orig)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].hist(l_orig.ravel(), bins=256)
    axes[0].set_title('Histograma Original (Canal L)')

    axes[1].hist(l_eq.ravel(), bins=256)
    axes[1].set_title('Histograma Após CLAHE')

    for ax in axes:
        ax.set_xlabel('Intensidade')
        ax.set_ylabel('Frequência')

    plt.tight_layout()

    caminho = PASTA_SAIDA / f"{nome_arquivo}_histograma.png"
    plt.savefig(caminho, dpi=300, bbox_inches='tight')


escala = 1

if __name__ == '__main__':
    for img in PASTA_ENTRADA.iterdir():
        frame = cv2.imread(img)

        if frame is None:
            print(f"Imagem nao encontrada: {img}")
            continue
        if escala != 1.0:
            frame = cv2.resize(frame, None, fx=escala, fy=escala)

        cinza_blur, frame_rgb = preprocessar(frame)

        cv2.imwrite(str(PASTA_SAIDA / f"{img.stem}_cinza_blur.png"), cinza_blur)
        mostrar_histograma(frame, img.stem)