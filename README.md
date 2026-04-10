# SPV — Contador de Comprimidos

Este repositório contém o desenvolvimento de um Sistema de Processamento Visual (SPV) projetado para a detecção e contagem automatizada de medicamentos em tempo real. O projeto foi desenvolvido como parte da disciplina Processamento Digital de Imagens na UFABC, com foco em auxiliar a organização de medicamentos para usuários com limitações motoras ou idosos.

## Descrição Técnica

O sistema utiliza técnicas de visão computacional para segmentar comprimidos em imagens capturadas via webcam. O desafio central abordado é a separação de objetos que possuem contato físico (sobreposição ou toque), resolvido através da Transformada de Watershed baseada na distância euclidiana dos objetos binarizados.

## Funcionalidades

* Detecção e contagem em tempo real via captura de vídeo.
* Tratamento de iluminação variável através de CLAHE (Contrast Limited Adaptive Histogram Equalization).
* Segmentação de objetos adjacentes utilizando Watershed.
* Visualização do pipeline completo de processamento em janelas simultâneas.
* Filtros morfológicos para redução de ruído e artefatos de fundo.

## Tecnologias e Dependências

* Python 3.10+
* OpenCV: Processamento de imagem e interface de vídeo.
* NumPy: Manipulação de matrizes e álgebra linear.
* Matplotlib: Geração de histogramas e visualizações estáticas.
* Jupyter Notebook: Ambiente para prototipagem e experimentação.

## Fluxo de Processamento

O sistema executa as seguintes etapas para cada frame capturado:

1. Conversão para Escala de Cinza: Redução da complexidade de dados.
2. Pré-processamento: Aplicação de CLAHE para ganho de contraste e Blur Gaussiano para suavização de texturas.
3. Binarização: Thresholding de Otsu para separação automática entre fundo e primeiro plano.
4. Limpeza Morfológica: Operações de Abertura e Fechamento para remover pequenos ruídos e preencher lacunas nos objetos.
5. Mapa de Distância e Watershed: Identificação dos centros de massa dos comprimidos e expansão das fronteiras para separação de objetos colados.
6. Extração de Contornos e Rotulação: Contagem final e desenho de caixas delimitadoras nos objetos detectados.

## Estrutura do Repositório

* spv_contador_comprimidos.ipynb: Documentação do desenvolvimento e testes com imagens estáticas.
* webcam_contador_comprimidos.ipynb: Implementação otimizada para execução em tempo real via webcam.
* cenario_de_aplicacao.ipynb: Relatório detalhando o contexto, motivação e estudo de caso do projeto.
* requirements.txt: Arquivo de configuração com as bibliotecas necessárias.

## Instalação e Uso

1. Clone este repositório:
   git clone https://github.com/usuario/projeto-pdi.git

2. Instale as bibliotecas necessárias:
   pip install -r requirements.txt

3. Execute o notebook principal:
   Abra o Jupyter Notebook e inicie o arquivo `webcam_contador_comprimidos.ipynb`. Pressione 'q' para encerrar a captura de vídeo durante a execução.

## Equipe (Os Laplacianos)

* Matheus Foresto Moselli
* Marcos Vinicius Medeiros da Silva
* Karl Eloy Marques Henrique