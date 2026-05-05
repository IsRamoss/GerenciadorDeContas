from datetime import datetime, date
import dados
def Adicionar():
    print("\n--- CADASTRO DE CONTA ---")

    # 1. Validação do Fornecedor (não permite vazio)
    while True:
        fornecedor = input("Digite o nome do fornecedor: ").strip()
        if fornecedor:
            break
        print("Erro: O nome do fornecedor não pode estar vazio.")

    # 2. Validação da Data (força formato correto)
    while True:
        data_input = input("Digite a data de vencimento (DD/MM/AAAA): ")
        try:
            vencimento = datetime.strptime(data_input, "%d/%m/%Y").date()
            break
        except ValueError:
            print("Erro: Formato inválido ou data inexistente. Use DD/MM/AAAA.")

    # 3. Validação do Tipo (usando Match Case)
    while True:
        print("\nTipo de documento:\n1-Boleto\n2-Cheque\n3-Pix\n4-Dinheiro")
        escolha_tipo = input("Escolha (1-4): ")
        match escolha_tipo:
            case "1": tipo = 'Boleto'; break
            case "2": tipo = 'Cheque'; break
            case "3": tipo = 'Pix'; break
            case "4": tipo = 'Dinheiro'; break
            case _: print("Opção inválida! Tente novamente.")

    # 4. Número do Documento
    numDoc = input("Digite o Nº do Documento: ").strip() or "S/N"

    # 5. Validação do Valor (impede letras e trata vírgula)
    while True:
        try:
            valor_str = input("Digite o valor: ").replace(',', '.')
            valor = float(valor_str)
            if valor < 0:
                print("Erro: O valor não pode ser negativo.")
                continue
            break
        except ValueError:
            print("Erro: Digite apenas números válidos (Ex: 150.50).")

    # 6. Validação do Status
    while True:
        print("\nStatus do Pagamento:\n1-Aberto\n2-Pago")
        escolha_status = input("Escolha (1-2): ")
        match escolha_status:
            case "1": status = "Aberto"; break
            case "2": status = "Pago"; break
            case _: print("Opção inválida!")

    codBarras = input("Digite o código de barras: ").strip() or "Não informado"

    # Exibição do resultado seguro
    print("\n" + "—"*40)
    print(f"📄 RESUMO DA CONTA CADASTRADA")
    print(f"—"*40)
    print(f"🏢 Fornecedor:    {fornecedor}")
    print(f"📅 Vencimento:    {vencimento.strftime('%d/%m/%Y')}")
    print(f"📑 Tipo Doc:      {tipo}")
    print(f"🔢 Nº Documento:  {numDoc}")
    print(f"💰 Valor:         R$ {valor:.2f}")
    print(f"✅ Status:        {status}")
    print(f"🔗 Cód. Barras:   {codBarras}")
    print("—"*40 + "\n")

    dadosCSV = (fornecedor,vencimento,tipo,numDoc,valor,status,codBarras)
    dados.salvarArquivo(dadosCSV)

def Editar():
    print("\n--- EDITAR CONTA ---")
    linhas = dados.lerTudo()
    
    if not linhas or len(linhas) <= 1:
        print("Nenhum dado encontrado para editar.")
        return

    # Exibe as contas (pulando o cabeçalho no índice 0)
    for i, linha in enumerate(linhas[1:], start=1):
        print(f"{i}. Fornecedor: {linha[0]} | Valor: {linha[4]} | Status: {linha[5]}")

    try:
        indice = int(input("\nDigite o número da conta que deseja editar: "))
        if 1 <= indice < len(linhas):
            print(f"\nEditando: {linhas[indice][0]}")
            
            # Pergunta qual campo mudar (exemplo simplificado com Status)
            print("Novo Status:\n1-Aberto\n2-Pago")
            novo_status = "Aberto" if input("Escolha: ") == "1" else "Pago"
            
            # Atualiza apenas o campo de Status (índice 5)
            linhas[indice][5] = novo_status
            
            # Salva a lista inteira de volta
            dados.sobrescreverArquivo(linhas)
            print("Alteração salva com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Digite um número.")


def Diario():
    hoje = date.today()
    linhas = dados.lerTudo()
    
    print(f"\n--- CONTAS QUE VENCEM HOJE ({hoje.strftime('%d/%m/%Y')}) ---")
    
    encontrou = False
    for i, linha in enumerate(linhas[1:], start=1):
        try:
            data_vencimento = datetime.strptime(linha[1], "%Y-%m-%d").date() 
        except ValueError:
            try:
                data_vencimento = datetime.strptime(linha[1], "%d/%m/%Y").date()
            except:
                continue

        if hoje == data_vencimento:
            print(f"{i}. Fornecedor: {linha[0]} | Valor: R$ {linha[4]} | Status: {linha[5]} | Código de Barras: {linha[6]}0")
            encontrou = True
    
    if not encontrou:
        print("Nenhuma conta vence hoje!")