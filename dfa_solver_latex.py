import json
import sys

def validar_dfa(dfa):
    """Valida a estrutura do DFA."""
    campos_obrigatorios = ['estados', 'alfabeto', 'estado_inicial', 'estados_finais', 'transicoes']
    for campo in campos_obrigatorios:
        if campo not in dfa:
            raise ValueError(f"DFA inválido: campo '{campo}' ausente")
    
    # Validar que o estado inicial está nos estados
    if dfa['estado_inicial'] not in dfa['estados']:
        raise ValueError(f"Estado inicial '{dfa['estado_inicial']}' não está na lista de estados")
    
    # Validar que os estados finais estão nos estados
    for estado in dfa['estados_finais']:
        if estado not in dfa['estados']:
            raise ValueError(f"Estado final '{estado}' não está na lista de estados")
    
    # Validar transições
    for chave in dfa['transicoes']:
        estado, simbolo = chave.split(',')
        if estado not in dfa['estados']:
            raise ValueError(f"Transição inválida: estado '{estado}' não está na lista de estados")
        if simbolo not in dfa['alfabeto']:
            raise ValueError(f"Transição inválida: símbolo '{simbolo}' não está no alfabeto")
        if dfa['transicoes'][chave] not in dfa['estados']:
            raise ValueError(f"Transição inválida: estado de destino '{dfa['transicoes'][chave]}' não está na lista de estados")

def transicao_estendida(dfa, estado_atual, palavra):
    """
    Executa a função de transição estendida δ*(q, w) e exibe o processo.
    
    Args:
        dfa: O autômato finito determinístico
        estado_atual: O estado inicial para a transição
        palavra: A palavra a ser processada
        
    Returns:
        Tupla (estado_final, lista_de_passos_em_latex)
    """
    resultado = []
    resultado.append(f"\\hat{{\\delta}}({estado_atual}, \\varepsilon) = {estado_atual} \\\\")
    
    for i, simbolo in enumerate(palavra, start=1):
        if simbolo not in dfa['alfabeto']:
            raise ValueError(f"Símbolo inválido: '{simbolo}' não pertence ao alfabeto {dfa['alfabeto']}")
        
        estado_anterior = estado_atual
        chave = f"{estado_atual},{simbolo}"
        estado_atual = dfa['transicoes'].get(chave)
        
        if estado_atual is None:
            resultado.append(f"\\hat{{\\delta}}({estado_anterior}, {palavra[:i]}) = \\text{{None}} \\text{{ (transição indefinida)}} \\\\")
            break
            
        prefixo = palavra[:i-1] if palavra[:i-1] != "" else "\\varepsilon"
        resultado.append(
            f"\\hat{{\\delta}}({dfa['estado_inicial']}, {palavra[:i]}) = "
            f"\\delta(\\hat{{\\delta}}({dfa['estado_inicial']}, {prefixo}), {simbolo}) = "
            f"\\delta({estado_anterior}, {simbolo}) = {estado_atual} \\\\"
        )
    return estado_atual, resultado

def aceita_palavra(dfa, palavra):
    """
    Verifica se a palavra é aceita pelo DFA e exibe o processo.
    
    Args:
        dfa: O autômato finito determinístico
        palavra: A palavra a ser verificada
        
    Returns:
        Boolean indicando se a palavra é aceita
    """
    try:
        estado_final, transicoes = transicao_estendida(dfa, dfa['estado_inicial'], palavra)
        for transicao in transicoes:
            print(transicao)
            
        if palavra == "":
            print(f"Palavra vazia processada. Estado final: {estado_final}")
        return estado_final in dfa['estados_finais']
    except ValueError as e:
        print(f"Erro: {e}")
        return False

def main():
    """Função principal do programa."""
    input_file = "input.json"
    
    try:
        with open(input_file, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{input_file}' não foi encontrado.")
        return
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{input_file}' não contém um JSON válido.")
        return
    
    try:
        dfa = dados["dfa"]
        palavra = dados["string"]
        
        # Validar o DFA antes de processar
        validar_dfa(dfa)
        
        print(f"Processando palavra: '{palavra if palavra else 'ε (vazia)'}'")
        print(f"Estado inicial: {dfa['estado_inicial']}")
        print(f"Estados finais: {', '.join(dfa['estados_finais'])}")
        print("\nPassos:")
        
        if aceita_palavra(dfa, palavra):
            print("\nA string pertence à linguagem do DFA.")
        else:
            print("\nA string NÃO pertence à linguagem do DFA.")
            
    except KeyError as e:
        print(f"Erro: Campo obrigatório ausente no arquivo JSON: {e}")
    except ValueError as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()