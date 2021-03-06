# Utilizando programação inteira para encontrar árvores geradoras mínimas 

Trabalho de programação inteira para a disciplina de Métodos Quantitativos da UDESC (Bacharelado em Engenharia de Software, CEAVI)

Lucas Moraes Schwambach

Mateus Lucas Cruz Brandt

## Instalação

É necessário ter o `glpk` instalando e disponível no path

No Ubuntu, basta fazer o seguinte
```bash
sudo apt install glpk-utils
```

Então, é necessário instalar as dependências de bibliotecas em Python do projeto:
```bash
pip install -r requirements.txt
```

Também é necessário ter o `graphiz` instalado e disponível no path. Ele é utilizado para gerar a representação visual da solução
No Ubuntu basta executar o seguinte comando:
```bash
sudo apt install graphviz
```

## Uso

Resolver uma instância, por exemplo tinyEWG.txt, com o modelo de programação linear
```bash
python3 ilp.py instances/tinyEWG.txt
```

Resolver uma instância, por exemplo 1000EWG.txt, com o algoritmo de Prim
```bash
python3 prim.py instances/1000EWG.txt
```

Em ambos os casos o argumento `--visual` pode ser adicionado no final para gerar uma imagem do grafo com sua árvore geradora mínima em destaque que será salva na pasta `images`

Instâncias podem ser geradas com o script `generate_instance.py`. Tentei fazer com que ele gerasse sempre grafos conexos, mas não deu certo

Com o `draw_instance.py` é possível gerar uma imagem da instância dada no `stdin`

## Referências

O modelo de programação linear inteira foi feito com base em http://www.columbia.edu/~cs2035/courses/ieor6614.S16/mst-lp.pdf

A implementação do algoritmo de Prim foi feita com base no capítulo 4.3 do Algorithms (Robert Sedgewick, Kevin Wayne); resumo dele e implementação disponíveis em https://algs4.cs.princeton.edu/43mst/. As instâncias (\*EWG.txt) também foram trazidas desse site
