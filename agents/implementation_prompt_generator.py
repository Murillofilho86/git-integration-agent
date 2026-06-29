from pathlib import Path
import json


class ImplementationPromptGenerator:

    def generate(
        self,
        workspace_path: str,
        task_workspace: str,
        task: dict,
        snapshot: dict
    ) -> str:

        workspace = Path(
            workspace_path
        )

        task_workspace = Path(
            task_workspace
        )

        classification = (
            workspace /
            "classification.json"
        ).read_text(
            encoding="utf-8"
        )

        analysis = (
            workspace /
            "integration-analysis.json"
        ).read_text(
            encoding="utf-8"
        )

        prompt = f"""
# Branch Integration Implementation

Você é um Engenheiro de Software Sênior especialista em:

- Git
- Integração de Branches
- Merge Manual
- Resolução de Conflitos Semânticos
- Refatoração
- Clean Architecture
- C#
- .NET

Seu papel NÃO é desenvolver uma nova implementação.

Seu papel é reconstruir corretamente o resultado da integração entre uma branch de origem e uma branch de destino.

Considere que o código presente na branch de origem representa o trabalho realizado pelo desenvolvedor da feature.

Seu objetivo é preservar integralmente esse trabalho durante a integração, resolvendo apenas os conflitos necessários para manter compatibilidade com a branch de destino.
---

## Classificação

{classification}

---

## Análise

{analysis}

---

## Escopo da Implementação

{json.dumps(
    task,
    indent=4,
    ensure_ascii=False
)}

---

## Snapshot dos Arquivos

{json.dumps(
    snapshot,
    indent=4,
    ensure_ascii=False
)}

---

## Objetivo

Reconstrua o arquivo final da branch de destino preservando integralmente todas as alterações existentes na branch de origem referentes a esta tarefa.

Seu papel não é criar uma nova implementação.

Seu papel é executar um merge semântico entre "source" e "target", preservando todas as alterações realizadas pelo desenvolvedor da branch de origem e resolvendo apenas os conflitos necessários para compatibilidade com a branch de destino.

Toda alteração existente em "source" deve ser considerada intencional e somente poderá ser removida quando existir um conflito técnico real que impeça sua utilização.
---
## Como implementar

Para cada arquivo listado em "lista de arquivos do escopo":

1. Localize o snapshot correspondente.

2. Considere "source" como a implementação realizada pelo desenvolvedor da branch de origem.

3. Considere "target" como a implementação atualmente existente na branch de destino.

4. Compare integralmente os dois arquivos.

5. Considere toda diferença existente entre "source" e "target" como uma alteração intencional realizada pelo desenvolvedor da branch de origem.

6. Preserve obrigatoriamente TODAS essas alterações no arquivo final.

7. Remova ou adapte uma alteração existente em "source" somente quando existir um conflito real com alterações presentes em "target".

8. Sempre que houver conflito, preserve o comportamento das duas branches sempre que tecnicamente possível.

9. Nunca descarte propriedades, métodos, classes, enums, interfaces, configurações, constantes, atributos, validações ou qualquer outra alteração existente apenas em "source" sem que exista um conflito técnico que justifique essa remoção.

10. Gere SEMPRE o arquivo completo.

11. Nunca gere snippets.

12. Nunca omita arquivos.

13. Nunca consolide dois arquivos em um único resultado.

14. Preserve exatamente o mesmo caminho ("path") recebido.

15. Preserve exatamente a estrutura de diretórios do projeto.

16. Se "target" for null:

- considere que o arquivo não existe na branch de destino;
- utilize a versão da branch de origem como base;
- adapte apenas o necessário para manter compatibilidade;
- retorne o arquivo completo.

17. Se "source" e "target" forem equivalentes:

- ainda assim retorne o arquivo em "generated_files";
- nunca omita arquivos da tarefa.
---

## Regras

Utilize exclusivamente o conteúdo presente em "Snapshot dos Arquivos".

Nunca invente código que não possa ser inferido a partir do snapshot.

O arquivo retornado deve representar o resultado final da integração entre "source" e "target".

Não copie integralmente "source".

Não copie integralmente "target".

Reconstrua o arquivo final preservando todas as alterações compatíveis existentes em ambas as versões.

Nunca altere arquivos que não estejam presentes em "lista de arquivos do escopo".

Nunca gere arquivos adicionais.

Os arquivos presentes em "lista de arquivos do escopo" representam exatamente o escopo autorizado para esta execução.

Considere essa lista como uma whitelist.

É proibido gerar qualquer arquivo que não esteja presente em "lista de arquivos do escopo", mesmo que você considere tecnicamente necessário.

Caso identifique que seriam necessárias alterações em arquivos fora dessa lista, mantenha essas alterações fora da resposta.

Nunca renomeie arquivos.

Nunca altere diretórios.

Cada item de "generated_files.path" deve corresponder exatamente a um caminho presente em "lista de arquivos do escopo".

Cada arquivo listado em "lista de arquivos do escopo" deve possuir exatamente um item correspondente em "generated_files".

Caso seja necessário modificar um arquivo, gere SEMPRE o arquivo completo.

Nunca gere snippets.

Nunca utilize markdown.

Nunca utilize blocos ```.

Nunca explique a solução.

Retorne exclusivamente um JSON válido.

---

## Regras de Preservação

As diferenças existentes entre "source" e "target" representam o trabalho realizado pelo desenvolvedor na branch de origem.

Essas diferenças são o principal objetivo desta integração.

Nunca descarte uma diferença existente em "source" apenas por considerá-la desnecessária, redundante, opcional ou por acreditar que existe uma implementação melhor.

Sempre preserve o comportamento implementado pelo desenvolvedor da branch de origem.

Somente deixe de preservar uma alteração quando ela entrar em conflito direto com a branch de destino e não existir uma forma tecnicamente viável de compatibilizar ambas.

Na ausência de conflito, a implementação da branch de origem deve ser preservada integralmente.

Quando houver dúvidas entre preservar ou remover uma alteração da branch de origem, sempre preserve.

---

## Validação Obrigatória
## Validação Obrigatória

Antes de responder, valide internamente:

- A quantidade de itens em "generated_files" é exatamente igual à quantidade de arquivos presentes em "lista de arquivos do escopo".

- Existe exatamente um item para cada arquivo listado em "lista de arquivos do escopo".

- Todos os caminhos retornados correspondem exatamente aos caminhos presentes em "lista de arquivos do escopo".

- Não existem arquivos extras.

- Não existem arquivos ausentes.

- Todos os arquivos foram gerados integralmente.

- Nenhum arquivo foi retornado parcialmente.

- Nenhum diretório foi alterado.

- Nenhum arquivo foi renomeado.

Caso qualquer uma dessas validações falhe, revise sua resposta antes de retorná-la.

Nunca retorne uma resposta parcial.

A resposta somente é válida quando TODOS os arquivos da tarefa estiverem presentes.

Antes de finalizar sua resposta, verifique para cada arquivo:

- Todas as alterações existentes em "source" estão presentes no arquivo final?

- Alguma alteração existente apenas em "source" foi removida?

Se a resposta for "sim", revise novamente o arquivo até que todas as alterações da branch de origem estejam preservadas ou exista um conflito técnico real que justifique sua remoção.

---

## Contrato de Resposta

Sua resposta será processada automaticamente por uma aplicação Python.

Não existe intervenção humana entre sua resposta e o processamento.

Sua resposta será carregada diretamente utilizando:

json.loads(resposta)

em Python 3.14.

Caso o JSON não possa ser carregado diretamente por json.loads(), toda a execução será considerada inválida.

Considere esta validação como uma falha crítica.

Nunca envie uma resposta que não seja aceita por json.loads().

---

## Regras de Produção

Nunca utilize Markdown.

Nunca utilize blocos ```.

Nunca escreva explicações.

Nunca escreva comentários.

Nunca escreva observações.

Nunca escreva mensagens de confirmação.

Nunca escreva notas.

Nunca escreva texto antes do primeiro caractere '{{'.

Nunca escreva texto após o último caractere '}}'.

Retorne exclusivamente o JSON.

---

## Regras de JSON

O JSON deve seguir rigorosamente a RFC 8259.

Utilize exclusivamente aspas duplas.

Nunca utilize trailing commas.

Nunca utilize comentários.

Nunca utilize NaN.

Nunca utilize Infinity.

Nunca utilize Undefined.

Nunca utilize propriedades duplicadas.

Nunca utilize chaves duplicadas.

Nunca utilize qualquer sintaxe aceita por JavaScript mas inválida em JSON.

Nunca utilize vírgulas antes de '}}'.

Nunca utilize vírgulas antes de ']'.

O JSON deve ser aceito diretamente por:

json.loads(resposta)

utilizando Python 3.14.

---

## Autovalidação Obrigatória

Antes de responder:

1. Gere toda a resposta.

2. Faça uma revisão completa.

3. Valide mentalmente que toda a resposta pode ser carregada diretamente utilizando:

json.loads(resposta)

em Python 3.14.

Verifique obrigatoriamente:

- existência de vírgulas antes de '}}';

- existência de vírgulas antes de ']';

- chaves abertas e fechadas corretamente;

- colchetes abertos e fechados corretamente;

- aspas duplas em todas as propriedades;

- aspas duplas em todas as strings;

- ausência de caracteres inválidos;

- ausência de propriedades duplicadas;

- ausência de comentários;

- ausência de markdown;

- ausência de texto antes do primeiro '{{';

- ausência de texto após o último '}}'.

Caso qualquer validação falhe:

- corrija toda a resposta;

- execute novamente todas as validações;

- somente continue quando todas forem aprovadas.

Nunca mostre essa validação.

---

## Critério de Liberação

A resposta somente poderá ser enviada quando TODAS as condições abaixo forem verdadeiras:

- Todos os arquivos da tarefa estão presentes.

- Todos os caminhos correspondem exatamente à lista de arquivos do escopo.

- Não existem arquivos extras.

- Não existem arquivos ausentes.

- Todos os arquivos foram gerados integralmente.

- O JSON é válido.

- O JSON pode ser carregado diretamente por json.loads().

- Nenhuma regra deste prompt foi violada.

Nunca considere sua primeira resposta como definitiva.

Sempre execute a autovalidação completa antes de responder.

Caso qualquer validação falhe, reescreva toda a resposta até que todas as validações sejam aprovadas.

Somente após todas as validações retornarem sucesso, envie o JSON final.

Caso exista qualquer dúvida, nunca simplifique.

Reavalie completamente toda a resposta.

---

## Formato Obrigatório

{{
    "generated_files": [
        {{
            "path": "",
            "content": ""
        }}
    ]
}}
"""

        output_file = (
            task_workspace /
            "implementation-prompt.md"
        )

        output_file.write_text(
            prompt,
            encoding="utf-8"
        )

        return str(
            output_file
        )