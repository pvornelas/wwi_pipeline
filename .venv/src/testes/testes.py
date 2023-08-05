import consultas
from datetime import datetime
import locale

def teste_tooltip_grafico_tendencia_faturamento():
    faturamento = 5929023.38
    imposto = 773351.38
    faturamento_liquido = 5155672.0
    lucro = 2582126.75
    venda = 2166
    pc_faturamento = 0.1416860124942011
    pc_lucro = 0.16013213804553308
    pc_venda = 0.15335463258785942
    mes_ano = datetime(2015, 7, 1)
    resultado = consultas.consulta_faturamento_lucro_e_vendas(mes_ano)
    print(resultado)
    if (resultado[0] == faturamento and resultado[1] == imposto and resultado[2] == faturamento_liquido and
        resultado[3] == lucro and resultado[4] == venda and resultado[5] == pc_faturamento and resultado[6] == pc_lucro and
        resultado[7] == pc_venda):
        print(f"Teste realizado com sucesso, para periodo {mes_ano.strftime('%m/%Y')}")
        print(f"Faturamento: {faturamento}")
        print(f"Imposto: {imposto}")
        print(f"Faturamento líquido: {faturamento_liquido}")
        print(f"Lucro: {lucro}")
        print(f"Venda: {venda}")
        print(f"Variação Faturamento: {pc_faturamento}")
        print(f"Variação Lucro: {pc_lucro}")
        print(f"Variação Venda: {pc_venda}")

def teste_tooltip_categoria_cliente():
    # Resultado para filtro periodo com inicio 01/05/2014 a 01/05/2015
    faturamento = 4130934.99
    imposto = 538817.94
    faturamento_liquido = 3592117.0500000003
    lucro = 1826043.1500000001
    venda = 1455
    margem_de_lucro =  0.4420411249318644
    ticket_medio =  2839.1305773195877
    periodo_inicio = datetime(2014, 5, 1)
    periodo_fim = datetime(2015, 5, 1)
    categoria = 7 # Categoria Corporate
    resultado = consultas.consulta_categoria_cliente(periodo_inicio, periodo_fim, categoria)
    print(resultado)
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

def teste_lead_time():
    lead_time = 8
    lead_time_esperado = 1
    data = datetime(2016, 5, 16)

    resultado = consultas.consulta_lead_time(data)
    if resultado[0] == lead_time and resultado[1] == lead_time_esperado:
        print(f"Teste realizado com sucesso para lead time em 16/05/2016.")
        print(f"Lead time: {lead_time}")
        print(f"Lead time esperado: {lead_time_esperado}")

if __name__ == "__main__":
    # teste_tooltip_grafico_tendencia_faturamento()
    teste_lead_time()
    # teste_tooltip_categoria_cliente()
    # teste_nivel_de_reabastecimento()