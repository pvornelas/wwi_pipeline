import consultas
from datetime import datetime

def teste_tooltip_grafico_tendencia_faturamento():
    faturamento = 5903050.86
    imposto = 769963.66
    faturamento_liquido = 5133087.2
    lucro = 2569934.3499999996
    venda = 2151
    pc_faturamento = 0.13811507649035273
    pc_lucro = 0.1560511693014058
    pc_venda = 0.14354066985645933
    mes_ano = datetime(2015, 7, 1)
    resultado = consultas.consulta_faturamento_lucro_e_vendas(mes_ano)
    if (resultado[0] == faturamento and resultado[1] == imposto and resultado[2] == faturamento_liquido and
        resultado[3] == lucro and resultado[4] == venda and resultado[5] == pc_faturamento and resultado[6] == pc_lucro and
        resultado[7] == pc_venda):
        print(f"Teste realizado com sucesso, para periodo entre {mes_ano.strftime('%m/%Y')}")
        print(f"Faturamento:{faturamento}")
        print(f"Imposto:{imposto}")
        print(f"Faturamento líquido:{faturamento_liquido}")
        print(f"Lucro:{lucro}")
        print(f"Venda:{venda}")
        print(f"Variação Faturamento:{pc_faturamento}")
        print(f"Variação Lucro:{pc_lucro}")
        print(f"Variação Venda:{pc_venda}")

def teste_tooltip_categoria_cliente():
    # Resultado para filtro periodo com inicio 01/05/2014 a 01/05/2015
    faturamento = 4133331.59
    imposto = 539130.54
    faturamento_liquido = 3594201.05
    lucro = 1826987.15
    venda = 1458
    margem_de_lucro =  0.4420132065910541
    ticket_medio =  2834.932503429355
    periodo_inicio = datetime(2014, 5, 1)
    periodo_fim = datetime(2015, 5, 1)
    categoria = 7 # Categoria Corporate
    resultado = consultas.consulta_tooltip_regiao(periodo_inicio, periodo_fim, categoria)
    if (resultado[0] == faturamento and resultado[1] == imposto and resultado[2] == faturamento_liquido and
            resultado[3] == lucro and resultado[4] == venda and resultado[5] == margem_de_lucro and
            resultado[6] == ticket_medio):
        print(f"Teste realizado com sucesso, para periodo entre {periodo_inicio.strftime('%d/%m/%Y')} e {periodo_fim.strftime('%d/%m/%Y')}")
        print(f"Faturamento:{faturamento}")
        print(f"Imposto:{imposto}")
        print(f"Faturamento líquido:{faturamento_liquido}")
        print(f"Lucro:{lucro}")
        print(f"Venda:{venda}")
        print(f"Margem de Lucro:{margem_de_lucro}")
        print(f"Ticket Médio:{ticket_medio}")

def teste_nivel_de_reabastecimento():
    # Verificação de produto em nível de reabastecimento
    descricao = '"The Gu" red shirt XML tag t-shirt (White) 5XL'
    quantidade = 3
    nivel_de_reabastecimento = 5
    resultado = consultas.consulta_produto_em_nivel_de_reabastecimento()
    print(resultado)
    if resultado[0] == descricao and resultado[1] == quantidade and resultado[2] == nivel_de_reabastecimento:
        print(f"Teste realizado com sucesso para produto em nível de reabastecimento.")
        print(f"Produto:{descricao}")
        print(f"Quantidade em estoque:{quantidade}")
        print(f"Nível de Reabasteimento:{nivel_de_reabastecimento}")

if __name__ == "__main__":
    teste_tooltip_grafico_tendencia_faturamento()
    teste_tooltip_categoria_cliente()
    teste_nivel_de_reabastecimento()