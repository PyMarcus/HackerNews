# gera gráfico de artigos mais votados no hackernews
import requests
from operator import itemgetter
from pygal import config, style
from pygal.style import LightenStyle, LightColorizedStyle
import pygal


try:
    dicionarioInformacoes = {}
    listaDeDicionarios = []

    url_base = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    requisicao = requests.get(url_base)  
    assert requisicao != '<Response [200]>'  # se for diferente de 200, encerra o programa
except requests.exceptions.RequestException:
    print('Erro na url')
else:
    conteudo = requisicao.json()  # gera dicionário com os vários ids
    for ids in conteudo[:50]:  # pega os 50 primeiros
        url2 = 'https://hacker-news.firebaseio.com/v0/item/' + str(ids) + '.json'
        nova_requisicao = requests.get(url2)
        resposta = nova_requisicao.json()
        dicionarioInformacoes = {
            'Título' : resposta['title'],
            'Link' :  'http://news.ycombinator.com/item?id=' + str(ids) + '.json',
            'Qnt_de_Comentários' : resposta.get('descendants', 0)  # se não tiver nada, coloca 0
        }
        listaDeDicionarios.append(dicionarioInformacoes)
    lista = sorted(listaDeDicionarios, key=itemgetter('Qnt_de_Comentários'), reverse=True)  # pega o mais recente e ordena de acordo com a quantidade
    lista_titulos, lista_links, lista_comentarios  = [], [], []
    for itens in listaDeDicionarios:
        if itens['Qnt_de_Comentários'] > 20:  # não quero os que têm  menos de 20 comentários
            print(f"Título : {itens['Título']}")
            lista_titulos.append(itens['Título'])
            print(f"Links : {itens['Link']}")
            lista_links.append(itens['Link'])
            print(f"Comentários : {itens['Qnt_de_Comentários']}")
            lista_comentarios.append(itens['Qnt_de_Comentários'])


    # gráfico:
    estilo = LightenStyle('#DF7401', base_style=LightColorizedStyle)
    configuracao = pygal.Config()
    configuracao.x_label_rotation = 45  # graus
    configuracao.show_legend = True
    configuracao.title_font_size = 20
    configuracao.major_label_font_size = 16
    configuracao.truncate_label = 15
    configuracao.show_y_guides = False  # sem linhas horizontais
    configuracao.width = 1000

    grafico = pygal.Bar(configuracao, style=estilo)
    grafico._title = 'Discurssões mais acalouradas no Hacker News'
    grafico.x_labels = lista_titulos
    grafico.add('Quantidade de comentários', lista_comentarios)
    grafico.render_to_file('graficoNews.svg')
