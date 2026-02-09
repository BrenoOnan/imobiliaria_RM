import csv
import os

class Imovel:
    def __init__(self, tipo, quartos, garagem, vagas_extra, tem_criancas):
        self.tipo = tipo
        self.quartos = quartos
        self.garagem = garagem
        self.vagas_extra = vagas_extra
        self.tem_criancas = tem_criancas
        self.valor_aluguel = 0

    def calcular_aluguel(self):
        try:
            if self.tipo == 1:  # Apartamento
                self.valor_aluguel = 700
                if self.quartos == 2:
                    self.valor_aluguel += 200
                if self.garagem:
                    self.valor_aluguel += 300
                if not self.tem_criancas:
                    self.valor_aluguel *= 0.95

            elif self.tipo == 2:  # Casa
                self.valor_aluguel = 900
                if self.quartos == 2:
                    self.valor_aluguel += 250
                if self.garagem:
                    self.valor_aluguel += 300

            elif self.tipo == 3:  # Estúdio
                self.valor_aluguel = 1200
                if self.garagem:
                    self.valor_aluguel += 250
                    self.valor_aluguel += self.vagas_extra * 60

            else:
                raise ValueError("Tipo de imóvel inválido.")

        except Exception as erro:
            print("❌ Erro ao calcular aluguel:", erro)

        return self.valor_aluguel


class Contrato:
    def __init__(self, valor_aluguel, parcelas):
        self.valor_contrato = 2000
        self.valor_aluguel = valor_aluguel
        self.parcelas = parcelas

    def valor_parcela_contrato(self):
        try:
            if self.parcelas <= 0:
                raise ValueError("Número de parcelas inválido.")
            return self.valor_contrato / self.parcelas
        except Exception as erro:
            print("❌ Erro no cálculo das parcelas:", erro)
            return 0

    def gerar_csv(self):
        try:
            print("📄 Gerando arquivo CSV...")

            with open("parcelas_orcamento.csv", "w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.writer(arquivo)

                escritor.writerow(["TIPO", "VALOR"])
                escritor.writerow(["Aluguel Mensal", f"R$ {self.valor_aluguel:.2f}"])
                escritor.writerow(["Contrato Total", "R$ 2000.00"])
                escritor.writerow(["Parcelas do Contrato", f"{self.parcelas}x"])
                escritor.writerow([])

                escritor.writerow(["PARCELAS DO CONTRATO"])
                for i in range(1, self.parcelas + 1):
                    escritor.writerow([f"Parcela {i}", f"R$ {self.valor_parcela_contrato():.2f}"])

                escritor.writerow([])
                escritor.writerow(["ALUGUEL - 12 MESES"])
                for i in range(1, 13):
                    escritor.writerow([f"Mês {i}", f"R$ {self.valor_aluguel:.2f}"])

            print("✅ CSV criado com sucesso!")

        except Exception as erro:
            print("❌ Erro ao gerar CSV:", erro)


def forma_pagamento():
    while True:
        print("\nForma de pagamento:")
        print("1 - Débito")
        print("2 - Crédito")

        opcao = input("Escolha a forma de pagamento (1 ou 2): ")

        if opcao == "1":
            return "Débito"
        elif opcao == "2":
            return "Crédito"
        else:
            print("❌ Opção inválida. Escolha apenas 1 ou 2.")


def menu_imovel():
    while True:
        print("=" * 30)
        print("IMOBILIÁRIA R.M".center(30))
        print("=" * 30)
        print("1 - Apartamento - 1 Quarto: R$ 700,00 | 2 Quartos: R$ 900,00")
        print("2 - Casa - 1 Quarto: R$900,00 | 2 Quartos: R$ 1.150,00")
        print("3 - Estúdio - R$ 1200,00 | até 2 garagens")

        try:
            tipo = int(input("Escolha o tipo de imóvel: "))
            if tipo in [1, 2, 3]:
                return tipo
            else:
                print("❌ Escolha apenas 1, 2 ou 3.")
        except ValueError:
            print("❌ Entrada inválida.")


def quantidade_quartos():
    while True:
        try:
            quartos = int(input("Quantidade de quartos (1 ou 2): "))
            if quartos in [1, 2]:
                return quartos
            else:
                print("❌ Permitido apenas 1 ou 2 quartos.")
        except ValueError:
            print("❌ Entrada inválida.")


def pergunta_sim_nao(mensagem):
    while True:
        resposta = input(mensagem).lower()
        if resposta in ["s", "n"]:
            return resposta == "s"
        else:
            print("❌ Responda apenas com 's' ou 'n'.")


def vagas_extra():
    while True:
        try:
            print("Vagas extras: R$ 60,00 cada (máximo 20)")
            vagas = int(input("Quantidade de vagas extras: "))
            if 0 <= vagas <= 20:
                return vagas
            else:
                print("❌ Permitido no máximo 20 vagas.")
        except ValueError:
            print("❌ Entrada inválida.")


def escolher_parcelas():
    while True:
        try:
            parcelas = int(input("Parcelar contrato em quantas vezes? (1 a 5): "))
            if 1 <= parcelas <= 5:
                return parcelas
            else:
                print("❌ Escolha entre 1 e 5 parcelas.")
        except ValueError:
            print("❌ Entrada inválida.")


# ====== EXECUÇÃO ======
while True:
    try:
        tipo = menu_imovel()

        quartos = 1
        if tipo in [1, 2]:
            quartos = quantidade_quartos()

        garagem = pergunta_sim_nao("Deseja 1 garagem? (s/n): ")
        tem_criancas = pergunta_sim_nao("Sem crianças haverá desconto no aluguel de 5% \nPossui crianças? (s/n): ")

        vagas = 0
        if tipo == 3 and garagem:
            vagas = vagas_extra()

        parcelas = escolher_parcelas()

        imovel = Imovel(tipo, quartos, garagem, vagas, tem_criancas)
        valor_mensal = imovel.calcular_aluguel()

        contrato = Contrato(valor_mensal, parcelas)
        valor_parcela = contrato.valor_parcela_contrato()
        contrato.gerar_csv()

        print("=" * 30)
        print("ORÇAMENTO FINAL".center(30))
        print("=" * 30)
        print(f"Valor do aluguel mensal 12x de: R$ {valor_mensal:.2f}")
        print("Contrato imobiliário: R$ 2.000,00")
        print(f"Parcelamento do contrato: {parcelas}x de R$ {valor_parcela:.2f}")
        print("Arquivo parcelas gerado com sucesso.")

        pagamento = forma_pagamento()

        print(f"Pagamento escolhido: {pagamento}")
        print("\n" + "=" * 30)
        print("OBRIGADO VOLTE SEMPRE!".center(30))
        print("=" * 30)

        break

    except Exception as erro:
        print("❌ Erro inesperado:", erro)
        break